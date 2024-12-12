#Vector 3D - An interactive python-based web app for mapping vectors
from vpython import *
from math import *

#Create scene and regulatory conditions
scene = canvas(width=1200, height=500, background=color.white, resizable=False, title="Vector3 - A Vector Mapping Tool")
scene.ambient = color.white * 0.8

global mouse
mouse = scene.mouse
distance = 5

plane_normal = vec(0, 1, 0)  
plane_distance = 0      

mode = "draw"
modes = ["Choose a mode:", "Draw", "Vector"]

user_arrow = None
vectorX, vectorY, vectorZ = None, None, None
cursor_marker = label(pos=vec(0,0,0), text="", visible=False)

scene.up = vec(0, 0, 1)
scene.camera.pos = vec(0, -distance, distance)
scene.camera.axis = vec(0, distance, -distance)


#Create the 3D Scene

s = sphere(radius=0.05, color=color.white)

#Generate the cartesian axes
x_axis = arrow(pos=vec(0,0,0), axis=vec(distance, 0, 0), color=color.red, round=True, shaftwidth=0.05)
y_axis = arrow(pos=vec(0,0,0), axis=vec(0, distance, 0), color=color.green, round=True, shaftwidth=0.05)
z_axis = arrow(pos=vec(0,0,0), axis=vec(0, 0, distance), color=color.blue, round=True, shaftwidth=0.05)

#Generate the inverted cartesian axes
x_inv_axis = arrow(pos=vec(0,0,0), axis=vec(-distance, 0, 0), color=color.red, round=True, shaftwidth=0.05)
y_inv_axis = arrow(pos=vec(0,0,0), axis=vec(0, -distance, 0), color=color.green, round=True, shaftwidth=0.05)
z_inv_axis = arrow(pos=vec(0,0,0), axis=vec(0, 0, -distance), color=color.blue, round=True, shaftwidth=0.05)

#Define vector draw function
def vector_draw():
    global start_position, user_arrow
    start_position = mouse.pos
    user_arrow = arrow(pos=vec(start_position), axis=vec(0,0,0), color=color.purple, round=True, shaftwidth=0.05)

#Define vector simulating function
def vector_simulate():
    current_positon = mouse.pos
    print(current_positon.x, draw_range, current_positon.y, current_positon.z)
    if current_positon: #The below code is a process to detect if drawn vectors are approraching the edge of the screen
        # if abs(current_positon.x) > (draw_range * 2.25) or abs(current_positon.y * 1.1) > (draw_range) or (current_positon.z) > (draw_range * 2):
        #     user_arrow.color = color.red
        #     scene.waitfor("mousemove")
        #     user_arrow.visible = False
        # else:
            user_arrow.axis = current_positon - user_arrow.pos

#ZakichanWasHere
def vector_create():
    global vectorX, vectorY, vectorZ, clearButton

    vectorX = winput(prompt='X:', bind=lambda: None, type='numeric')
    vectorY = winput(prompt='Y:', bind=lambda: None, type='numeric')
    vectorZ = winput(prompt='Z:', bind=lambda: None, type='numeric')
    clearButton = button(bind=vector_clear, text='Go!')

#ZakichanWasHere
def vector_clear():
    global drawnVector
    if vectorX.text != '' and vectorY.text != '' and vectorZ.text != '':
        drawnVector = arrow(pos=vec(0,0,0), axis=vec(float(vectorX.text), float(vectorY.text), float(vectorZ.text)), color=color.purple, round=True, shaftwidth=0.05)
        vectorX.delete()
        vectorY.delete()
        vectorZ.delete()
        clearButton.delete()
        vector_create()
    else:
        print("Please enter a value for all vectors.")
    


#Create any userinput functions
def mode_changer(event): #Detects any mode changes and adjusts keybindings
    global mode
    scene.unbind("mousedown", vector_draw)
    scene.unbind("mousemove", vector_simulate)

    if event.index == 0 or event.index == 1:
        mode = "draw"

        scene.bind("mousedown", vector_draw)
        scene.bind("mousemove", vector_simulate)
        if vectorX is not None and vectorY is not None and vectorZ is not None: #ZakichanWasHere
            vectorX.delete()
            vectorY.delete()
            vectorZ.delete()
            clearButton.delete()

        print("Draw Mode Set!")


    if event.index == 2:
        mode = "vector"

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


#Define the cursor scanning system
def cursor_checker(cursor_marker):
    if mouse.pick:
        if mouse.pick == x_axis:
            cursor_marker.visible = True
            cursor_marker.text = "X-Axis!"
            cursor_marker.pos = mouse.pos

        if mouse.pick == y_axis:
            cursor_marker.visible = True
            cursor_marker.text = "Y-Axis!"
            cursor_marker.pos = mouse.pos
        
        if mouse.pick == z_axis:
            cursor_marker.visible = True
            cursor_marker.text = "Z-Axis!"
            cursor_marker.pos = mouse.pos

        if isinstance(mouse.pick, arrow) and mouse.pick != x_axis and mouse.pick != y_axis and mouse.pick != z_axis:
            current_object = mouse.pick
            if current_object:
                local_magnitude = current_object.axis.mag
                local_start = round(current_object.pos.x, 2), round(current_object.pos.y, 2), round(current_object.pos.z, 2),
                local_end = round(current_object.axis.x, 2), round(current_object.axis.x, 2), round(current_object.axis.x, 2)
                local_alpha = round(degrees(acos(float(current_object.axis.x)/float(local_magnitude))), 2)
                local_beta = round(degrees(acos(float(current_object.axis.y)/float(local_magnitude))), 2)
                local_gamma = round(degrees(acos(float(current_object.axis.z)/float(local_magnitude))), 2)
                cursor_marker.text = "Generated Vector\nMagnitude: " + str(round(local_magnitude, 3)) + "\nFrom " + str(local_start) + "\nTo " + str(local_end) + "\nα=" + str(local_alpha) + "\nß=" + str(local_beta) + "\nΓ=" + str(local_gamma)
                cursor_marker.visible = True
                cursor_marker.pos = mouse.pos
    else:
        cursor_marker.visible = False
     
#Create user objects
menu(bind=mode_changer, choices=modes, selected="Current", index=0)
checkbox(bind=show_invertedaxes, text="Show inverted axes", checked="False")
scene.append_to_caption('\n\n')

#Intialize the scene loop
print("Welcome to Vector3D")
scene.bind("mousedown", vector_draw)
scene.bind("mousemove", vector_simulate)


while True:
    cursor_checker(cursor_marker)
    draw_range = scene.range
    rate(15)
