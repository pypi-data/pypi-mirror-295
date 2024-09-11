from xl_database import db
from jsonschema import validate


class DatabaseMixin:
    @staticmethod
    def flush():
        db.session.flush()

    @staticmethod
    def commit():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def query_(*args, **kwargs):
        return db.session.query(*args, **kwargs)

    @staticmethod
    def add_all(items):
        db.session.add_all(items)
        db.session.commit()
        return items


class QueryMixin:
    @classmethod
    def select(cls, params, conds):
        """ 筛选(模糊匹配）
        ?name=1&asset_sn=2019-BG-5453
        """
        flts = []
        for cond in conds:
            value = params.get(cond)
            flts += [getattr(cls, cond).like(f'%{value}%')
                     ] if value not in [None, ''] else []
        return flts

    @classmethod
    def select_(cls, params, conds):
        """ 筛选(精确匹配）
        ?name=1&asset_sn=2019-BG-5453
        """
        flts = []
        for cond in conds:
            value = params.get(cond)
            flts += [getattr(cls, cond) ==
                     value] if value not in [None, ''] else []
        return flts

    @classmethod
    def select_date(cls, attr_name, params):
        """ 日期筛选"""
        flts = []
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        flts += [getattr(cls, attr_name) >= start_date] if start_date else []
        flts += [getattr(cls, attr_name) <= end_date] if end_date else []
        return flts

    @staticmethod
    def all(cls, query, method='to_json'):
        """返回全部记录
        """
        items = query.all()
        return [getattr(item, method)() for item in items]

    @staticmethod
    def paginate(query, params, method='to_json'):
        """分页
        page_size=100&page_num=1
        """
        page_num = int(params.get('page_num', '1'))
        page_size = int(params.get('page_size', '10'))
        pagination = query.paginate(page_num, per_page=page_size)
        rst = {
            'items': [getattr(item, method)() for item in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages
        }
        return rst


class MapperMixin:
    @staticmethod
    def jsonlize(items):
        return [item.to_json() for item in items]

    @classmethod
    def add_(cls, data):
        obj = cls.new(data)
        obj.add_one()
        return obj

    @classmethod
    def add(cls, data, sync=True):
        if hasattr(cls, '__schema__'):
            validate(instance=data, schema=cls.__schema__)
        obj = cls.add_(data)
        if sync:
            cls.commit()
        return obj
    
    @classmethod
    def add_list(cls, data, sync=True):
        for item in data:
            cls.add(item, sync=False)
        if sync:
            cls.commit()

    @classmethod
    def save(cls, primary_key, data, sync=True):
        if hasattr(cls, '__schema__'):
            validate(instance=data, schema=cls.__schema__)
        obj = cls.get_one(primary_key)
        if obj:
            obj.update(data)
            if sync:
                cls.commit()
        else:
            cls.add(data, sync=sync)

    @classmethod
    def get_one(cls, primary_key):
        return cls.query.get(primary_key)

    @classmethod
    def delete_list(cls, sync=True, **kwargs):
        cls.make_query(**kwargs).delete(synchronize_session=False)
        if sync:
            cls.commit()

    @classmethod
    def make_flts(cls, **kwargs):
        return [getattr(cls, k) == v for k, v in kwargs.items() if v is not None]

    @classmethod
    def make_query(cls, **kwargs):
        flts = cls.make_flts(**kwargs)
        return cls.filter(*flts)

    @classmethod
    def get_list(cls, order_by=None, **kwargs):
        query = cls.make_query(**kwargs)
        if order_by:
            for order_key, order_way in order_by.items():
                query = query.order_by(getattr(cls, order_key).desc(
                ) if order_way == 'desc' else getattr(cls, order_key).asc())
        return query.all()

    @classmethod
    def get_json(cls, primary_key):
        obj = cls.get_one(primary_key)
        return obj.to_json() if obj else {}

    @classmethod
    def get_jsons(cls, page_num=None, page_size=None, order_by=None, **kwargs):
        if page_num or page_size:
            pagination = {
                'page_num': page_num if page_num else 1,
                'page_size': page_size if page_size else 20
            }
            query = cls.make_query(**kwargs)
            if order_by:
                for order_key, order_way in order_by.items():
                    query = query.order_by(getattr(cls, order_key).desc(
                    ) if order_way == 'desc' else getattr(cls, order_key).asc())
            return cls.paginate(query, pagination)
        else:
            items = cls.get_list(order_by=order_by, **kwargs)
            return cls.jsonlize(items)

    @classmethod
    def get_attrs(cls, attr_names, **kwargs):
        flts = cls.make_flts(**kwargs)
        attrs = [getattr(cls, attr_name) for attr_name in attr_names]
        return cls.query_(*attrs).filter(*flts).all()

    @classmethod
    def get_map(cls, attr_names):
        rst_map = {}
        for item in cls.get_attrs(attr_names):
            a, b = item
            rst_map[a] = b
        return rst_map
