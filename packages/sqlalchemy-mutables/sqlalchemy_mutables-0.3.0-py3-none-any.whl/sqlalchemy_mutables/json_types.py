# this file is used for backwards compatibility with versions <=0.2.1
from sqlalchemy_mutables.mutables import (
    json_type,
    NestedMutableJSONColumn,
    NestedMutableJSONProperty,
)

json_type = json_type
JSONType = NestedMutableJSONColumn
JSONProperty = NestedMutableJSONProperty
