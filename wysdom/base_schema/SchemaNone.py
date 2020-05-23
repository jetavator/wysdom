from .SchemaType import SchemaType


class SchemaNone(SchemaType):
    """
    A schema requiring a null value.
    """
    type_name: str = 'null'

