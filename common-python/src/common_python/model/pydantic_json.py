import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sap
import pydantic


class PydanticJson(sa.types.TypeDecorator):
    """Pydantic type.
    SAVING:
    - Uses SQLAlchemy JSON type under the hood.
    - Acceps the pydantic model and converts it to a dict on save.
    - SQLAlchemy engine JSON-encodes the dict to a string.
    RETRIEVING:
    - Pulls the string from the database.
    - SQLAlchemy engine JSON-decodes the string to a dict.
    - Uses the dict to create a pydantic model.

    Source: https://gist.github.com/imankulov/4051b7805ad737ace7d8de3d3f934d6b
    """
    # If you work with PostgreSQL, you can consider using
    # sqlalchemy.dialects.postgresql.JSONB instead of a
    # generic sa.types.JSON
    #
    # Ref: https://www.postgresql.org/docs/13/datatype-json.html
    impl = sa.types.JSON

    def __init__(self, pydantic_type):
        super().__init__()
        self.pydantic_type = pydantic_type

    def load_dialect_impl(self, dialect):
        # Use JSONB for PostgreSQL and JSON for other databases.
        if dialect.name == "postgresql":
            return dialect.type_descriptor(sap.JSONB())
        else:
            return dialect.type_descriptor(sa.JSON())

    def process_bind_param(self, value, dialect):
        return value.dict() if value else None
        # If you use FasAPI, you can replace the line above with their jsonable_encoder().
        # E.g.,
        # from fastapi.encoders import jsonable_encoder
        # return jsonable_encoder(value) if value else None

    def process_result_value(self, value, dialect):
        return pydantic.parse_obj_as(self.pydantic_type, value) if value else None
