from psychopy import visual, event, core, gui, data
import os                           # for file/folder operations
import numpy.random as rnd          # for random number generators

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
response_duration = 1
ISI_duration = 2

trials = data.TrialHandler(directionList, nReps=3, extraInfo=exp_info,
                           method='random', originPath=datapath)

stimulus_onset = core.Clock()
rt_clock = core.Clock()
ISI_onset = core.Clock()
key_onset = core.Clock()

    
keys = event.getKeys(keyList=['left','right', 'up','down', 'escape', 'space'])

nDone = 0
for itrial in trials:
    print(itrial['dirVal'])
    # Set the clocks to 0
    stimulus_onset.reset()
    rt_clock.reset()
    ISI_onset.reset()
    key_onset.reset()
    # Start the trial
    while stimulus_onset.getTime() < stimulus_duration:
        rdk.setDir(itrial['dirVal'])
        fixSpot.draw()
        rdk.draw()
        win.flip()
        # For the stimulus duration,
        # Listen for the keys
    key_onset.reset()
    #rt_clock.reset()
    while key_onset.getTime() <= response_duration:
        keys = event.getKeys(keyList=['left','right', 'up','down', 'escape', 'space'])
        if len(keys) > 0:
            break
        
    # Analyze the keypress
    if keys:
        keyResponse = event.getKeys(keyList=['left','right', 'up','down', 'escape', 'space'])
        rt = rt_clock.getTime()
        '''if 'escape' in keys:
            # Escape press = quit the experiment
            break
        else:
            # arrow keys = collect responses; register response time
            keyResponse = keys #event.getKeys(keyList=['left','right', 'up','down', 'escape', 'space'])
            rt = rt_clock.getTime()'''

    else:
        # No press = missed trial; maximal response time
        keyResponse = 0
        rt = 0
        
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

'''# Write summary data to screen
trials.printAsText(stimOut=['sf', 'ori'],
                   dataOut=['RT_mean', 'RT_std', 'choice_raw'])

# Write summary data to a text file ...
trials.saveAsText(fileName='testData',
                  stimOut=['sf', 'ori'],
                  dataOut=['RT_mean', 'RT_std', 'choice_raw'])

# ... or an xlsx file (which supports sheets)
trials.saveAsExcel(fileName='testData',
                   sheetName='rawData',
                   stimOut=['sf', 'ori'],
                   dataOut=['RT_mean', 'RT_std', 'choice_raw'])

# Save a copy of the whole TrialHandler object, which can be reloaded later to
# re-create the experiment.
trials.saveAsPickle(fileName='testData')

# Wide format is useful for analysis with R or SPSS.
df = trials.saveAsWideText('testDataWide.txt')'''

