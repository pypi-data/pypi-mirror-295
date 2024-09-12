from typing import Any
from unittest import TestCase

from more_itertools.recipes import pairwise
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, Session

from src.sqlalchemy_mutables.mutables import (
    NestedMutable,
    NestedMutableDict,
    NestedMutableDictColumn,
)


Base = declarative_base()


class Table(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    column = Column(NestedMutableDictColumn)


class BaseTestCase(TestCase):
    _column_type: type(NestedMutable)

    def assert_base_column(self, table: Table, value: Any, type_: type = None):
        type_ = type_ or self._column_type
        assert isinstance(table.column, type_)
        assert table.column == value

    def assert_nested_column_type(
        self, column: Any, parent: NestedMutable, type_: type = None
    ):
        type_ = type_ or self._column_type
        assert isinstance(column, type_)
        if issubclass(type_, NestedMutable):
            assert isinstance(column._parent_mutable, NestedMutable)
            assert column._parent_mutable is parent


class TestRoot(BaseTestCase):
    def test_init_object(self):
        table = Table(column={"a": "b"})
        self.assert_base_column(
            table, value={"a": "b"}, type_=NestedMutableDict
        )

    def test_set_object(self):
        table = Table()
        table.column = {"a": "b"}
        self.assert_base_column(
            table, value={"a": "b"}, type_=NestedMutableDict
        )

    def test_init_primitive(self):
        table = Table(column=None)
        self.assert_base_column(table, value=None, type_=type(None))

    def test_set_primitive(self):
        table = Table()
        table.column = None
        self.assert_base_column(table, value=None, type_=type(None))


class TestNested(BaseTestCase):
    def test_init_nested_object(self):
        table = Table(column={"a": {"b": {"c": {"d": "e"}}}})

        self.assert_base_column(
            table,
            value={"a": {"b": {"c": {"d": "e"}}}},
            type_=NestedMutableDict,
        )

        columns = [
            table.column,
            table.column["a"],
            table.column["a"]["b"],
            table.column["a"]["b"]["c"],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(
                child, parent, type_=NestedMutableDict
            )

        self.assert_nested_column_type(
            table.column["a"]["b"]["c"]["d"],
            table.column["a"]["b"]["c"],
            type_=str,
        )

        assert table.column["a"] == {"b": {"c": {"d": "e"}}}
        assert table.column["a"]["b"] == {"c": {"d": "e"}}
        assert table.column["a"]["b"]["c"] == {"d": "e"}
        assert table.column["a"]["b"]["c"]["d"] == "e"


class TestDatabase(BaseTestCase):
    session: Session

    @classmethod
    def _truncate(cls):
        cls.session.execute("TRUNCATE `my_table`;")
        assert cls.session.query(Table).count() == 0

    @classmethod
    def setUpClass(cls):
        engine = create_engine("mysql+pymysql://root@localhost:3310/my_db")
        cls.session = create_session(engine, autoflush=False, autocommit=False)
        cls.session.execute(
            "CREATE TABLE IF NOT EXISTS `my_table` ("
            "id INT PRIMARY KEY AUTO_INCREMENT,"
            "`column` JSON"
            ")"
        )
        cls._truncate()

    def tearDown(self):
        self._truncate()

    def test_equality_operator(self):
        values = [None, {"a": {"b": "c"}}]

        for value in values:
            self.session.add(Table(column=value))
            self.session.commit()

            result = (
                self.session.query(Table).filter(Table.column == value).all()
            )
            assert len(result) == 1

    def test_nested_object(self):
        # create nested entity
        table = Table(column={"a": {"b": {"c": {"d": "e"}}}})
        self.session.add(table)
        self.session.commit()

        table_id = table.id

        # make nested change
        table.column["a"]["b"] = {"f": {"g": "h"}}
        self.session.commit()

        # garbage collect entity
        self.session.expunge(table)
        del table

        # assert change persisted
        table = self.session.query(Table).filter(Table.id == table_id).first()
        assert table.column["a"]["b"]["f"]["g"] == "h"

        # make nested change
        table.column["a"]["b"]["f"]["g"] = "i"
        self.session.commit()

        # garbage collect entity
        self.session.expunge(table)
        del table

        # # assert change persisted
        table = self.session.query(Table).filter(Table.id == table_id).first()
        assert table.column["a"]["b"]["f"]["g"] == "i"

    def test_multiple_root_objects_get_parent(self):
        table = Table(column={"a": ["b"], "c": ("d",), "e": {"f": "g"}})
        self.session.add(table)
        self.session.commit()

        assert len(table.column) == 3
        for value in table.column.values():
            assert value._parent_mutable is table.column


class TestObjectMethods(BaseTestCase):
    _column_type = NestedMutableDict

    def test_setitem(self):
        table = Table(column={})
        table.column["a"] = {"b": {"c": "d"}}

        self.assert_base_column(table, value={"a": {"b": {"c": "d"}}})

        columns = [table.column, table.column["a"], table.column["a"]["b"]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)
        self.assert_nested_column_type(
            table.column["a"]["b"]["c"], table.column["a"]["b"], type_=str
        )

        assert table.column["a"] == {"b": {"c": "d"}}
        assert table.column["a"]["b"] == {"c": "d"}
        assert table.column["a"]["b"]["c"] == "d"

    def test_setdefault(self):
        table = Table(column={"a": {"b": "c"}})
        table.column.setdefault("d", {"e": "f"})

        self.assert_base_column(table, value={"a": {"b": "c"}, "d": {"e": "f"}})
        self.assert_nested_column_type(table.column["a"], table.column)
        self.assert_nested_column_type(
            table.column["a"]["b"], table.column["a"], type_=str
        )
        self.assert_nested_column_type(table.column["d"], table.column)
        self.assert_nested_column_type(
            table.column["d"]["e"], table.column["d"], type_=str
        )

        assert table.column == {"a": {"b": "c"}, "d": {"e": "f"}}
        assert table.column["a"] == {"b": "c"}
        assert table.column["a"]["b"] == "c"
        assert table.column["d"] == {"e": "f"}
        assert table.column["d"]["e"] == "f"

    def test_update(self):
        table = Table(column={"a": "b"})
        table.column.update({"c": {"d": {"e": "f"}}}, g={"h": {"i": "j"}})

        expected = {
            "a": "b",
            "c": {"d": {"e": "f"}},
            "g": {"h": {"i": "j"}},
        }
        self.assert_base_column(table, value=expected)

        columns = [table.column, table.column["c"], table.column["c"]["d"]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)

        columns = [table.column, table.column["g"], table.column["g"]["h"]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)

        self.assert_nested_column_type(
            table.column["a"], table.column, type_=str
        )
        self.assert_nested_column_type(
            table.column["c"]["d"]["e"], table.column["c"]["d"], type_=str
        )
        self.assert_nested_column_type(
            table.column["g"]["h"]["i"], table.column["g"]["h"], type_=str
        )

        assert table.column["a"] == "b"
        assert table.column["c"] == {"d": {"e": "f"}}
        assert table.column["c"]["d"] == {"e": "f"}
        assert table.column["c"]["d"]["e"] == "f"
        assert table.column["g"] == {"h": {"i": "j"}}
        assert table.column["g"]["h"] == {"i": "j"}
        assert table.column["g"]["h"]["i"] == "j"
