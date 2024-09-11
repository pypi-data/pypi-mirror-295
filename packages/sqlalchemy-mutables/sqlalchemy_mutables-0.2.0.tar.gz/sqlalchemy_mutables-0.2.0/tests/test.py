from unittest import TestCase

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
)

Base = declarative_base()


class Table(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    _column = Column("column", JSONType)
    column: json_type = JSONProperty("_column")


class TestRoot(TestCase):
    def test_init_object(self):
        table = Table(column={"a": "b"})
        assert isinstance(table.column, _NestedMutableObject)
        assert table.column == {"a": "b"}
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), _NestedMutableObject)
        assert table._column.get("value") == {"a": "b"}

    def test_init_array(self):
        table = Table(column=["a"])
        assert isinstance(table.column, _NestedMutableArray)
        assert table.column == ["a"]
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), _NestedMutableArray)
        assert table._column.get("value") == ["a"]

        table = Table(column=("a",))
        assert isinstance(table.column, _NestedMutableArray)
        assert table.column == ["a"]
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), _NestedMutableArray)
        assert table._column.get("value") == ["a"]

    def test_init_primitive(self):
        table = Table(column="str")
        assert isinstance(table.column, str)
        assert table.column == "str"
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), str)
        assert table._column.get("value") == "str"

    def test_set_object(self):
        table = Table()
        table.column = {"a": "b"}
        assert isinstance(table.column, _NestedMutableObject)
        assert table.column == {"a": "b"}
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), _NestedMutableObject)
        assert table._column.get("value") == {"a": "b"}

    def test_set_primitive(self):
        table = Table()
        table.column = "str"
        assert isinstance(table.column, str)
        assert table.column == "str"
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), str)
        assert table._column.get("value") == "str"

        table = Table()
        table.column = 123
        assert isinstance(table.column, int)
        assert table.column == 123
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), int)
        assert table._column.get("value") == 123

        table = Table()
        table.column = 12.3
        assert isinstance(table.column, float)
        assert table.column == 12.3
        assert isinstance(table._column, _NestedMutableWrapper)
        assert isinstance(table._column.get("value"), float)
        assert table._column.get("value") == 12.3

        table = Table()
        table.column = True
        assert table.column is True
        assert isinstance(table._column, _NestedMutableWrapper)
        assert table._column.get("value") is True

        table = Table()
        table.column = None
        assert table.column is None
        assert table._column.get("value") is None


class TestNested(TestCase):

    def test_init_nested_object(self):
        table = Table(column={"a": {"b": {"c": {"d": "e"}}}})
        assert isinstance(table.column, _NestedMutableObject)
        assert table.column == {"a": {"b": {"c": {"d": "e"}}}}
        assert isinstance(table._column, _NestedMutableWrapper)
        assert table._column.get("value") == {"a": {"b": {"c": {"d": "e"}}}}

        assert isinstance(table.column["a"], _NestedMutableObject)
        assert table.column["a"] == {"b": {"c": {"d": "e"}}}

        assert isinstance(table.column["a"]["b"], _NestedMutableObject)
        assert table.column["a"]["b"] == {"c": {"d": "e"}}

        assert isinstance(table.column["a"]["b"]["c"], _NestedMutableObject)
        assert table.column["a"]["b"]["c"] == {"d": "e"}

        assert isinstance(table.column["a"]["b"]["c"]["d"], str)
        assert table.column["a"]["b"]["c"]["d"] == "e"

    def test_init_nested_array(self):
        table = Table(column=["a", ["b", ["c", ["d"]]]])
        assert isinstance(table.column, _NestedMutableArray)
        assert table.column == ["a", ["b", ["c", ["d"]]]]
        assert isinstance(table._column, _NestedMutableWrapper)
        assert table._column.get("value") == ["a", ["b", ["c", ["d"]]]]

        assert isinstance(table.column[0], str)
        assert table.column[0] == "a"
        assert isinstance(table.column[1], _NestedMutableArray)
        assert table.column[1] == ["b", ["c", ["d"]]]

        assert isinstance(table.column[1][0], str)
        assert table.column[1][0] == "b"
        assert isinstance(table.column[1][1], _NestedMutableArray)
        assert table.column[1][1] == ["c", ["d"]]

        assert isinstance(table.column[1][1][0], str)
        assert table.column[1][1][0] == "c"
        assert isinstance(table.column[1][1][1], _NestedMutableArray)
        assert table.column[1][1][1] == ["d"]

        assert isinstance(table.column[1][1][1][0], str)
        assert table.column[1][1][1][0] == "d"

        table = Table(column=("a", ("b", ("c", ("d",)))))
        assert isinstance(table.column, _NestedMutableArray)
        assert table.column == ["a", ["b", ["c", ["d"]]]]
        assert isinstance(table._column, _NestedMutableWrapper)
        assert table._column.get("value") == ["a", ["b", ["c", ["d"]]]]

        assert isinstance(table.column[0], str)
        assert table.column[0] == "a"
        assert isinstance(table.column[1], _NestedMutableArray)
        assert table.column[1] == ["b", ["c", ["d"]]]

        assert isinstance(table.column[1][0], str)
        assert table.column[1][0] == "b"
        assert isinstance(table.column[1][1], _NestedMutableArray)
        assert table.column[1][1] == ["c", ["d"]]

        assert isinstance(table.column[1][1][0], str)
        assert table.column[1][1][0] == "c"
        assert isinstance(table.column[1][1][1], _NestedMutableArray)
        assert table.column[1][1][1] == ["d"]

        assert isinstance(table.column[1][1][1][0], str)
        assert table.column[1][1][1][0] == "d"


class TestDBAPI(TestCase):
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

        assert len(table.column) == 3
        for value in table.column.values():
            assert value._parent_mutable is table._column

    def test_multiple_root_arrays_get_parent(self):
        table = Table(column=[["a"], ("b",), {"c": "d"}])
        self.session.add(table)
        self.session.commit()

        assert len(table.column) == 3
        for value in table.column:
            assert value._parent_mutable is table._column


class TestObjectMethods(TestCase):
    def test_setitem(self):
        object = _NestedMutableObject()
        object["a"] = {"b": {"c": "d"}}
        assert object["a"] == {"b": {"c": "d"}}
        assert object["a"]._parent_mutable is object
        assert isinstance(object["a"]["b"], _NestedMutableObject)
        assert object["a"]["b"] == {"c": "d"}
        assert object["a"]["b"]._parent_mutable is object["a"]

    def test_setdefault(self):
        object = _NestedMutableObject({"a": {"b": "c"}})
        object.setdefault("d", {"e": "f"})
        assert isinstance(object["d"], _NestedMutableObject)
        assert object["d"] == {"e": "f"}
        assert object["d"]._parent_mutable is object

    def test_update(self):
        object = _NestedMutableObject({"a": "b"})
        object.update({"c": {"d": {"e": "f"}}}, g={"h": {"i": "j"}})

        assert isinstance(object, _NestedMutableObject)
        assert object == {
            "a": "b",
            "c": {"d": {"e": "f"}},
            "g": {"h": {"i": "j"}},
        }
        assert object._parent_mutable is None

        assert isinstance(object["c"], _NestedMutableObject)
        assert object["c"] == {"d": {"e": "f"}}
        assert object["c"]._parent_mutable is object

        assert isinstance(object["c"]["d"], _NestedMutableObject)
        assert object["c"]["d"] == {"e": "f"}
        assert object["c"]["d"]._parent_mutable is object["c"]

        assert isinstance(object["g"], _NestedMutableObject)
        assert object["g"] == {"h": {"i": "j"}}
        assert object["g"]._parent_mutable is object

        assert isinstance(object["g"]["h"], _NestedMutableObject)
        assert object["g"]["h"] == {"i": "j"}
        assert object["g"]["h"]._parent_mutable is object["g"]


class TestArrayMethods(TestCase):
    def test_setstate(self):
        array = _NestedMutableArray()
        array.__setstate__(["a", ["b", ["c"]]])

        assert isinstance(array, _NestedMutableArray)
        assert array == ["a", ["b", ["c"]]]
        assert array._parent_mutable is None

        assert isinstance(array[1], _NestedMutableArray)
        assert array[1] == ["b", ["c"]]
        assert array[1]._parent_mutable is array

        assert isinstance(array[1][1], _NestedMutableArray)
        assert array[1][1] == ["c"]
        assert array[1][1]._parent_mutable is array[1]

    def test_setitem(self):
        array = _NestedMutableArray(["a", ["b", ["c"]]])
        array[1] = ["d", ["e"]]

        assert isinstance(array, _NestedMutableArray)
        assert array == ["a", ["d", ["e"]]]
        assert array._parent_mutable is None

        assert isinstance(array[1], _NestedMutableArray)
        assert array[1] == ["d", ["e"]]
        assert array[1]._parent_mutable is array

        assert isinstance(array[1][1], _NestedMutableArray)
        assert array[1][1] == ["e"]
        assert array[1][1]._parent_mutable is array[1]

    def test_append(self):
        array = _NestedMutableArray()
        array.append(["a", ["b", ["c"]]])

        assert isinstance(array[0], _NestedMutableArray)
        assert array[0] == ["a", ["b", ["c"]]]
        assert array[0]._parent_mutable is array

        assert isinstance(array[0][1], _NestedMutableArray)
        assert array[0][1] == ["b", ["c"]]
        assert array[0][1]._parent_mutable is array[0]

        assert isinstance(array[0][1][1], _NestedMutableArray)
        assert array[0][1][1] == ["c"]
        assert array[0][1][1]._parent_mutable is array[0][1]

    def test_extend(self):
        array = _NestedMutableArray()
        array.extend(["a", ["b", ["c"]]])

        assert isinstance(array, _NestedMutableArray)
        assert array == ["a", ["b", ["c"]]]
        assert array._parent_mutable is None

        assert isinstance(array[1], _NestedMutableArray)
        assert array[1] == ["b", ["c"]]
        assert array[1]._parent_mutable is array

        assert isinstance(array[1][1], _NestedMutableArray)
        assert array[1][1] == ["c"]
        assert array[1][1]._parent_mutable is array[1]

    def test_insert(self):
        array = _NestedMutableArray(["a", "b", "c"])
        array.insert(1, ["d", ["e", ["f"]]])
        assert array == ["a", ["d", ["e", ["f"]]], "b", "c"]

        assert isinstance(array[1], _NestedMutableArray)
        assert array[1] == ["d", ["e", ["f"]]]
        assert array[1]._parent_mutable is array

        assert isinstance(array[1][1], _NestedMutableArray)
        assert array[1][1] == ["e", ["f"]]
        assert array[1][1]._parent_mutable is array[1]

        assert isinstance(array[1][1][1], _NestedMutableArray)
        assert array[1][1][1] == ["f"]
        assert array[1][1][1]._parent_mutable is array[1][1]
