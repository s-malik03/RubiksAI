import tkinter as tk
from array import *
import numpy
import copy

class Cube():

    def __init__(self,face=None,actions=None):

        if face!=None:

            self.face=face

        else:
            self.face=numpy.full((6,3,3,),
                             "##############" #used to initialize array with enough space for each color in string format
                             ) #array storing all faces and their arrays. 6x3x3 array
        self.mappings={ #dictionary to translate x,y coordinates on cube into respective position in array. 0,0 is considered square in the middle of the face
            (0,0):(1,1),
            (0,1):(0,1),
            (0,-1):(2,1),
            (1,0):(1,2),
            (1,1):(0,2),
            (1,-1):(2,2),
            (-1,0):(1,0),
            (-1,1):(0,0),
            (-1,-1):(2,0)
        }

        if actions==None:
            self.actions=[] #actions array storing a list of all previous actions called on the cube. Once a goal state is reached, there will be no need to backtrace, rather all actions will already be present in the goal state and can be displayed
        else:
            self.actions=actions

    def WriteToFace(self,facenum,row,column,value):

        self.face[facenum][row][column]=value #the array contents are referenced in the following manner: [face][row][column]

    def GetValue(self,fnum,row,column):

        return self.face[fnum][row][column]

    def GetFace(self,num):

        return self.face[num] #returns 2 dimensional array of specified face number

    def GetAllFaces(self): #basically returns entire cube array

        return self.face

    def LastAction(self):

        if(len(self.actions)!=0):

            return self.actions[-1]

        else:

            return 0

    def ClockWise(self,facenumber): #gets new value of face after rotating it clockwise

        f=numpy.full((3,3),"#############") #reason numpy.full is used is because using vanilla python arrays causes all faces to be overwritten when changing an individual face
        for y in range(-1,2):
            for x in range(-1,2):
                xy=self.mappings[(x,y)]
                r=xy[0]
                c=xy[1]
                x2=0-x
                xy_=self.mappings[(y,x2)]
                r2=xy_[0]
                c2=xy_[1]
                f[r2][c2]=copy.deepcopy(self.face[facenumber][r][c])
        return copy.deepcopy(f) #deepcopy is used as in case of arrays usually a reference is assigned to the original array causing messy memory issues. So a function is used to copy the array

    def AntiClockWise(self,facenumber): #gets new value of face after rotating it anti-clockwise

        f=numpy.full((3,3),"#############")
        for y in range(-1,2):
            for x in range(-1,2):
                xy=self.mappings[(x,y)]
                r=xy[0]
                c=xy[1]
                y2=0-y
                xy_=self.mappings[(y2,x)]
                r2=xy_[0]
                c2=xy_[1]
                f[r2][c2]=self.face[facenumber][r][c]
        return copy.deepcopy(f)

    def U(self):

        newface=copy.deepcopy(self.face)
        newface[0][0]=self.face[3][0]
        newface[4][0]=self.face[0][0]
        newface[5][0]=self.face[4][0]
        newface[3][0]=self.face[5][0]
        newface[1]=self.ClockWise(1)
        self=Cube(copy.deepcopy(newface))
        return self

    def L(self):

        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[0][i][0]=self.face[1][i][0]
            newface[1][i][0]=self.face[5][i][2]
            newface[2][i][0]=self.face[0][i][0]
            newface[5][i][2]=self.face[2][i][0]
        newface[4]=self.ClockWise(4)
        self=Cube(copy.deepcopy(newface))
        return self

    def F(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][2][i] = self.face[4][i][2]
            newface[4][i][2] = self.face[2][0][i]
            newface[2][0][i] = self.face[3][i][0]
            newface[3][i][0] = self.face[1][2][i]
        newface[0]=self.ClockWise(0)
        self=Cube(copy.deepcopy(newface))
        return self

    def R(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[0][i][2] = self.face[2][i][2]
            newface[2][i][2] = self.face[5][i][0]
            newface[5][i][0] = self.face[1][i][2]
            newface[1][i][2] = self.face[0][i][2]
        newface[3]=self.ClockWise(3)

        self=Cube(copy.deepcopy(newface))
        return self

    def B(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][0][i] = self.face[3][i][2]
            newface[3][i][2] = self.face[2][2][i]
            newface[2][2][i] = self.face[4][i][0]
            newface[4][i][0] = self.face[1][0][i]
        newface[5] = self.ClockWise(5)

        self=Cube(copy.deepcopy(newface))
        return self

    def D(self):

        newface=copy.deepcopy(self.face)
        newface[4][2]=self.face[5][2]
        newface[0][2]=self.face[4][2]
        newface[5][2]=self.face[3][2]
        newface[3][2]=self.face[0][2]
        newface[2]=self.ClockWise(2)

        self=Cube(copy.deepcopy(newface))
        return self

    def U_(self):

        newface=copy.deepcopy(self.face)
        newface[3][0]=self.face[0][0]
        newface[0][0]=self.face[4][0]
        newface[4][0]=self.face[5][0]
        newface[5][0]=self.face[3][0]
        newface[1]=self.AntiClockWise(1)

        self=Cube(copy.deepcopy(newface))
        return self

    def L_(self):

        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][i][0]=self.face[0][i][0]
            newface[5][i][2]=self.face[1][i][0]
            newface[0][i][0]=self.face[2][i][0]
            newface[2][i][0]=self.face[5][i][2]
        newface[4]=self.AntiClockWise(4)

        self=Cube(copy.deepcopy(newface))
        return self

    def F_(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][2][i] = self.face[3][i][0]
            newface[3][i][0] = self.face[2][0][i]
            newface[2][0][i] = self.face[4][i][2]
            newface[4][i][2] = self.face[1][2][i]
        newface[0] = self.AntiClockWise(0)

        self=Cube(copy.deepcopy(newface))
        return self

    def R_(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[0][i][2]=self.face[1][i][2]
            newface[1][i][2]=self.face[5][i][0]
            newface[5][i][0]=self.face[2][i][2]
            newface[2][i][2]=self.face[0][i][2]
        newface[3]=self.AntiClockWise(3)

        self=Cube(copy.deepcopy(newface))
        return self

    def B_(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][0][i] = self.face[4][i][0]
            newface[4][i][0] = self.face[2][2][i]
            newface[2][2][i] = self.face[3][i][2]
            newface[3][i][2] = self.face[1][0][i]
        newface[5] = self.AntiClockWise(5)

        self=Cube(copy.deepcopy(newface))
        return self

    def D_(self):

        newface=copy.deepcopy(self.face)
        newface[4][2]=self.face[0][2]
        newface[0][2]=self.face[3][2]
        newface[5][2]=self.face[4][2]
        newface[3][2]=self.face[5][2]
        newface[2]=self.AntiClockWise(2)
        self=Cube(copy.deepcopy(newface))
        return self



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
    for i in range(len(moves)):
        current_move = notations[moves[i]]
        c = current_move(c)
    return c



moves = format("F2 L' D' F2 L F' D' B' U B L' B U' F B U2 D L' R B D2 R L2 D2 U'")
#or manually set moves
print(moves)

c = scramble(moves,c)
print(Cube.GetAllFaces(c))
