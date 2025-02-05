import sys
from collections import deque


MOVES = ["U", "U'", "D", "D'", "F", "F'", "B", "B'", "L", "L'", "R", "R'"]


class Cube:
    def __init__(self, state=None):
        """
        Internal representation uses keys:
           'U': Up (Top)
           'D': Down (Bottom)
           'F': Front
           'B': Back
           'L': Left
           'R': Right
        Each face is stored as a list of 9 stickers (flattened 3x3).
        If no state is provided, a solved cube is created.
        """
        if state is not None:
            self.state = state
        else:
            self.state = {  #goal state / default solved state
                'U': ['W'] * 9,  # Up (Top)
                'D': ['Y'] * 9,  # Down (Bottom)
                'F': ['G'] * 9,  # Front
                'B': ['B'] * 9,  # Back
                'L': ['O'] * 9,  # Left
                'R': ['R'] * 9   # Right
            }

    def _rotate_face_clockwise(self, face):
        """
        Rotate a face 90° clockwise.
           [0, 1, 2,
            3, 4, 5,
            6, 7, 8]
        After a clockwise rotation the new order is:
           [6, 3, 0, 7, 4, 1, 8, 5, 2]
        """
        old = self.state[face].copy()
        self.state[face] = [old[6], old[3], old[0],
                            old[7], old[4], old[1],
                            old[8], old[5], old[2]]

    def move_U(self):
        """
        Rotate the Up (top) face clockwise and cycle the adjacent top rows.
        When looking directly at the U face, the cycle should be:
          
        """
        self._rotate_face_clockwise('U')
        temp = self.state['F'][:3].copy()
        self.state['F'][:3] = self.state['R'][:3]
        self.state['R'][:3] = self.state['B'][:3]
        self.state['B'][:3] = self.state['L'][:3]
        self.state['L'][:3] = temp

    def move_D(self):
        """
        Rotate the Down (bottom) face clockwise and cycle the adjacent bottom rows.
        When looking directly at the D face (from below), the cycle should be:
          F_bottom ← L_bottom, L_bottom ← B_bottom, B_bottom ← R_bottom, R_bottom ← F_bottom.
        """
        self._rotate_face_clockwise('D')
        temp = self.state['F'][6:9].copy()
        self.state['F'][6:9] = self.state['L'][6:9]
        self.state['L'][6:9] = self.state['B'][6:9]
        self.state['B'][6:9] = self.state['R'][6:9]
        self.state['R'][6:9] = temp

    def move_F(self):
        """Rotate the Front face clockwise and cycle the adjacent edges."""
        self._rotate_face_clockwise('F')
        temp = self.state['U'][6:9].copy()
        self.state['U'][6] = self.state['L'][8]
        self.state['U'][7] = self.state['L'][5]
        self.state['U'][8] = self.state['L'][2]
        self.state['L'][2] = self.state['D'][0]
        self.state['L'][5] = self.state['D'][1]
        self.state['L'][8] = self.state['D'][2]
        self.state['D'][0] = self.state['R'][6]
        self.state['D'][1] = self.state['R'][3]
        self.state['D'][2] = self.state['R'][0]
        self.state['R'][0] = temp[2]
        self.state['R'][3] = temp[1]
        self.state['R'][6] = temp[0]

    def move_B(self):
        """Rotate the Back face clockwise and cycle the adjacent edges."""
        self._rotate_face_clockwise('B')
        temp = self.state['U'][:3].copy()
        self.state['U'][0] = self.state['R'][2]
        self.state['U'][1] = self.state['R'][5]
        self.state['U'][2] = self.state['R'][8]
        self.state['R'][2] = self.state['D'][8]
        self.state['R'][5] = self.state['D'][7]
        self.state['R'][8] = self.state['D'][6]
        self.state['D'][6] = self.state['L'][0]
        self.state['D'][7] = self.state['L'][3]
        self.state['D'][8] = self.state['L'][6]
        self.state['L'][0] = temp[2]
        self.state['L'][3] = temp[1]
        self.state['L'][6] = temp[0]

    def move_L(self):
        """Rotate the Left face clockwise and cycle the adjacent edges."""
        self._rotate_face_clockwise('L')
        temp = [self.state['U'][0], self.state['U'][3], self.state['U'][6]]
        self.state['U'][0] = self.state['B'][8]
        self.state['U'][3] = self.state['B'][5]
        self.state['U'][6] = self.state['B'][2]
        self.state['B'][8] = self.state['D'][0]
        self.state['B'][5] = self.state['D'][3]
        self.state['B'][2] = self.state['D'][6]
        self.state['D'][0] = self.state['F'][0]
        self.state['D'][3] = self.state['F'][3]
        self.state['D'][6] = self.state['F'][6]
        self.state['F'][0] = temp[0]
        self.state['F'][3] = temp[1]
        self.state['F'][6] = temp[2]

    def move_R(self):
        """Rotate the Right face clockwise and cycle the adjacent edges."""
        self._rotate_face_clockwise('R')
        temp = [self.state['U'][2], self.state['U'][5], self.state['U'][8]]
        self.state['U'][2] = self.state['F'][2]
        self.state['U'][5] = self.state['F'][5]
        self.state['U'][8] = self.state['F'][8]
        self.state['F'][2] = self.state['D'][2]
        self.state['F'][5] = self.state['D'][5]
        self.state['F'][8] = self.state['D'][8]
        self.state['D'][2] = self.state['B'][6]
        self.state['D'][5] = self.state['B'][3]
        self.state['D'][8] = self.state['B'][0]
        self.state['B'][6] = temp[0]
        self.state['B'][3] = temp[1]
        self.state['B'][0] = temp[2]

    def apply_move(self, move):
        """
        Apply a move given as a string.
        For example:
           "R"   → rotate the right face clockwise,
           "U'"  → rotate the top face anti-clockwise (3 clockwise moves),
           "F2"  → perform a 180° turn of the front face.
        """
        count = 1
        if move.endswith("2"):
            count = 2
            move = move[0]
        elif move.endswith("'"):
            count = 3  # Three clockwise moves equal one counterclockwise move.
            move = move[0]
        for _ in range(count):
            getattr(self, "move_" + move)()

    def get_state_string(self):
        """
           'U' -> 'T' (Top)
           'D' -> 'B' (Bottom)
           'F' -> 'F'
           'B' -> 'A' (bAck)
           'L' -> 'L'
           'R' -> 'R'
        Each face is printed as: FaceID:Value
        """
        mapping = {'U': 'T', 'D': 'B', 'F': 'F', 'B': 'A', 'L': 'L', 'R': 'R'}
        parts = []
        for internal_face, output_face in mapping.items():
            parts.append(f"{output_face}:{''.join(self.state[internal_face])}")
        return " ".join(parts)

    def __str__(self):
        return self.get_state_string()


def parse_initial_state(state_str):
    """
    Given a state string (e.g.,
    "T:WWWWWWWWW F:GGGGGGGGG R:RRRRRRRRR A:BBBBBBBBB L:OOOOOOOOO B:YYYYYYYYY"),
    convert it into the internal state dictionary.
    """
    file_to_internal = {'T': 'U', 'B': 'D', 'F': 'F', 'A': 'B', 'L': 'L', 'R': 'R'}
    state = {}
    tokens = state_str.strip().split()
    for token in tokens:
        try:
            face, stickers = token.split(":")
        except ValueError:
            raise ValueError(f"Token '{token}' is not in the expected format 'Face:Stickers'.")
        if face not in file_to_internal:
            raise ValueError(f"Unknown face ID in token: {face}")
        internal_face = file_to_internal[face]
        if len(stickers) != 9:
            raise ValueError(f"Face {face} must have exactly 9 stickers.")
        state[internal_face] = list(stickers)
    for f in ['U', 'D', 'F', 'B', 'L', 'R']:
        if f not in state:
            raise ValueError(f"Missing face in initial state: {f}")
    return state


def scramble_cube(input_file, output_file):
    """
    Reads an input file with:
      - Line 1: initial cube state (e.g.,
         T:WWWWWWWWW F:GGGGGGGGG R:RRRRRRRRR A:BBBBBBBBB L:OOOOOOOOO B:YYYYYYYYY)
      - Line 2 onwards: one move per line:
         <faceID> <moveID>
         <faceID> <moveID>
    Applies the moves sequentially and writes to the output file:
      Line 1: the scrambled (new) state
      Line 2: the original initial state
    """
    with open(input_file, "r") as f:
        lines = f.readlines()

    if not lines:
        raise ValueError("Input file is empty.")

    initial_state_str = lines[0].strip()
    initial_state = parse_initial_state(initial_state_str)

    # Create a Cube from the initial state.
    cube = Cube(state=initial_state.copy())

    # Mapping from file face IDs to internal ones.
    file_to_internal = {'T': 'U', 'B': 'D', 'F': 'F', 'A': 'B', 'L': 'L', 'R': 'R'}

    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) != 2:
            continue  # skip malformed lines
        face, move_dir = parts
        if face not in file_to_internal:
            print(f"Warning: Unknown face '{face}' skipped.")
            continue
        internal_face = file_to_internal[face]
        # Build the move string: Clockwise = e.g. "U"; Anti-clockwise = "U'"
        if move_dir == 'C':
            move_str = internal_face
        elif move_dir == 'A':
            move_str = internal_face + "'"
        else:
            print(f"Warning: Unknown move direction '{move_dir}' skipped.")
            continue
        cube.apply_move(move_str)

    with open(output_file, "w") as f:
        f.write(cube.get_state_string() + "\n")
        initial_cube = Cube(state=initial_state)
        f.write(initial_cube.get_state_string() + "\n")
        
        
def cube_to_tuple(cube):
    """
    Convert a cube’s state into a hashable tuple.
    The order we use here is: U, F, R, B, L, D.
    """
    return (tuple(cube.state['U']),
            tuple(cube.state['F']),
            tuple(cube.state['R']),
            tuple(cube.state['B']),
            tuple(cube.state['L']),
            tuple(cube.state['D']))

def bfs_solve(initial_cube, goal_cube):
    """
    Uses Breadth-First Search (BFS) to find the minimum sequence of moves
    that transforms the initial cube state into the goal cube state.
    
    Parameters:
      initial_cube: an instance of Cube representing the scrambled state.
      goal_cube: an instance of Cube representing the solved (goal) state.
    
    Returns:
      A list of moves (e.g. ["R", "U'", "F", ...]) that solves the puzzle,
      or None if no solution is found.
    """
    goal_tuple = cube_to_tuple(goal_cube)
    queue = deque()
    visited = set()

    # Each element in the queue is a tuple: (cube, move_sequence)
    queue.append((initial_cube, []))
    visited.add(cube_to_tuple(initial_cube))

    while queue:
        current_cube, path = queue.popleft()
        if cube_to_tuple(current_cube) == goal_tuple:
            return path  # Found a solution!
        
        # Try all possible moves.
        for move in MOVES:
            # Create a deep copy of the current cube by copying its state.
            new_cube = Cube(state={k: v.copy() for k, v in current_cube.state.items()})
            new_cube.apply_move(move)
            state_id = cube_to_tuple(new_cube)
            if state_id not in visited:
                visited.add(state_id)
                queue.append((new_cube, path + [move]))
    return None  # In case no solution is found.


def bidirectional_bfs_solve(start_cube, goal_cube):
    """
    Solve the 3x3x3 Rubik's Cube using bidirectional BFS.
    Returns the shortest sequence of moves to solve the cube.
    """
    if start_cube.get_state_string() == goal_cube.get_state_string():
        return []  # Already solved

    # Bidirectional Search Setup
    frontier_start = deque([(start_cube, [])])
    frontier_goal = deque([(goal_cube, [])])

    visited_start = {cube_to_tuple(start_cube): []}
    visited_goal = {cube_to_tuple(goal_cube): []}

    while frontier_start and frontier_goal:
        # Expand forward from the start state
        if frontier_start:
            cube, path = frontier_start.popleft()
            for move in MOVES:
                new_cube = Cube(state={k: v.copy() for k, v in cube.state.items()})
                new_cube.apply_move(move)
                state_tuple = cube_to_tuple(new_cube)

                if state_tuple in visited_goal:
                    return path + [move] + visited_goal[state_tuple][::-1]  # Solution found!

                if state_tuple not in visited_start:
                    visited_start[state_tuple] = path + [move]
                    frontier_start.append((new_cube, path + [move]))

        # Expand backward from the goal state
        if frontier_goal:
            cube, path = frontier_goal.popleft()
            for move in MOVES:
                new_cube = Cube(state={k: v.copy() for k, v in cube.state.items()})
                new_cube.apply_move(move)
                state_tuple = cube_to_tuple(new_cube)

                if state_tuple in visited_start:
                    return visited_start[state_tuple] + [move] + path[::-1]  # Solution found!

                if state_tuple not in visited_goal:
                    visited_goal[state_tuple] = path + [move]
                    frontier_goal.append((new_cube, path + [move]))

    return None  # No solution found



if __name__ == "__main__":
    # Load the problem from "problem.txt"
    with open("problem.txt", "r") as f:
        lines = f.readlines()

    if len(lines) < 2:
        raise ValueError("The problem file must have at least two lines (scrambled state and goal state).")

    initial_state_str = lines[0].strip()
    goal_state_str = lines[1].strip()

    # Convert to internal state dictionaries
    initial_state = parse_initial_state(initial_state_str)
    goal_state = parse_initial_state(goal_state_str)

    # Create Cube instances
    initial_cube = Cube(state=initial_state)
    goal_cube = Cube(state=goal_state)

    # Solve with Bi-BFS
    solution = bidirectional_bfs_solve(initial_cube, goal_cube)

    if solution:
        print("\nSolution found in {} moves:".format(len(solution)))
        print(solution)
    else:
        print("\nNo solution found.")
