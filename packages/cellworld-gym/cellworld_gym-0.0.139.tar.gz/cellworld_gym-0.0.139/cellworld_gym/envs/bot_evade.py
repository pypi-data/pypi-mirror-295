import enum
import typing
import cellworld_game as cwgame
import numpy as np
import math
from ..core import Observation, Environment
from gymnasium import Env
from gymnasium import spaces


class BotEvadeObservation(Observation):
    fields = ["prey_x",
              "prey_y",
              "prey_direction",
              "predator_x",
              "predator_y",
              "predator_direction",
              "prey_goal_distance",
              "predator_prey_distance",
              "puffed",
              "puff_cooled_down",
              "finished"]


class BotEvadeEnv(Environment):

    PointOfView = cwgame.BotEvade.PointOfView

    AgentRenderMode = cwgame.Agent.RenderMode

    class ObservationType(enum.Enum):
        DATA = 0
        PIXELS = 1

    class ActionType(enum.Enum):
        DISCRETE = 0
        CONTINUOUS = 1

    def __init__(self,
                 world_name: str,
                 use_lppos: bool,
                 use_predator: bool,
                 max_step: int = 300,
                 reward_function: typing.Callable[[BotEvadeObservation], float] = lambda x: 0,
                 time_step: float = .25,
                 render: bool = False,
                 real_time: bool = False,
                 point_of_view: PointOfView = PointOfView.TOP,
                 agent_render_mode: AgentRenderMode = AgentRenderMode.SPRITE,
                 observation_type: ObservationType = ObservationType.DATA,
                 action_type: ActionType = ActionType.DISCRETE,
                 prey_max_forward_speed: float = 0.5,
                 prey_max_turning_speed: float = 20.0,
                 predator_prey_forward_speed_ratio: float = .15,
                 predator_prey_turning_speed_ratio: float = .175):

        if observation_type == BotEvadeEnv.ObservationType.PIXELS and not render:
            raise ValueError("Cannot use PIXELS observation type without render")
        self.max_step = max_step
        self.reward_function = reward_function
        self.time_step = time_step
        self.loader = cwgame.CellWorldLoader(world_name=world_name)

        if use_lppos:
            self.action_list = self.loader.tlppo_action_list
        else:
            self.action_list = self.loader.full_action_list

        self.action_type = action_type
        if self.action_type == BotEvadeEnv.ActionType.DISCRETE:
            self.action_space = spaces.Discrete(len(self.action_list))
        else:
            self.action_space = spaces.Box(0.0, 1.0, (2,), dtype=np.float32)

        self.model = cwgame.BotEvade(world_name=world_name,
                                     real_time=real_time,
                                     render=render,
                                     use_predator=use_predator,
                                     point_of_view=point_of_view,
                                     agent_render_mode=agent_render_mode,
                                     prey_max_forward_speed=prey_max_forward_speed,
                                     prey_max_turning_speed=prey_max_turning_speed,
                                     predator_prey_forward_speed_ratio=predator_prey_forward_speed_ratio,
                                     predator_prey_turning_speed_ratio=predator_prey_turning_speed_ratio)
        self.observation_type = observation_type
        if self.observation_type == BotEvadeEnv.ObservationType.DATA:
            self.observation = BotEvadeObservation()
            self.observation_space = spaces.Box(-np.inf, np.inf, self.observation.shape, dtype=np.float32)
        else:
            self.observation = self.model.view.get_screen(normalized=True)
            self.observation_space = spaces.Box(0.0, 1.0, self.observation.shape, dtype=np.float32)
        self.prey_trajectory_length = 0
        self.predator_trajectory_length = 0
        self.episode_reward = 0
        self.step_count = 0
        Environment.__init__(self)

    def __update_observation__(self):
        if self.observation_type == BotEvadeEnv.ObservationType.DATA:
            self.observation.prey_x = self.model.prey.state.location[0]
            self.observation.prey_y = self.model.prey.state.location[1]
            self.observation.prey_direction = math.radians(self.model.prey.state.direction)

            if self.model.use_predator and self.model.prey_data.predator_visible:
                self.observation.predator_x = self.model.predator.state.location[0]
                self.observation.predator_y = self.model.predator.state.location[1]
                self.observation.predator_direction = math.radians(self.model.predator.state.direction)
            else:
                self.observation.predator_x = 0
                self.observation.predator_y = 0
                self.observation.predator_direction = 0

            self.observation.prey_goal_distance = self.model.prey_data.prey_goal_distance
            self.observation.predator_prey_distance = self.model.prey_data.predator_prey_distance
            self.observation.puffed = self.model.prey_data.puffed
            self.observation.puff_cooled_down = self.model.puff_cool_down
            self.observation.finished = not self.model.running
        else:
            self.observation = self.model.view.get_screen()
        return self.observation

    def set_action(self, action: typing.Union[int, typing.Tuple[float, float]]):
        if self.action_type == BotEvadeEnv.ActionType.DISCRETE:
            self.model.prey.set_destination(self.action_list[action])
        else:
            self.model.prey.set_destination(tuple(action))

    def __step__(self):
        self.step_count += 1
        truncated = (self.step_count >= self.max_step)
        obs = self.__update_observation__()
        reward = self.reward_function(obs)
        self.episode_reward += reward

        if self.model.prey_data.puffed:
            self.model.prey_data.puffed = False
        if not self.model.running or truncated:
            survived = 1 if not self.model.running and self.model.prey_data.puff_count == 0 else 0
            info = {"captures": self.model.prey_data.puff_count,
                    "reward": self.episode_reward,
                    "is_success": survived,
                    "survived": survived,
                    "agents": {}}
        else:
            info = {}
        return obs, reward, not self.model.running, truncated, info

    def replay_step(self, agents_state: typing.Dict[str, cwgame.AgentState]):
        self.model.set_agents_state(agents_state=agents_state,
                                    delta_t=self.time_step)
        return self.__step__()

    def step(self, action: typing.Union[int, typing.Tuple[float, float]]):
        self.set_action(action=action)
        model_t = self.model.time + self.time_step
        while self.model.running and self.model.time < model_t:
            self.model.step()
        Environment.step(self, action=action)
        return self.__step__()

    def __reset__(self):
        self.episode_reward = 0
        self.step_count = 0
        return self.__update_observation__(), {}

    def reset(self,
              options: typing.Optional[dict] = None,
              seed=None):
        self.model.reset()
        Environment.reset(self, options=options, seed=seed)
        return self.__reset__()

    def replay_reset(self, agents_state: typing.Dict[str, cwgame.AgentState]):
        self.model.reset()
        self.model.set_agents_state(agents_state=agents_state)
        return self.__reset__()

    def close(self):
        self.model.close()
        Env.close(self=self)

