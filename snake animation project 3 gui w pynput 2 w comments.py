# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snakeapp.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

#!/usr/bin/env python
from time import sleep                      #no need for the whole library we just need the sleep function
import opc
import threading                            #to run loops seperate from GUI or any parent thread
import numpy
import colorsys
import random               
import sys, string, os                      #import all necessery libraries
from pynput.keyboard import Listener,Key,Controller #this library is for checking keypresses or the mouse clicks
from PyQt5 import QtCore, QtGui, QtWidgets  #from GUI library import only what needed

os.system("readopcForStrands.exe")          #open the les matrix simulator app
client = opc.Client('localhost:7890')       #rgb led address to send the Send pixels forever at 30 frames per second
 
Red =   255, 0,   0                         #predifined rgb values ill be using
Black = 0,   100, 0
Green = 50, 255, 50
really_black = 0, 50,   0               
play = True                                 #until true snake function loop runs
Position = 4                                #the snakes head starts from the 5th pixel and after moves from there depending on the direction
Direction = 1                               #direction is to the right by one at start
counter = 40                                #counter starts from 40
counter_division = 40                       #every fourty loop new red dots for the snake to eat
snake_not_running = True                    #will make these false later
listener_not_running = True                 #will make these false later when started running threads, probably not necessery but will be good in the GUI i think
snake_body_list = [0,1,2,3,4]               #snakes body in the start
snake_list = [(Black)]*360                  #screens rgb colors all set to blackish

class Ui_MainWindow(object):                #GUI created using pyqt5 designer
    def setupUi(self, MainWindow):          #setting up GUI parameters, window buttons and stuff according to as it was drawn in designer
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(384, 299)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons8-snake-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 50, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 20, 121, 121))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("icons8-snake-96.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 140, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 100, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 384, 25))
        self.menubar.setObjectName("menubar")
        self.menuRun_Simulator = QtWidgets.QMenu(self.menubar)
        self.menuRun_Simulator.setObjectName("menuRun_Simulator")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGo = QtWidgets.QAction(MainWindow)
        self.actionGo.setObjectName("actionGo")
        self.actionExit_Game = QtWidgets.QAction(MainWindow)
        self.actionExit_Game.setObjectName("actionExit_Game")
        self.menuRun_Simulator.addAction(self.actionGo)
        self.menuRun_Simulator.addAction(self.actionExit_Game)
        self.menubar.addAction(self.menuRun_Simulator.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_2.clicked.connect(lambda:self.startTheThread(self.restartGame))
        self.pushButton_2.clicked.connect(lambda:self.startTheThread(self.snake_auto))  #specifying what happens when button pushed or action button triggered
        self.pushButton.clicked.connect(lambda:self.startTheThread(self.stopIt))        #when clicked the functions will run through another function that will 
        self.actionGo.triggered.connect(lambda:self.startTheThread(self.runSimulator))  #run them on a seperate thread
        self.actionExit_Game.triggered.connect(lambda:self.startTheThread(self.exitApp))
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake"))
        self.pushButton.setText(_translate("MainWindow", "Stop (x)"))
        self.label_2.setText(_translate("MainWindow", "Controlls: W A S D "))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.menuRun_Simulator.setTitle(_translate("MainWindow", "Run Simulator"))
        self.actionGo.setText(_translate("MainWindow", "Go"))
        self.actionExit_Game.setText(_translate("MainWindow", "Exit Game"))

    def restartGame(self):
        global play
        global Position
        global Direction
        global counter
        global snake_body_list
        Position = 4                                #the snakes head starts from the 5th pixel and after moves from there depending on the direction
        Direction = 1                               #direction is to the right by one at start
        counter = 40                                #counter starts from 40
        snake_body_list = [0,1,2,3,4]
        play = True
    
    def startTheThread(self, function):                 #runs the chosen function from the argument on a separate thread
        self.t = threading.Thread(target = function)    #make t a thread and run it with the start command
        self.t.start()                                  #to wait for thread to be finished: t.join()
        
    def runSimulator(self):
        os.system("readopcForStrands.exe")              #run Simultor.exe, which has to be in same folder
        
    def exitApp(self):                                  #exit works but the pop up window is displayed behind main window, not sure ghow to fix it yet
        print("exit triggered")
        exit(self)

    def stopIt(self):                                   #function called when loops needs to stop
        global play                                     #global variable
        self.clear_screen(Black)
        print("stop loop")
        play = False
        
#                   MAIN FUNCTION
    def snake_auto(self):                               #running in backround automatically going in the direction unless changed    
        global play                                     #if it wasnt global the variable would only exist in this function
        while True:                                     #while i didnt die (meaning i dint bump into myself) the loop runs)
            if play == False:                           #break while loop if died or stopped game
                break
            #print("auto-snake running")
            self.clear_screen(Black)                    #clear everything from before
            self.random_dot(3)                          #create 3 red dots for the snake to eat
            sleep(0.02)                                 #wait a bit just for flashing effect
            self.way_to_go()                            #decide which way to go
            self.draw_snake()                           #after decided draw the snake and the dots as well
            self.did_i_die(snake_body_list)             #when have new position of our snake, check it bumped into itself
            sleep(0.2)

    def did_i_die(self, listOfElems):                   #check if we died in the game
        global play
        #print("list to check:")
        #print(listOfElems)
        if len(listOfElems) == len(set(listOfElems)):   #check it by looking for duplicates(there cant be any) in the snake_body_list
            #print("didnt die yet")
            play = True                                 #when true the main loop breaks
            #return False
            
        else:
            print("game over")
            self.clear_screen(Black)                    #if no two of the same pixels in the list same stop playing and display message
            self.display_loser()
            play = False
            #return True
        
    def draw_snake(self):                               #this function creates the line of pixels for the snake to display for the next loop
        for i in snake_body_list:                       
            snake_list[i] = Green                       #change black rgb colors to green in the list
        client.put_pixels(snake_list)                   #display it
        if Position not in random_list:                 #if we didnt "eat red dots" meaning the snakes heads new position is not the same as the red dot
            snake_body_list.pop(0)                      #delete first item of list which is actually the last pixel of the snake because didnt eat red dot
        else:
            random_list.remove(Position)                #If ate red dot than remove that dot 
        snake_body_list.append(Position)                #move the snake to the new position by one pixel

    def way_to_go(self):                                #deciding wich wway to go
        global Position
        Position = Direction + Position                 #depending on button pressed or not or witch creae the new position to move towards
        if Position <0:                                 #this part is to ttake the snake back if left the screen
            Position+=360
        if Position>359:
            Position-=360

    def random_dot(self, nr):                           #this is where the randomly appearing dots are created  nr: number of dont u want
        global counter                                  #global variables to use in other functions
        global random_position
        global random_list
        if counter%counter_division == 0:               #if theres no remainder it means another 40 loops passed
            random_list = []                            #clear the red dots list
            for i in range(nr):                         #create new ones
                random_position = random.randint(0,359)
                random_list.append(random_position)     #add it to the previously emptied list
        for i in random_list:                           #now turn those pixels red
            snake_list[i] = Red
        counter += 1                                    #loop counter
       
    def clear_screen(self, color):                      #all pixels to black so new pixel positions can be displayed
        #print("screen cleared")
        global snake_list
        snake_list = [(color)]*360
        client.put_pixels(snake_list)

    def display_loser(self):                            #when game over display a message
        self.clear_screen(really_black)
        L_list = [61, 121, 181, 241, 301, 302, 303, 304]
        O_list = [66, 67, 68, 69, 126, 129, 186, 189, 246, 249, 306, 307, 308, 309]
        S_list = [71, 72, 73, 74, 131, 191, 192, 193, 194, 254, 311, 312, 313, 314]
        E_list = [76, 77, 78, 79, 136, 196, 197, 198, 199, 256, 316, 317, 318, 319]
        R_list = [81, 82, 83, 84, 141, 144, 201, 202, 203, 204, 261, 263, 321, 324]
        loser_list = L_list + O_list + S_list + E_list + R_list
        for i in range(len(loser_list)):    #moved the text to the middle of the display lokks nicer this way
            loser_list[i] +=  18
        for i in loser_list:                #display the letter in red
            snake_list[i] = Red
        client.put_pixels(snake_list)

def on_press(key):                          #function called when any keyboard keys pressed
    print(key, " key pressed")
    handle_key(key) 

def on_release(key):                        #same but when released
    global play
    if is_stop_switch(key):                 #if x was pressed than stop the game
        print("STOP(x) key released")        
        play=False     

def handle_key(key):                        #the function that decides is the right keys were pressed and what to do
    if is_valid_character(key):
        if is_control_switch(key):
            control_snake(key)              #if it was one of the control keys than run function and check what to do
        else:
            print("not a control key")
    else:
        print('no attribute')
        
def is_stop_switch(key):                    #returns true if the right key pressed
    return key.char == 'x'

def is_valid_character(key):                #checks if the key has valid attribure
    return hasattr(key, 'char')

def is_control_switch(key):                 #only run control_snake function when the key pressed was in the list
    return key.char in ['w', 'a', 's', 'd']

def control_snake(key):                     #withc way to move how much unless its opposite of previous direction
    global Direction
    if key.char == 'w' and Direction != 60:
        Direction = -60
        print("up")
    if key.char == 's'and Direction != -60:
        print("down")
        Direction =  60
    if key.char == 'a'and Direction != 1:
        print("left")
        Direction = -1
    if key.char == 'd'and Direction != -1:
        print("right")
        Direction =  1

def keyboard_listener():                    #function listening keypress events (not the qt built in one that one didnt work yet)
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()                     #waiting for thread to finish
        
if listener_not_running:
    l = threading.Thread(target = keyboard_listener)   #run function once only, probably not necessery
    l.start()
    listener_not_running = False


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())