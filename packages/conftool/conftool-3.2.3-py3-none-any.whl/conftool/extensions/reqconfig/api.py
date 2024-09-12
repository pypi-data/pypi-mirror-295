"""API for requestctl."""

import contextlib
import difflib
import logging
from typing import Callable, Dict, List, Optional, Tuple
import pyparsing as pp

from conftool import configuration
from conftool.kvobject import KVObject, Entity
from conftool.cli import ConftoolClient, ObjectTypeError
from . import translate, view
from .constants import ACTION_ENTITIES, ACTION_TO_DSL
from .error import RequestctlError
from .schema import SCHEMA, get_obj_from_slug

logger = logging.getLogger("reqctl")


def client(config: Optional[str] = None) -> ConftoolClient:
    """Create a ConftoolClient instance configured for requestctl."""
    return ConftoolClient(
        configfile=config,
        config=None if config is not None else configuration.Config(),
        schema=SCHEMA,
        irc_logging=False,
    )


def get_object_type_from_entity(entity: Entity) -> str:
    """Get the object type from an entity."""
    return entity.__class__.__name__.lower()


class RequestctlExpressionProcessor:
    """Represents an action expression in requestctl."""

    def __init__(self, cl: ConftoolClient):
        self.client = cl
        self.basedir: Optional[str] = None
        self._obj_exist = self._is_obj_on_backend
        self.expression_grammar = self.grammar()
        self.vcl_translator = translate.VCLTranslator(cl.schema)
        self.haproxy_translator = translate.HAProxyDSLTranslator(cl.schema)

    def set_search_func(self, search_func: Callable):
        """Set the search function to use."""
        self._obj_exist = search_func
        self.expression_grammar = self.grammar()

    def reset_search_func(self):
        """Reset the search function to the default."""
        self._obj_exist = self._is_obj_on_backend
        self.expression_grammar = self.grammar()

    def parse(self, expression: str) -> pp.ParseResults:
        """Parse an expression."""
        return self.expression_grammar.parseString(expression, parseAll=True)

    def parse_as_list(self, expression: str) -> List[str]:
        """Parse an expression and return a list of strings."""

        def flatten(parse):
            res = []
            for el in parse:
                if isinstance(el, list):
                    res.extend(flatten(el))
                else:
                    res.append(el)
            return res

        parsed = self.parse(expression)
        return flatten(parsed.asList())

    def parse_as_vcl(self, expression: str) -> str:
        """Parse an expression and return a VCL expression."""
        parsed = self.parse_as_list(expression)
        return self.vcl_translator.from_expression(parsed)

    def parse_as_haproxy(self, expression: str) -> str:
        """Parse an expression and return a HAProxy expression."""
        parsed = self.parse_as_list(expression)
        return self.haproxy_translator.from_expression(parsed)

    def grammar(self) -> pp.Forward:
        """
        Pyparsing based grammar for expressions in actions.

        BNF of the grammar:
        <grammar> ::= <item> | <item> <boolean> <grammar>
        <item> ::= <pattern> | <ipblock> | "(" <grammar> ")"
        <pattern> ::= "pattern@" <pattern_path>
        <ipblock> ::= "ipblock@"<ipblock_path>
        <boolean> ::= "AND" | "OR" | "AND NOT" | "OR NOT"

        """
        boolean = (
            pp.Keyword("AND NOT") | pp.Keyword("OR NOT") | pp.Keyword("AND") | pp.Keyword("OR")
        )
        lpar = pp.Literal("(")
        rpar = pp.Literal(")")
        element = pp.Word(pp.alphanums + "/-_")
        pattern = pp.Combine("pattern@" + element.setParseAction(self._validate_pattern))
        ipblock = pp.Combine("ipblock@" + element.setParseAction(self._validate_ipblock))
        grm = pp.Forward()
        item = pattern | ipblock | lpar + grm + rpar
        grm << pp.Group(item) + pp.ZeroOrMore(pp.Group(boolean + item))
        return grm

    def _validate_pattern(self, _all, _pos, tokens):
        """Ensure a pattern referenced exists."""
        for pattern in tokens:
            if not self._obj_exist("pattern", pattern):
                msg = f"The pattern {pattern} is not present on the backend."
                logger.error(msg)
                # also raise an exception to make parsing fail.
                raise pp.ParseException(msg)

    def _validate_ipblock(self, _all, _pos, tokens):
        """Ensure an ipblock referenced exists."""
        for ipblock in tokens:
            if not self._obj_exist("ipblock", ipblock):
                msg = f"The ipblock {ipblock} is not present on the backend."
                logger.error(msg)
                raise pp.ParseException(msg)

    def _is_obj_on_backend(self, obj_type: str, slug: str) -> bool:
        """Checks if the pattern exists on the backend."""
        obj = get_obj_from_slug(self.client.get(obj_type), slug)
        return obj.exists


class RequestctlApi:
    """API for requestctl."""

    def __init__(self, cl: ConftoolClient):
        self.client = cl
        self.expression_processor = RequestctlExpressionProcessor(cl)
        # Hooks to allow modifying the behaviour of the api
        self._hooks: Dict[str, Callable] = {}

    @contextlib.contextmanager
    def hook(self, label: str, hook: Callable):
        """Set a hook for a specific label in the current context.

        Currently supported labels are:
        - write_confirmation: called before writing an object to the backend.
            The signature of the function is `hook(obj: Entity, changes: Dict) -> bool`.
        - delete_confirmation: called before deleting an object from the backend.
            The signature of the function is `hook(obj: Entity) -> bool`.
        - validate: called before validating the changes to an object.
            The signature of the function is `hook(obj: Entity, changes: Dict) -> Dict`.

        Args:
            label (str): The label for the hook.
            hook (callable): The hook to set.

        Examples:
        ```python
        with api.hook("write_confirmation", my_hook):
            api.write(obj, changes)
        ```
        """
        old_hook = self._hooks.get(label, None)
        self._hooks[label] = hook
        yield
        self._hooks[label] = old_hook

    def set_hook(self, label: str, hook: Callable):
        """Set a hook for a specific label.

        The supported labels are the same as for the `hook` context manager.

        Args:
            label (str): The label for the hook.
            hook (callable): The hook to set.

        """
        self._hooks[label] = hook

    def get(self, obj_type: str, slug: str) -> Optional[Entity]:
        """Get an object by name.

        Args:
            obj_type (str): The type of object to get.
            slug (str): The slug representing tag/name of the object.

        Returns:
            The object if the object type is supported, None otherwise.

        Raises:
            RequestctlError when the slug doesn't contain a path separator.
        """
        try:
            return get_obj_from_slug(self.client.get(obj_type), slug)
        except ObjectTypeError as e:
            logger.error(e)
            return None

    def all(self, obj_type: str) -> List[KVObject]:
        """Get all objects of a type as a list.

        Args:
            obj_type (str): The type of object to get.

        Returns:
            A list of objects of the specified type.

        Raises:
            ObjectTypeError when the object type is not supported.

        """
        return self.client.get(obj_type).all()

    def write(self, obj: Entity, to_load: Dict) -> None:
        """Write an object to the backend.

        Args:
            obj (conftool.kvobject.Entity): The object to write.
            to_load (dict): The values to write.

        Raises:
            RequestctlError when the object is not valid.
            BackendError when the write fails.
        """
        obj_type = get_object_type_from_entity(obj)
        to_load = self.validate(obj, to_load)
        # Allow inserting a hook to confirm the write
        hook = self._hooks.get("write_confirmation", None)
        if hook is not None and not hook(obj, to_load):
            return

        if obj.exists:
            logger.info("Updating %s %s", obj_type, obj.pprint())
            obj.update(to_load)
        else:
            logger.info("Creating %s %s", obj_type, obj.pprint())
            obj.from_net(to_load)
            obj.write()

    def create(self, obj_type: str, slug: str, value: Dict) -> None:
        """Create an object on the backend.

        Args:
            obj_type (str): The type of object to create.
            slug (str): The slug representing tag/name of the object.
            value (dict): The values to write.

        Raises:
            RequestctlError when the object already exists
            BackendError when the write fails.
        """
        self._create_or_update(obj_type, slug, value, update=False)

    def update(self, obj_type: str, slug: str, value: Dict) -> None:
        """Update an object on the backend.

        Args:
            obj_type (str): The type of object to update.
            slug (str): The slug representing tag/name of the object.
            value (dict): The values to write.

        Raises:
            RequestctlError when the object does not exist
            BackendError when the write fails.
        """
        self._create_or_update(obj_type, slug, value, update=True)

    def delete(self, obj: Entity) -> None:
        """Delete an object from the backend.


        Args:
            obj (conftool.kvobject.Entity): The object to delete.

        Raises:
            RequestctlError when the object is used by an action.
            BackendError when the delete fails.
        """
        obj_type = get_object_type_from_entity(obj)
        if not obj.exists:
            return
        # If the object is a pattern or an ipblock, we need to check if it is used by any action
        if obj_type in ["pattern", "ipblock"]:
            expr = f"{obj_type}@{obj.pprint()}"
            for action_type in ACTION_ENTITIES:
                matches = [
                    r.pprint() for r in self.client.get(action_type).all() if expr in r.expression
                ]
                if matches:
                    raise RequestctlError(
                        f"{obj_type} {obj.pprint()} is used by the following {action_type}: "
                        f"{','.join(matches)}"
                    )
        logger.info("Deleting %s %s", obj_type, obj.pprint())
        # Allow inserting a hook to confirm the write
        hook = self._hooks.get("delete_confirmation", None)
        if hook is not None and not hook(obj):
            return
        obj.delete()

    def get_dsl_for(self, objects: List[Entity], show_disabled: bool = False) -> str:
        """Get the DSL for a given group of entities.

        Args:
            objects (List[conftool.kvobject.Entity]): The objects to get the DSL for.
            show_disabled (bool): Whether to show non-enabled objects.

        Returns:
            str: The DSL for the objects.

        Raises:
            RequestctlError when the object type is not supported or there is an
            error parsing the expression.
        """
        if not objects:
            return ""
        entity = get_object_type_from_entity(objects[0])
        if entity not in ACTION_ENTITIES:
            raise RequestctlError(f"{entity} cannot produce a DSL.")
        if entity == "haproxy_action":
            return self._get_haproxy_dsl_for(objects, show_disabled)
        elif entity == "action":
            return self._get_vcl_for(objects, show_disabled)

    def validate(self, obj: Entity, changes: Dict) -> Dict:
        """Verify the changes to an object before writing them to the backend.

        In the case of actions, we also check that the expression is valid and
        we normalize it before writing it to the backend.

        Args:
            obj (conftool.kvobject.Entity): The object to validate.
            changes (dict): The changes to validate.

        Returns:
            dict: The validated changes.

        Raises:
            RequestctlError when the changes are invalid
        """
        object_type = get_object_type_from_entity(obj)
        if object_type == "pattern":
            if changes.get("body", False) and changes.get("method", "") != "POST":
                raise RequestctlError("Cannot add a request body in a request other than POST.")
        if object_type not in ACTION_ENTITIES:
            return changes
        try:
            changes["expression"] = " ".join(
                self.expression_processor.parse_as_list(changes["expression"])
            )
        except pp.ParseException as e:
            raise RequestctlError(e) from e

        if object_type == "haproxy_action":
            if obj.bw_throttle and changes.get("silent_drop", False):
                raise RequestctlError("Cannot have both bandwidth throttling and silent drop.")

        # Allow inserting a hook to validate the changes
        hook = self._hooks.get("validate", None)
        if hook is not None:
            changes = hook(obj, changes)
        return changes

    def get_actions_by_site(self, object_type: str) -> Dict[str, Dict[str, List[Entity]]]:
        """Get all active actions, organized by site and type.

        Organize actions by type, cluster and site, and return a dic of the
        actions for the selected action type.

        For VCL generation, we organize them by cache cluster and by site as follows:
        - $cluster/global: all rules that go to all sites for cache misses
        - $cluster/hit-global: all rules that go to all sites for cache hits
        - $cluster/$site: all rules that go to a specific site for cache misses
        - $cluster/hit-$site: all rules that go to a specific site for cache hits

        For HAProxy DSL generation, we organize them by cluster and site as follows:
        - $cluster/$site: all rules that go to a specific site
        - $cluster/global: all rules that go to all sites

        Args:
            object_type (str): The type of object to get.

        Returns:
            dict: The objects organized by cluster and site.
        """
        output = {}
        if object_type not in ACTION_ENTITIES:
            raise ObjectTypeError(f"{object_type} is not a valid action type.")
        for action in self.all(object_type):
            if not (action.enabled or action.log_matching):
                continue
            cluster = action.tags["cluster"]
            if cluster not in output:
                output[cluster] = {}
            # Each rule can be applied one, multiple sites or to all
            sites = ["global"]
            if action.sites:
                sites = action.sites

            for site in sites:
                if object_type == "action" and not action.cache_miss_only:
                    site = f"hit-{site}"
                if site not in output[cluster]:
                    output[cluster][site] = []
                output[cluster][site].append(action)

        return output

    def get_dsl_diffs(self, object_type: str) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """Get the diffs between the currently committed DSL and what would
        be generated by the current actions.

        The return value is organized by cluster and looks like the data structure
        returned by get_actions_by_site.

        Args:
            object_type (str): The type of object to get.

        Returns:
            dict: each entry is a tuple including the generated DSL and the diffs with the current
            value.
        """
        diffs = {}
        actions = self.get_actions_by_site(object_type)
        dsl_type = ACTION_TO_DSL[object_type]

        def get_dsl(obj: Entity) -> str:
            if dsl_type == "vcl":
                return obj.vcl
            return obj.dsl

        for cluster, sites in actions.items():
            diffs[cluster] = {}
            for site, actions in sites.items():
                # In HAProxy, we need to add the global rules to the site rules
                # so we can generate the full configuration including all ACLs.
                if object_type == "haproxy_action":
                    if "global" in sites and not site == "global":
                        actions.extend(sites["global"])
                new_dsl = self.get_dsl_for(actions)
                # If the object doesn't exist on the backend, the DSL is empty
                current_dsl = get_dsl(self.get(dsl_type, f"{cluster}/{site}"))
                diffs[cluster][site] = (
                    new_dsl,
                    self._dsl_diff(current_dsl, new_dsl, f"{cluster}/{site}"),
                )
        # Now find things that were removed: we cycle over all the DSL objects
        # currently on the backend and check if they are in the diffs.
        try:
            for dsl in self.all(dsl_type):
                cluster = dsl.tags["cluster"]
                site = dsl.name
                if cluster not in diffs:
                    diffs[cluster] = {}
                if site not in diffs[cluster]:
                    diffs[cluster][site] = (
                        "",
                        self._dsl_diff(get_dsl(dsl), "", f"{cluster}/{site}"),
                    )
        except ValueError:
            # this means there are no dsl objects on the backend
            pass
        return diffs

    def _get_vcl_for(self, objects: List[Entity], show_disabled: bool) -> str:
        """Get the VCL for a given action."""
        render_type = "vcl" if show_disabled else "commit"
        for action in objects:
            action.vcl_expression = self.expression_processor.parse_as_vcl(action.expression)
        return view.get("vcl").render(objects, render_type)

    def _get_haproxy_dsl_for(self, objects: List[Entity], show_disabled: bool) -> str:
        """Get the HAProxy configuration for a list of actions."""
        haproxy_actions = [a for a in objects if a.enabled or a.log_matching or show_disabled]
        for haproxy_action in haproxy_actions:
            haproxy_action.parsed_expression = self.expression_processor.parse_as_list(
                haproxy_action.expression
            )
        translator = self.expression_processor.haproxy_translator
        # Now translate them to acls and add the haproxy_expression property
        acls = translator.acls_from_actions(haproxy_actions)
        for haproxy_action in haproxy_actions:
            haproxy_action.haproxy_expression = self.expression_processor.parse_as_haproxy(
                haproxy_action.expression
            )
        return view.get("haproxycfg").render(haproxy_actions, acls)

    def _create_or_update(self, obj_type: str, slug: str, value: Dict, update: bool = True) -> None:
        """Write an object to the backend.
        Args:
            obj_type: The type of object to write.
            slug: The slug representing tag/name of the object.
            value: The values to write.
            update: Whether to update the object if it exists or create it.
            validate: Whether to validate the changes before writing them.

        Raises:
            RequestctlError
        """
        obj = get_obj_from_slug(self.client.get(obj_type), slug)
        if update and not obj.exists:
            raise RequestctlError(
                f"{slug} does not exist on the backend, and an update was requested."
            )
        if not update and obj.exists:
            raise RequestctlError(
                f"{slug} already exists on the backend, and creation was requested."
            )

        if update and not obj.changed(value):
            return

        self.write(obj, value)

    def _dsl_diff(self, old: str, new: str, slug: str) -> str:
        """Diffs between two pieces of DSL."""
        if old == "":
            fromfile = "null"
        else:
            fromfile = f"{slug}.old"
        if new == "":
            tofile = "null"
        else:
            tofile = f"{slug}.new"
        return "".join(
            [
                line + "\n"
                for line in difflib.unified_diff(
                    old.splitlines(), new.splitlines(), fromfile=fromfile, tofile=tofile
                )
            ]
        )
