import tkinter as tk
from array import *
import numpy
import copy
from notation_functions import Cube
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

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
            node=self.frontier[-1] #nodes removed using stack method, i.e. first in last out
            self.frontier=self.frontier[:-1]
            return node

    def queue_remove(self):

        if len(self.frontier)==0: #frontier empty so all nodes explored therefore no solution
            raise Exception("No Solution")
        else:
            node=self.frontier[0] #nodes removed using stack method, i.e. first in last out
            self.frontier=self.frontier[1:]
            return node

    def flush(self):

        self.backup=copy.deepcopy(self.frontier)

        self.frontier=[]

    def restore(self):

        self.frontier=self.backup

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
        if current_string not in dict2:
            formatted[i] = current_string
        if current_string in dict2:
            formatted[i] = dict2[current_string]
            formatted.insert(i+1,dict2[current_string])
            count += 1
        i += 1

    print(formatted)
    return formatted

def scramble(moves, c):

    stack1=[]

    stack1.append(copy.deepcopy(c))

    for m in moves:

        cur=stack1.pop(0)

        if(len(stack1)>1):

            raise Exception("STLN")

        if(m=="U"):

            stack1.append(cur.U())

        elif(m=="L"):

            stack1.append(cur.L())

        elif(m=="F"):

            stack1.append(cur.F())

        elif(m=="R"):

            stack1.append(cur.R())

        elif(m=="B"):

            stack1.append(cur.B())

        elif(m=="D"):

            stack1.append(cur.D())

        elif(m=="U'"):

            stack1.append(cur.U_())

        elif(m=="L'"):

            stack1.append(cur.L_())

        elif(m=="F'"):

            stack1.append(cur.F_())

        elif(m=="R'"):

            stack1.append(cur.R_())

        elif(m=="B'"):

            stack1.append(cur.B_())

        elif(m=="D'"):

            stack1.append(cur.D_())

        else:

            print(m)

            raise Exception("X")

    cur=stack1.pop(0)

    return cur

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
        CubeFace[5][1][2]==CubeFace[5][1][1] and
        CubeFace[4][1][0]==CubeFace[4][1][1] and
        total_score>=1111
    ):
        total_score+=2

    if(
        CubeFace[1][0][2]==CubeFace[1][1][1] and
        CubeFace[3][0][2]==CubeFace[3][1][1] and
        CubeFace[5][0][0]==CubeFace[5][1][1] and
        CubeFace[5][1][0]==CubeFace[5][1][1] and
        CubeFace[3][1][2]==CubeFace[3][1][1] and
        total_score>=1111
    ):
        total_score+=20

    if(
        CubeFace[1][2][0]==CubeFace[1][1][1] and
        CubeFace[4][0][2]==CubeFace[4][1][1] and
        CubeFace[0][0][0]==CubeFace[0][1][1] and
        CubeFace[0][1][0]==CubeFace[0][1][1] and
        CubeFace[4][1][2]==CubeFace[4][1][1] and
        total_score>=1111
    ):
        total_score+=200

    if(
        CubeFace[1][2][2]==CubeFace[1][1][1] and
        CubeFace[3][0][0]==CubeFace[3][1][1] and
        CubeFace[0][0][2]==CubeFace[0][1][1] and
        CubeFace[0][1][2]==CubeFace[0][1][1] and
        CubeFace[3][1][0]==CubeFace[3][1][1] and
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

def CheckCross(CubeState):
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

    return total_score

stack=Frontier()

def Solve(CubeObj):
    g=nx.DiGraph()
    node=0
    stack=Frontier() #initialize frontier
    stack.add( #add initial state to frontier
        Node(CubeObj,node)
        )
    g.add_node(node)
    cnd=True
    nodes_explored=0
    score=0
    try:
        while cnd:
            os.system("cls")
            print("Nodes explored:"+ str(nodes_explored))
            print("Frontier size:"+str(len(stack.frontier)))
            print("Heuristic Stage:"+str(score))
            current_node=stack.queue_remove()
            parent=current_node.number
            try:
                while(len(current_node.state.actions)>52):
                    current_node=stack.queue_remove()
                    parent=current_node.number
            except:
                score=0
                stack.restore()
            g.add_node(current_node.number)
            g.add_edge(current_node.parent,current_node.number)
            nodes_explored+=1
            if(Heuristic(current_node.state)>1111):
                cnd=False
            elif(Heuristic(current_node.state)>score):
                score=Heuristic(current_node.state)
                stack.flush()
                stack.add(current_node)
            else:
                 #add further nodes to frontier after applying actions
                if(current_node.state.LastAction()!="U`" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="U":
                    node+=1
                    stack.add(
                        Node(current_node.state.U(),node,parent )
                        )


                if(current_node.state.LastAction()!="L`" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="L":
                    node+=1
                    stack.add(
                        Node(current_node.state.L(),node,parent )
                        )


                if(current_node.state.LastAction()!="F`" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="F":
                    node+=1
                    stack.add(
                        Node(current_node.state.F(),node,parent )
                        )


                if(current_node.state.LastAction()!="R`" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="R":
                    node+=1
                    stack.add(
                        Node(current_node.state.R(),node,parent )
                        )


                if(current_node.state.LastAction()!="B`" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="B":
                    node+=1
                    stack.add(
                        Node(current_node.state.B(),node,parent )
                        )


                if(current_node.state.LastAction()!="D`" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="D":
                    node+=1
                    stack.add(
                        Node(current_node.state.D(),node,parent )
                        )


                if(current_node.state.LastAction()!="U" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="U`":
                    node+=1
                    stack.add(
                        Node(current_node.state.U_(),node,parent )
                        )


                if(current_node.state.LastAction()!="L" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="L`":
                    node+=1
                    stack.add(
                        Node(current_node.state.L_(),node,parent )
                        )


                if(current_node.state.LastAction()!="F" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="F`":
                    node+=1
                    stack.add(
                        Node(current_node.state.F_(),node,parent )
                        )


                if(current_node.state.LastAction()!="R" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="R`":
                    node+=1
                    stack.add(
                        Node(current_node.state.R_(),node,parent )
                        )

                if(current_node.state.LastAction()!="B" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="B`":
                    node+=1
                    stack.add(
                        Node(current_node.state.B_(),node,parent )
                        )


                if(current_node.state.LastAction()!="D" or len(current_node.state.actions)==0) and current_node.state.LastThree()!="D`":
                    node+=1
                    stack.add(
                        Node(current_node.state.D_(),node,parent )
                        )
        solution=current_node.state #temporary solution
        g.add_node("S")
        g.add_edge(current_node.parent,"S")
        #write_dot(g,'test.dot')
        #pos =graphviz_layout(g, prog='dot')
        nx.draw_planar(g,with_labels=True,arrows=True)
        plt.show()
        plt.savefig("Diagnostic.png")
        return solution

    except KeyboardInterrupt:
        print("Nodes explored:"+str(nodes_explored))
        print("Frontier size"+str(len(stack.frontier)))
        print("Heuristic score:"+str(Heuristic(current_node.state)))
        print(current_node.state.actions)
        print(current_node.state.face)
        print(diag)
        pause=os.system("pause")
        nx.draw_planar(g,with_labels=True)
        plt.savefig("Diagnostic.png")
        plt.show()
    return solution #optimal solution after all nodes explored

initc=Cube()

mov=format("D L' F L2 B' D' B R' U D R L' B2 F' U R U D' R D' R2 L' B' R' F2")

initc.face=[[['green', 'green', 'green'],
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

initc=scramble(mov,initc)

print(initc.actions)

print(initc.face)

os.system("pause")

initc.actions=[]

S=Solve(initc)
print("Actions required to solve:")
for a in S.actions:
    print(a)
a=input("press any key to continue")
