from __future__ import print_function
import sys
import copy

sys.path.append('..')
sys.path.append('watten')

import games.watten.watten as watten
import numpy as np

from core.interfaces.Game import Game

from loggers import stdout_logger

class WattenGame(Game):
    def __init__(self):
        self.trueboard = watten.WorldWatten()

    def reset(self):
        self.trueboard = watten.WorldWatten()

    def get_cur_player(self):
        player = self.trueboard.get_player()
        return player

    def get_players_num(self):
        return 2

    def get_action_size(self):
        return 49

    def get_observation_size(self):
        return 212, 1

    def make_move(self, action):
        # stdout_logger.info("make move")
        game_status, next_player = self.trueboard.act(action)
        if game_status == "end" and self.trueboard.is_game_end():
            if self.trueboard.is_won(next_player):
                return 1.0, next_player
            else:
                return -1.0, next_player
        else:
            return 0.0, next_player

    def get_valid_moves(self, player=None):
        # self.trueboard.actions.append("Valid moves are %s" % self.trueboard.get_valid_moves() )
        return self.trueboard.get_valid_moves_zeros()

    def is_ended(self):
        return self.trueboard.is_game_end()

    def is_draw(self):
        # in Watten a game can never end with a draw
        return False

    def get_score(self, player):
        player_curr = 1 if player == 0 else -1
        # player_enemy = player_curr * -1

        if self.trueboard.is_game_end():
            if self.trueboard.is_won(player_curr):
                return 1.0
            else:
                return -1.0
        return 0.0

    def get_observation(self, player):
        player_in = 1 if player == 0 else -1
        observation = self.trueboard.observe(player_in)
        return observation

    def get_observation_str(self, observation):
        if isinstance(observation, np.ndarray):
            return observation.tostring()
        else:
            return str(observation)

    def get_display_str(self):
        self.trueboard.display()
        return ""

    def clone(self):
        cloned_game = WattenGame()
        cloned_game.trueboard = self.trueboard.deepcopy()
        return cloned_game

    def reset_unknown_states(self, player):
        pass
