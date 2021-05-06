from wysdom import UserObject, UserProperty


class Person(UserObject):
    first_name: str = UserProperty(str)
    last_name: str = UserProperty(
        str, default="", default_function=lambda x: x.first_name
    )
