from typing import TypeVar

from sqlalchemy import JSON, cast, literal, TypeDecorator
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.mutable import Mutable, MutableList, MutableDict
from sqlalchemy.orm.attributes import flag_modified, InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression


__all__ = [
    "json_type",
    "NestedMutableListColumn",
    "NestedMutableDictColumn",
    "NestedMutableJSONColumn",
    "NestedMutableJSONProperty"
]


json_type = TypeVar("json_type", str, int, float, list, tuple, bool, type(None))


_primitive_types = (str, int, float, bool, type(None))


class NestedMutable:
    # TODO: weakref?
    _parent_mutable: "NestedMutable" = None

    def changed(self):
        """Subclasses should call this method whenever change events occur."""
        if isinstance(self, NestedMutable) and self._parent_mutable is not None:
            self._parent_mutable.changed()

        for parent, key in self._parents.items():
            flag_modified(parent, key)

    @classmethod
    def coerce(cls, key, value, parent_mutable=None):
        if isinstance(value, cls):
            return value

        if isinstance(value, _primitive_types):
            return value

        if isinstance(value, dict):
            return NestedMutableDict.coerce(
                key, value, parent_mutable=parent_mutable
            )

        if isinstance(value, (tuple, list)):
            return NestedMutableList.coerce(
                key, value, parent_mutable=parent_mutable
            )

        return Mutable.coerce(key, value)


class NestedMutableList(NestedMutable, MutableList):
    @classmethod
    def coerce(cls, key, value, parent_mutable=None):
        if not isinstance(value, (list, tuple)):
            return Mutable.coerce(key, value)

        coerced_value = cls(value)

        # set parent for changed event propagation
        coerced_value._parent_mutable = parent_mutable

        # coerce children
        for i, child_value in enumerate(coerced_value):
            coerced_value[i] = NestedMutable.coerce(
                i, child_value, parent_mutable=coerced_value
            )

        return coerced_value

    def __setstate__(self, state):
        self[:] = [
            NestedMutable.coerce(i, x, parent_mutable=self)
            for i, x in enumerate(state)
        ]

    def __setitem__(self, index, value):
        value = NestedMutable.coerce(index, value, parent_mutable=self)
        list.__setitem__(self, index, value)
        self.changed()

    # not supported for 3.9?
    # def __setslice__(self, start, end, value):
    #     value = [_NestedMutable.coerce(i, x, parent_mutable=self) for i, x in enumerate(value)]
    #     list.__setslice__(self, start, end, value)
    #     self.changed()

    def append(self, x):
        list.append(
            self, NestedMutable.coerce(len(self), x, parent_mutable=self)
        )
        self.changed()

    def extend(self, x):
        x = [
            NestedMutable.coerce(i, y, parent_mutable=self)
            for i, y in enumerate(x)
        ]
        list.extend(self, x)
        self.changed()

    def insert(self, i, x):
        x = NestedMutable.coerce(i, x, parent_mutable=self)
        list.insert(self, i, x)
        self.changed()


class NestedMutableDict(NestedMutable, MutableDict):
    @classmethod
    def coerce(cls, key, value, parent_mutable=None):
        if not isinstance(value, dict):
            return Mutable.coerce(key, value)

        coerced_value = cls(value)

        # set parent for changed event propagation
        coerced_value._parent_mutable = parent_mutable

        # coerce children
        for child_key, child_value in coerced_value.items():
            coerced_value[child_key] = NestedMutable.coerce(
                child_key, child_value, parent_mutable=coerced_value
            )

        return coerced_value

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events."""
        value = NestedMutable.coerce(key, value, parent_mutable=self)
        dict.__setitem__(self, key, value)
        self.changed()

    def setdefault(self, key, value):
        value = NestedMutable.coerce(key, value, parent_mutable=self)
        result = dict.setdefault(self, key, value)
        self.changed()
        return result

    def update(self, *a, **kw):
        dict_ = a[0] if len(a) == 1 else {}
        for k, v in {**dict_, **kw}.items():
            self[k] = v


class NestedMutableJSON(NestedMutable, MutableDict):
    @classmethod
    def coerce(cls, key, value, parent_mutable=None):
        if not isinstance(value, (dict, list, tuple, *_primitive_types)):
            return Mutable.coerce(key, value)

        nested_mutable_json = cls()
        value = NestedMutable.coerce(
            key, value, parent_mutable=nested_mutable_json
        )

        iterator = []
        if isinstance(value, dict):
            iterator = value.items()
        if isinstance(value, tuple):
            value = list(value)
        if isinstance(value, list):
            iterator = enumerate(value)

        for id_, sub_value in iterator:
            value[id_] = NestedMutable.coerce(
                id_, sub_value, parent_mutable=value
            )

        nested_mutable_json["value"] = value
        return nested_mutable_json

    def __eq__(self, other):
        if isinstance(other, NestedMutableJSON):
            other = other.get("value")

        return self.get("value") == other

    def __str__(self):
        return str(self.get("value"))


def _json_property(key: str, fget=None, fset=None) -> hybrid_property:
    def get(self):
        hybrid_property_ = getattr(self, key)

        # skip if hybrid_property is not instantiated
        if isinstance(hybrid_property_, InstrumentedAttribute):
            return hybrid_property_

        return hybrid_property_.get("value")

    def set_(self, value):
        if fset is not None:
            value = fset(value)

        setattr(self, key, value)

    return hybrid_property(fget=get, fset=set_)


class CustomList(JSON):
    class comparator_factory(JSON.Comparator):
        def __eq__(self, other):
            if isinstance(other, (list, tuple)):
                return BinaryExpression(self.expr, cast(other, JSON()), "=")

            return super().__eq__(other)


class CustomDict(JSON):
    class comparator_factory(JSON.Comparator):
        def __eq__(self, other):
            if isinstance(other, dict):
                return BinaryExpression(self.expr, cast(other, JSON()), "=")

            return super().__eq__(other)


class CustomJSON(JSON):
    class comparator_factory(JSON.Comparator):
        def __eq__(self, other):
            if isinstance(other, (dict, list, tuple)):
                return BinaryExpression(self.expr, cast(other, JSON()), "=")

            if isinstance(other, type(None)):
                # TODO: implement 'strict' param? only allow JSON null?
                return BinaryExpression(
                    self.expr, cast(literal("null"), JSON()), "="
                )

            return super().__eq__(other)


class DictType(TypeDecorator):
    impl = CustomDict(none_as_null=True)

    coerce_to_is_types = (type(None),)

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)


class ListType(TypeDecorator):
    impl = CustomList(none_as_null=True)

    coerce_to_is_types = (type(None),)

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)


class JSONType(TypeDecorator):
    impl = CustomJSON

    coerce_to_is_types = (type(None), bool)

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value, dialect):
        if isinstance(value, NestedMutableJSON):
            value = value.get("value")
        return value

    def process_result_value(self, value, dialect):
        return value


NestedMutableListColumn = NestedMutableList.as_mutable(ListType)
NestedMutableDictColumn = NestedMutableDict.as_mutable(DictType)
NestedMutableJSONColumn = NestedMutableJSON.as_mutable(JSONType)
NestedMutableJSONProperty = _json_property
