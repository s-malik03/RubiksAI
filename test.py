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


    print(formatted)





#scrambles cube for different solutions
moves = [
"B" ,"B", "U", "R", "R", "U", "B", "B", "R", "F'", "U'", "D", "D", "B", "D", "L", "L", "R", "D",
"D", "U", "U", "R", "R", "L", "L", "F'", "U", "B", "F", "U", "U", "B", "U", "R"]
def scramble(moves, c):
    notations = {
    "U":Cube.U,
    "U'":Cube.U_,
    "L":Cube.L,
    "L'":Cube.L_,
    "F":Cube.F,
    "F'":Cube.F_,
    "B":Cube.B,
    "B'":Cube.B_,
    "D":Cube.D,
    "D'":Cube.D_,
    "R":Cube.R,
    "R'":Cube.R_
    }
    for i in moves:
        print(i)
        current_move = notations[i]
        c  = current_move(c)
    a = Cube.GetAllFaces(c)
    print(a)
    return c




format("B2 R F2 D' U' R' F2 B' U2 F' U D L' U2 B U F' U2 L' R' U' L2 F2 L' F")
