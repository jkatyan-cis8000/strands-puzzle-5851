from game_engine import GameState, GameBoard
from themes import generate_puzzle
from ui import StrandsUI


def main():
    puzzle_data = generate_puzzle()
    
    # Create a board and populate it with puzzle data
    board = GameBoard()
    state = GameState(board)
    state.themed_words = puzzle_data["themed_words"]
    state.spangram = puzzle_data["spangram"]
    
    ui = StrandsUI(state)
    ui.game_loop()


if __name__ == "__main__":
    main()
