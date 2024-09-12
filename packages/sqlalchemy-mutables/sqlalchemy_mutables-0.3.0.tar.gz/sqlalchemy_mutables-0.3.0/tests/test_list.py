from typing import Any
from unittest import TestCase

from more_itertools.recipes import pairwise
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, Session

from src.sqlalchemy_mutables.mutables import (
    NestedMutable,
    NestedMutableList,
    NestedMutableListColumn,
)


Base = declarative_base()


class Table(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    column = Column(NestedMutableListColumn)


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
    def test_init_array(self):
        table = Table(column=["a"])
        self.assert_base_column(table, value=["a"], type_=NestedMutableList)

        table = Table(column=("a",))
        self.assert_base_column(table, value=["a"], type_=NestedMutableList)

    def test_set_array(self):
        table = Table()
        table.column=["a"]
        self.assert_base_column(table, value=["a"], type_=NestedMutableList)

        table = Table()
        table.column = column=("a",)
        self.assert_base_column(table, value=["a"], type_=NestedMutableList)

    def test_init_primitive(self):
        table = Table(column=None)
        self.assert_base_column(table, value=None, type_=type(None))

    def test_set_primitive(self):
        table = Table()
        table.column = None
        self.assert_base_column(table, value=None, type_=type(None))


class TestNested(BaseTestCase):
    def test_init_nested_array(self):
        table = Table(column=["a", ["b", ["c", ["d"]]]])

        self.assert_base_column(
            table,
            value=["a", ["b", ["c", ["d"]]]],
            type_=NestedMutableList,
        )

        columns = [
            table.column,
            table.column[1],
            table.column[1][1],
            table.column[1][1][1],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(
                child, parent, type_=NestedMutableList
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
            type_=NestedMutableList,
        )

        columns = [
            table.column,
            table.column[1],
            table.column[1][1],
            table.column[1][1][1],
        ]
        for parent, child in pairwise(columns):
            self.assert_nested_column_type(
                child, parent, type_=NestedMutableList
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
        values = (None, ["a", "b"])

        for value in values:
            self.session.add(Table(column=value))
        self.session.commit()

        for value in values:
            result = (
                self.session.query(Table).filter(Table.column == value).all()
            )
            assert len(result) == 1

    def test_nested_array(self):
        # create nested entity
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

    def test_multiple_root_arrays_get_parent(self):
        table = Table(column=[["a"], ("b",), {"c": "d"}])
        self.session.add(table)
        self.session.commit()

        assert len(table.column) == 3
        for value in table.column:
            assert value._parent_mutable is table.column


class TestArrayMethods(BaseTestCase):
    _column_type = NestedMutableList

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
