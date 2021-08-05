from sqlalchemy import inspect


def object_as_dict(obj):
    """將DB Obj轉換為 DICT"""
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}