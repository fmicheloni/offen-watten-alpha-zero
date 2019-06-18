from EnvironmentSelector import EnvironmentSelector
import operator


class WattenEngine():
    def __init__(self):
        print("Init Watten Engine")

        self.init_nnet()

    def init_nnet(self):
        env_selector = EnvironmentSelector()
        agent_nnet = env_selector.get_agent("watten_agent_nnet")

        self.nnet = agent_nnet

    def get_valid_moves(self, game):
        return game.get_valid_moves_no_zeros()

    def make_move_against_ai(self, game, move):
        current_player = game.get_cur_player()
        game_result, next_player = game.make_move(move)

        states_after_moves = []

        if next_player == current_player:
            states_after_moves.append({'state': game.get_player_visible_state(current_player), 'move': move})
            return states_after_moves

        while next_player != current_player:
            prediction = self.nnet.predict(game, next_player)[0]
            valid_moves = game.get_valid_moves() * prediction

            best_move_perc = max(enumerate(valid_moves), key=operator.itemgetter(1))
            best_move = best_move_perc[0]

            print("Picked action [%d] with perc [%.4f]" % best_move_perc)

            game_result, next_player = game.make_move(best_move)

            states_after_moves.append({
                'state': game.get_player_visible_state(current_player),
                'move': best_move,
                'game_result': game_result
            })

            if game_result != 0.0:
                break

        return states_after_moves
