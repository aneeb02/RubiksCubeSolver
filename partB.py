from collections import deque
import copy

# Cube class, contains all relevant functions
class Cube:
    def __init__(self, state=None):
        if state is not None:
            self.state = state
        else:
            self.state = {
                'T': ['W'] * 9,  # Top = white
                'B': ['Y'] * 9,  # Bottom = yellow
                'F': ['G'] * 9,  # Front = green 
                'A': ['B'] * 9,  # Back = blue
                'L': ['O'] * 9,  # Left = orange
                'R': ['R'] * 9   # Right = red
            }

    def rotate_faceC(self, face):
        prev = self.state[face].copy()
        self.state[face] = [prev[6], prev[3], prev[0],
                            prev[7], prev[4], prev[1],
                            prev[8], prev[5], prev[2]]

    # --- Move functions ---
    # Left clockwise
    def Left_Clockwise(self):
        self.rotate_faceC('L')
        temp = [self.state['T'][0], self.state['T'][3], self.state['T'][6]]  # Save Top's left column.
        # Top[0,3,6] = Back[8,5,2]
        self.state['T'][0] = self.state['A'][8]
        self.state['T'][3] = self.state['A'][5]
        self.state['T'][6] = self.state['A'][2]
        # Back[2,5,8] = Bottom[6,3,0]
        self.state['A'][8] = self.state['B'][0]
        self.state['A'][5] = self.state['B'][3]
        self.state['A'][2] = self.state['B'][6]
        # Bottom[0,3,6] = Front[0,3,6]
        self.state['B'][0] = self.state['F'][0]
        self.state['B'][3] = self.state['F'][3]
        self.state['B'][6] = self.state['F'][6]
        # Front[0,3,6] = Top[0,3,6]
        self.state['F'][0] = temp[0]
        self.state['F'][3] = temp[1]
        self.state['F'][6] = temp[2]
    
    # Bottom clockwise
    def Bottom_Clockwise(self):
        """
        F_bottom ← L_bottom, L_bottom ← A_bottom, A_bottom ← R_bottom, R_bottom ← F_bottom.
        """  
        self.rotate_faceC('B')
        temp = self.state['F'][6:9].copy()
        # Front[6,7,8] = Left[6,7,8]
        self.state['F'][6:9] = self.state['L'][6:9]
        # Left[6,7,8] = Back[6,7,8]
        self.state['L'][6:9] = self.state['A'][6:9]
        # Back[6,7,8] = Right[6,7,8]
        self.state['A'][6:9] = self.state['R'][6:9]
        # Right[6,7,8] = Front[6,7,8]
        self.state['R'][6:9] = temp

    # Front clockwise
    def Front_Clockwise(self):
        self.rotate_faceC('F')
        temp = self.state['T'][6:9].copy()  
        # Top[6,7,8] = Left[8,5,2]
        self.state['T'][6] = self.state['L'][8]
        self.state['T'][7] = self.state['L'][5]
        self.state['T'][8] = self.state['L'][2]
        # Left[8,5,2] = Bottom[2,1,0]
        self.state['L'][2] = self.state['B'][0]
        self.state['L'][5] = self.state['B'][1]
        self.state['L'][8] = self.state['B'][2]
        # Bottom [0,1,2] = Right[6,3,0]
        self.state['B'][0] = self.state['R'][6]
        self.state['B'][1] = self.state['R'][3]
        self.state['B'][2] = self.state['R'][0]
        # Right[0,3,6] = Top[6,7,8]
        self.state['R'][0] = temp[2]
        self.state['R'][3] = temp[1]
        self.state['R'][6] = temp[0]
    
    # Back clockwise
    def Back_Clockwise(self):
        self.rotate_faceC('A')
        temp = self.state['T'][:3].copy()  
        # Top[0,1,2] = Right[2,5,8]
        self.state['T'][0] = self.state['R'][2]
        self.state['T'][1] = self.state['R'][5]
        self.state['T'][2] = self.state['R'][8]
        # Right[8,5,2] = Bottom[6,7,8]
        self.state['R'][2] = self.state['B'][8]
        self.state['R'][5] = self.state['B'][7]
        self.state['R'][8] = self.state['B'][6]
        # Bottom[6,7,8] = Left[0,3,6]
        self.state['B'][6] = self.state['L'][0]
        self.state['B'][7] = self.state['L'][3]
        self.state['B'][8] = self.state['L'][6]
        # Left[0,3,6] = Top[2,1,0]
        self.state['L'][0] = temp[2]
        self.state['L'][3] = temp[1]
        self.state['L'][6] = temp[0]
    
    # Top clockwise
    def Top_Clockwise(self):
        self.rotate_faceC('T')
        temp = self.state['F'][:3].copy()
        # Front[0,1,2] = Right[0,1,2]
        self.state['F'][:3] = self.state['R'][:3]
        # Right[0,1,2] = Back[0,1,2]
        self.state['R'][:3] = self.state['A'][:3]
        # Back[0,1,2] = Left[0,1,2]
        self.state['A'][:3] = self.state['L'][:3]
        # Left[0,1,2] = Front[0,1,2]
        self.state['L'][:3] = temp

    # Right clockwise
    def Right_Clockwise(self):        
        self.rotate_faceC('R')
        temp = [self.state['T'][2], self.state['T'][5], self.state['T'][8]]  
        # Top[2,5,8] = Front[2,5,8]
        self.state['T'][2] = self.state['F'][2]
        self.state['T'][5] = self.state['F'][5]
        self.state['T'][8] = self.state['F'][8]
        # Front[2,5,8] = Bottom[2,5,8]
        self.state['F'][2] = self.state['B'][2]
        self.state['F'][5] = self.state['B'][5]
        self.state['F'][8] = self.state['B'][8]
        # Bottom[2,5,8] = Back[6,3,0]
        self.state['B'][2] = self.state['A'][6]
        self.state['B'][5] = self.state['A'][3]
        self.state['B'][8] = self.state['A'][0]
        # Back[6,3,0] = Top[2,5,8]
        self.state['A'][6] = temp[0]
        self.state['A'][3] = temp[1]
        self.state['A'][0] = temp[2]
    
    # Apply a move on cube based on moveId.
    def move_cube(self, faceId, moveId):
        # One clockwise move, or three clockwise moves (which is equivalent to one anticlockwise move)
        moveCount = 1 if moveId == "C" else 3 if moveId == "A" else None
        if moveCount is None:
            raise ValueError("Invalid move direction. Use 'C' or 'A'.")
        
        faceId_to_function = {
            "T": "Top_Clockwise",
            "B": "Bottom_Clockwise",  
            "F": "Front_Clockwise",
            "A": "Back_Clockwise",    
            "L": "Left_Clockwise",
            "R": "Right_Clockwise"
        }
        func_name = faceId_to_function.get(faceId)
        if func_name is None:
            raise ValueError(f"Invalid face id: {faceId}")
        move_function = getattr(self, func_name)
        for _ in range(moveCount):
            move_function()

    def print_cube(self):      
        row = []
        # Note: the print order here is T, F, R, A, L, B.
        for face in ['T', 'F', 'R', 'A', 'L', 'B']:
            row.append(f"{face}:{''.join(self.state[face])}")
        return " ".join(row)
    
    def __str__(self):
        return self.print_cube()
    
    def get_state_tuple(self):
        """Convert cube state to a hashable tuple."""
        return tuple(tuple(self.state[face]) for face in ['T', 'F', 'R', 'A', 'L', 'B'])

    def get_neighbors(self):
        """Generate all possible next moves (neighbors)."""
        moves = [('T', 'C'), ('T', 'A'), ('B', 'C'), ('B', 'A'), 
                 ('F', 'C'), ('F', 'A'), ('A', 'C'), ('A', 'A'), 
                 ('L', 'C'), ('L', 'A'), ('R', 'C'), ('R', 'A')]
        neighbors = []
        for move in moves:
            new_cube = copy.deepcopy(self)  # Create a new cube instance
            new_cube.move_cube(*move)
            neighbors.append((new_cube.get_state_tuple(), move))  # Store state & move
        return neighbors

# BFS Algorithm (for completeness)
def bfs_solve(initial_cube):
    """Breadth-First Search to find solution to a Rubik's Cube with basic pruning.
       Pruning rule: do not perform a move on the same face consecutively.
    """
    count = 0
    initial_state = initial_cube.get_state_tuple()
    goal_state = Cube().get_state_tuple()  # The solved state

    frontier = deque([(initial_cube, [])])  # Each element is (Cube instance, path of moves)
    visited = set()
    visited.add(initial_state)

    while frontier:
        current_cube, path = frontier.popleft()
        
        # Check if we have reached the solved state.
        if current_cube.get_state_tuple() == goal_state:
            return path  # Return the sequence of moves that solved the cube

        # Generate neighbors.
        for next_state, move in current_cube.get_neighbors():
            # --- Pruning step ---
            # If the last move in the path was on the same face, skip this neighbor.
            # This avoids immediately undoing or overcomplicating the previous move.
            if path and move[0] == path[-1][0]:
                continue

            if next_state not in visited:
                visited.add(next_state)
                # Create a new cube state by applying the move.
                new_cube = copy.deepcopy(current_cube)
                new_cube.move_cube(*move)
                frontier.append((new_cube, path + [move]))  # Append new move sequence
                count +=1
                print(path, count)

    return None  # If no solution is found.

# Simple BFS without pruning
def bfs(initial_cube):
    """Breadth-First Search to find solution to a Rubik's Cube."""
    count = 0
    initial_state = initial_cube.get_state_tuple()
    goal_state = Cube().get_state_tuple()  # The solved state

    frontier = deque([(initial_cube, [])])  # (Cube state, Path to reach it)
    visited = set()
    visited.add(initial_state)

    while frontier:
        current_cube, path = frontier.popleft()
        if current_cube.get_state_tuple() == goal_state:
            return path  # Return solution

        for next_state, move in current_cube.get_neighbors():
            if next_state not in visited:
                visited.add(next_state)
                new_cube = copy.deepcopy(current_cube)
                new_cube.move_cube(*move)
                frontier.append((new_cube, path + [move]))  # Append new move sequence
                count+=1
                print(path,count)

    return None  # No solution found
  
#BFS with pruning
def bfs_solve(initial_cube):
    """
    Breadth-First Search with basic pruning.
    Pruning rule: do not perform a move on the same face consecutively.
    """
    initial_state = initial_cube.get_state_tuple()
    goal_state = Cube().get_state_tuple()  # The solved state

    frontier = deque([(initial_cube, [])])  # Each element is (Cube instance, path of moves)
    visited = set()
    visited.add(initial_state)

    while frontier:
        current_cube, path = frontier.popleft()
        
        # Check if we have reached the solved state.
        if current_cube.get_state_tuple() == goal_state:
            return path  # Return the sequence of moves that solved the cube

        # Generate neighbors.
        for next_state, move in current_cube.get_neighbors():
            # --- Pruning step ---
            # If the last move in the path was on the same face, skip this neighbor.
            # This avoids immediately undoing or overcomplicating the previous move.
            if path and move[0] == path[-1][0]:
                continue

            if next_state not in visited:
                visited.add(next_state)
                # Create a new cube state by applying the move.
                new_cube = copy.deepcopy(current_cube)
                new_cube.move_cube(*move)
                frontier.append((new_cube, path + [move]))  # Append new move sequence

    return None  # If no solution is found.

  
# --- New helper functions for file I/O ---

def parse_cube_state(state_str):
    """
    Parse a cube state string into a dictionary.
    Expected format (all on one line):
      T:XXXXXXXXX F:XXXXXXXXX R:XXXXXXXXX A:XXXXXXXXX L:XXXXXXXXX B:XXXXXXXXX
    where each X is a color character.
    """
    state = {}
    tokens = state_str.strip().split()
    for token in tokens:
        if ':' not in token:
            continue  # Skip malformed tokens.
        face, colors = token.split(':', 1)
        if len(colors) != 9:
            raise ValueError(f"Expected 9 color characters for face {face}, got: {colors}")
        state[face] = list(colors)
    # Ensure all 6 faces are present.
    for face in ['T', 'B', 'F', 'A', 'L', 'R']:
        if face not in state:
            raise ValueError(f"Missing face '{face}' in the initial state.")
    return state

def scramble_cube_from_file(input_filename, output_filename):
    """
    Read a file containing the initial cube state on the first line and a series of moves (one per line).
    Each move consists of a faceID and a moveID (separated by whitespace).
    Apply the moves sequentially to obtain a new (scrambled) cube state.
    Finally, write the new state and the initial state (each on its own line) to the output file.
    """
    # Read and parse the input file.
    with open(input_filename, 'r') as file:
        lines = file.readlines()
    
    if not lines:
        raise ValueError("Input file is empty.")

    initial_state_str = lines[0].strip()
    state = parse_cube_state(initial_state_str)
    cube = Cube(state=state)

    # Process each move line.
    for line in lines[1:]:
        move_line = line.strip()
        if not move_line:
            continue  # Skip empty lines.
        parts = move_line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid move format in line: '{line.strip()}'")
        face, move = parts
        cube.move_cube(face, move)
    
    # Get the final state (after applying moves).
    final_state_str = cube.print_cube()
    
    # Write the final and initial states into the output file.
    with open(output_filename, 'w') as file:
        file.write(final_state_str + "\n")
        file.write(initial_state_str + "\n")
    
    print(f"Scrambled cube state written to {output_filename}")

# --- Main function ---
if __name__ == '__main__':
    # Example usage of the new scrambling function:
    # Assume 'scramble_moves.txt' contains:
    #   T:WWWWWWWWW F:GGGGGGGGG R:RRRRRRRRR A:BBBBBBBBB L:OOOOOOOOO B:YYYYYYYYY
    #   F C
    #   T A
    #   R C
    #   B C
    # (Each move is on its own line.)
    input_filename = 'scramble_moves.txt'
    output_filename = 'cube_problem.txt'
    
    scramble_cube_from_file(input_filename, output_filename)
    
    # Optionally, you can load the scrambled cube and run the BFS solver:
    # For example, read the scrambled state from the output file’s first line:
    with open(output_filename, 'r') as file:
        scrambled_state_line = file.readline().strip()
    scrambled_state = parse_cube_state(scrambled_state_line)
    rubiksCube = Cube(state=scrambled_state)
    
    print("Scrambled Cube:")
    print(rubiksCube)
    
    solution_moves = bfs(rubiksCube)
    
    if solution_moves:
        print("\nSolution found:")
        for move in solution_moves:
            print(f"Move {move[0]} {move[1]}")
    else:
        print("\nNo solution found.")
