import collections
from conftool import yaml_safe_load


class ConfigurationError(Exception):
    """Exception raised when we fail to load the configuration."""


def get(configfile: str) -> "Config":
    """
    Loads the config from file
    """
    try:
        config = yaml_safe_load(configfile, default={})
        return Config(**config)
    except Exception as exc:
        raise ConfigurationError(exc) from exc


ConfigBase = collections.namedtuple(
    "Config",
    [
        "driver",
        "hosts",
        "namespace",
        "api_version",
        "pools_path",
        "driver_options",
        "tcpircbot_host",
        "tcpircbot_port",
        "cache_path",
        "read_only",
        "extensions_config",
    ],
)


class ReqConfiguration:
    """Container for configuration of requestctl"""

    def __init__(self, **kwargs) -> None:
        if "haproxy_path" in kwargs:
            self.haproxy_path = kwargs["haproxy_path"]
        else:
            self.haproxy_path = "/etc/haproxy/"


class ExtensionsConfig:
    """Container for configuration of extensions"""

    def __init__(self, **kwargs) -> None:
        self.reqconfig = ReqConfiguration(**kwargs.get("reqconfig", {}))


class Config(ConfigBase):
    def __new__(
        cls,
        driver="etcd",
        hosts=["http://localhost:2379"],
        namespace="/conftool",
        api_version="v1",
        pools_path="pools",
        driver_options={},
        tcpircbot_host="",
        tcpircbot_port=0,
        cache_path="/var/cache/conftool",
        read_only=False,
        extensions_config={},
    ):
        if pools_path.startswith("/"):
            raise ValueError("pools_path must be a relative path.")

        return super().__new__(
            cls,
            driver=driver,
            hosts=hosts,
            namespace=namespace,
            api_version=api_version,
            pools_path=pools_path,
            driver_options=driver_options,
            tcpircbot_host=tcpircbot_host,
            tcpircbot_port=int(tcpircbot_port),
            cache_path=cache_path,
            read_only=read_only,
            extensions_config=ExtensionsConfig(**extensions_config),
        )

    def requestctl(self) -> ReqConfiguration:
        return self.extensions_config.reqconfig
