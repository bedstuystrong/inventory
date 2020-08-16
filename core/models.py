import abc

from typing import Optional

import pydantic


def _get_alias_generator(aliases):
    """Creates a pydantic alias generator for translating from member variable names to airtable field names"""

    def _alias_generator(name):
        if name == "id":
            return "id"

        if name not in aliases:
            raise ValueError(f"Provided name does not have an alias: {name}")

        return aliases.get(name)

    return _alias_generator


class BaseModel(pydantic.BaseModel, abc.ABC):
    id: str

    @classmethod
    def from_airtable(cls, raw_dict):
        return cls(id=raw_dict["id"], **raw_dict["fields"])

    def to_airtable(self):
        fields = self.dict(by_alias=True, exclude_none=True)
        del fields["id"]

        return {
            "id": self.id,
            "fields": fields,
        }


class ItemsByHouseholdSizeModel(BaseModel):
    item: str
    unit: str

    one_persons: int
    two_persons: int
    three_persons: int
    four_persons: int
    five_persons: int
    six_persons: int
    seven_persons: int
    eight_persons: int

    # TODO : what does it mean when a field doesn't have a category?
    category: Optional[str]

    class Config:
        alias_generator = _get_alias_generator(
            {
                "item": "Item",
                "unit": "Unit",
                "category": "Category",
                "one_persons": "1 Person(s)",
                "two_persons": "2 Person(s)",
                "three_persons": "3 Person(s)",
                "four_persons": "4 Person(s)",
                "five_persons": "5 Person(s)",
                "six_persons": "6 Person(s)",
                "seven_persons": "7 Person(s)",
                "eight_persons": "8 Person(s)",
            }
        )

    def get_quantity(self, household_size):
        if household_size < 1 or household_size > 8:
            raise ValueError(f"Provided unsupported household size: {household_size}")

        household_size_attr_name = {
            1: "one_persons",
            2: "two_persons",
            3: "three_persons",
            4: "four_persons",
            5: "five_persons",
            6: "six_persons",
            7: "seven_persons",
            8: "eight_persons",
        }[household_size]

        return getattr(self, household_size_attr_name)
