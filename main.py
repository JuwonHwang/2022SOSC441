import psychtoolbox as ptb
from psychopy import visual, event, data, core, sound
from random import *

sample_sound = sound.Sound('I.wav')
ws = [1536, 864]
black = [-1,-1,-1]
wait_time = 0.5
win = visual.Window(ws,[30,30],color=black, fullscr=True)

loudness = [1,2,3,4,5]
test_loundness = randint(1,5)

def wp(position):
    return [position[0]/ws[0],position[1]/ws[1]]

def drawlines(_lines):
    for line in _lines:
        line.draw()

def imagine(_win,_lines):
    drawlines(_lines)
    _win.flip()
    core.wait(wait_time)
    _win.flip()
    core.wait(wait_time)
    

linelength = 30
lines = [visual.Line(win, start=wp([0,linelength]), end=wp([0,-linelength])),
        visual.Line(win, start=wp([linelength,0]), end=wp([-linelength,0]))]
stim_text = 'Loud / Soft'
message = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = stim_text) 
select_text = loudness
select_message = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = select_text) 

# select loud or small
message.draw()
win.flip()
event.waitKeys()

# random flash
n = randint(1,6)
for i in range(n):
    imagine(win,lines)
    
# play sound 
nextFlip = win.getFutureFlipTime(clock='ptb')
sample_sound.play(when=nextFlip)
core.wait(2)

# select level

select_message.draw()
win.flip()
timer = core.Clock()
keys = event.waitKeys(keyList=['1','2','3','4','5'], modifiers=False, timeStamped=timer)
print(keys)

# close
win.close()