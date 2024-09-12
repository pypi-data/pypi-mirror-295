import typing
from types import UnionType, GenericAlias

class TypeInfo(typing.NamedTuple):
    type: typing.Type
    is_optional: bool
    
    
def annotation_extract_primary_type(annotation: typing.Any) -> TypeInfo:
    if typing.get_origin(annotation) is UnionType:
        args = typing.get_args(annotation)
        if len(args) == 2 and args[1] == type(None):
            return TypeInfo(args[0], is_optional=True)
        else:
            return TypeInfo(annotation, is_optional=False)
    else:
        return TypeInfo(annotation, is_optional=False)
