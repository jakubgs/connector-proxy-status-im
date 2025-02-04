import json

from typing import Any
from typing import Dict

from connector_postgresql.baseCommand import BaseCommand

class CreateTable(BaseCommand):
    """CreateTable."""

    def __init__(self, table_name: str, schema: Dict[str, Any]):
        """__init__."""
        self.table_name = table_name
        self.schema = schema

    def execute(self, config, task_data):

        columns = self._column_definitions(self.schema)
        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"CREATE TABLE {self.table_name} ({columns});"

        return self.execute_query(sql, config)

    def _column_definitions(self, schema):
        def column_defintion(column):
            # TODO: allow column type/constraints to be specified
            return f"{column} VARCHAR"

        column_names = schema["columns"]
        column_definitions = map(column_defintion, column_names)
        
        return ",".join(column_definitions)
