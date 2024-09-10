import typing
import cellworld_game as cwgame
import numpy as np
import math

from ..core import Observation, Environment
from cellworld_game import AgentState
from gymnasium import Env
from gymnasium import spaces


class OasisObservation(Observation):
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
              "finished",
              "goal_attained",
              "goal_time_left"]


class OasisEnv(Environment):
    def __init__(self,
                 world_name: str,
                 goal_locations: typing.List[typing.Tuple[float, float]],
                 use_lppos: bool,
                 use_predator: bool,
                 goal_sequence_generator: typing.Callable[[None], typing.List[int]] = None,
                 max_step: int = 300,
                 reward_function: typing.Callable[[OasisObservation], float] = lambda x: 0,
                 time_step: float = .25,
                 render: bool = False,
                 real_time: bool = False):

        self.max_step = max_step
        self.reward_function = reward_function
        self.time_step = time_step
        self.loader = cwgame.CellWorldLoader(world_name=world_name)
        self.observation = OasisObservation()
        self.observation_space = spaces.Box(-np.inf, np.inf, (len(self.observation),), dtype=np.float32)
        if use_lppos:
            self.action_list = self.loader.tlppo_action_list
        else:
            self.action_list = self.loader.full_action_list

        self.action_space = spaces.Discrete(len(self.action_list))

        self.model = cwgame.Oasis(world_name=world_name,
                                  real_time=real_time,
                                  render=render,
                                  use_predator=use_predator,
                                  goal_locations=goal_locations,
                                  goal_sequence_generator=goal_sequence_generator)
        self.prey_trajectory_length = 0
        self.predator_trajectory_length = 0
        self.episode_reward = 0
        self.step_count = 0
        Environment.__init__(self)

    def __update_observation__(self):
        self.observation.prey_x = self.model.prey.state.location[0]
        self.observation.prey_y = self.model.prey.state.location[1]
        self.observation.prey_direction = math.radians(self.model.prey.state.direction)

        if self.model.use_predator and self.model.visibility.line_of_sight(self.model.prey.state.location, self.model.predator.state.location):
            self.observation.predator_x = self.model.predator.state.location[0]
            self.observation.predator_y = self.model.predator.state.location[1]
            self.observation.predator_direction = math.radians(self.model.predator.state.direction)
        else:
            self.observation.predator_x = 0
            self.observation.predator_y = 0
            self.observation.predator_direction = 0

        self.observation.prey_goal_distance = self.model.prey_goal_distance
        self.observation.predator_prey_distance = self.model.predator_prey_distance
        self.observation.puffed = self.model.puffed
        self.observation.puff_cooled_down = self.model.puff_cool_down
        self.observation.goal_attained = self.model.goal_achieved
        if self.observation.goal_attained:
            self.observation.goal_time_left = self.model.goal_time - self.model.goal_achieved_time
        else:
            self.observation.goal_time_left = 0
        self.observation.finished = not self.model.running
        return self.observation

    def set_action(self, action: int):
        self.model.prey.set_destination(self.action_list[action])

    def __step__(self):
        self.step_count += 1
        truncated = (self.step_count >= self.max_step)
        obs = self.__update_observation__()
        reward = self.reward_function(obs)
        self.episode_reward += reward

        if self.model.puffed:
            self.model.puffed = False
        if not self.model.running or truncated:
            survived = 1 if not self.model.running and self.model.puff_count == 0 else 0
            info = {"captures": self.model.puff_count,
                    "reward": self.episode_reward,
                    "is_success": survived,
                    "survived": survived,
                    "agents": {}}
        else:
            info = {}
        return obs, reward, not self.model.running, truncated, info

    def replay_step(self, agents_state: typing.Dict[str, AgentState]):
        self.model.set_agents_state(agents_state=agents_state,
                                    delta_t=self.time_step)
        return self.__step__()

    def step(self, action: int):
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
              options={},
              seed=None):
        self.model.reset()
        Environment.reset(self, options=options, seed=seed)
        return self.__reset__()

    def replay_reset(self, agents_state: typing.Dict[str, AgentState]):
        self.model.reset()
        self.model.set_agents_state(agents_state=agents_state)
        return self.__reset__()

    def close(self):
        self.model.close()
        Env.close(self=self)

