import enum

from typing import Type

import pydantic

from . import config, models


class TableSpec(pydantic.BaseModel):
    name: str
    model_cls: Type[models.BaseModel]

    def get_airtable_name(self):
        return config.Config.load().airtable.table_names[self.name]


class Table(enum.Enum):
    ITEMS_BY_HOUSEHOLD_SIZE = TableSpec(
        name="items_by_household_size", model_cls=models.ItemsByHouseholdSizeModel,
    )

    def find_table_for(cls, model_cls):
        for table in self:
            if model_cls == table.model_cls:
                return table

        raise ValueError(f"Provided model does not have an associated table: {model}")
