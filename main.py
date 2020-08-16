from core import airtable, tables


if __name__ == "__main__":
    client = airtable.Client()
    # NOTE that this will return a list of `ItemsByHouseholdSizeModel`
    res = client.get_all(tables.Table.ITEMS_BY_HOUSEHOLD_SIZE)
    print(res[0])
    print(res[0].get_quantity(3))
    print(res[0].to_airtable())
