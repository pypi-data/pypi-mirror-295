import typing
import numpy as np
from enum import Enum
from gymnasium import Env


class Observation(np.ndarray):
    fields = []  # list of field names in the observation

    def __init__(self):
        super().__init__()
        for index, field in enumerate(self.__class__.fields):
            self._create_property(index=index,
                                  field=field)
        self.field_enum = Enum("fields", {field: index for index, field in enumerate(self.__class__.fields)})

    def __new__(cls):
        # Create a new array of zeros with the given shape and dtype
        shape = (len(cls.fields),)
        dtype = np.float32
        buffer = None
        offset = 0
        strides = None
        order = None
        obj = super(Observation, cls).__new__(cls, shape, dtype, buffer, offset, strides, order)
        obj.fill(0)
        return obj

    def _create_property(self,
                         index: int,
                         field: str):
        def getter(self):
            return self[index]

        def setter(self, value):
            self[index] = value

        setattr(self.__class__, field, property(getter, setter))

    def __setitem__(self, field: typing.Union[Enum, int], value):
        if isinstance(field, Enum):
            np.ndarray.__setitem__(self, field.value, value)
        else:
            np.ndarray.__setitem__(self, field, value)

    def __getitem__(self, field: typing.Union[Enum, int]) -> np.ndarray:
        if isinstance(field, Enum):
            return np.ndarray.__getitem__(self, field.value)
        else:
            return np.ndarray.__getitem__(self, field)


class Reward(object):
    def __init__(self,
                 reward_structure: dict):
        self.reward_structure = reward_structure

    def __call__(self, observation: Observation) -> float:
        reward = 0.0
        for field, multiplier in self.reward_structure.items():
            offset = 0
            if isinstance(multiplier, list):
                offset = multiplier[1]
                multiplier = multiplier[0]
            reward += offset + multiplier * observation[observation.field_enum[field].value]
        return reward


class Environment(Env):
    def __init__(self):
        self.event_handlers: typing.Dict[str, typing.List[typing.Callable]] = {"reset": [],
                                                                               "step": []}

    def __handle_event__(self, event_name: str, *args):
        for handler in self.event_handlers[event_name]:
            handler(*args)

    def add_event_handler(self, event_name: str, handler: typing.Callable):
        if event_name not in self.event_handlers:
            raise "Event handler not registered"
        self.event_handlers[event_name].append(handler)

    def reset(self,
              options: typing.Optional[dict] = None,
              seed=None):
        self.__handle_event__("reset", options, seed)

    def step(self, action: int):
        self.__handle_event__("step", action)


