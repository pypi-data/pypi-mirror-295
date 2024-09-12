from typing import Any
from unittest import TestCase

from more_itertools.recipes import pairwise
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, Session

from src.sqlalchemy_mutables.json_types import (
    JSONType,
    JSONProperty,
    _NestedMutableObject,
    _NestedMutableArray,
    _NestedMutableWrapper,
    json_type,
    _NestedMutable,
)


Base = declarative_base()


class Table(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    _column = Column("column", JSONType)
    column: json_type = JSONProperty("_column")


class BaseTestCase(TestCase):
    _column_type: type(_NestedMutable)

    def assert_base_column(self, table: Table, value: Any, type_: type = None):
        type_ = type_ or self._column_type
        assert isinstance(table.column, type_)
        assert isinstance(table._column, _NestedMutableWrapper)
        if issubclass(type_, _NestedMutable):
            assert table.column._parent_mutable is table._column
        assert table._column.get("value") is table.column
        assert table.column == value
        assert table._column.get("value") == value

    def assert_nested_column_type(
        self, column: Any, parent: _NestedMutable, type_: type = None
    ):
        type_ = type_ or self._column_type
        assert isinstance(column, type_)
        if issubclass(type_, _NestedMutable):
            assert isinstance(column._parent_mutable, _NestedMutable)
            assert column._parent_mutable is parent


class TestRoot(BaseTestCase):
    def test_init_object(self):
        table = Table(column={"a": "b"})
        self.assert_base_column(
            table, value={"a": "b"}, type_=_NestedMutableObject
        )

    def test_init_array(self):
        table = Table(column=["a"])
        self.assert_base_column(table, value=["a"], type_=_NestedMutableArray)

        table = Table(column=("a",))
        self.assert_base_column(table, value=["a"], type_=_NestedMutableArray)

    def test_init_primitive(self):
        for value in [None, False, 1, 2.3, "4"]:
            table = Table(column=value)
            self.assert_base_column(table, value=value, type_=type(value))

    def test_set_object(self):
        table = Table()
        table.column = {"a": "b"}
        self.assert_base_column(
            table, value={"a": "b"}, type_=_NestedMutableObject
        )

    def test_set_primitive(self):
        for value in [None, False, 1, 2.3, "4"]:
            table = Table()
            table.column = value
            self.assert_base_column(table, value=value, type_=type(value))


class TestNested(BaseTestCase):
    def test_init_nested_object(self):
        table = Table(column={"a": {"b": {"c": {"d": "e"}}}})

        self.assert_base_column(
            table,
            value={"a": {"b": {"c": {"d": "e"}}}},
            type_=_NestedMutableObject,
        )

        columns = [
            table.column,
            table.column["a"],
            table.column["a"]["b"],
            table.column["a"]["b"]["c"],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(
                child, parent, type_=_NestedMutableObject
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

    def test_init_nested_array(self):
        table = Table(column=["a", ["b", ["c", ["d"]]]])

        self.assert_base_column(
            table,
            value=["a", ["b", ["c", ["d"]]]],
            type_=_NestedMutableArray,
        )

        columns = [
            table.column,
            table.column[1],
            table.column[1][1],
            table.column[1][1][1],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(
                child, parent, type_=_NestedMutableArray
            )

        self.assert_nested_column_type(
            table.column[1][1][1][0], table.column[1][1][1], type_=str
        )

        assert table.column[0] == "a"
        assert table.column[1] == ["b", ["c", ["d"]]]
        assert table.column[1][0] == "b"
        assert table.column[1][1] == ["c", ["d"]]
        assert table.column[1][1][0] == "c"
        assert table.column[1][1][1] == ["d"]
        assert table.column[1][1][1][0] == "d"

        table = Table(column=("a", ("b", ("c", ("d",)))))
        self.assert_base_column(
            table,
            value=["a", ["b", ["c", ["d"]]]],
            type_=_NestedMutableArray,
        )

        columns = [
            table.column,
            table.column[1],
            table.column[1][1],
            table.column[1][1][1],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(
                child, parent, type_=_NestedMutableArray
            )

        self.assert_nested_column_type(
            table.column[1][1][1][0], table.column[1][1][1], type_=str
        )

        assert table.column[0] == "a"
        assert table.column[1] == ["b", ["c", ["d"]]]
        assert table.column[1][0] == "b"
        assert table.column[1][1] == ["c", ["d"]]
        assert table.column[1][1][0] == "c"
        assert table.column[1][1][1] == ["d"]
        assert table.column[1][1][1][0] == "d"


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
        values = (None, True, 1, "str", {"a": {"b": "c"}}, ["a", "b"])

        for value in values:
            self.session.add(Table(column=value))
        self.session.commit()

        for value in values:
            result = (
                self.session.query(Table).filter(Table.column == value).all()
            )
            assert len(result) == 1

    def test_wrapper_not_persisted_in_db(self):
        # create nested JSON entity
        table = Table(column={"a": "b"})
        self.session.add(table)
        self.session.commit()

        table_id = table.id

        raw_column_value = self.session.execute(
            f"SELECT my_table.`column` FROM my_table WHERE my_table.id = {table_id};"
        ).scalar()
        assert "value" not in raw_column_value
        assert raw_column_value == '{"a": "b"}'

    def test_nested_object(self):
        # create nested JSON entity
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

    def test_nested_array(self):
        # create nested JSON entity
        table = Table(column=["a", ["b", ["c", ["d"]]]])
        self.session.add(table)
        self.session.commit()

        table_id = table.id

        # make nested change
        table.column[1][1] = ["e", ["f", ["g"]]]
        self.session.commit()

        # garbage collect entity
        self.session.expunge(table)
        del table

        # assert change persisted
        table = self.session.query(Table).filter(Table.id == table_id).first()
        assert table.column[1][1] == ["e", ["f", ["g"]]]

        # make nested change
        table.column[1][1][1] = "i"
        self.session.commit()

        # garbage collect entity
        self.session.expunge(table)
        del table

        # # assert change persisted
        table = self.session.query(Table).filter(Table.id == table_id).first()
        assert table.column[1][1][1] == "i"

    def test_multiple_root_objects_get_parent(self):
        table = Table(column={"a": ["b"], "c": ("d",), "e": {"f": "g"}})
        self.session.add(table)
        self.session.commit()

        assert table.column._parent_mutable is table._column
        assert len(table.column) == 3
        for value in table.column.values():
            assert value._parent_mutable is table.column

    def test_multiple_root_arrays_get_parent(self):
        table = Table(column=[["a"], ("b",), {"c": "d"}])
        self.session.add(table)
        self.session.commit()

        assert table.column._parent_mutable is table._column
        assert len(table.column) == 3
        for value in table.column:
            assert value._parent_mutable is table.column


class TestObjectMethods(BaseTestCase):
    _column_type = _NestedMutableObject

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


class TestArrayMethods(BaseTestCase):
    _column_type = _NestedMutableArray

    def test_setstate(self):
        table = Table(column=[])
        table.column.__setstate__(["a", ["b", ["c"]]])

        self.assert_base_column(table, value=["a", ["b", ["c"]]])

        columns = [table.column, table.column[1], table.column[1][1]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)
        self.assert_nested_column_type(
            table.column[1][1][0], table.column[1][1], type_=str
        )

        assert table.column[1] == ["b", ["c"]]
        assert table.column[1][0] == "b"
        assert table.column[1][1] == ["c"]
        assert table.column[1][1][0] == "c"

    def test_setitem(self):
        table = Table(column=["a", ["b", ["c"]]])
        table.column[1] = ["d", ["e"]]

        self.assert_base_column(table, value=["a", ["d", ["e"]]])

        columns = [table.column, table.column[1], table.column[1][1]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)
        self.assert_nested_column_type(
            table.column[1][1][0], table.column[1][1], type_=str
        )

        assert table.column[1] == ["d", ["e"]]
        assert table.column[1][0] == "d"
        assert table.column[1][1] == ["e"]
        assert table.column[1][1][0] == "e"

    def test_append(self):
        table = Table(column=[])
        table.column.append(["a", ["b", ["c"]]])

        self.assert_base_column(table, value=[["a", ["b", ["c"]]]])

        columns = [
            table.column,
            table.column[0],
            table.column[0][1],
            table.column[0][1][1],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)
        self.assert_nested_column_type(
            table.column[0][1][1][0], table.column[0][1][1], type_=str
        )

        assert table.column[0] == ["a", ["b", ["c"]]]
        assert table.column[0][0] == "a"
        assert table.column[0][1] == ["b", ["c"]]
        assert table.column[0][1][0] == "b"
        assert table.column[0][1][1] == ["c"]
        assert table.column[0][1][1][0] == "c"

    def test_extend(self):
        table = Table(column=[])
        table.column.extend(["a", ["b", ["c"]]])

        self.assert_base_column(table, value=["a", ["b", ["c"]]])

        columns = [table.column, table.column[1], table.column[1][1]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)
        self.assert_nested_column_type(
            table.column[1][1][0], table.column[1][1], type_=str
        )

        assert table.column[0] == "a"
        assert table.column[1] == ["b", ["c"]]
        assert table.column[1][0] == "b"
        assert table.column[1][1] == ["c"]
        assert table.column[1][1][0] == "c"

    def test_insert(self):
        table = Table(column=["a", "b", "c"])
        table.column.insert(1, ["d", ["e", ["f"]]])

        self.assert_base_column(
            table, value=["a", ["d", ["e", ["f"]]], "b", "c"]
        )

        columns = [table.column, table.column[1], table.column[1][1]]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(child, parent)
        self.assert_nested_column_type(
            table.column[1][1][0], table.column[1][1], type_=str
        )

        assert table.column[0] == "a"
        assert table.column[1] == ["d", ["e", ["f"]]]
        assert table.column[1][1] == ["e", ["f"]]
        assert table.column[1][1][1] == ["f"]
        assert table.column[1][1][1][0] == "f"
        assert table.column[2] == "b"
        assert table.column[3] == "c"
