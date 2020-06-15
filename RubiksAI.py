import tkinter as tk
from array import *

class OptionMenu(tk.Frame): 

    def __init__(self, master, status, *options):

        super().__init__(master) 

        self.status = tk.StringVar()
        self.status.set(status)
        self.dropdown = tk.OptionMenu(self, self.status, *options)
        self.dropdown.pack()

    def getval(self):

        return self.status.get()

        
class Cube():

    def __init__(self):

        self.face=[[["","",""],["","",""],["","",""]]]*6

    def WriteToFace(self,facenum,row,column,value):

        self.face[facenum][row][column]=value

    def GetValue(self,fnum,row,column):

        return self.face[fnum][row][column]

    def GetFace(self,num):

        return self.face[num]


def GetInput(CubeObject):

    faces=[None]*6

    for fn in range(0,6):

        Window=tk.Tk()

        Window.title("Face "+str(fn))

        color=[OptionMenu(Window,"white","white","yellow","orange","red","blue","green")]*9

        i=0

        for r in range(3):

            for c in range(3):

                color[i]=OptionMenu(Window,"white","white","yellow","orange","red","blue","green")

                color[i].grid(row=r,column=c)

                i=i+1

        button = tk.Button(text = "Submit", command = lambda: Window.destroy())

        button.grid(row=4,column=1)

        Window.mainloop()

        faces[fn]=color

    count=0

    for fn in range(0,6):

        count=0

        for r in range(0,3):

            for c in range(0,3):

                CubeObject.WriteToFace(fn,r,c,faces[fn][count].getval())

                count=count+1

    return CubeObject


c=Cube()

c=GetInput(c)




        
