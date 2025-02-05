from collections import deque
import itertools
import sys


class Cube3x3:
    """
    A 3x3x3 Rubik's Cube represented using corner and edge permutations.
    This approach models the cube as a permutation puzzle rather than a full face representation.
    """
    
    # Corner and Edge Indexing
    CORNER_POSITIONS = list(range(8))  # 8 corners
    EDGE_POSITIONS = list(range(12))   # 12 edges

    # Moves (Quarter Turns)
    MOVES = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]

    def __init__(self, corners=None, edges=None):
        """
        Cube is represented as permutations of corner and edge pieces.
        """
        if corners is None:
            self.corners = tuple(range(8))  # Solved state (corners in order)
        else:
            self.corners = corners

        if edges is None:
            self.edges = tuple(range(12))  # Solved state (edges in order)
        else:
            self.edges = edges

    def apply_move(self, move):
        """
        Apply a given move to the cube, updating the corner and edge permutations.
        """
        move_permutations = {
            "U":  {"corners": (1, 2, 3, 0), "edges": (1, 2, 3, 0)},
            "U'": {"corners": (0, 3, 2, 1), "edges": (0, 3, 2, 1)},
            "D":  {"corners": (5, 6, 7, 4), "edges": (5, 6, 7, 4)},
            "D'": {"corners": (4, 7, 6, 5), "edges": (4, 7, 6, 5)},
            "L":  {"corners": (4, 0, 3, 7), "edges": (4, 0, 8, 7)},
            "L'": {"corners": (7, 3, 0, 4), "edges": (7, 8, 0, 4)},
            "R":  {"corners": (1, 5, 6, 2), "edges": (1, 5, 9, 6)},
            "R'": {"corners": (2, 6, 5, 1), "edges": (6, 9, 5, 1)},
            "F":  {"corners": (0, 1, 5, 4), "edges": (0, 9, 5, 8)},
            "F'": {"corners": (4, 5, 1, 0), "edges": (8, 5, 9, 0)},
            "B":  {"corners": (3, 2, 6, 7), "edges": (3, 10, 6, 11)},
            "B'": {"corners": (7, 6, 2, 3), "edges": (11, 6, 10, 3)},
        }

        if move in move_permutations:
            corners_perm = move_permutations[move]["corners"]
            edges_perm = move_permutations[move]["edges"]

            # Apply the permutation by rotating indices
            self.corners = tuple(self.corners[i] if i not in corners_perm else self.corners[corners_perm[(corners_perm.index(i) - 1) % 4]] for i in self.CORNER_POSITIONS)
            self.edges = tuple(self.edges[i] if i not in edges_perm else self.edges[edges_perm[(edges_perm.index(i) - 1) % 4]] for i in self.EDGE_POSITIONS)

    def get_state_tuple(self):
        """Returns a hashable tuple of (corners, edges) for use in BFS."""
        return (self.corners, self.edges)

    def is_solved(self):
        """Checks if the cube is in the solved state."""
        return self.corners == tuple(range(8)) and self.edges == tuple(range(12))


def bidirectional_bfs_solve(start_cube, goal_cube):
    """
    Solve the 3x3x3 Rubik's Cube using bidirectional BFS.
    Returns the shortest sequence of moves to solve the cube.
    """
    if start_cube.is_solved():
        return []  # Already solved

    frontier_start = deque([(start_cube, [])])
    frontier_goal = deque([(goal_cube, [])])

    visited_start = {start_cube.get_state_tuple(): []}
    visited_goal = {goal_cube.get_state_tuple(): []}

    while frontier_start and frontier_goal:
        # Expand forward from the start state
        if frontier_start:
            cube, path = frontier_start.popleft()
            for move in Cube3x3.MOVES:
                new_cube = Cube3x3(cube.corners, cube.edges)
                new_cube.apply_move(move)
                state_tuple = new_cube.get_state_tuple()

                if state_tuple in visited_goal:
                    return path + [move] + visited_goal[state_tuple][::-1]  # Solution found!

                if state_tuple not in visited_start:
                    visited_start[state_tuple] = path + [move]
                    frontier_start.append((new_cube, path + [move]))

        # Expand backward from the goal state
        if frontier_goal:
            cube, path = frontier_goal.popleft()
            for move in Cube3x3.MOVES:
                new_cube = Cube3x3(cube.corners, cube.edges)
                new_cube.apply_move(move)
                state_tuple = new_cube.get_state_tuple()

                if state_tuple in visited_start:
                    return visited_start[state_tuple] + [move] + path[::-1]  # Solution found!

                if state_tuple not in visited_goal:
                    visited_goal[state_tuple] = path + [move]
                    frontier_goal.append((new_cube, path + [move]))

    return None  # No solution found


def apply_scramble(cube, scramble):
    """Applies a given scramble sequence to a cube."""
    moves = scramble.split()
    for move in moves:
        cube.apply_move(move)

def parse_cube_state(filename="problem.txt"):
    """Reads the problem file and extracts the full cube state as corner and edge permutations."""
    try:
        with open(filename, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        # Debug Output: Check file content
        print("DEBUG: Raw file contents:")
        for i, line in enumerate(lines):
            print(f"Line {i+1}: {repr(line)}")  # Print each line with special characters

        # Ensure exactly six lines for cube faces
        if len(lines) != 6:
            raise ValueError("Invalid problem file format. It must have exactly six lines.")

        # Map file format face IDs to internal representation
        file_to_internal = {'T': 'U', 'B': 'D', 'F': 'F', 'A': 'B', 'L': 'L', 'R': 'R'}
        cube_state = {}

        for line in lines:
            parts = line.split(":")
            if len(parts) != 2:
                raise ValueError(f"Invalid format in problem file: {line}")
            face_id, stickers = parts
            if face_id not in file_to_internal:
                raise ValueError(f"Unknown face ID: {face_id}")
            if len(stickers) != 9:
                raise ValueError(f"Invalid number of stickers for face {face_id}. Expected 9.")

            internal_face = file_to_internal[face_id]
            cube_state[internal_face] = list(stickers)

        return cube_state  # Returns correctly formatted dictionary

    except FileNotFoundError:
        sys.exit(f"Error: {filename} not found. Please create it with a valid cube state.")
        
def convert_sticker_state_to_permutations(sticker_state):
    """
    Converts a full face sticker representation into a corner and edge permutation representation.
    This version maps sticker colors to face labels using the centers, and then builds sorted strings.
    """
    # Build mapping from color to face based on center stickers.
    color_to_face = {}
    for face, stickers in sticker_state.items():
        center_color = stickers[4]  # center is always index 4
        color_to_face[center_color] = face

    # Define solved state corner/edge representations (sorted so that we can compare)
    SOLVED_CORNERS = tuple(''.join(sorted(corner)) for corner in ('URF', 'UFL', 'ULB', 'UBR', 'DRB', 'DBL', 'DLF', 'DFR'))
    SOLVED_EDGES = tuple(''.join(sorted(edge)) for edge in ('UR', 'UF', 'UL', 'UB', 'DR', 'DF', 'DL', 'DB', 'FR', 'FL', 'BR', 'BL'))

    # These specify which stickers (by face and index) form each physical corner and edge.
    CORNER_POSITIONS = [
        ('U', 'R', 'F'), ('U', 'F', 'L'), ('U', 'L', 'B'), ('U', 'B', 'R'),
        ('D', 'R', 'B'), ('D', 'B', 'L'), ('D', 'L', 'F'), ('D', 'F', 'R')
    ]
    EDGE_POSITIONS = [
        ('U', 'R'), ('U', 'F'), ('U', 'L'), ('U', 'B'),
        ('D', 'R'), ('D', 'F'), ('D', 'L'), ('D', 'B'),
        ('F', 'R'), ('F', 'L'), ('B', 'R'), ('B', 'L')
    ]

    corner_perm = []
    # The indices [8, 2, 0] correspond to positions on the face for each corner.
    for target_corner in CORNER_POSITIONS:
        # Collect the three stickers from the cube state
        try:
            found_corner_colors = [sticker_state[f][i] for f, i in zip(target_corner, [8, 2, 0])]
        except KeyError as e:
            raise ValueError(f"Face {e} not found in sticker state.") from e
        # Map the colors to face labels using the centers.
        found_corner_faces = [color_to_face[color] for color in found_corner_colors]
        # Sort them so that they match our solved representation.
        found_corner = ''.join(sorted(found_corner_faces))
        try:
            index = SOLVED_CORNERS.index(found_corner)
        except ValueError:
            raise ValueError(f"Corner {found_corner} not found in solved corners: {SOLVED_CORNERS}")
        corner_perm.append(index)

    edge_perm = []
    # The indices [5, 3] correspond to positions on the face for each edge.
    for target_edge in EDGE_POSITIONS:
        found_edge_colors = [sticker_state[f][i] for f, i in zip(target_edge, [5, 3])]
        found_edge_faces = [color_to_face[color] for color in found_edge_colors]
        found_edge = ''.join(sorted(found_edge_faces))
        try:
            index = SOLVED_EDGES.index(found_edge)
        except ValueError:
            raise ValueError(f"Edge {found_edge} not found in solved edges: {SOLVED_EDGES}")
        edge_perm.append(index)

    return tuple(corner_perm), tuple(edge_perm)


if __name__ == "__main__":
    # Read the full scrambled cube state from the problem file
    scrambled_sticker_state = parse_cube_state()

    
    # Convert the scrambled sticker state into the correct format
    scrambled_corners, scrambled_edges = convert_sticker_state_to_permutations(scrambled_sticker_state)

    # Create a Cube3x3 instance with corner/edge permutations
    scrambled_cube = Cube3x3(corners=scrambled_corners, edges=scrambled_edges)

    # Define the goal state (solved cube)
    goal_cube = Cube3x3()  # A fresh instance is already solved

    # Solve the scrambled cube
    solution = bidirectional_bfs_solve(scrambled_cube, goal_cube)

    # Output results
    print("\nScrambled Cube State:")
    for face, stickers in scrambled_sticker_state.items():
        print(f"{face}: {''.join(stickers)}")

    if solution is not None:
      print("\nSolution found in {} moves:".format(len(solution)))
      print(" ".join(solution))
    else:
      print("\nNo solution found.")
