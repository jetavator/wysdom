from typing import Dict

import wysdom


class ServiceExample(wysdom.UserObject):

    type: str = wysdom.UserProperty(str)

    def name(self) -> str:
        return wysdom.key(self)


class DBServiceExample(ServiceExample):

    type: str = wysdom.UserProperty(str)


class LocalSparkExample(DBServiceExample):

    type: str = wysdom.UserProperty(wysdom.SchemaConst('local_spark'))


class StorageExample(wysdom.UserObject):

    source: str = wysdom.UserProperty(str)
    vault: str = wysdom.UserProperty(str)
    star: str = wysdom.UserProperty(str)
    logs: str = wysdom.UserProperty(str)


class Example(wysdom.UserObject, wysdom.ReadsJSON):

    prefix: str = wysdom.UserProperty(str, default="jetavator")
    drop_schema_if_exists: bool = wysdom.UserProperty(bool, default=False)
    skip_deploy: bool = wysdom.UserProperty(bool, default=False)
    environment_type: str = wysdom.UserProperty(str, default="local_spark")
    services: Dict[str, ServiceExample] = wysdom.UserProperty(
        wysdom.SchemaDict(ServiceExample), default={})
    storage: StorageExample = wysdom.UserProperty(StorageExample)
    compute: str = wysdom.UserProperty(str)
