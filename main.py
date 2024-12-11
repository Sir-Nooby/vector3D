#Vector 3D - An interactive python-based web app for mapping vectors
from vpython import *

#Create scene and regulatory conditions
scene = canvas(width=1200, height=500, background=color.white, resizable=False, title="Vector3 - A Vector Mapping Tool")

scene.ambient = color.white * 0.8

distance = 5

mode = "draw"
modes = ["Choose a mode:", "Draw", "Vector"]

#Create horizonal surface for vectors to rest off
plane_normal = vec(0, 1, 0)  
plane_distance = 0           

global mouse
mouse = scene.mouse

scene.up = vec(0, 0, 1)
scene.camera.pos = vec(0, -distance, distance)
scene.camera.axis = vec(0, distance, -distance)


#Create the 3D Scene

s = sphere(radius=0.05, color=color.white)

#Generate the cartesian axises
x_axis = arrow(pos=vec(0,0,0), axis=vec(distance, 0, 0), color=color.red, round=True, shaftwidth=0.05)
y_axis = arrow(pos=vec(0,0,0), axis=vec(0, distance, 0), color=color.green, round=True, shaftwidth=0.05)
z_axis = arrow(pos=vec(0,0,0), axis=vec(0, 0, distance), color=color.blue, round=True, shaftwidth=0.05)

#Generate the inverted cartesian axises
x_inv_axis = arrow(pos=vec(0,0,0), axis=vec(-distance, 0, 0), color=color.red, round=True, shaftwidth=0.05)
y_inv_axis = arrow(pos=vec(0,0,0), axis=vec(0, -distance, 0), color=color.green, round=True, shaftwidth=0.05)
z_inv_axis = arrow(pos=vec(0,0,0), axis=vec(0, 0, -distance), color=color.blue, round=True, shaftwidth=0.05)


#Just to fix NameError lol #ZakichanWasHere
originX, originY, originZ, endX, endY, endZ, start_from_origin = None, None, None, None, None, None, None

#Define vector draw function
def vector_draw():
    global start_position, user_arrow
    start_position = mouse.pos
    user_arrow = arrow(pos=vec(start_position), axis=vec(0,0,0), color=color.purple, round=True, shaftwidth=0.05)

#Define vector simulating function
def vector_simulate():
    current_positon = mouse.pos
    print(current_positon.x, draw_range, current_positon.y, current_positon.z)
    if current_positon:
        # if abs(current_positon.x) > (draw_range * 2.25) or abs(current_positon.y * 1.1) > (draw_range) or (current_positon.z) > (draw_range * 2):
        #     user_arrow.color = color.red
        #     scene.waitfor("mousemove")
        #     user_arrow.visible = False
        # else:
            user_arrow.axis = current_positon - user_arrow.pos

#ZakichanWasHere
def origin_switch(event):  # WORKS
    global start_from_origin, originX, originY, originZ, endX, endY, endZ, clearButton
    if event.checked:
        start_from_origin = True
        if originX is not None and originY is not None and originZ is not None and endX is not None and endY is not None and endZ is not None:
            originX.delete()
            originY.delete()
            originZ.delete()
            endX.delete()
            endY.delete()
            endZ.delete()
            clearButton.delete()
        vector_create()
        

    else:
        start_from_origin = False
        if originX is not None and originY is not None and originZ is not None and endX is not None and endY is not None and endZ is not None:
            originX.delete()
            originY.delete()
            originZ.delete()
            endX.delete()
            endY.delete()
            endZ.delete()
            clearButton.delete()
        vector_create()
        
def doNothing():
    pass
#ZakichanWasHere
def vector_create(): #DOESNT WORK
    global originX, originY, originZ, endX, endY, endZ, clearButton, start_from_origin

    if not start_from_origin:
        originX = winput(prompt='Start X:', bind=doNothing, type='numeric')
        originY = winput(prompt='Start Y:', bind=doNothing, type='numeric')
        originZ = winput(prompt='Start Z:', bind=doNothing, type='numeric')
    endX = winput(prompt='End X:', bind=doNothing, type='numeric')
    endY = winput(prompt='End Y:', bind=doNothing, type='numeric')
    endZ = winput(prompt='End Z:', bind=doNothing, type='numeric')
    clearButton = button(bind=vector_clear, text='Go!')

#ZakichanWasHere
def vector_clear(): #DOESNT WORK
    global drawnVector, start_from_origin
    if not start_from_origin:
        if originX.text != '' and originY.text != '' and originZ.text != '':
            drawnVector = arrow(pos=vec(float(originX.text), float(originY.text), float(originZ.text)), axis=vec(float(endX.text) - float(originX.text), float(endY.text) - float(originY.text), float(endZ.text) - float(originZ.text)), color=color.purple, round=True, shaftwidth=0.05)
        else:
            print("Please enter 3 origin values.")
    else:
        if endX.text != '' and endY.text != '' and endZ.text != '':
            drawnVector = arrow(pos=vec(0,0,0), axis=vec(float(endX.text), float(endY.text), float(endZ.text)), color=color.purple, round=True, shaftwidth=0.05)
        else:
            print("Please enter 3 end values.")
    
    
    if originX is not None and originY is not None and originZ is not None and endX is not None and endY is not None and endZ is not None:
        originX.delete()
        originY.delete()
        originZ.delete()
        endX.delete()
        endY.delete()
        endZ.delete()
        clearButton.delete()
    vector_create()
    
    

#Create any userinput functions
def mode_changer(event): #Detects any mode changes and adjusts keybindings ###SHOULD WORK
    global mode, origin_checker
    scene.unbind("mousedown", vector_draw)
    scene.unbind("mousemove", vector_simulate)

    if event.index == 0 or event.index == 1:
        mode = "draw"
        scene.bind("mousedown", vector_draw)
        scene.bind("mousemove", vector_simulate)
        if originX is not None and originY is not None and originZ is not None and endX is not None and endY is not None and endZ is not None: #ZakichanWasHere
            originX.delete()
            originY.delete()
            originZ.delete()
            endX.delete()
            endY.delete()
            endZ.delete()
            origin_checker.delete()
            clearButton.delete()

        print("Draw Mode Set!")


    if event.index == 2:
        mode = "vector"
        origin_checker = checkbox(bind=origin_switch, text="Start from Origin")
        print("Vector Mode Set!")
        vector_create()
        

        scene.unbind("mousedown", vector_draw)
        scene.unbind("mousemove", vector_simulate)

    

def show_invertedaxes(event):
    if event.checked:
        x_inv_axis.visible = True
        y_inv_axis.visible = True
        z_inv_axis.visible = True
    else:
        x_inv_axis.visible = False
        y_inv_axis.visible = False
        z_inv_axis.visible = False

    
menu(bind=mode_changer, choices=modes, selected="Current", index=0)
checkbox(bind=show_invertedaxes, text="Show inverted axes", checked=True)
origin_checker = checkbox(bind=origin_switch, text="Start from Origin", checked=False)
origin_checker.delete()
scene.append_to_caption('\n\n') 

#Intialize the scene loop
print("Welcome to Vector3D")
scene.bind("mousedown", vector_draw)
scene.bind("mousemove", vector_simulate)



while True:
    draw_range = scene.range
    rate(5)
