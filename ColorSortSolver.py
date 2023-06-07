##imports
import math
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *


#making the function call once and then have the data at the ready
map_data_persistent = []
map_data_num_dic = {
    "Flask": 0,
    "flask": 0,
    "Flasks": 0,
    "flasks": 0,
    "Ball": 1,
    "ball": 1,
    "Balls": 1,
    "balls": 1
    }
def map_data(value):

    if type(value) != str:
        raise TypeError("value must be a string")
        
    #Get the correct index of the list
    if value in map_data_num_dic:
        index = map_data_num_dic[value]
    else:
        raise ValueError("value must be one of the following: Flask, flask, Flasks, flasks, Ball, ball, Balls, balls")

    #return earlier data
    global map_data_persistent
    if map_data_persistent != []:
        return map_data_persistent[index]

    #return false if no data exists yet
    return False


#get array of the balls in flasks
data = []
def set_map_data(flask, ball):
    if type(flask) != int:
        raise TypeError("flask value must be an int")
    if type(ball) != int:
        raise TypeError("ball value must be an int")
    if flask <= 0:
        raise ValueError("flask value must be above 0")
    if ball <= 0:
        raise ValueError("ball value must be above 0")
    
    global map_data_persistent
    map_data_persistent = [flask, ball]
    global data
    data = [[0 for j in range(map_data("Balls"))] for i in range(map_data("flasks")+2)]
    color_list = ["red","blue3","yellow","green2","orange","magenta","turquoise1","DarkOrchid4","light pink","steelblue2","saddle brown","gray","pale green","white","pink","dark goldenrod","green","sea green","khaki","gray16"]
    for flask in range(flask):
        for ball in range(len(data[flask])):
            data[flask][ball] = color_list[flask]
    
#Do a move
def move(start, end, force = False):
    if type(start) != int:
        raise TypeError("start value must be an int")
    if type(end) != int:
        raise TypeError("end value must be an int")
    if type(force) != bool:
        raise TypeError("force value must be a bool")

    
    if start < 0 or start >= map_data("flask")+2:
        raise ValueError("start value is out of range")
    if end < 0 or end >= map_data("flask")+2:
        raise ValueError("end value is out of range")
    
    
    #check if it is a move
    if start == end:
        return False
    global data
    #check if the end has a free space
    if data[end][-1] != 0:
        return False
    #find the first color
    for index_start, color_start in reversed(list(enumerate(data[start]))):
        if color_start != 0:
            break
    #error if no color is found
    if color_start == 0:
        return False
    #find the ball below the empty spot
    for index_end, color_end in reversed(list(enumerate(data[end]))):
        if color_end != 0:
            break
    #check if the flask is emtpy or the ball below is the same color
    if color_end != 0 and color_end != color_start and force == False:
        return False
    #go to the lowest empty space
    if color_end != 0:
        index_end += 1
    #move the ball from one place to the other
    #print("moving " + str(color_start) + " from " + str(start) + "(" + str(index_start) + ")" + str(data[start]) + " to " + str(end) + "(" + str(index_end) + ")" + str(data[end]))
    data[end][index_end] = color_start
    data[start][index_start] = 0
    return [start,index_start,end,index_end]
#returns true if moving happens and false if not
    

def check_complete():
    #make a list
    flasks = [False for i in range(map_data("flask")+2)]
    index = -1
    #check all flasks
    for flask in data:
        index += 1
        #filter for all non empty flasks
        break_check = False
        #check the balls
        for ball in flask:
            if ball != flask[0]:
                break_check = True
                break
        #set to true if it breaks
        if break_check == True:
            flasks[index] = True
    #check if completed
    victory = 0
    for complete in flasks:
        if complete:
            victory += 1
    if victory == 0:
        return True
    return victory

def detect_loop(steps):
    """Returns a bolean based on if the Steps contain a looping part."""
    
    #throw out the correct errors for debugging.
    if type(steps) != list:
        raise TypeError("steps is not a list")
    if len(steps) % 2 == 1:
        raise ValueError("steps is an odd number")
    for x in steps:
        if type(x) != int:
            raise TypeError("values in the list are not int")
        if x >= map_data("flasks")+2:
            raise ValueError("Values are out of flask range")

    #detect if a series of steps get repeated and detect the size of that loop
    biggest_loop = False
    for i in range(2,int((len(steps)+2)/2),2):
        test_steps = steps[:i*-1]
        if test_steps[i*-1:] == steps[i*-1:] and i > 2:
            detection_list = [[0 for j in range(map_data("flasks")+2)],[0 for j in range(map_data("flasks")+2)]]
            for k in range(0,i,2):
                detection_list[0][steps[(k+1)*-1]] += 1
                detection_list[1][steps[(k+2)*-1]] += 1
            if detection_list[0] == detection_list[1]:
                biggest_loop = i
    return biggest_loop

def bouncing(steps):
    """Gives back a bolean based on if the new step would undo a previous move"""

    #throw out errors when shit is going down
    if type(steps) != list:
        raise TypeError("steps is not a list")
    if len(steps) % 2 == 1:
        raise ValueError("steps is an odd number")
    for x in steps:
        if type(x) != int:
            raise TypeError("values in the list are not int")
        if x >= map_data("flasks")+2:
            raise ValueError("Values are out of flask range")
        
    #put in the test to check for bouncing. It can redo moves, but it can not undo moves if both piles have not been changed since then.
    bouncing = 0
    for action in range(2,len(steps),2):
        test_step = [steps[(action+2)*-1], steps[(action+1)*-1]]
        if test_step[0] == steps[-1] or test_step[0] == steps[-2]:
            bouncing = 1
        if test_step[1] == steps[-1] or test_step[1] == steps[-2]:
            bouncing = 1
        if test_step[0] == steps[-1] and test_step[1] == steps[-2]:
            bouncing = 2
        if bouncing != 0:
            break
    if bouncing <= 1:
        return False
    return True

def skipping(steps):
    """Gives back a bool based on if the current flask you want to put it in better off skipped"""
    
    #throw out errors when shit is going down
    if type(steps) != list:
        raise TypeError("steps is not a list")
    if len(steps) % 2 == 1:
        raise ValueError("steps is an odd number")
    for x in steps:
        if type(x) != int:
            raise TypeError("values in the list are not int")
        if x >= map_data("flasks")+2:
            raise ValueError("Values are out of flask range")
    
    #skip to fill an flask already with that single color
    #detect if the flask you put it in has a single ball color. If it does not you might not want to skip it.
    #steps[-1] is the end flask and steps[-2] is the starting flask
    for balls in range(map_data("balls")):
        if data[steps[-1]][balls] != data[steps[-1]][0] and data[steps[-1]][balls] != 0:
            return False
    
    for color_here in reversed(data[steps[-2]]):
        if color_here != 0:
            break
    if color_here == 0:
        return False
    if data[steps[-1]][0] != 0 and data[steps[-1]][0] != color_here:
        return False
    first_void = False
    highest_stack = 0
    highest_flask = 0
    for flask in range(map_data("flask")+2):
        #find the first void for later usage
        if not first_void:
            if data[flask][0] == 0:
                fully_void = True
                for balls in data[flask]:
                    if balls != 0:
                        fully_void = False
                if fully_void:
                    first_void = flask
        #find the first biggest stack of balls of the same color and skip if you are not hovering over that.
        if data[flask][0] == color_here:
            flask_good = True
            stack = 0
            for balls in range(map_data("balls")):
                if data[flask][balls] == color_here:
                    stack += 1
                if data[flask][balls] != color_here and data[flask][balls] != 0:
                    flask_good = False
            #detect highest stack
            if stack > highest_stack and flask_good:
                highest_stack = stack
                highest_flask = flask
    #return true if you are not overing over the biggest stack
    if highest_stack > 0:
        return steps[-1] != highest_flask
    #return true if you are not on the first
    return data[steps[-1]][0] == 0 and first_void != steps[-1]

def twice_twice(steps):
    """Gives back a bolean based on if the new step could better be merged with a previous one."""

    #throw out errors when shit is going down
    if type(steps) != list:
        raise TypeError("steps is not a list")
    if len(steps) % 2 == 1:
        raise ValueError("steps is an odd number")
    for x in steps:
        if type(x) != int:
            raise TypeError("values in the list are not int")
        if x >= map_data("flasks")+2:
            raise ValueError("Values are out of flask range")

    #you can not move the same one twice in a row
    if len(steps) > 3:
        #test for one step back
        if steps[-2] == steps [-3]:
            return True
        #test for n steps back
        twicing = 0
        test_action = 0
        for action in range(2,len(steps),2):
            test_step = [steps[(action+2)*-1], steps[(action+1)*-1]]
            if test_step[0] == steps[-1] or test_step[0] == steps[-2]:
                twicing = 1
            if test_step[1] == steps[-1] or test_step[1] == steps[-2]:
                twicing = 1
            if test_step[1] == steps[-2]:
                twicing = 2
            if twicing != 0:
                test_action = action
                break
        if twicing == 2:
            for action in steps[(test_action)*-1:]:
                if action == steps[(test_action+2)*-1]:
                    return False    
            return True
    return False

def full_flask(steps):
    #throw out errors when shit is going down
    if type(steps) != list:
        raise TypeError("steps is not a list")
    if len(steps) % 2 == 1:
        raise ValueError("steps is an odd number")
    for x in steps:
        if type(x) != int:
            raise TypeError("values in the list are not int")
        if x >= map_data("flasks")+2:
            raise ValueError("Values are out of flask range")

    
    #check if starting flask only has a single colour and is full. No destroying completed flasks
    if data[steps[-2]][-1] == 0 or data[steps[-2]][-1] == data[steps[-2]][0]:
        for balls in data[steps[-2]][:-1]:
            if balls != data[steps[-2]][0]:
                return False
        if data[steps[-2]][-1] == data[steps[-2]][0]:
            return True
        if data[steps[-2]][-1] == 0:
            for x in range(map_data("flasks")+2):
                if data[steps[-2]][0] == data[x][0]:
                    return steps[-2] == x
    return False

steps = [0,0]
def repeating_moves():
    """Calculates a solution to the problem given in the global data variable. The solution comes in a list of steps"""

    global steps
    steps = [-2,-2]
    Victory = False
    if check_complete() == True:
        Victory = True
        steps = []
    
    while not Victory:
        

        #undo a move
        if steps[-2] == -2:
            steps[-2] += 1
            steps[-1] = -2
        else:   
            del steps[-2:]
            if len(steps) == 0:
                return False
            move(steps[-1], steps[-2], True)
            steps[-2] -= 1
            steps[-1] -= 1
        
        while steps[-2] >= -1 and steps[-2] < map_data("flask")+1 and not Victory:
            steps[-2] += 1
##            print("first: ",steps)
            if not twice_twice(steps):
##                print("twice twice: ",steps)
                if not full_flask(steps):
##                    print("full flask: ",steps)
                        
                    if steps[-1] >= map_data("flask")+1:
                        steps[-1] = -2
                    steps[-1] += 1
##                    print("second: ", steps)
                    while steps[-1] >= -1 and steps[-1] < map_data("flask")+1 and not Victory:
                        steps[-1] += 1
##                        print("third: ",steps)

                        if not bouncing(steps):
##                            print("bounce: ", steps)
                            if not skipping(steps):
##                                print("skipping: ",steps)

                                #do the move
                                if move(steps[-2], steps[-1]) != False:
##                                    print("moved: ",steps)
                                    if check_complete() == True:
                                        Victory = True
                                        break

                                    #this code should prevent looping
                                    loop = detect_loop(steps)    
##                                    print("loops: ",loop)
                                    if  not loop:
                                        steps = steps + [-2,-2]
                                    else:
                                        for x in range(0, loop, 2):
                                            move(steps[-1], steps[-2], True)
                                            del steps[-2:]
                                        move(steps[-1], steps[-2], True)
                                        



    #return the final info
    return steps





#begin with screen layouts and shit

tkin = Tk()
style = ttk.Style()
screen_storage = []

#define the screen and start it
def install_screen():
    Geo = "1400x800"

    global tkin
    #window setup
    tkin.title("Color Sort Solver")
    tkin.configure(background="white")
    tkin.resizable(False,False)
    tkin.geometry(Geo)

    global style
    style.configure("MySlider.Horizontal.TScale", foreground="black", background="white")


#this is what the base screen needs
flask_value = DoubleVar()
ball_value = DoubleVar()
def start_screen():
    global screen_storage

    #define the layout
    tkin.columnconfigure(0, weight=6)
    tkin.columnconfigure(1, weight=2)
    tkin.columnconfigure(2, weight=4)
    tkin.columnconfigure(3, weight=1)
    tkin.columnconfigure(4, weight=6)
    tkin.rowconfigure(0, weight=6)
    tkin.rowconfigure(1, weight=3)
    tkin.rowconfigure(2, weight=3)
    tkin.rowconfigure(3, weight=3)
    tkin.rowconfigure(4, weight=3)
    tkin.rowconfigure(5, weight=6)

    #set the proper values in the bars
    flask_count = map_data("flasks")
    ball_count = map_data("balls")
    if flask_count == False:
        flask_count = 1
    if ball_count == False:
        ball_count = 1

    #call all labels I need
    screen_storage.append(ttk.Label(tkin, anchor = NW, foreground="white",background="white"))
    screen_storage[-1].grid(column=0,row=0)
    screen_storage.append(ttk.Label(tkin, anchor = CENTER, padding=1, text="Ball sorter", background="light blue"))
    screen_storage[-1].grid(column=1,row=1,columnspan=3)
    screen_storage.append(ttk.Label(tkin, anchor = CENTER, padding=1, text="Select amount of flasks:", background="light blue"))
    screen_storage[-1].grid(column=1,row=2)
    screen_storage.append(ttk.Scale(tkin, from_=1, to=20, style="MySlider.Horizontal.TScale", variable = flask_value, command = flask_slider))
    screen_storage[-1].grid(column=2,row=2,sticky='we')
    screen_storage.append(ttk.Label(tkin, anchor = CENTER, padding=1, text=flask_count))
    screen_storage[-1].grid(column=3,row=2)
    screen_storage.append(ttk.Label(tkin, anchor = CENTER, padding=1, text="Select amount of balls:", background="light blue"))
    screen_storage[-1].grid(column=1,row=3)
    screen_storage.append(ttk.Scale(tkin, from_=1, to=20, style="MySlider.Horizontal.TScale", variable = ball_value, command = ball_slider))
    screen_storage[-1].grid(column=2,row=3,sticky='we')
    screen_storage.append(ttk.Label(tkin, anchor = CENTER, padding=1, text=ball_count))
    screen_storage[-1].grid(column=3,row=3)
    screen_storage.append(ttk.Button(tkin, padding=1, text="Place balls", command = next_button))
    screen_storage[-1].grid(column=1,row=4,columnspan=3)
    screen_storage.append(ttk.Label(tkin, anchor = NW, foreground="white", background="white"))
    screen_storage[-1].grid(column=4,row=5)

#have a number behind the two sliders represent your choise
def flask_slider(event):
    flask = flask_value.get()
    flask = math.floor(flask)
    if flask <= 0:
        flask = 1
    screen_storage[4].configure(text=flask)
    
def ball_slider(event):
    ball = ball_value.get()
    ball = math.floor(ball)
    if ball <= 0:
        ball = 1
    screen_storage[7].configure(text=ball)

def next_button():
    #get the flask and ball values from the sliders
    flask = flask_value.get()
    flask = math.floor(flask)
    if flask <= 0:
        flask = 1
    ball = ball_value.get()
    ball = math.floor(ball)
    if ball <= 0:
        ball = 1
    #make the map based on those values
    set_map_data(flask, ball)
    screen_clearer()
    flask_screen()

#deletes everything on the screen
def screen_clearer():
    global screen_storage
    for widget in screen_storage:
        widget.destroy()
    screen_storage = []
    return True

#everything needed for all the flasks
cv = Canvas(tkin, width=1400, height=900, bg="white", highlightthickness=0)
flask_list = []
def flask_screen():
    global cv
    cv.grid(row=0, column=0, sticky=W)

    global flask_list
    flask_list = []
    flask_size = [90,map_data("balls")*60+5]

    #how to spawn the flask with less than 8 total
    if map_data("flasks")+2 <= 8:
        spawn_y = 400 - flask_size[1]/2
        spawn_x = 700 - ((map_data("flasks")+1)*60+45)
        
        flask_list += flask_row(spawn_x,spawn_y,map_data("Flasks")+2)

    #how to spawn flasks with less than 16 total
    elif map_data("flasks")+2 <= 16:
        top_row = math.ceil((map_data("flasks")+2)/2)
        spawn_y = 385 - flask_size[1]
        spawn_x = 700 - (top_row*60+45)
        flask_list += flask_row(spawn_x,spawn_y,top_row)
        #end of the top row and start of the bottom row
        bottom_row = math.floor((map_data("flasks")+2)/2)
        spawn_y = 415
        spawn_x = 700 - (bottom_row*60+45)
        flask_list += flask_row(spawn_x,spawn_y,bottom_row)

    else:
        top_row = math.ceil((map_data("flasks")+2)/3)
        spawn_y = 370 - flask_size[1]*1.5
        spawn_x = 700 - (top_row*60+45)
        flask_list += flask_row(spawn_x,spawn_y,top_row)
        #end of the top row and start of the middle row
        middle_row = round((map_data("flasks")+2)/3)
        spawn_y = 400 - flask_size[1]/2
        spawn_x = 700 - (middle_row*60+45)
        flask_list += flask_row(spawn_x,spawn_y,middle_row)
        #end of the middle row and start of the bottom row
        bottom_row = math.floor((map_data("flasks")+2)/3)
        spawn_y = 430 + flask_size[1]/2
        spawn_x = 700 - (bottom_row*60+45)
        flask_list += flask_row(spawn_x,spawn_y,bottom_row)

    for flask in range(len(flask_list)-2):
        for ball in range(len(flask_list[flask])):
            flask_list[flask][ball][2] = ball_draw(flask_list[flask][ball][0], flask_list[flask][ball][1], data[flask][ball])

    buttons()
    cv.update()

def ball_draw(x, y, color):
    screen_storage.append(cv.create_arc(x,y,60+x,60+y,start=90,extent=359,width=2,fill=color,style=CHORD))
    return screen_storage[-1]

def flask_row(x, y, count):
    flask_list = []
    for i in range(count):
        flask_list += [flask_draw(x+i*120,y)]
    return flask_list
    
def flask_draw(x, y):
    lonk = (map_data("balls")-1)*60
    screen_storage.append(cv.create_arc(10+x,-5+lonk+y,80+x,65+lonk+y,start=180,extent=180,style=ARC,width=2))
    screen_storage.append(cv.create_line(10+x,10+y,10+x,30+lonk+y,width=2))
    screen_storage.append(cv.create_line(80+x,10+y,80+x,30+lonk+y,width=2))
    screen_storage.append(cv.create_arc(-10+x,y,10+x,20+y,start=0,extent=90,style=ARC,width=2))
    screen_storage.append(cv.create_arc(80+x,y,100+x,20+y,start=90,extent=90,style=ARC,width=2))

    ball_locations = []
    for place in reversed(range(map_data("balls"))):
        ball_locations += [[15+x,place*60+y,0]]
    return ball_locations

def buttons():
    screen_storage.append(cv.create_rectangle(10,10,60,30,fill="gray85"))
    screen_storage.append(cv.create_text(36,20,text="< back"))
    solution_buttons()
    
#the buttons to get a solution and move forwards and backwards trough the solution
solve_buttons_values = []
def solution_buttons(state = False):
    global solve_buttons_values
    global cv
    if state == True:
        for x in solve_buttons_values:
            cv.delete(x)
        screen_storage.append(cv.create_rectangle(1200,720,1290,760,fill="gray85"))
        screen_storage.append(cv.create_text(1245,740,text="<<<"))
        screen_storage.append(cv.create_rectangle(1300,720,1390,760,fill="gray85"))
        screen_storage.append(cv.create_text(1345,740,text=">>>"))
        screen_storage.append(cv.create_rectangle(1200,770,1390,790,fill="gray85"))
        screen_storage.append(cv.create_text(1295,780,text="delete solution"))
        solve_buttons_values = screen_storage[-6:]
    else:
        for x in solve_buttons_values:
            cv.delete(x)
        screen_storage.append(cv.create_rectangle(1200,720,1390,760,fill="gray85"))
        screen_storage.append(cv.create_text(1295,740,text="solve"))
        screen_storage.append(cv.create_rectangle(1200,770,1390,790,fill="gray85"))
        screen_storage.append(cv.create_text(1295,780,text="apply gravity"))
        solve_buttons_values = screen_storage[-4:]



#Text at the bottom of the screen
text_values = []
def set_text_to(string = False):
    global text_values
    if type(string) == bool:
        for x in text_values:
            cv.delete(x)
        text_values = []
    else:
        for x in text_values:
            cv.delete(x)
        screen_storage.append(cv.create_text(700,750,text=string,font = ['TkDefaultFont', '40', 'bold']))
        text_values = screen_storage[-1:]
    
#deletes everything on the screen
def canvas_clearer():
    global screen_storage
    cv.delete('all')
    screen_storage = []
    return True

selection_box = []
def select_box(flask, ball, remove=False):
    global selection_box
    if remove == True:
        for x in selection_box:
            cv.delete(x)
        return True
    coords = flask_list[flask][ball][:2]
    screen_storage.append(cv.create_arc(coords[0]-2,coords[1]-2,coords[0]+62,coords[1]+62,style=ARC,start=20,extent=50,width=3,outline="gray63"))
    screen_storage.append(cv.create_arc(coords[0]-2,coords[1]-2,coords[0]+62,coords[1]+62,style=ARC,start=110,extent=50,width=3,outline="gray63"))
    screen_storage.append(cv.create_arc(coords[0]-2,coords[1]-2,coords[0]+62,coords[1]+62,style=ARC,start=200,extent=50,width=3,outline="gray63"))
    screen_storage.append(cv.create_arc(coords[0]-2,coords[1]-2,coords[0]+62,coords[1]+62,style=ARC,start=290,extent=50,width=3,outline="gray63"))
    selection_box += screen_storage[-4:]
    

#everything for click events
select = []
solution = []
def click(event):
    clicked = [event.x, event.y]
    global select
    global solution
    global solve_buttons_values

    #the back button
    if clicked[0] >= 10 and clicked[0] <= 60 and clicked[1] >= 10 and clicked[1] <= 30:
        canvas_clearer()
        select = []
        solution = []
        cv.grid_remove()
        start_screen()
        return

    set_text_to()

    #only do the following if no solution is present
    if len(solution) == 0:
        #check if you clicked a ball
        for flask in range(len(flask_list)):
            for ball in range(len(flask_list[flask])):
                if clicked[0] >= flask_list[flask][ball][0] and clicked[0] <= flask_list[flask][ball][0] + 60 and clicked[1] >= flask_list[flask][ball][1] and clicked[1] <= flask_list[flask][ball][1] + 60:
                    if select == []:
                        select = [flask,ball]
                        select_box(flask,ball)
                    elif select == [flask, ball]:
                        select = []
                        select_box(flask,ball,True)
                    else :
                        #move all the data to the new pos
                        timely = [data[select[0]][select[1]],flask_list[select[0]][select[1]][2]]
                        cv.move(flask_list[flask][ball][2],flask_list[select[0]][select[1]][0]-flask_list[flask][ball][0],flask_list[select[0]][select[1]][1]-flask_list[flask][ball][1])
                        cv.move(timely[1],flask_list[flask][ball][0]-flask_list[select[0]][select[1]][0],flask_list[flask][ball][1]-flask_list[select[0]][select[1]][1])
                        data[select[0]][select[1]] = data[flask][ball]
                        flask_list[select[0]][select[1]][2] = flask_list[flask][ball][2]
                        data[flask][ball] = timely[0]
                        flask_list[flask][ball][2] = timely[1]
                        
                        select = []
                        select_box(flask,ball,True)
                    return

        #get a solution
        if clicked[0] >= 1200 and clicked[0] <= 1390 and clicked[1] >= 720 and clicked[1] <= 760:
            gravity()
            solution = repeating_moves()
            if solution == False:
                #no solution found
                set_text_to("no solution found")
                solution = []
            elif solution == []:
                #the problem is already the solved state
                set_text_to("problem already solved")
            else:
                for action in range(0,len(solution),2):
                    action1 = (action + 1) * -1
                    move(solution[action1],solution[action1-1],True)
                solution_buttons(True)
                select_box(0,0,True)
                select = 0
                #print(solution)
                #print(data)
        if clicked[0] >= 1200 and clicked[0] <= 1390 and clicked[1] >= 770 and clicked[1] <= 790:
            gravity()

    #if a solution exist do these things:
    else:
        if clicked[0] >= 1200 and clicked[0] <= 1290 and clicked[1] >= 720 and clicked[1] <= 760:
            backward()
        if clicked[0] >= 1300 and clicked[0] <= 1390 and clicked[1] >= 720 and clicked[1] <= 760:
            forward()
        if clicked[0] >= 1200 and clicked[0] <= 1390 and clicked[1] >= 770 and clicked[1] <= 790:
            solution = []
            select = []
            solution_buttons()

#move the solution forwards
def forward(event=False):
    set_text_to()
    global solution
    if len(solution) == 0:
        return False
    global select
    if select + 2 > len(solution):
        return False
    movement = move(solution[select],solution[select+1])
    if movement != False:
        print(movement)
        cv.move(flask_list[movement[0]][movement[1]][2], flask_list[movement[2]][movement[3]][0] - flask_list[movement[0]][movement[1]][0], flask_list[movement[2]][movement[3]][1] - flask_list[movement[0]][movement[1]][1])
        flask_list[movement[2]][movement[3]][2] = flask_list[movement[0]][movement[1]][2]
        flask_list[movement[0]][movement[1]][2] = 0
        select += 2

#move the solution backwards
def backward(event=False):
    set_text_to()
    global solution
    if len(solution) == 0:
        return False
    global select
    if select - 2 < 0:
        return False
    movement = move(solution[select-1],solution[select-2],True)
    if movement != False:
        cv.move(flask_list[movement[0]][movement[1]][2], flask_list[movement[2]][movement[3]][0] - flask_list[movement[0]][movement[1]][0], flask_list[movement[2]][movement[3]][1] - flask_list[movement[0]][movement[1]][1])
        flask_list[movement[2]][movement[3]][2] = flask_list[movement[0]][movement[1]][2]
        flask_list[movement[0]][movement[1]][2] = 0
        select -= 2

def gravity(event=False):
    set_text_to()
    #makes all the balls fall down to the lowest positions in the flask
    for flask in range(len(data)):
        empty_levels = []
        for ball in range(len(data[flask])):
            if data[flask][ball] == 0:
                empty_levels.append(ball)
            if data[flask][ball] != 0:
                if len(empty_levels) >= 1:
                    timely = [data[flask][empty_levels[0]],flask_list[flask][empty_levels[0]][2]]
                    cv.move(flask_list[flask][ball][2],flask_list[flask][empty_levels[0]][0]-flask_list[flask][ball][0],flask_list[flask][empty_levels[0]][1]-flask_list[flask][ball][1])
                    cv.move(timely[1],flask_list[flask][ball][0]-flask_list[flask][empty_levels[0]][0],flask_list[flask][ball][1]-flask_list[flask][empty_levels[0]][1])
                    data[flask][empty_levels[0]] = data[flask][ball]
                    flask_list[flask][empty_levels[0]][2] = flask_list[flask][ball][2]
                    data[flask][ball] = timely[0]
                    flask_list[flask][ball][2] = timely[1]
                    del empty_levels[0]
                    empty_levels.append(ball)
                    

if __name__ == '__main__':
    cv.bind("<Button-1>", click)
    tkin.bind("<KeyPress-Left>", backward)
    tkin.bind("<KeyPress-Right>", forward)
    tkin.bind("<KeyPress-Down>", gravity)


    install_screen()
    start_screen()

    tkin.mainloop()
