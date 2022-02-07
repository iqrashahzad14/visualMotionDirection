'''
Psychopy Experiment
Visual Motion Direction Discrimination Task
Exp design: 2 hand positions/Blocks X 4 directions/Trials
RDKs move in 4 translational directions
Task- press the arrow keys relevant for each direction
record the response accuracy and reaction time 
-Iqra Shahzad'''


from psychopy import visual, event, core, gui, data
import os                           # for file/folder operations
import numpy as np          
from psychopy.hardware import keyboard
import random, os, csv


#setting a global sut down key = escape
event.globalKeys.add(key='escape', func=core.quit, name='shutdown')

exp_name = "RDKMotionDirection"
info = {'subNb':'','sessionNb':'','handedness':""}
if not gui.DlgFromDict(info, order=['subNb', 'sessionNb', 'handedness']).OK:      
    core.quit()  
#log
log_path = '/Users/shahzad/Documents/PsychopyExpt/myPsychopyhapticsexpt/visMotinDirecJupyter/data/'+'sub'+ info['subNb']+'_'+ data.getDateStr(format="%Y-%m-%d-%H%M")
log = open(log_path+".csv",'w')  
writer = csv.writer(log, delimiter=";")
cols="subNb","blockNb","handPos","trialNb","trialDirection","respKey","RT", "accuracy"
writer.writerow(cols)

#set the screen
win = visual.Window(size=[1536, 960], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

#stimuli

fixCross = visual.ShapeStim(win,vertices='cross',units='pix', size=(10,10),color='black',ori=0, pos=(0, 0),
    lineWidth=1,     colorSpace='rgb',  lineColor=[1,1,1], fillColor=[1,1,1],
    opacity=1, depth=-1.0, interpolate=True)

rdk = visual.DotStim(win,units='pix', 
    nDots=50, dotSize=20,
    speed=4, dir=1.0,  coherence=1.0,
    fieldPos=(0.0, 0.0), fieldSize=(800,800),fieldShape='circle',
    signalDots='same', noiseDots='position',dotLife=10,
    color=[1.0,1.0,1.0], colorSpace='rgb', opacity=1,
    depth=0.0, name='',autoLog=True)

ISI = visual.TextStim(win,text=" ")

block_message=visual.TextStim(win)

#set the keyboard
kb = keyboard.Keyboard()

#constants
if int(info['subNb']) % 2 == 0:
    handPos = ['palmup','palmdown']
else:
    handPos = ['palmdown','palmup'] 

nBlocks = 2

stimulus_duration = 1
response_duration = 2
ISI_duration = 2

#set the clocks
stimulus_onset = core.Clock()
key_onset = core.Clock()
ISI_onset = core.Clock()

dirVal=[0.0, 180.0, 90.0, -90.0] #direction values


for iBlock in range(nBlocks):
        textBlock=handPos[iBlock]
        block_message.setText(textBlock)
        block_message.draw()
        win.flip() 
        keys = event.waitKeys(keyList=['space']) # Wait for a spacebar press to start the trial
        np.random.shuffle(dirVal) #list of directions shuffled in each block
    
        for iTrial in range(4):
            print(dirVal[iTrial])
            # Set the clocks to 0
            stimulus_onset.reset()
            key_onset.reset()
            kb.clock.reset()  # when you want to start the timer from
            ISI_onset.reset() 
            keys = kb.getKeys(['right', 'left', 'up','down'])
            # Start the trial
            while stimulus_onset.getTime() < stimulus_duration:
                rdk.setDir(dirVal[iTrial])
                fixCross.draw()
                rdk.draw()
                win.flip()
                # For the stimulus duration,
                # Listen for the keys
            while key_onset.getTime() <= response_duration:
                keys = kb.getKeys(['right', 'left', 'up','down', 'escape'])
                if len(keys) > 0:
                    break
            for key in keys:
                keyResponse = key.name
                rt= key.rt
                print(key.name, key.rt)
                #analyse responses
                if dirVal[iTrial] == 0.0 and keyResponse == 'right':
                    accu =1
                elif dirVal[iTrial] == 180.0 and keyResponse == 'left':
                    accu =1
                elif dirVal[iTrial] == 90.0 and keyResponse == 'up':
                    accu =1
                elif dirVal[iTrial] == -90.0 and keyResponse == 'down':
                    accu =1
                else:
                    accu = 0

                #
                row=info['subNb'],iBlock+1,textBlock,iTrial+1,dirVal[iTrial],keyResponse,rt, accu
                writer.writerow(row)
          
            while ISI_onset.getTime() < ISI_duration:
                ISI.draw()
                win.flip()
                            
        
        win.flip()
        core.wait(1)

# Quit the experiment
win.close()
