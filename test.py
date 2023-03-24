import pydirectinput

# Press and hold Ctrl+Shift+Z
pydirectinput.keyDown('ctrl')
pydirectinput.keyDown('shift')
pydirectinput.keyDown('z')

# Move mouse pointer down 5 times
for i in range(5):
    pydirectinput.moveRel(0, 50)

# Release all keys
pydirectinput.keyUp('ctrl')
pydirectinput.keyUp('shift')
pydirectinput.keyUp('z')