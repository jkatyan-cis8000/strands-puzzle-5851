import random
import sys

from game_engine import GameBoard, GameState


class StrandsUI:
    """Command-line interface for the Strands puzzle game."""

    COLOR_BLUE = '\033[94m'
    COLOR_YELLOW = '\033[93m'
    COLOR_GRAY = '\033[90m'
    COLOR_RESET = '\033[0m'

    def __init__(self, game_state: GameState):
        """Initialize the UI.
        
        Args:
            game_state: The current game state
        """
        self.game_state = game_state
        self.selected_cells: list[tuple[int, int]] = []
        self.input_buffer: str = ''

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        print('\033[2J\033[H', end='')

    def get_cell_color(self, row: int, col: int) -> str:
        """Get the color for a cell based on which words it belongs to.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            ANSI color code
        """
        letter = self.game_state.board.get_letter(row, col)
        
        if letter == '':
            return self.COLOR_RESET
            
        for word in self.game_state.themed_words:
            if word in self.game_state.found_words:
                positions = self.game_state.board.find_word(word)
                if (row, col) in positions:
                    return self.COLOR_BLUE
                    
        if self.game_state.found_spangram and self.game_state.spangram:
            positions = self.game_state.board.find_word(self.game_state.spangram)
            if (row, col) in positions:
                return self.COLOR_YELLOW
                
        return self.COLOR_GRAY

    def display_grid(self) -> None:
        """Display the game grid with highlighting."""
        self.clear_screen()
        
        print("\n" + "=" * 40)
        print("           STRANDS PUZZLE")
        print("=" * 40 + "\n")
        
        print("Found words:", len(self.game_state.found_words))
        print(f"  Themed: {len(self.game_state.get_themed_words_found())} / {len(self.game_state.themed_words)}")
        print(f"  Non-theme: {len(self.game_state.non_theme_words)}")
        if self.game_state.found_spangram:
            print(f"  Spangram: {self.game_state.spangram}")
        print()
        
        print("  " + " ".join(f"{col}" for col in range(8)))
        print("  " + "-" * 16)
        
        for row in range(6):
            row_str = f"{row}|"
            for col in range(8):
                color = self.get_cell_color(row, col)
                letter = self.game_state.board.get_letter(row, col)
                if not letter:
                    letter = "_"
                row_str += f"{color}{letter}{self.COLOR_RESET}|"
            print(row_str)
        print()
        
        if self.selected_cells:
            print(f"Selected: {len(self.selected_cells)} cells")
            word = "".join(self.game_state.board.get_letter(r, c) for r, c in self.selected_cells)
            print(f"Current word: {word}")
        else:
            print("Selected: 0 cells")
        print()

    def display_themed_words(self) -> None:
        """Display the list of themed words."""
        print("\nThemed words to find:")
        for i, word in enumerate(self.game_state.themed_words, 1):
            if word in self.game_state.found_words:
                color = self.COLOR_BLUE
                status = "[FOUND]"
            else:
                color = self.COLOR_RESET
                status = "[      ]"
            print(f"{color}{status} {word}{self.COLOR_RESET}")

    def display_non_theme_words(self) -> None:
        """Display found non-theme words."""
        if self.game_state.non_theme_words:
            print("\nNon-theme words found:")
            for word in self.game_state.non_theme_words:
                print(f"  - {word}")

    def show_hint(self) -> tuple[int, int]:
        """Show a hint cell containing a letter from an unfound themed word.
        
        Returns:
            The (row, col) of the hint cell
        """
        unfound_themes = [w for w in self.game_state.themed_words if w not in self.game_state.found_words]
        hint_cells = []
        
        for word in unfound_themes:
            positions = self.game_state.board.find_word(word)
            if positions:
                hint_cells.extend(positions)
        
        if not hint_cells:
            for r in range(6):
                for c in range(8):
                    if not self.game_state.board.is_cell_filled(r, c):
                        hint_cells.append((r, c))
        
        if not hint_cells:
            return (-1, -1)
            
        hint = random.choice(hint_cells)
        print(f"\nHint: Try cell ({hint[0]}, {hint[1]})")
        return hint

    def handle_cell_selection(self, row: int, col: int) -> None:
        """Handle selecting a cell.
        
        Args:
            row: Row index
            col: Column index
        """
        if self.selected_cells:
            last_row, last_col = self.selected_cells[-1]
            neighbors = self.game_state.board.get_cell_neighbors(last_row, last_col)
            if (row, col) not in neighbors and (row, col) not in self.selected_cells:
                print("\nInvalid selection: must be adjacent to last cell!")
                return
                
        if (row, col) in self.selected_cells:
            idx = self.selected_cells.index((row, col))
            self.selected_cells = self.selected_cells[:idx + 1]
        else:
            self.selected_cells.append((row, col))

    def handle_word_submit(self) -> None:
        """Submit the currently selected word."""
        if not self.selected_cells:
            print("\nNo cells selected!")
            return
            
        word = "".join(self.game_state.board.get_letter(r, c) for r, c in self.selected_cells)
        
        if len(word) < 4:
            print(f"\nWord '{word}' is too short (min 4 letters)")
            return
            
        if word in self.game_state.found_words:
            print(f"\nAlready found: {word}")
            return
            
        positions = self.game_state.board.find_word(word)
        if positions is None:
            print(f"\nCannot find word '{word}' on board!")
            return
            
        is_spangram = self.game_state.board.is_spangram(positions)
        is_theme = word in self.game_state.themed_words
        
        self.game_state.add_found_word(word, is_theme=is_theme, is_spangram=is_spangram)
        
        print(f"\nFound: {word}!")
        if is_spangram:
            print("  *** SPANGRAM! ***")
        elif is_theme:
            print("  (Themed word)")
        else:
            print("  (Non-theme word)")
            
        non_theme_count = self.game_state.get_non_theme_count()
        if non_theme_count > 0 and non_theme_count % 3 == 0:
            print(f"\n--- Hint unlocked after {non_theme_count} non-theme words! ---")
            self.game_state.unlock_hint()
            self.show_hint()
        
        self.selected_cells = []
        self.input_buffer = ''

    def handle_clear_selection(self) -> None:
        """Clear the current selection."""
        self.selected_cells = []
        self.input_buffer = ''
        print("\nSelection cleared")

    def handle_quit(self) -> None:
        """Quit the game."""
        print("\nThanks for playing!")
        sys.exit(0)

    def show_instructions(self) -> None:
        """Show game instructions."""
        print("\n=== CONTROLS ===")
        print("Enter cell coordinates (e.g., '0,1' for row 0, col 1)")
        print("Commands:")
        print("  submit  - Submit current selection")
        print("  clear   - Clear current selection")
        print("  hint    - Get a hint")
        print("  help    - Show this help")
        print("  quit    - Quit the game")
        print("================\n")

    def process_input(self, input_str: str) -> bool:
        """Process user input.
        
        Args:
            input_str: The input string
            
        Returns:
            True if game should continue, False if quit
        """
        input_str = input_str.strip().lower()
        
        if not input_str:
            return True
            
        if input_str in ('quit', 'q', 'exit', 'x'):
            self.handle_quit()
            return False
            
        if input_str in ('help', 'h', '?'):
            self.show_instructions()
            return True
            
        if input_str in ('submit', 's'):
            self.handle_word_submit()
            return True
            
        if input_str in ('clear', 'c'):
            self.handle_clear_selection()
            return True
            
        if input_str in ('hint', 'h'):
            self.show_hint()
            return True
            
        try:
            if ',' in input_str:
                row, col = input_str.split(',')
                row = int(row.strip())
                col = int(col.strip())
                if 0 <= row < 6 and 0 <= col < 8:
                    self.handle_cell_selection(row, col)
                else:
                    print("\nInvalid coordinates! Use 0-5 for row, 0-7 for col")
            else:
                self.input_buffer += input_str
                print(f"Buffer: {self.input_buffer}")
        except (ValueError, IndexError):
            print("\nInvalid input! Enter 'row,col' or a command")
            
        return True

    def game_loop(self) -> None:
        """Run the main game loop."""
        self.show_instructions()
        
        while not self.game_state.check_completion():
            self.display_grid()
            self.display_themed_words()
            self.display_non_theme_words()
            
            user_input = input("Enter cell (row,col) or command: ")
            if not self.process_input(user_input):
                break
                
        self.display_grid()
        print("\n" + "=" * 40)
        print("           PUZZLE COMPLETE!")
        print("=" * 40)
        print(f"\nYou found {len(self.game_state.found_words)} words!")
        print(f"  Themed: {len(self.game_state.get_themed_words_found())}")
        print(f"  Non-theme: {len(self.game_state.non_theme_words)}")
        if self.game_state.found_spangram:
            print(f"  Spangram: {self.game_state.spangram}")
        print(f"\nHints used: {self.game_state.hints_unlocked}")


def create_sample_game() -> GameState:
    """Create a sample game with a predefined board.
    
    Returns:
        A GameState with a sample puzzle
    """
    grid = [
        ['S', 'A', 'T', 'U', 'R', 'N', ' ', ' '],
        [' ', 'P', 'L', 'A', 'N', 'E', 'T', ' '],
        [' ', ' ', 'M', 'O', 'O', 'N', ' ', ' '],
        [' ', ' ', ' ', 'S', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    
    board = GameBoard(grid)
    state = GameState(board)
    state.themed_words = ['PLANET', 'MOON', 'STAR', 'SUN']
    state.spangram = 'SATURN'
    
    return state


def main() -> None:
    """Main entry point."""
    print("Welcome to Strands!")
    print("\n1. Start new game")
    print("2. Load sample puzzle")
    
    choice = input("\nSelect option (1-2): ").strip()
    
    if choice == '2':
        game_state = create_sample_game()
    else:
        board = GameBoard()
        game_state = GameState(board)
        
    ui = StrandsUI(game_state)
    ui.game_loop()


if __name__ == '__main__':
    main()
