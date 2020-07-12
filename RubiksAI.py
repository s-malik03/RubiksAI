import tkinter as tk
from array import *
import numpy
import copy
from notation_functions import Cube
import os

class Node(): #to contain current state and parent state

    def __init__(self,state):

        self.state=state

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

def HeuristicOld(CubeState): #returns a score based on how many faces are solved. Currently not intelligent, merely to check if goal state has been achieved

    score=0
    for CubeFace in CubeState.face:
        print(CubeFace)
        cmp1=CubeFace[0]==CubeFace[1]
        cmp2=CubeFace[1]==CubeFace[2]
        if cmp1.all() and cmp2.all():
            score=score+1
    return score

def Heuristic(CubeState):

    total_score=0
    face_score=0
    for CubeFace in CubeState.face:
        check=CubeFace[0][0]
        for Row in CubeFace:
            for Col in Row:
                if Col==check:
                    face_score+=1
        if face_score==9:
            total_score+=1
    return total_score

def Solve(CubeObj):

    stack=Frontier() #initialize frontier
    stack.add( #add initial state to frontier
        Node(CubeObj)
        )
    optimal=25
    i=0
    nodes_explored=0
    while(len(stack.frontier)!=0):
        current_node=stack.remove() #remove last node from frontier
        nodes_explored+=1
        os.system("cls")
        print("Nodes explored:"+ str(nodes_explored))
        if(len(current_node.state.actions)>optimal):
            current_node=stack.remove() #if more than 25 moves have been done on the Cube state then discard this state and remove next state from frontier
        elif(Heuristic(current_node.state)==6): #if goal state has been reached, return node state
            solution=current_node.state #temporary solution
            optimal=len(current_node.state.actions)
        else: #add further nodes to frontier after applying actions
            if(current_node.state.LastAction!="U"):
                stack.add(
                    Node(current_node.state.U() )
                    )
            if(current_node.state.LastAction!="L"):
                stack.add(
                    Node(current_node.state.L() )
                    )
            if(current_node.state.LastAction!="F"):
                stack.add(
                    Node(current_node.state.F() )
                    )
            if(current_node.state.LastAction!="R"):
                stack.add(
                    Node(current_node.state.R() )
                    )
            if(current_node.state.LastAction!="B"):
                stack.add(
                    Node(current_node.state.B() )
                    )
            if(current_node.state.LastAction!="D"):
                stack.add(
                    Node(current_node.state.D() )
                    )
            if(current_node.state.LastAction!="U`"):
                stack.add(
                    Node(current_node.state.U_() )
                    )
            if(current_node.state.LastAction!="L`"):
                stack.add(
                    Node(current_node.state.L_() )
                    )
            if(current_node.state.LastAction!="F`"):
                stack.add(
                    Node(current_node.state.F_() )
                    )
            if(current_node.state.LastAction!="R`"):
                stack.add(
                    Node(current_node.state.R_() )
                    )
            if(current_node.state.LastAction!="B`"):
                stack.add(
                    Node(current_node.state.B_() )
                    )
            if(current_node.state.LastAction!="D`"):
                stack.add(
                    Node(current_node.state.D_() )
                    )
    return solution #optimal solution after all nodes explored

c=Cube()
#c=GetInput(c)
c.face=[[['green', 'blue', 'orange'],
  ['blue', 'yellow', 'blue'],
  ['blue', 'red', 'red']],

 [['white', 'yellow', 'green'],
  ['white', 'blue', 'orange'],
  ['orange', 'orange', 'white']],

 [['red', 'yellow', 'yellow'],
  ['white', 'green', 'yellow'],
  ['orange', 'green', 'red']],

 [['green', 'yellow', 'red'],
  ['white', 'orange', 'green'],
  ['blue', 'green', 'yellow']],

 [['orange', 'green', 'yellow'],
  ['red', 'red', 'red'],
  ['blue', 'orange', 'white']],

 [['white', 'blue', 'blue'],
  ['red', 'white', 'white'],
  ['green', 'orange', 'yellow']]]
S=Solve(c)
print("Actions required to solve:")
for a in S.actions:
    print(a)
a=input("press any key to continue")
