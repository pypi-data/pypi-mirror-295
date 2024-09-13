from amsdal.migration.utils import object_schema_to_table_schema as object_schema_to_table_schema
from amsdal_models.classes.model import Model

class ClassVersionsMixin:
    """
    Mixin class to manage class versions and related table schemas.
    """
    @classmethod
    def _create_table(cls, class_object: Model, *, skip_class_meta: bool = False) -> None: ...
    @classmethod
    def init_class_versions(cls, *, create_tables: bool = False) -> None:
        """
        Initializes class versions and optionally creates tables.

        Args:
            create_tables (bool, optional): Whether to create tables. Defaults to False.

        Returns:
            None
        """
    @staticmethod
    def register_internal_classes() -> None:
        """
        Registers internal classes with the class version manager.

        Returns:
            None
        """
