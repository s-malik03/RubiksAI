import tkinter as tk
from array import *
import numpy
import copy
from notation_functions import Cube
import os
import networkx as nx
import matplotlib.pyplot as plt

class Node(): #to contain current state and parent state

    def __init__(self,state,number,parent=0):

        self.state=state
        self.number=number
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

diag=[]

def fd(n):

    first_digit = n
    while (first_digit >= 10):
        first_digit = first_digit // 10
    return first_digit

def Heuristic(CubeState):

    total_score=0
    CubeFace=CubeState.face

    if (
        CubeFace[1][0][1]==CubeFace[1][1][1] and
        CubeFace[5][0][1]==CubeFace[5][1][1]
    ):
        total_score+=1

    if (
        CubeFace[1][1][0]==CubeFace[1][1][1] and
        CubeFace[4][0][1]==CubeFace[4][1][1]
    ):
        total_score+=10


    if (
        CubeFace[1][1][2]==CubeFace[1][1][1] and
        CubeFace[3][0][1]==CubeFace[3][1][1]
    ):
        total_score+=100


    if (
        CubeFace[1][2][1]==CubeFace[1][1][1] and
        CubeFace[0][0][1]==CubeFace[0][1][1]
    ):
        total_score+=1000

    if(
        CubeFace[1][0][0]==CubeFace[1][1][1] and
        CubeFace[4][0][0]==CubeFace[4][1][1] and
        CubeFace[5][0][2]==CubeFace[5][1][1] and
        total_score>=1111
    ):
        total_score+=2

    if(
        CubeFace[1][0][2]==CubeFace[1][1][1] and
        CubeFace[3][0][2]==CubeFace[3][1][1] and
        CubeFace[5][0][0]==CubeFace[5][1][1] and
        total_score>=1111
    ):
        total_score+=20

    if(
        CubeFace[1][2][0]==CubeFace[1][1][1] and
        CubeFace[4][0][2]==CubeFace[4][1][1] and
        CubeFace[0][0][0]==CubeFace[0][1][1] and
        total_score>=1111
    ):
        total_score+=200

    if(
        CubeFace[1][2][2]==CubeFace[1][1][1] and
        CubeFace[3][0][0]==CubeFace[3][1][1] and
        CubeFace[0][0][2]==CubeFace[0][1][1] and
        total_score>=1111
    ):
        total_score+=2000

    return total_score

def OldHeuristic(CubeState):

    total_score=0
    face_score=0
    for CubeFace in CubeState.face:
        face_score=0
        check=CubeFace[0][0]
        for Row in CubeFace:
            for Col in Row:
                if Col==check:
                    face_score+=1
        if face_score==9:
            total_score+=1
    return total_score

def Solve(CubeObj):

    g=nx.Graph()
    node=0
    stack=Frontier() #initialize frontier
    stack.add( #add initial state to frontier
        Node(CubeObj,node)
        )
    g.add_node(node)
    optimal=1000
    i=0
    nodes_explored=0
    score=0
    min=0
    stage=0
    try:
        while(len(stack.frontier)!=0):
            current_node=stack.remove() #remove last node from frontier
            parent=current_node.number
            if(fd(Heuristic(current_node.state))==(stage+1)):
                stage=fd(Heuristic(current_node.state))
            if(Heuristic(current_node.state)>score and ((Heuristic(current_node.state)%10)!=0)) or ((fd(Heuristic(current_node.state))==(stage+1)) and (Heuristic(current_node.state)>score)):
                min=len(current_node.state.actions)
                score=Heuristic(current_node.state)
            while(Heuristic(current_node.state)<score):
                current_node=stack.remove() #remove last node from frontier
                parent=current_node.number
                if(fd(Heuristic(current_node.state))==(stage+1)):
                    stage=fd(Heuristic(current_node.state))
                if(Heuristic(current_node.state)>score and ((Heuristic(current_node.state)%10)!=0)) or ((fd(Heuristic(current_node.state))==(stage+1)) and (Heuristic(current_node.state)>score)):
                    min=len(current_node.state.actions)
                    score=Heuristic(current_node.state)
            os.system("cls")
            print("Nodes explored:"+ str(nodes_explored))
            print("Frontier size:"+str(len(stack.frontier)))
            print("Manhattan Distance to solution:"+str(2222-score))
            while(len(current_node.state.actions)>optimal):
                current_node=stack.remove() #if more than 25 moves have been done on the Cube state then discard this state and remove next state from frontier
                parent=current_node.number
                while(Heuristic(current_node.state)<score and len(current_node.state.actions)<=min):
                    current_node=stack.remove() #remove last node from frontier
                    parent=current_node.number
                    if(fd(Heuristic(current_node.state))==(stage+1)):
                        stage=fd(Heuristic(current_node.state))
                    if(Heuristic(current_node.state)>score and ((Heuristic(current_node.state)%10)!=0)) or ((fd(Heuristic(current_node.state))==(stage+1)) and (Heuristic(current_node.state)>score)):
                        min=len(current_node.state.actions)
                        score=Heuristic(current_node.state)
            nodes_explored+=1
            g.add_node(current_node.number)
            g.add_edge(current_node.parent,current_node.number)
            if(Heuristic(current_node.state)==2222): #if goal state has been reached, return node state
                solution=current_node.state #temporary solution
                g.add_node("S")
                g.add_edge(current_node.parent,"S")
                nx.draw(g,with_labels=True)
                plt.show()
                plt.savefig("Diagnostic.png")
                return solution
            else:
                 #add further nodes to frontier after applying actions
                if(current_node.state.LastAction()!="U`" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.U(),node,parent )
                        )


                if(current_node.state.LastAction()!="L`" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.L(),node,parent )
                        )


                if(current_node.state.LastAction()!="F`" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.F(),node,parent )
                        )


                if(current_node.state.LastAction()!="R`" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.R(),node,parent )
                        )


                if(current_node.state.LastAction()!="B`" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.B(),node,parent )
                        )


                if(current_node.state.LastAction()!="D`" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.D(),node,parent )
                        )


                if(current_node.state.LastAction()!="U" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.U_(),node,parent )
                        )


                if(current_node.state.LastAction()!="L" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.L_(),node,parent )
                        )


                if(current_node.state.LastAction()!="F" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.F_(),node,parent )
                        )


                if(current_node.state.LastAction()!="R" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.R_(),node,parent )
                        )

                if(current_node.state.LastAction()!="B" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.B_(),node,parent )
                        )


                if(current_node.state.LastAction()!="D" or len(current_node.state.actions)==0):
                    node+=1
                    stack.add(
                        Node(current_node.state.D_(),node,parent )
                        )

    except KeyboardInterrupt:
        print("Nodes explored:"+str(nodes_explored))
        print("Frontier size"+str(len(stack.frontier)))
        print("Heuristic score:"+str(Heuristic(current_node.state)))
        print(current_node.state.actions)
        print(current_node.state.face)
        print(diag)
        pause=os.system("pause")
        nx.draw(g,with_labels=True)
        plt.savefig("Diagnostic.png")
        plt.show()
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
