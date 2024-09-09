from typing import TypeVar

from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.ext.mutable import (Mutable, MutableDict, MutableList)
from sqlalchemy.orm.attributes import flag_modified


_primitive_types = (str, int, float, bool, type(None))
json_type = TypeVar('json_type', str, int, float, list, tuple, bool, type(None))


class _NestedMutable:
    # TODO: weakref?
    _parent_mutable: "_NestedMutable" = None

    def changed(self):
        """Subclasses should call this method whenever change events occur."""
        if isinstance(self, _NestedMutable) and self._parent_mutable is not None:
            self._parent_mutable.changed()

        for parent, key in self._parents.items():
            flag_modified(parent, key)

    @classmethod
    def coerce(cls, key, value, parent_mutable = None):
        if isinstance(value, cls):
            return value

        if isinstance(value, _primitive_types):
            return value

        if isinstance(value, dict):
            return _NestedMutableObject.coerce(key, value, parent_mutable=parent_mutable)

        if isinstance(value, (tuple, list)):
            return _NestedMutableArray.coerce(key, value, parent_mutable=parent_mutable)

        return Mutable.coerce(key, value)


class _NestedMutableObjectBase(_NestedMutable, MutableDict):
    @classmethod
    def coerce(cls, key, value, parent_mutable = None):
        if not isinstance(value, dict):
            return Mutable.coerce(key, value)

        coerced_value = cls(value)

        # set parent for changed event propagation
        if parent_mutable is not None:
            coerced_value._parent_mutable = parent_mutable

        # coerce children
        for child_key, child_value in coerced_value.items():
            coerced_value[child_key] = _NestedMutable.coerce(
                child_key, child_value, parent_mutable=coerced_value
            )

        return coerced_value


class _NestedMutableObject(_NestedMutableObjectBase):

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events."""
        value = _NestedMutable.coerce(key, value, parent_mutable=self)
        dict.__setitem__(self, key, value)
        self.changed()

    def setdefault(self, key, value):
        value = _NestedMutable.coerce(key, value, parent_mutable=self)
        result = dict.setdefault(self, key, value)
        self.changed()
        return result

    def update(self, *a, **kw):
        if len(a) > 1:  # not allowed by python
            raise NotImplementedError
        elif len(a) == 1:
            a = ({k: _NestedMutableObject.coerce(k, v, parent_mutable=self) for k, v in a[0].items()},)

        for k, v in kw.items():
            kw[k] = _NestedMutable.coerce(k, v, parent_mutable=self)

        dict.update(self, *a, **kw)
        self.changed()



class _NestedMutableArray(_NestedMutable, MutableList):
    @classmethod
    def coerce(cls, key, value, parent_mutable=None):
        if not isinstance(value, (list, tuple)):
            return Mutable.coerce(key, value)

        coerced_value = cls(value)

        # set parent for changed event propagation
        if parent_mutable is not None:
            coerced_value._parent_mutable = parent_mutable

        # coerce children
        for i, child_value in enumerate(coerced_value):
            coerced_value[i] = super().coerce(i, child_value, parent_mutable=coerced_value)

        return coerced_value

    def __setstate__(self, state):
        self[:] = [_NestedMutable.coerce(i, x, parent_mutable=self) for i, x in enumerate(state)]

    def __setitem__(self, index, value):
        value = _NestedMutable.coerce(index, value, parent_mutable=self)
        list.__setitem__(self, index, value)
        self.changed()

    # not supported for 3.9?
    # def __setslice__(self, start, end, value):
    #     value = [_NestedMutable.coerce(i, x, parent_mutable=self) for i, x in enumerate(value)]
    #     list.__setslice__(self, start, end, value)
    #     self.changed()

    def append(self, x):
        list.append(self, _NestedMutable.coerce(len(self), x, parent_mutable=self))
        self.changed()

    def extend(self, x):
        x = [_NestedMutable.coerce(i, y, parent_mutable=self) for i, y in enumerate(x)]
        list.extend(self, x)
        self.changed()

    def insert(self, i, x):
        x = _NestedMutable.coerce(i, x, parent_mutable=self)
        list.insert(self, i, x)
        self.changed()


class _NestedMutableWrapper(_NestedMutableObjectBase):
    ...


def _json_property(key: str, fget=None, fset=None) -> property:
    def get(self):
        json_object = getattr(self, key)
        if not isinstance(json_object, _NestedMutableWrapper):
            raise Exception  # TODO

        # don't assign parent to primitives
        value = json_object.get("value")

        # set parent for parsed dict root values
        if isinstance(value, dict):
            for child_value in value.values():
                if not isinstance(child_value, _primitive_types):
                    child_value._parent_mutable = json_object

        # set parent for parsed list root values
        if isinstance(value, list):
            for child_value in value:
                if not isinstance(child_value, _primitive_types):
                    child_value._parent_mutable = json_object

        if fget is not None:
            value = fget(value)

        return value

    def set_(self, value):
        if fset is not None:
            value = fset(value)
        value = _NestedMutable.coerce(key, value)
        json_object = _NestedMutableWrapper(value=value)
        if not isinstance(value, _primitive_types):
            value._parent_mutable = json_object

        setattr(self, key, json_object)

    return property(fget=get, fset=set_)


class JSONType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        print(type(value.get("value")), value.get("value"))
        return value.get("value")

    def process_result_value(self, value, dialect):
        value = _NestedMutable.coerce("value", value)
        return _NestedMutableWrapper(value=value)


JSONType = _NestedMutableWrapper.as_mutable(JSONType)
JSONProperty = _json_property
