from typing import Optional


class GameBoard:
    """Manages the 6x8 grid, tracks placed letters, and validates words."""

    def __init__(self, grid: Optional[list[list[str]]] = None):
        """Initialize the game board.
        
        Args:
            grid: Optional 6x8 grid of letters. If None, creates empty board.
        """
        if grid is None:
            self.grid = [['' for _ in range(8)] for _ in range(6)]
        else:
            if len(grid) != 6 or any(len(row) != 8 for row in grid):
                raise ValueError("Grid must be 6x8")
            self.grid = [row[:] for row in grid]
        self.width = 8
        self.height = 6

    def get_letter(self, row: int, col: int) -> str:
        """Get the letter at a specific cell."""
        return self.grid[row][col]

    def set_letter(self, row: int, col: int, letter: str) -> None:
        """Set the letter at a specific cell."""
        self.grid[row][col] = letter

    def is_cell_filled(self, row: int, col: int) -> bool:
        """Check if a cell has a letter."""
        return bool(self.grid[row][col])

    def is_full(self) -> bool:
        """Check if the entire board is filled."""
        return all(self.grid[row][col] for row in range(6) for col in range(8))

    def get_cell_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        """Get all valid neighboring cells (including diagonals)."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 6 and 0 <= new_col < 8:
                    neighbors.append((new_row, new_col))
        return neighbors

    def find_word(self, word: str) -> Optional[list[tuple[int, int]]]:
        """Find if a word can be formed by adjacent cells.
        
        Args:
            word: The word to find
            
        Returns:
            List of cell positions forming the word, or None if not found
        """
        if not word:
            return None
            
        word = word.upper()
        
        def dfs(r, c, idx, path, visited):
            if idx == len(word):
                return path
            if (r, c) in visited:
                return None
            if self.grid[r][c] != word[idx]:
                return None
                
            visited.add((r, c))
            path.append((r, c))
            
            for nr, nc in self.get_cell_neighbors(r, c):
                result = dfs(nr, nc, idx + 1, path, visited)
                if result:
                    return result
                    
            path.pop()
            visited.remove((r, c))
            return None
        
        for r in range(6):
            for c in range(8):
                if self.grid[r][c] == word[0]:
                    result = dfs(r, c, 0, [], set())
                    if result:
                        return result
        return None

    def can_place_word(self, positions: list[tuple[int, int]]) -> bool:
        """Check if a word can be placed at the given positions.
        
        Args:
            positions: List of (row, col) positions
            
        Returns:
            True if all positions are adjacent and valid
        """
        if not positions:
            return False
            
        if len(positions) == 1:
            return True
            
        for i in range(len(positions) - 1):
            r1, c1 = positions[i]
            r2, c2 = positions[i + 1]
            if abs(r1 - r2) > 1 or abs(c1 - c2) > 1:
                return False
            if (r1, c1) == (r2, c2):
                return False
                
        return True

    def is_spangram(self, positions: list[tuple[int, int]]) -> bool:
        """Check if a word touches two opposite sides of the board.
        
        Args:
            positions: List of (row, col) positions forming the word
            
        Returns:
            True if the word touches two opposite sides
        """
        if not positions:
            return False
            
        rows = {p[0] for p in positions}
        cols = {p[1] for p in positions}
        
        touches_top = 0 in rows
        touches_bottom = 5 in rows
        touches_left = 0 in cols
        touches_right = 7 in cols
        
        return (touches_top and touches_bottom) or (touches_left and touches_right)

    def place_word(self, word: str, positions: list[tuple[int, int]]) -> bool:
        """Place a word on the board at the given positions.
        
        Args:
            word: The word to place
            positions: List of (row, col) positions
            
        Returns:
            True if placement was successful
        """
        if len(word) != len(positions):
            return False
        if not self.can_place_word(positions):
            return False
            
        for i, (row, col) in enumerate(positions):
            self.grid[row][col] = word[i]
        return True


class GameState:
    """Tracks game state including found words, hints, and completion status."""

    def __init__(self, board: Optional[GameBoard] = None):
        """Initialize game state.
        
        Args:
            board: Optional GameBoard instance. If None, creates a new empty board.
        """
        self.board = board if board is not None else GameBoard()
        self.found_words: set[str] = set()
        self.themed_words: list[str] = []
        self.spangram: Optional[str] = None
        self.found_spangram = False
        self.non_theme_words: list[str] = []
        self.hints_unlocked = 0
        self.completed = False

    def add_found_word(self, word: str, is_theme: bool = False, is_spangram: bool = False) -> bool:
        """Add a found word to the game state.
        
        Args:
            word: The word found
            is_theme: Whether this is a themed word
            is_spangram: Whether this is the spangram
            
        Returns:
            True if the word was newly found, False if already found
        """
        word = word.upper()
        if word in self.found_words:
            return False
            
        self.found_words.add(word)
        
        if is_spangram:
            self.spangram = word
            self.found_spangram = True
        elif is_theme:
            self.themed_words.append(word)
        else:
            self.non_theme_words.append(word)
            
        return True

    def get_non_theme_count(self) -> int:
        """Get the count of non-theme words found."""
        return len(self.non_theme_words)

    def get_hints_to_unlock(self) -> int:
        """Get how many more hints need to be unlocked."""
        return (self.get_non_theme_count() // 3) - self.hints_unlocked

    def unlock_hint(self) -> None:
        """Unlock a hint."""
        self.hints_unlocked += 1

    def check_completion(self) -> bool:
        """Check if the game is completed (board filled and spangram found).
        
        Returns:
            True if game is completed
        """
        self.completed = self.board.is_full() and self.found_spangram
        return self.completed

    def get_themed_words_found(self) -> list[str]:
        """Get list of themed words found so far."""
        return [w for w in self.themed_words if w in self.found_words]
