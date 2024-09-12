import sqlalchemy
from sqlalchemy import select

from caqtus.session.sql._path_table import SQLSequencePath


if __name__ == "__main__":
    top_query = (
        select(SQLSequencePath)
        .where(SQLSequencePath.parent_id == 5)
        .cte(recursive=True)
    )
    alias = sqlalchemy.orm.aliased(top_query)
    descendants_query = top_query.union(
        select(SQLSequencePath).join(alias, SQLSequencePath.parent_id == alias.c.id)
    )
    query = select(alias).select_from(descendants_query)

    print(query.compile())
