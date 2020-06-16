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

    def WriteToFace(self,facenum,row,column,value):

        self.face[facenum][row][column]=value

    def GetValue(self,fnum,row,column):

        return self.face[fnum][row][column]

    def GetFace(self,num):

        return self.face[num]

    def GetAllFaces(self):

        return self.face


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




        
