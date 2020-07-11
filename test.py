from notation_functions import Cube


c= Cube()


c.face=[[['white', 'green', 'green'],
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




Cube.R_(c)
array = Cube.GetAllFaces(c)
print(array)
