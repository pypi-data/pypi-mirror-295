# from pydantic import BaseModel as _BaseModel
from pydantic import BaseModel

from typing import Any, Dict, Type, get_origin, get_args, Union

from json import JSONEncoder

#
# def _default(self, obj):
#     return getattr(obj.__class__, "json", _default.default)(obj)


# _default.default = JSONEncoder().default
# JSONEncoder.default = _default


# class BaseModel(_BaseModel):
#     """
#     BaseModel that is subscriptable like a dictionary
#     """

# def __init__(self, data=None, **kwargs):
#     if data is not None:
#         if not isinstance(data, dict):
#             raise TypeError(
#                 f"Expected a dictionary for initialization, got {type(data).__name__}"
#             )
#         kwargs.update(data)
#
#     fields = self.__annotations__
#     for field_name, field_type in fields.items():
#         if field_name in kwargs:
#             origin = get_origin(field_type)
#             args = get_args(field_type)
#
#             if origin:
#                 # Check for List, Dict, or Optional
#                 if origin is list and args and issubclass(args[0], BaseModel):
#                     kwargs[field_name] = [
#                         args[0](**item) if isinstance(item, dict) else item
#                         for item in kwargs[field_name]
#                     ]
#                 elif origin is dict and args and issubclass(args[1], BaseModel):
#                     kwargs[field_name] = {
#                         k: args[1](**v) if isinstance(v, dict) else v
#                         for k, v in kwargs[field_name].items()
#                     }
#                 elif origin is Union and BaseModel in args:
#                     # Handling Optional[BaseModel] case
#                     actual_type = next(t for t in args if issubclass(t, BaseModel))
#                     if isinstance(kwargs[field_name], dict):
#                         kwargs[field_name] = actual_type(**kwargs[field_name])
#             elif issubclass(field_type, BaseModel):
#                 kwargs[field_name] = field_type(**kwargs[field_name])
#
#     super().__init__(**kwargs)
#
# def __getitem__(self, item):
#     return self.__dict__[item]
#
# def __setitem__(self, key, value):
#     setattr(self, key, value)
#
# def __len__(self):
#     return len(self.__dict__)
#
# def __contains__(self, item):
#     return item in self.__dict__
#
# def __iter__(self):
#     return iter(self.__dict__)
#
# def keys(self):
#     return self.__dict__.keys()
#
# def values(self):
#     return self.__dict__.values()
#
# def get(self, key, default=None):
#     return self.__dict__.get(key, default)
#
# def update(self, data: Dict[str, Any]):
#     for key, value in data.items():
#         field_type = self.__annotations__.get(key, type(value))
#         if issubclass(field_type, BaseModel) and isinstance(value, dict):
#             value = field_type(**value)
#         setattr(self, key, value)
#     return self
#
# def __json__(self):
#     return self.model_dump(mode="json")
#
# def __delitem__(self, key):
#     delattr(self, key)
#
# def items(self):
#     return self.__dict__.items()
