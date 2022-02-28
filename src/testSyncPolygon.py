from psychopy import visual, event, core, gui, data
import os                           # for file/folder operations
import numpy as np          
from psychopy.hardware import keyboard
import random, os, csv

#First let's add a few packages, that we will need for the device
import ctypes
import sys
import threading
import time

# We load the wrapper
filename = "libStreaming_CachedPoint_ctypes.so"
prg = ctypes.cdll.LoadLibrary(filename)

# The array will run in a thread in the background, waiting for the rest of our instrunctions
thread = threading.Thread(target=prg.start_array, args=()) #create said thread
thread.daemon = True  # Daemonize thread
thread.start()     # Start the execution


#setting a global sut down key = escape
event.globalKeys.add(key='escape', func=core.quit, name='shutdown')


#exp_name = "RDKMotionDirection"
#info = {'subNb':'','sessionNb':''}
#if not gui.DlgFromDict(info, order=['subNb', 'sessionNb', 'handedness']).OK:      
#    core.quit()  

'''
#log
log_path = '/Users/shahzad/Documents/PsychopyExpt/TRYbuilder_visualTactileMotionDirectionDiscrimination/ExptCode/data/'+'sub'+ info['subNb']+'_'+ data.getDateStr(format="%Y-%m-%d-%H%M")
log = open(log_path+".csv",'w')  
writer = csv.writer(log, delimiter=";")
cols="subNb","blockNb","handPos","trialNb","trialDirection","respKey","RT", "accuracy"
writer.writerow(cols)
'''

#set the screen
win = visual.Window(size=[1536, 960], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

#visual stimuli
rdk = visual.DotStim(win,units='pix', 
    nDots=50, dotSize=20,
    speed=4, dir=1.0,  coherence=1.0,
    fieldPos=(0.0, 0.0), fieldSize=(800,800),fieldShape='circle',
    signalDots='same', noiseDots='position',dotLife=10,
    color=[1.0,1.0,1.0], colorSpace='rgb', opacity=1,
    depth=0.0, name='',autoLog=True)
    

polygon = visual.Rect(
    win=win, name='polygon',
    width=(2, 2)[0], height=(2, 2)[1],
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=1.0, depth=0.0, interpolate=True)

    
#tac stimuli
f_s = 40e3 #We set our sampling rate frequency to 40k, which is the default rate
duration = 0.5 #0.5 sec duration #we are going to produce 1s long stimuli
t = np.arange(0,duration,1./f_s) #create the vector "time"

### Creation of a line
length_line = 0.02 ## the line will be 2cm long
f_stm = 100 ## the line is created at a rate of 100Hz
v_point = length_line*f_stm ##this is the speed of the focal point on the line

#ping pong line. I.e. the focal point would move back and forth on the line ->; <-; ->; etc... instead of ->; jump back to begining; -> ;
tmp = np.mod(t*v_point, 2*length_line) 
x_point = np.where(tmp <= length_line, tmp, 2*length_line - tmp) - length_line/2

### Line motion
length_motion = 0.1 ## the line will move across 10cm
v_line = length_motion/duration ## the line will be drawn only once during the stimulus duration

y_point = np.mod(t*v_line, length_motion) - length_motion/2

def tacDirVal(dir, x_point, y_point, t):
    if dir == "NONE":
        x_pos = x_point*0
        y_pos = y_point*0
    if dir == "UP":
        x_pos = x_point
        y_pos = y_point

    if dir == "DOWN":
        x_pos = x_point
        y_pos = -y_point
        
    if dir == "RIGHT":
        x_pos = y_point
        y_pos = x_point
        
    if dir == "LEFT":
        x_pos = -y_point
        y_pos = x_point
                
    z_pos = np.ones_like(x_pos)*0.1 #10cm above array
                ###

    # The wrapper takes double as input, so we will create the appropriate casting type, length included
    arr_t = ctypes.c_double * len(t) #type are defined using ctypes

    #casting x,y and z position
    xc = arr_t(*x_pos)
    yc = arr_t(*y_pos)
    zc = arr_t(*z_pos)

    # we send the casted vector positions to the device, specificing how long the vectors are
    res = prg.set_positions(xc, yc, zc, (len(t)))
    print(res) #res is the length of the data received

    return x_pos, y_pos, z_pos, arr_t, xc, yc, zc, res

    
stimulus_onset=core.Clock()    
stimulus_duration = 0.5 #0.1s

visOpacity=[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
tacVal=['NONE', 'RIGHT','NONE', 'RIGHT', 'NONE', 'RIGHT', 'NONE', 'RIGHT','NONE', 'RIGHT'] #direction values


for iTrial in range(9):
    stimulus_onset.reset()
    # Start the trial
    while stimulus_onset.getTime() < stimulus_duration:
        polygon.setOpacity(visOpacity[iTrial])
        dir = tacVal[iTrial]
        tacDirVal(dir, x_point, y_point, t)
        polygon.draw()
        win.flip()
        prg.play_sensation(2)
        
        

    