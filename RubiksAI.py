import tkinter as tk
from array import *
import numpy
import copy

class Node(): #to contain current state and parent state

    def __init__(self,state,parent):

        self.state=state
        self.parent=parent

class Frontier(): #to store all nodes to be explored

    def __init__(self):

        self.frontier=[] #array to store Node instances

    def add(self,node):

        self.frontier.append(node)

    def remove(self):

        if len(self.frontier)==0: #frontier empty so all nodes explored therefore no solution
            raise Exception("No Solution")
        else:
            node=self.frontier[0] #nodes removed using stack method, i.e. first in last out
            self.frontier=self.frontier[1:]
            return node

class OptionMenu(tk.Frame): #dropdown list object

    def __init__(self, coordinates, master, status, *options):

        super().__init__(master)
        self.status = tk.StringVar()
        self.status.set(status)
        self.dropdown = tk.OptionMenu(self, self.status, *options)
        self.dropdown.pack()
        self.coordinates=coordinates

    def getval(self): #gets last value selected in dropdown list

        return self.status.get()

class Cube():

    def __init__(self):

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
        self.actions=[] #actions array storing a list of all previous actions called on the cube. Once a goal state is reached, there will be no need to backtrace, rather all actions will already be present in the goal state and can be displayed

    def WriteToFace(self,facenum,row,column,value):

        self.face[facenum][row][column]=value #the array contents are referenced in the following manner: [face][row][column]

    def GetValue(self,fnum,row,column):

        return self.face[fnum][row][column]

    def GetFace(self,num):

        return self.face[num] #returns 2 dimensional array of specified face number

    def GetAllFaces(self): #basically returns entire cube array

        return self.face

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
                f[r2][c2]=self.face[facenumber][r][c]
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

    def U(self): #this is a clockwise notation function.

        newface=copy.deepcopy(self.face) #as seen in this case had the array been assigned normally like newface=self.face ; it would simply assign a reference to self.face, therefore changes to newface would invariably lead to changes to self.face
        newface[0][0]=self.face[3][0] # for each movement, there are certain changes where universal logic cannot easily be applied, such as the exchanging of rows or columns between faces. In this case each row or column has to individually be assigned to its new face
        newface[4][0]=self.face[0][0] # in this case it was a horizontal movement in reference to face0 so only rows were swapped
        newface[5][0]=self.face[4][0]
        newface[3][0]=self.face[5][0]
        newface[1]=self.ClockWise(1)
        self.face=copy.deepcopy(newface)
        self.actions.append("U") #appends the notation used to the actions array

    def L(self):

        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[0][i][0]=self.face[1][i][0] #in this case columns had to be swapped, so different logic had to be applied
            newface[1][i][0]=self.face[5][i][0]
            newface[2][i][0]=self.face[0][i][0]
            newface[5][i][0]=self.face[2][i][0]
        newface[4]=self.Clockwise(4)
        self.face=copy.deepcopy(newface)
        self.actions.append("L")

    def F(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][2][i] = self.face[3][i][0]
            newface[3][i][0] = self.face[2][0][i]
            newface[2][0][i] = self.face[4][i][2]
            newface[4][i][2] = self.face[1][2][i]
        newface[0]=self.ClockWise(face)
        self.face=copy.deepcopy(newface)
        self.actions.append("F")
        #not done
    def R(self):

        self.actions.append("R")

    def B(self):

        self.actions.append("B")

    def D(self):

        self.actions.append("D")

    def U_(self): #all notation functions ending with _ are anticlockwise rotations

        self.actions.append("U`")

    def L_(self):

        self.actions.append("L`")

    def F_(self):
        newface=copy.deepcopy(self.face)
        for i in range(0,3):
            newface[1][2][i] = self.face[4][i][2]
            newface[4][i][2] = self.face[2][0][i]
            newface[2][0][i] = self.face[3][i][0]
            newface[3][i][0] = self.face[1][2][i]
        newface[0] = self.AntiClockWise(face)
        self.face=copy.deepcopy(newface)
        self.actions.append("F`")
        #not done
    def R_(self):

        self.actions.append("R`")

    def B_(self):

        self.actions.append("B`")

    def D_(self):

        self.actions.append("D`")

def GetInput(CubeObject):

    faces=[None]*6 #similar to faces array in Cube instance yet will be filled with color array of instances of OptionMenu. Will be a 6x9 array. Rows and Columns are not regarded here. Order is from left to right, up to down
    for fn in range(0,6):
        Window=tk.Tk() #initializes gui to choose colors, new window for each face
        Window.title("Face "+str(fn))
        color=[OptionMenu((0,0),
                          Window,
                          "white",
                          "white",
                          "yellow",
                          "orange",
                          "red",
                          "blue",
                          "green"
                          )
               ]*9
        i=0
        for r in range(3):
            for c in range(3):
                color[i]=OptionMenu((r,c), #row and column number of color
                                    Window,
                                    "white",
                                    "white",
                                    "yellow",
                                    "orange",
                                    "red",
                                    "blue",
                                    "green"
                                    )
                color[i].grid(row=r,
                              column=c
                              )
                i=i+1
        button = tk.Button(text = "Submit",
                           command = lambda: Window.destroy() #button to close window
                           )
        button.grid(row=4,
                    column=1
                    )
        Window.mainloop()
        faces[fn]=color #current face is set to color array of current face
    for f in range(0,6): #takes the value from each dropdown menu and assigns to its respective position on the cube
        count=0
        for x in range(0,3):
            for y in range(0,3):
                CubeObject.WriteToFace(f,
                                       x,
                                       y,
                                       faces[f][count].getval()
                                       )
                count=count+1
    return CubeObject

def Heuristic(CubeState): #returns a score based on how many faces are solved. Currently not intelligent, merely to check if goal state has been achieved

    score=0
    for CubeFace in CubeState.face:
        cmp1=CubeFace[0]==CubeFace[1]
        cmp2=CubeFace[1]==CubeFace[2]
        if cmp1.all() and cmp2.all():
            score=score+1
    return score

def Solve(CubeObj):

    stack=Frontier() #initialize frontier
    stack.add( #add initial state to frontier
        Node(CubeObj,none)
        )
    optimal=25
    while(len(stack.frontier)!=0):
        current_node=stack.remove() #remove last node from frontier
        if(len(current_node.state.actions)>optimal):
            current_node=stack.remove() #if more than 25 moves have been done on the Cube state then discard this state and remove next state from frontier
        if(Heuristic(current_node.state)==6): #if goal state has been reached, return node state
            solution=current_node.state #temporary solution
            optimal=len(current_node.state.actions)
        else: #add further nodes to frontier after applying actions
            stack.add(
                Node(current_node.state.U(),current_node)
                )
            stack.add(
                Node(current_node.state.L(),current_node)
                )
            stack.add(
                Node(current_node.state.F(),current_node)
                )
            stack.add(
                Node(current_node.state.R(),current_node)
                )
            stack.add(
                Node(current_node.state.B(),current_node)
                )
            stack.add(
                Node(current_node.state.D(),current_node)
                )
            stack.add(
                Node(current_node.state.U_(),current_node)
                )
            stack.add(
                Node(current_node.state.L_(),current_node)
                )
            stack.add(
                Node(current_node.state.F_(),current_node)
                )
            stack.add(
                Node(current_node.state.R_(),current_node)
                )
            stack.add(
                Node(current_node.state.B_(),current_node)
                )
            stack.add(
                Node(current_node.state.D_(),current_node)
                )
    return solution #optimal solution after all nodes explored

c=Cube()
c=GetInput(c)
S=Solve(c)
print("Actions required to solve:")
for a in S.actions:
    print(a)
