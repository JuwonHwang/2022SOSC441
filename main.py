import psychtoolbox as ptb
from psychopy import visual, event, data, core, sound
from random import *
import csv
from datetime import datetime

class Condition:
    def __init__(self):
        self.loudness = [0,1] # 0 : loud , 1 : soft
        self.intensity = [1,2,3,4,5]
        self.repetition = [1,2,3,4,5,6]
        self.cases = [tuple([i,j,k]) for i in self.loudness for j in self.intensity for k in self.repetition]
        shuffle(self.cases)

sample_sound = [sound.Sound('sounds/s'+str(i)+'.wav') for i in range(5)]
ws = [1536, 864]
win = visual.Window(ws,[30,30],color='black', fullscr=True)
now = datetime.now().strftime('%m_%d %H_%M')

def wp(position):
    return [position[0]/ws[0],position[1]/ws[1]]

def drawlines(_lines):
    for line in _lines:
        line.draw()

def imagine(_lines, wait_time):
    drawlines(_lines)
    win.flip()
    core.wait(wait_time)
   
def waitEsc():
    keys = event.waitKeys() # until button press
    if 'escape' in keys:
        win.close()
        exit()
 

linelength = 60
lines = [visual.Line(win, start=wp([0,linelength]), end=wp([0,-linelength]), lineColor='white'),
        visual.Line(win, start=wp([linelength,0]), end=wp([-linelength,0]), lineColor='white')]

redlines = [visual.Line(win, start=wp([0,linelength]), end=wp([0,-linelength]), lineColor='red'),
        visual.Line(win, start=wp([linelength,0]), end=wp([-linelength,0]), lineColor='red')]

select_message = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = '1  2  3  4  5', height=0.2)

cnd = Condition()

def isloud(a):
    return 'loud' if a == 0 else 'soft'

def block(writer):
    for loudness, intensity, repetition in cnd.cases:
        # loudness imagery cue determination 
        message = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = isloud(loudness), height=0.3)
        message.draw()
        win.flip()
        waitEsc()
        
        for i in range(repetition): # repetetion
            imagine(lines, 0.5) # cross line
            win.flip()
            core.wait(0.5)
    
        imagine(redlines, 1) # cross red line
        win.flip()
        
        # play sound 
        nextFlip = win.getFutureFlipTime(clock='ptb')
        sample_sound[intensity-1].play(when=nextFlip)
        core.wait(0.3)
        
        # select level
        
        select_message.draw()
        win.flip()
        judgement = event.waitKeys(keyList=['1','2','3','4','5'], modifiers=False)[0]
        # csv write
        writer.writerow({'loudness': isloud(loudness),
                         'intensity': intensity,
                         'repetition': repetition,
                         'judgement': int(judgement)})
    return 0    
        
        
textBox = visual.TextBox2(win, text = '', font='Malgun Gothic', color = 'white'
                       , borderColor = 'white', editable=True, alignment='center', letterHeight=0.2)
textBox.draw()
win.flip()

keys = [] # until button press
while 'return' not in keys:
    keys = event.getKeys()
    textBox.draw()
    win.flip()

sample_text = 'We will present you with 5 levels of sound of increasing magnitude.'
sample_massage = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = sample_text, height=0.15)
sample_massage.draw()
win.flip()

waitEsc()

for i in cnd.intensity:
    intensity_massage = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = str(i), height=0.5)
    intensity_massage.draw()
    win.flip()
    nextFlip = win.getFutureFlipTime(clock='ptb')
    sample_sound[i-1].play(when=nextFlip)
    core.wait(0.5)
    win.flip()
    core.wait(0.5)

waitEsc()

name = textBox.text.replace('\n','')
with open('result/' + name + '_' + now + '.csv', 'w', newline='') as csvfile:
    fieldnames = ['loudness', 'intensity', 'repetition', 'judgement']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    block(writer)

# close
win.close()
exit()