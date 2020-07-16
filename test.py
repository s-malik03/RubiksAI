from notation_functions import Cube


c= Cube()


c.face=[[['green', 'green', 'green'],
  ['green', 'green', 'green'],
  ['green', 'green', 'green']],

 [['white', 'white', 'white'],
  ['white', 'white', 'white'],
  ['white', 'white', 'white']],

 [['yellow', 'yellow', 'yellow'],
  ['yellow', 'yellow', 'yellow'],
  ['yellow', 'yellow', 'yellow']],

 [['red', 'red', 'red'],
  ['red', 'red', 'red'],
  ['red', 'red', 'red']],

 [['orange', 'orange', 'orange'],
  ['orange', 'orange', 'orange'],
  ['orange', 'orange', 'orange']],

 [['blue', 'blue', 'blue'],
  ['blue', 'blue', 'blue'],
  ['blue', 'blue', 'blue']]]



def format(string):
    dict1 = {
    "F'":"F_",
    "R'":"R_",
    "U'":"U_",
    "B'":"B_",
    "L'":"L_",
    "D'":"D_"
    }
    dict2 = {
    "F2":"F",
    "R2":"R",
    "U2":"U",
    "B2":"B",
    "L2":"L",
    "D2":"D"
    }
    formatted = string.split(" ")
    count, i = len(formatted), 0
    while i < count:
        current_string = formatted[i]
        if current_string in dict1:
            formatted[i] = dict1[current_string]
        if current_string in dict2:
            formatted[i] = dict2[current_string]
            formatted.insert(i+1,dict2[current_string])
            count += 1
        i += 1

    return formatted






#scrambles cube for different solutions

def scramble(moves, c):
    notations = {
    "U":Cube.U,
    "U_":Cube.U_,
    "L":Cube.L,
    "L_":Cube.L_,
    "F":Cube.F,
    "F_":Cube.F_,
    "B":Cube.B,
    "B_":Cube.B_,
    "D":Cube.D,
    "D_":Cube.D_,
    "R":Cube.R,
    "R_":Cube.R_
    }
    for i in moves:
        current_move = notations[i]
        c = current_move(c)
    return c




moves = format("F")
print(moves)

c = scramble(moves,c)
print(Cube.GetFace(c,0))
