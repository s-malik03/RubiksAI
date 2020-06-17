import tkinter as tk
from array import *
import numpy

class OptionMenu(tk.Frame): 

    def __init__(self, coordinates, master, status, *options):

        super().__init__(master) 

        self.status = tk.StringVar()
        self.status.set(status)
        self.dropdown = tk.OptionMenu(self, self.status, *options)
        self.dropdown.pack()
        self.coordinates=coordinates

    def getval(self):

        return self.status.get()

        
class Cube():

    def __init__(self):

        self.face=numpy.full((6,3,3,),"##############")

        self.mappings={

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

        self.actions=[]

    def WriteToFace(self,facenum,row,column,value):

        self.face[facenum][row][column]=value

    def GetValue(self,fnum,row,column):

        return self.face[fnum][row][column]

    def GetFace(self,num):

        return self.face[num]

    def GetAllFaces(self):

        return self.face

    def ClockWise(self,facenumber):

        f=numpy.full((3,3),"#############")

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

        return f

    def U(self):

        newface=numpy.full((6,3,3,),"##############")

        newface[0][0]=self.face[3][0]

        newface[4][0]=self.face[0][0]

        newface[5][0]=self.face[4][0]

        newface[3][0]=self.face[5][0]

        newface[1]=self.ClockWise(1)

        self.face=newface

        self.actions.append("U")


def GetInput(CubeObject):

    faces=[None]*6

    FaceArray=[[["","",""],["","",""],["","",""]]]*6

    for fn in range(0,6):

        Window=tk.Tk()

        Window.title("Face "+str(fn))

        color=[OptionMenu((0,0),Window,"white","white","yellow","orange","red","blue","green")]*9

        i=0

        for r in range(3):

            for c in range(3):

                color[i]=OptionMenu((r,c),Window,"white","white","yellow","orange","red","blue","green")

                color[i].grid(row=r,column=c)

                i=i+1

        button = tk.Button(text = "Submit", command = lambda: Window.destroy())

        button.grid(row=4,column=1)

        Window.mainloop()

        faces[fn]=color

    for f in range(0,6):

        count=0

        for x in range(0,3):

            for y in range(0,3):

                CubeObject.WriteToFace(f,x,y,faces[f][count].getval())

                count=count+1

    return CubeObject


c=Cube()

c=GetInput(c)

for x in range(0,6):

    print(c.GetFace(x))

print(c.ClockWise(0))




        
