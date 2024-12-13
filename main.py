#Vector 3D - An interactive python-based web app for mapping vectors - By SirNooby and Zakichan (Sirzak)
from vpython import *
from math import * #Delete this if using Web VPython

#Create scene and regulatory conditions
scene = canvas(width=1200, height=425, background=color.white, resizable=True, title="Vector3D - A Vector Mapping Tool (V1.0)                        Created by <a href='https://github.com/Sir-Nooby' target='_blank'>SirNooby</a> and <a href='https://github.com/ZakichanMC' target='_blank'>Zakichan</a>                                   Need Help? <a href='https://github.com/Sir-Nooby/vector3' target='_blank'> Read the Vector3D Documentation</a>") #Chamge the height if using Web VPython (475)
scene.ambient = color.white * 0.8

global mouse
mouse = scene.mouse
distance = 5

plane_normal = vec(0, 1, 0)  
plane_distance = 0      

mode = "draw"
modes = ["Draw", "Vector"]

tick_marks = False
user_arrow = None
vectorX, vectorY, vectorZ = None, None, None
originX, originY, originZ, endX, endY, endZ, start_from_origin = None, None, None, None, None, None, None
boxes_list, show_boxes = [], False

cursor_marker = label(pos=vec(0,0,0), text="", visible=False)

#Set up the inital camera
scene.up = vec(0, 0, 1) 
scene.camera.pos = vec(distance+1, distance+1, distance+1)
scene.camera.axis = vec(-distance-1, -distance-1, -distance-1)


#Create the 3D Scene and Geometry
s = sphere(radius=0.05, color=color.white)

#Generate the cartesian axes
x_axis = arrow(pos=vec(0,0,0), axis=vec(distance, 0, 0), color=color.red, round=True, shaftwidth=0.05)
y_axis = arrow(pos=vec(0,0,0), axis=vec(0, distance, 0), color=color.green, round=True, shaftwidth=0.05)
z_axis = arrow(pos=vec(0,0,0), axis=vec(0, 0, distance), color=color.blue, round=True, shaftwidth=0.05)

#Generate the inverted cartesian axes
x_inv_axis = arrow(pos=vec(0,0,0), axis=vec(-distance, 0, 0), color=color.red, round=True, shaftwidth=0.05)
y_inv_axis = arrow(pos=vec(0,0,0), axis=vec(0, -distance, 0), color=color.green, round=True, shaftwidth=0.05)
z_inv_axis = arrow(pos=vec(0,0,0), axis=vec(0, 0, -distance), color=color.blue, round=True, shaftwidth=0.05)

#Generate Hidden Elements (Length, Width, Height)
xy_plane = box(size=vec(distance*2, distance*2, 0.15), color=color.red, opacity=0.3, visible=False)
xz_plane = box(size=vec(distance*2, 0.15, distance*2), color=color.blue, opacity=0.3, visible=False)
yz_plane = box(size=vec(0.15, distance*2, distance*2), color=color.green, opacity=0.3, visible=False)

tick_marksx = [label(pos=vec(i, 0, 0), text="|", height=24, box=False, opacity=0, visible=False) for i in range(1, distance)]
tick_marksy = [label(pos=vec(0, i, 0), text="|", height=24, box=False, opacity=0, visible=False) for i in range(1, distance)]
tick_marksz = [label(pos=vec(0, 0, i), text="―", height=24, box=False, opacity=0, visible=False) for i in range(1, distance)]

tick_marksinv_x = [label(pos=vec(-i, 0, 0), text="|", height=24, box=False, opacity=0, visible=False) for i in range(1, distance)]
tick_marksinv_y = [label(pos=vec(0, -i, 0), text="|", height=24, box=False, opacity=0, visible=False) for i in range(1, distance)]
tick_marksinv_z = [label(pos=vec(0, 0, -i), text="―", height=24, box=False, opacity=0, visible=False) for i in range(1, distance)]


#Define vector draw function
def vector_draw():
    global start_position, user_arrow, user_box
    start_position = mouse.pos
    user_arrow = arrow(pos=vec(start_position), axis=vec(0,0,0), color=color.purple, round=True, shaftwidth=0.05)
    user_box = box(pos=user_arrow.pos + (user_arrow.axis / 2), size=user_arrow.axis, color=color.cyan, opacity=0.25, visible=True)
    if not show_boxes:
        user_box.visible = False
    boxes_list.append(user_box)


#Define vector simulating function
def vector_simulate():
    current_positon = mouse.pos
    if current_positon: #The below code is a process to detect if drawn vectors are approraching the edge of the screen
        # if abs(current_positon.x) > (draw_range * 2.25) or abs(current_positon.y * 1.1) > (draw_range) or (current_positon.z) > (draw_range * 2):
        #     user_arrow.color = color.red
        #     scene.waitfor("mousemove")
        #     user_arrow.visible = False
        # else:
            user_arrow.axis = current_positon - user_arrow.pos
            user_box.pos = user_arrow.pos + (user_arrow.axis / 2)
            user_box.size = user_arrow.axis


def origin_switch(event):
    global start_from_origin, originX, originY, originZ, endX, endY, endZ, clearButton
    if event.checked:
        start_from_origin = True
        if None not in {originX, originY, originZ, endX, endY, endZ}:
            for i in [originX, originY, originZ, endX, endY, endZ, clearButton]:
                i.delete()
        vector_create()
    else:
        start_from_origin = False
        if None not in {originX, originY, originZ, endX, endY, endZ}:
            for i in [originX, originY, originZ, endX, endY, endZ, clearButton]:
                i.delete()
        vector_create()


def toggle_boxes(event):
    global show_boxes
    if event.checked:
        show_boxes = True
        if len(boxes_list) > 0:
            for i in boxes_list:
                i.visible = True
    else:
        show_boxes = False
        if len(boxes_list) > 0:
            for i in boxes_list:
                i.visible = False


def doNothing():
    pass


def vector_create():
    global originX, originY, originZ, endX, endY, endZ, clearButton, start_from_origin
    if not start_from_origin:
        originX = winput(prompt='Start X:', bind=doNothing, type='numeric')
        originY = winput(prompt='Start Y:', bind=doNothing, type='numeric')
        originZ = winput(prompt='Start Z:', bind=doNothing, type='numeric')
    endX = winput(prompt='\nEnd X:', bind=doNothing, type='numeric')
    endY = winput(prompt='End Y:', bind=doNothing, type='numeric')
    endZ = winput(prompt='End Z:', bind=doNothing, type='numeric')
    clearButton = button(bind=vector_clear, text='Go!')


def vector_clear():
    global drawnVector, start_from_origin, drawnBox
    if not start_from_origin:
        if '' not in {originX.text, originY.text, originZ.text,}:
            drawnVector = arrow(pos=vec(float(originX.text), float(originY.text), float(originZ.text)), axis=vec(float(endX.text) - float(originX.text), float(endY.text) - float(originY.text), float(endZ.text) - float(originZ.text)), color=color.purple, round=True, shaftwidth=0.05)
            drawnBox = box(pos=drawnVector.pos + (drawnVector.axis / 2), size=drawnVector.axis, color=color.cyan, opacity=0.25)
            if not show_boxes:
                drawnBox.visible = False
            boxes_list.append(drawnBox)
        else:
            print("Please enter 3 origin values.")
    else:
        if '' not in {endX.text, endY.text, endZ.text,}:
            drawnVector = arrow(pos=vec(0,0,0), axis=vec(float(endX.text), float(endY.text), float(endZ.text)), color=color.purple, round=True, shaftwidth=0.05)
            drawnBox = box(pos=drawnVector.pos + (drawnVector.axis / 2), size=drawnVector.axis, color=color.cyan, opacity=0.25)
            if not show_boxes:
                drawnBox.visible = False
            boxes_list.append(drawnBox)
        else:
            print("Please enter 3 end values.")
    
    if None not in {originX, originY, originZ, endX, endY, endZ}:
        for i in [originX, originY, originZ, endX, endY, endZ, clearButton]:
            i.delete()
    vector_create()
    

#Create any user input functions
def mode_changer(event): #Detects any mode changes and adjusts keybindings
    global mode, origin_checker
    scene.unbind("mousedown", vector_draw)
    scene.unbind("mousemove", vector_simulate)

    if event.index == 0:
        mode = "draw"
        scene.bind("mousedown", vector_draw)
        scene.bind("mousemove", vector_simulate)
        if None not in {originX, originY, originZ, endX, endY, endZ}:
            for i in [originX, originY, originZ, endX, endY, endZ, clearButton, origin_checker]:
                i.delete()


    if event.index == 1:
        mode = "vector"
        origin_checker = checkbox(bind=origin_switch, text="Start from Origin\n")
        scene.unbind("mousedown", vector_draw)
        scene.unbind("mousemove", vector_simulate)
        vector_create()


#Show the axis planes
def show_axisplanes(event):
    xy_plane.visible = xz_plane.visible = yz_plane.visible = event.checked


#Create the inverted axes
def show_invertedaxes(event):
    x_inv_axis.visible = y_inv_axis.visible = z_inv_axis.visible = event.checked

    if event.checked and tick_marks == True:
        for i in range(distance-1):
            tick_marksinv_x[i].visible = tick_marksinv_y[i].visible = tick_marksinv_z[i].visible = True
    else:
        for i in range(distance-1):
            tick_marksinv_x[i].visible = tick_marksinv_y[i].visible = tick_marksinv_z[i].visible = False


#Create the tick marks system
def show_tickmarks(event):
    global tick_marks
    if event.checked:
        tick_marks = True
        for i in range(distance-1):
            tick_marksx[i].visible = tick_marksy[i].visible = tick_marksz[i].visible = True
            if x_inv_axis.visible == True:
                tick_marksinv_x[i].visible = tick_marksinv_y[i].visible = tick_marksinv_z[i].visible = True
    else:
        tick_marks = False
        for i in range(distance-1):
            tick_marksx[i].visible = tick_marksy[i].visible = tick_marksz[i].visible = False
            tick_marksinv_x[i].visible = tick_marksinv_y[i].visible = tick_marksinv_z[i].visible = False


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

        if mouse.pick == x_inv_axis:
            cursor_marker.visible = True
            cursor_marker.text = "-X-Axis!"
            cursor_marker.pos = mouse.pos
        
        if mouse.pick == y_inv_axis:
            cursor_marker.visible = True
            cursor_marker.text = "-Y-Axis!"
            cursor_marker.pos = mouse.pos
        
        if mouse.pick == z_inv_axis:
            cursor_marker.visible = True
            cursor_marker.text = "-Z-Axis!"
            cursor_marker.pos = mouse.pos

        if isinstance(mouse.pick, arrow) and mouse.pick not in {x_axis, y_axis, z_axis, x_inv_axis, y_inv_axis, z_inv_axis}:
            current_object = mouse.pick
            if current_object:
                local_magnitude = current_object.axis.mag
                local_start = round(current_object.pos.x, 2), round(current_object.pos.y, 2), round(current_object.pos.z, 2)
                local_end = round(current_object.axis.x, 2), round(current_object.axis.y, 2), round(current_object.axis.z, 2)
                local_alpha = round(degrees(acos(float(current_object.axis.x)/float(local_magnitude))), 2)
                local_beta = round(degrees(acos(float(current_object.axis.y)/float(local_magnitude))), 2)
                local_gamma = round(degrees(acos(float(current_object.axis.z)/float(local_magnitude))), 2)
                cursor_marker.text = "Generated Vector\nMagnitude: " + str(round(local_magnitude, 3)) + "\nFrom " + str(local_start) + "\nTo " + str(local_end) + "\nα=" + str(local_alpha) + "\nß=" + str(local_beta) + "\nΓ=" + str(local_gamma)
                cursor_marker.visible = True
                cursor_marker.pos = mouse.pos
    else:
        cursor_marker.visible = False


#Create UI/UX  objects
scene.append_to_caption("Mode: ")
menu(bind=mode_changer, choices=modes, selected="Current", index=0)
scene.append_to_caption("   ") #Filler Line, adding two whitespace for spacing
inverted_checker = checkbox(bind=show_invertedaxes, text="Show Inverted Axes  ", checked=True)
tick_checker =checkbox(bind=show_tickmarks, text="Show Tick Marks   ", checked=False)
axis_checker = checkbox(bind=show_axisplanes, text="Show Axis Planes  ", checked=False)
box_checker = checkbox(bind=toggle_boxes, text="Show Box Guides  ", checked=False)
scene.append_to_caption("\n\n")

#Intialize the scene loop
scene.bind("mousedown", vector_draw)
scene.bind("mousemove", vector_simulate)


while True:
    cursor_checker(cursor_marker)
    draw_range = scene.range
    rate(20)
