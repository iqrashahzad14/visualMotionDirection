from psychopy import visual, event, core, gui, data
import os                           # for file/folder operations
import numpy.random as rnd          # for random number generators
from psychopy.hardware import keyboard


#setting a global sut down key = escape
event.globalKeys.add(key='escape', func=core.quit, name='shutdown')

datapath = 'data'
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'RDK Direction'
exp_info = {
            'participantID': '',
            'participantName': '',
            'gender': '',
            'age':'',
            'handedness': '',
            
            }
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()

# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participantID'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)

win = visual.Window(
    size=[1536, 960], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

fixSpot = visual.ShapeStim(win,vertices='cross',units='pix', size=(10,10),color='black',ori=0, pos=(0, 0),
    lineWidth=1,     colorSpace='rgb',  lineColor=[1,1,1], fillColor=[1,1,1],
    opacity=1, depth=-1.0, interpolate=True)

rdk = visual.DotStim(
    win,units='pix', 
    nDots=50, dotSize=20,
    speed=4, dir=1.0,  coherence=1.0,
    fieldPos=(0.0, 0.0), fieldSize=(800,800),fieldShape='circle',
    signalDots='same', noiseDots='position',dotLife=10,
    color=[1.0,1.0,1.0], colorSpace='rgb', opacity=1,
    depth=0.0, name='',autoLog=True)

ISI = visual.TextStim(win,text=" ",color='red', height=20)

directionList= [{'dirName': 'LEFT', 'dirVal': 180.0}, {'dirName': 'RIGHT', 'dirVal': 0.0}, {'dirName': 'UP', 'dirVal': 90.0}, {'dirName': 'DOWN', 'dirVal': -90.0}]
#rnd.shuffle(directionList)

stimulus_duration = 1
response_duration = 2
ISI_duration = 2

trials = data.TrialHandler(directionList, nReps=3, extraInfo=exp_info,
                           method='random', originPath=datapath)

stimulus_onset = core.Clock()
rt_clock = core.Clock()
ISI_onset = core.Clock()
key_onset = core.Clock()

kb = keyboard.Keyboard()

nDone = 0
for itrial in trials:
    print(itrial['dirVal'])
    # Set the clocks to 0
    stimulus_onset.reset()
    ISI_onset.reset()
    key_onset.reset()
    kb.clock.reset()  # when you want to start the timer from
    keys = kb.getKeys(['right', 'left', 'up','down'])
    # Start the trial
    while stimulus_onset.getTime() < stimulus_duration:
        rdk.setDir(itrial['dirVal'])
        fixSpot.draw()
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
        print(key.name, key.rt, key.duration)
  
    while ISI_onset.getTime() < ISI_duration:
        ISI.draw()
        win.flip()
        
    # Add the current trial's data to the TrialHandler

    trials.data.add('rt', rt)  # add the data to our set
    trials.data.add('keyResponse', keyResponse)
 
    nDone += 1

    # Advance to the next trial


#======================
# End of the experiment
#======================

# Save all data to a file
trials.saveAsWideText(data_fname + '.csv', delim=',')

# Quit the experiment
win.close()
