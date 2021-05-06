from wysdom import UserObject, UserProperty


class Address(UserObject):
    zip_code: int = UserProperty(int, pattern=r"^[0-9]{5}$")
