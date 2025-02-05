
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
        self.state[face] = [prev[6], prev[3], prev[0],prev[7], prev[4], prev[1],prev[8], prev[5], prev[2]]

    # --- Move functions ---
    #left clockwise
    def Left_Clockwise(self):
        self.rotate_faceC('L')
        temp = [self.state['T'][0], self.state['T'][3], self.state['T'][6]]  # Save Top's left column.
        #top[0,3,6] = bAck[8,5,2]
        self.state['T'][0] = self.state['A'][8]
        self.state['T'][3] = self.state['A'][5]
        self.state['T'][6] = self.state['A'][2]
        # bAck[2,5,8] = bottom [6,3,0]
        self.state['A'][8] = self.state['B'][0]
        self.state['A'][5] = self.state['B'][3]
        self.state['A'][2] = self.state['B'][6]
        # bottom[0,3,6] = front[0,3,6]
        self.state['B'][0] = self.state['F'][0]
        self.state['B'][3] = self.state['F'][3]
        self.state['B'][6] = self.state['F'][6]
        # front[0,3,6] = top[0,3,6]
        self.state['F'][0] = temp[0]
        self.state['F'][3] = temp[1]
        self.state['F'][6] = temp[2]
    
    #bottom clockwise
    def Bottom_Clockwise(self):
        """
          F_bottom ← L_bottom, L_bottom ← A_bottom, A_bottom ← R_bottom, R_bottom ← F_bottom.
        """  
        self.rotate_faceC('B')
        temp = self.state['F'][6:9].copy()
        #front[6,7,8] = left[6,7,8]
        self.state['F'][6:9] = self.state['L'][6:9]
        #left[6,7,8] = bAck[6,7,8]
        self.state['L'][6:9] = self.state['A'][6:9]
        #bAck[6,7,8] = right[6,7,8]
        self.state['A'][6:9] = self.state['R'][6:9]
        #right[6,7,8] = front[6,7,8]
        self.state['R'][6:9] = temp

    def Front_Clockwise(self):
        self.rotate_faceC('F')
        temp = self.state['T'][6:9].copy()  
        # Top[6,7,8] = left[8,5,2]
        self.state['T'][6] = self.state['L'][8]
        self.state['T'][7] = self.state['L'][5]
        self.state['T'][8] = self.state['L'][2]
        # Left[8,5,2] = bottom[2,1,0]
        self.state['L'][2] = self.state['B'][0]
        self.state['L'][5] = self.state['B'][1]
        self.state['L'][8] = self.state['B'][2]
        # Bottom [0,1,2] = right[6,3,0]
        self.state['B'][0] = self.state['R'][6]
        self.state['B'][1] = self.state['R'][3]
        self.state['B'][2] = self.state['R'][0]
        # right[0,3,6] = top[6,7,8]
        self.state['R'][0] = temp[2]
        self.state['R'][3] = temp[1]
        self.state['R'][6] = temp[0]
    
    #back clockwise
    def Back_Clockwise(self):
        self.rotate_faceC('A')
        temp = self.state['T'][:3].copy()  
        # Top[0,1,2] = right[2,5,8]
        self.state['T'][0] = self.state['R'][2]
        self.state['T'][1] = self.state['R'][5]
        self.state['T'][2] = self.state['R'][8]
        # Right[8,5,2] = bottom[6,7,8]
        self.state['R'][2] = self.state['B'][8]
        self.state['R'][5] = self.state['B'][7]
        self.state['R'][8] = self.state['B'][6]
        # Bottom[6,7,8] = left[0,3,6]
        self.state['B'][6] = self.state['L'][0]
        self.state['B'][7] = self.state['L'][3]
        self.state['B'][8] = self.state['L'][6]
        # Left[0,3,6] = top[2,1,0]
        self.state['L'][0] = temp[2]
        self.state['L'][3] = temp[1]
        self.state['L'][6] = temp[0]
    
    #Top clockwise
    def Top_Clockwise(self):
        self.rotate_faceC('T')
        temp = self.state['F'][:3].copy()
        #front[0,1,2] = right[0,1,2]
        self.state['F'][:3] = self.state['R'][:3]
        #right[0,1,2] = bAck[0,1,2]
        self.state['R'][:3] = self.state['A'][:3]
        #bAck[0,1,2] = left[0,1,2]
        self.state['A'][:3] = self.state['L'][:3]
        #left[0,1,2] = front[0,1,2]
        self.state['L'][:3] = temp

    
    #right clockwise
    def Right_Clockwise(self):        
        self.rotate_faceC('R')
        temp = [self.state['T'][2], self.state['T'][5], self.state['T'][8]]  
        # Top[8,5,2] = front[8,5,2]
        self.state['T'][2] = self.state['F'][2]
        self.state['T'][5] = self.state['F'][5]
        self.state['T'][8] = self.state['F'][8]
        # Front[2,5,8] = bottom[2,5,8]
        self.state['F'][2] = self.state['B'][2]
        self.state['F'][5] = self.state['B'][5]
        self.state['F'][8] = self.state['B'][8]
        # Bottom[2,5,8] = bAck[6,3,0]
        self.state['B'][2] = self.state['A'][6]
        self.state['B'][5] = self.state['A'][3]
        self.state['B'][8] = self.state['A'][0]
        # Back[6,3,0] = top[2,5,8]
        self.state['A'][6] = temp[0]
        self.state['A'][3] = temp[1]
        self.state['A'][0] = temp[2]
    
    #apply a move on cube based on moveId
    def move_cube(self, faceId, moveId):
        moveCount = 1
        if moveId == "C":
         moveCount = 1
        elif moveId == "A":
         moveCount = 3
        else:
         raise ValueError("Invalid move direction. Use 'C', 'A'.")
        
        faceId_to_function={
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
        for face in ['T', 'F', 'R', 'A', 'L', 'B']:
            row.append(f"{face}:{''.join(self.state[face])}")
        return " ".join(row)
    def __str__(self):
        return self.print_cube()

#main function
if __name__ == '__main__':
    rubiksCube=Cube(state=None)
    #moves format= {faceId,moveId} 
    #moveIds = C for clockwise, A for anticlockwise
    moves_seq=['F,C', 'T,A', 'R,C','L,C']

    try:
        for move in moves_seq:
            faceId, dir = move.strip().split(',')
            rubiksCube.move_cube(faceId, dir)
            print(f"After move {faceId},{dir}:")
            print(rubiksCube)
        
    except Exception as e:
        print("Error:", e)