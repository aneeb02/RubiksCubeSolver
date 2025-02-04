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
            self.state = {
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
        The face is stored as a list of 9 elements:
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
          F_top ← R_top, R_top ← B_top, B_top ← L_top, L_top ← F_top.
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
        Convert the internal cube state to a string using the file face IDs.
        We use the mapping:
           'U' -> 'T' (Top)
           'D' -> 'B' (Bottom)
           'F' -> 'F'
           'B' -> 'A' (bAck)
           'L' -> 'L'
           'R' -> 'R'
        Each face is printed as: FaceID:XXXXXXXXX
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
      - Subsequent lines: one move per line specified as:
         <faceID> <moveID>
         (faceID ∈ {T, B, F, L, R, A} and moveID ∈ {C, A})
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


# --- Example usage ---
if __name__ == '__main__':
    input_filename = "cube_moves.txt"
    output_filename = "scrambled_output.txt"

    try:
        scramble_cube(input_filename, output_filename)
        print(f"Scrambled cube state and initial state written to {output_filename}")
    except Exception as e:
        print("Error:", e)
