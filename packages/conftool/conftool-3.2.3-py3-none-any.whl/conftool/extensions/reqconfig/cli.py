"""
This is the cli interface for the reqconfig extension.
Given the interface is very different from the other *ctl commands,
We don't necessarily derive it from the base cli tools.
"""

import argparse
import ipaddress
import logging
import pathlib
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple

import yaml
from wmflib.interactive import AbortError, ask_confirmation

from conftool import yaml_safe_load
from conftool.cli import ConftoolClient
from conftool.drivers import BackendError
from conftool.extensions.reqconfig.translate import (
    VSLTranslator,
)
from conftool.kvobject import Entity

from . import api
from . import view
from .constants import ACTION_ENTITIES
from .schema import SCHEMA, get_obj_from_slug, SYNC_ENTITIES
from .error import RequestctlError

logger = logging.getLogger("reqctl")

# Mapping of commands to entities. This is used to determine the entity type
# If the list is empty, the object type will be determined from the command line.
CMD_TO_ENTITY = {
    "validate": [],
    "sync": [],
    "dump": [],
    "enable": ACTION_ENTITIES,
    "disable": ACTION_ENTITIES,
    "get": [],
    "vcl": ["action"],
    "log": ["action"],
    "find": ACTION_ENTITIES,
    "find-ip": ["ipblock"],
    "commit": ACTION_ENTITIES,
    "haproxycfg": ["haproxy_action"],
}


SCOPE_TO_ENTITY = {
    "varnish": ["action"],
    "haproxy": ["haproxy_action"],
}


def is_obj_on_fs(client: ConftoolClient, path: str) -> Callable:
    """Check if an object is on the filesystem."""

    def _is_obj_on_fs(obj_type: str, slug: str) -> bool:
        on_disk: pathlib.Path = (
            pathlib.Path(path) / client.get(obj_type).base_path() / f"{slug}.yaml"
        )
        return on_disk.is_file()

    return _is_obj_on_fs


def _remove_enabled(_, changes: Dict[str, Any]) -> Dict[str, Any]:
    """Remove the enabled state from the changes."""
    try:
        del changes["enabled"]
    except KeyError:
        pass
    return changes


class Requestctl:
    """Cli tool to interact with the dynamic banning of urls."""

    def __init__(self, args: argparse.Namespace) -> None:
        if args.debug:
            lvl = logging.DEBUG
        else:
            lvl = logging.INFO
        logging.basicConfig(
            level=lvl,
            format="%(asctime)s - %(name)s "
            "(%(module)s:%(funcName)s:%(lineno)d) - %(levelname)s - %(message)s",
        )
        self.args = args
        # Now let's load the schema
        self.client = api.client(self.args.config)

        self.schema = self.client.schema

        # Load the right entities
        self.classes = {obj: self.client.get(obj) for obj in self.object_types}
        # If we only have one entity, we can use it directly
        if len(self.classes) == 1:
            self.cls = list(self.classes.values())[0]
        else:
            self.cls = None
        if "git_repo" in self.args and self.args.git_repo is not None and self.cls is not None:
            self.base_path: Optional[pathlib.Path] = (
                pathlib.Path(self.args.git_repo) / self.cls.base_path()
            )
        else:
            self.base_path = None
        # Load the parsing grammar. If the command is validate, use on-disk check of existence for
        # patterns.
        # Otherwise, check on the datastore.
        self.api = api.RequestctlApi(self.client)
        # We never sync enabled from disk
        self.api.set_hook("validate", _remove_enabled)

        if self.args.command == "validate":
            self.api.expression_processor.set_search_func(
                is_obj_on_fs(self.client, self.args.basedir)
            )

    @property
    def object_types(self) -> List[str]:
        """The object type we're operating on."""
        if self.args.command not in CMD_TO_ENTITY:
            raise RequestctlError(
                f"Command {self.args.command} not listed in Requestctl.CMD_TO_ENTITY"
            )
        # If we don't have forced values for the specific command, we expect an object type
        # to be passed in the command line.
        if not CMD_TO_ENTITY[self.args.command]:
            return [self.args.object_type]

        # To make things more user-friendly, we sometimes allow selecting a "scope" of objects
        if "scope" in self.args and self.args.scope in SCOPE_TO_ENTITY:
            return SCOPE_TO_ENTITY[self.args.scope]
        # Otherwise we return the values from the mapping
        return CMD_TO_ENTITY[self.args.command]

    def run(self):
        """Runs the action defined in the cli args."""
        try:
            command = getattr(self, self.args.command.replace("-", "_"))
        except AttributeError as e:
            raise RequestctlError(f"Command {self.args.command} not implemented") from e

        # TODO: add support to let a custom exit code surface, for example for
        # "failed successfully" operations
        command()

    def validate(self):
        """Scans a directory, checks validity of the objects.

        Raises an exception if invalid objects have been found.
        """
        # The code is quite similar to the one in sync; however abstracting it
        # gets ugly fast. I chose code readability over DRY here consciously.
        root_path = pathlib.Path(self.args.basedir)
        failed = False
        for obj_type in SYNC_ENTITIES:
            self.cls = self.client.get(obj_type)
            for tag, fpath in self._get_files_for_object_type(root_path, obj_type):
                obj, from_disk = self._entity_from_file(tag, fpath)
                try:
                    self.api.validate(obj, from_disk)
                except RequestctlError as e:
                    failed = True
                    logger.error("%s %s is invalid: %s", obj_type, obj.pprint(), e)
                    continue
        if failed:
            raise RequestctlError("Validation failed, see above.")

    def sync(self):
        """Synchronizes entries for an entity from files on disk."""
        # Let's keep things simple, we only have one layer of tags
        # for request objects.
        failed = False
        # Set cls to the right entity
        self.cls = self.client.get(self.args.object_type)
        for tag, fpath in self._get_files_for_object_type(
            pathlib.Path(self.args.git_repo), self.args.object_type
        ):
            obj, from_disk = self._entity_from_file(tag, fpath)
            with self.api.hook("write_confirmation", self._write_confirmation_hook()):
                try:
                    self.api.write(obj, from_disk)
                except RequestctlError as e:
                    failed = True
                    logger.error("Error parsing %s, skipping: %s", obj.pprint(), e)
                except BackendError as e:
                    logger.error("Error writing to etcd for %s: %s", obj.pprint(), e)
                    failed = True
                    continue

        # If we're not purging, let's stop here.
        if not self.args.purge:
            if failed:
                raise RequestctlError(
                    "synchronization had issues, please check the output for details."
                )
            return

        # Now let's find any object that is in the datastore and not on disk.
        for reqobj in self.cls.all():
            if not self._should_have_path(reqobj).is_file():
                with self.api.hook("delete_confirmation", self._delte_confirmation_hook()):
                    try:
                        self.api.delete(reqobj)
                    except RequestctlError as e:
                        failed = True
                        logger.error("Error deleting %s: %s", reqobj.pprint(), e)
                    except BackendError as e:
                        logger.error("Error deleting %s from etcd: %s", reqobj.pprint(), e)
                        failed = True
                        continue

        if failed:
            raise RequestctlError("synchronization had issues, please check the logs for details.")

    def dump(self):
        """Dump an object type."""
        if self.cls is None:
            raise RequestctlError(
                "No object type selected for dumping. This is a bug, please report it."
            )
        for reqobj in self.cls.all():
            object_path = self.base_path / f"{reqobj.pprint()}.yaml"
            object_path.absolute().parent.mkdir(parents=True, exist_ok=True)
            contents = reqobj.asdict()[reqobj.name]
            object_path.write_text(yaml.dump(contents))

    def enable(self):
        """Enable an action."""
        self._enable(True)

    def disable(self):
        """Disable an action."""
        self._enable(False)

    def get(self):
        """Get an object, or an entire class of them, print them out."""
        # We should only call this when a class is selected
        if self.cls is None:
            raise RequestctlError(
                "No object type selected for getting. This is a bug, please report it."
            )
        self._pprint(self._get())

    def log(self):
        """Print out the varnishlog command corresponding to the selected action."""
        objs = self._get(must_exist=True)
        objs[0].vsl_expression = self._vsl_from_expression(objs[0].expression)
        print(view.get("vsl").render(objs, "action"))

    def find(self):
        """Find actions that correspond to the searched pattern."""
        pattern = f"pattern@{self.args.search_string}"
        ipblock = f"ipblock@{self.args.search_string}"
        matches = 0
        for action in self._get():
            tokens = self.api.expression_processor.parse_as_list(action.expression)
            if pattern in tokens or ipblock in tokens:
                matches += 1
                object_type = api.get_object_type_from_entity(action)
                print(f"{object_type}: {action.pprint()}, expression: {action.expression}")
        if not matches:
            print("No entries found.")

    def find_ip(self):
        """Find if the given IP is part of any IP block on disk."""
        # TODO: mayybe search on the datastore?
        if self.base_path is None:
            raise RequestctlError("No git repo specified, cannot search for IP blocks.")
        ip = ipaddress.ip_address(self.args.ip)
        found = False
        for file in self.base_path.glob("**/*.yaml"):
            content = yaml_safe_load(file, {})
            for prefix in content["cidrs"]:
                if ip in ipaddress.ip_network(prefix):
                    found = True
                    ipblock = file.relative_to(self.base_path).with_suffix("")
                    print(f"IP {ip} is part of prefix {prefix} in ipblock {ipblock}")

        if not found:
            print(f"IP {ip} is not part of any ipblock on disk")

    def vcl(self):
        """Print out the VCL for a specific action."""
        objs = self._get(must_exist=True)
        print(self.api.get_dsl_for(objs, show_disabled=True))

    def haproxycfg(self):
        """Print out the haproxy config for a specific action."""
        haproxy_actions = self._get(must_exist=True)
        print(self.api.get_dsl_for(haproxy_actions, show_disabled=True))

    def commit(self):
        """Commit the enabled actions to the DSLs, asking confirmation with a diff."""
        # All the actions that are not disabled or without log_matching, organized by
        # cluster and type
        batch: bool = self.args.batch
        if not batch:
            print("### Varnish VCL changes ###")

        self._commit_vcl(batch)
        if not batch:
            print("### HAProxy DSL changes ###")
        self._commit_haproxy(batch)

    # End public interface
    def _commit_vcl(self, batch: bool):
        diffs = self.api.get_dsl_diffs("action")
        for cluster, entries in diffs.items():
            for name, data in entries.items():
                dsl, diff = data
                if not batch and not self._confirm_diff(diff):
                    continue
                dsl_obj = self.client.get("vcl")(cluster, name)
                # If the dsl is empty, we need to nullify the vcl
                if not dsl:
                    if dsl_obj.exists:
                        dsl_obj.vcl = ""
                        dsl_obj.write()
                else:
                    # If the dsl is not empty, we need to write it
                    dsl_obj.vcl = dsl
                    dsl_obj.write()

    def _commit_haproxy(self, batch: bool):
        diffs = self.api.get_dsl_diffs("haproxy_action")
        for cluster, entries in diffs.items():
            for name, data in entries.items():
                dsl, diff = data
                if not batch and not self._confirm_diff(diff):
                    continue
                dsl_obj = self.client.get("haproxy_dsl")(cluster, name)
                # If the dsl is empty, we need to remove the dsl. However,
                # in the case of HAProxy, we need to remove the object alltogether
                # so that the fallback global configuration will be picked up
                # instead.
                if not dsl:
                    if dsl_obj.exists:
                        dsl_obj.delete()
                else:
                    # If the dsl is not empty, we need to write it
                    dsl_obj.dsl = dsl
                    dsl_obj.write()

    def _get_files_for_object_type(
        self, root_path: pathlib.Path, obj_type: str
    ) -> Generator[Tuple[str, pathlib.Path], None, None]:
        """Gets files in a directory that can contain objects."""
        entity_path: pathlib.Path = root_path / self.client.get(obj_type).base_path()
        if not pathlib.Path.exists(entity_path):
            return None
        for tag_path in entity_path.iterdir():
            # skip files in the root dir, including any hidden dirs and the special
            # .. and . references
            if not tag_path.is_dir() or tag_path.parts[-1].startswith("."):
                continue
            tag = tag_path.name
            for fpath in tag_path.glob("*.yaml"):
                yield (tag, fpath)

    def _confirm_diff(self, diff: str) -> bool:
        """Confirm if a change needs to be carried on or not."""
        if not diff:
            return False
        print(diff)
        try:
            ask_confirmation("Ok to commit these changes?")
        except AbortError:
            return False
        return True

    def _get(self, must_exist: bool = False) -> List[Entity]:
        """Get an object, or all of them, return them as a list."""
        objs = []
        has_path = "object_path" in self.args and self.args.object_path

        for cls in self.classes:
            if has_path:
                obj = self.api.get(cls, self.args.object_path)
                if obj.exists:
                    objs.append(obj)
            else:
                objs.extend(self.api.all(cls))
        if must_exist and has_path and not objs:
            raise RequestctlError(
                f"{list(self.classes.keys())} '{self.args.object_path}' not found."
            )

        return objs

    def _enable(self, enable: bool):
        """Ban a type of request."""
        for cls in self.classes.values():
            action = get_obj_from_slug(cls, self.args.action)
            if not action.exists:
                continue
            action.update({"enabled": enable})
            # Printing this unconditionally *might* be confusing, as there's nothing to commit if
            # enabling an already-enabled action. So we could check first, with action.changed(),
            # but it probably isn't worth the extra roundtrip.
            print("Remember to commit the change with: sudo requestctl commit")
            return

        # If we got here, the action was not found.
        raise RequestctlError(f"{self.args.action} does not exist, cannot enable/disable.")

    def _pprint(self, entities: List[Entity]):
        """Pretty print the results."""
        # VCL and VSL output modes are only supported for "action"
        # Also, pretty mode is disabled for all but patterns and ipblocks.
        # Actions should be supported, but is temporarily disabled
        #  while we iron out the issues with old versions of tabulate
        output_config = {
            "action": {"allowed": ["vsl", "vcl", "yaml", "json"], "default": "yaml"},
            "haproxy_action": {"allowed": ["yaml", "json", "haproxycfg"], "default": "json"},
            "vcl": {"allowed": ["yaml", "json"], "default": "json"},
            "haproxy_dsl": {"allowed": ["yaml", "json"], "default": "json"},
        }
        # We need output and object type to determine the output format
        if not all([self.args.output, self.args.object_type]):
            raise RequestctlError("Cannot use pprint without output and object type.")
        out = self.args.output
        object_type = self.args.object_type
        if object_type in output_config:
            conf = output_config[object_type]
            if out not in conf["allowed"]:
                out = conf["default"]
        print(view.get(out).render(entities, object_type))

    def _entity_from_file(self, tag: str, file_path: pathlib.Path) -> Tuple[Entity, Optional[Dict]]:
        """Get an entity from a file path, and the corresponding data to update."""
        from_disk = yaml_safe_load(file_path, {})
        entity_name = file_path.stem
        if self.cls is None:
            raise RequestctlError(
                "No entity selected when trying to load from disk."
                "Please ensure self.cls is set before calling this method."
                "This is a bug in the code. If you see this message, please report it."
            )
        entity = self.cls(tag, entity_name)
        return (entity, from_disk)

    def _write_confirmation_hook(self) -> Callable:
        def _object_diff(entity: Entity, to_load: Dict[str, Any]) -> bool:
            """Asks for confirmation of changes if needed."""
            # find the object type from the entity
            obj_type = api.get_object_type_from_entity(entity).capitalize()
            if entity.exists:
                changes = entity.changed(to_load)
                action = "modify"
                msg = f"{obj_type} {entity.pprint()} will be changed:"
            else:
                action = "create"
                changes = to_load
                msg = f"{obj_type} will be created:"

            if self.args.interactive and changes:
                print(msg)
                for key, value in changes.items():
                    print(f"{entity.name}.{key}: '{getattr(entity, key)}' => {value}")
                try:
                    ask_confirmation(f"Do you want to {action} this object?")
                except AbortError:
                    return False
            return True

        return _object_diff

    def _delte_confirmation_hook(self) -> Callable:
        def _delete_confirmation(entity: Entity) -> bool:
            """Ask for confirmation before deleting an object."""
            if self.args.interactive:
                try:
                    ask_confirmation(f"Proceed to delete {entity.pprint()}?")
                except AbortError:
                    return False
            return True

    def _should_have_path(self, obj: Entity) -> pathlib.Path:
        """Path expected on disk for a specific entity."""
        tag = SCHEMA[api.get_object_type_from_entity(obj)]["tags"][0]
        return self.base_path / obj.tags[tag] / f"{obj.name}.yaml"

    def _vsl_from_expression(self, expression: str) -> str:
        parsed = self.api.expression_processor.parse_as_list(expression)
        vsl = VSLTranslator(self.client.schema)
        return vsl.from_expression(parsed)
