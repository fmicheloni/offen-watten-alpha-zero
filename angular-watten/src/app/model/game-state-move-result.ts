import {GameState} from "./game-state";

export class GameStateMoveResult {
  state: GameState;
  move: number;
  game_result: string;
  player: number;
}
