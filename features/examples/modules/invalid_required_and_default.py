from wysdom import UserObject, UserProperty


class Person(UserObject):
    first_name: str = UserProperty(str)
    last_name: str = UserProperty(str, default="", optional=False)
