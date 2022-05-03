import psychtoolbox as ptb
from psychopy import visual, event, data, core, sound
from random import *

sample_sound = sound.Sound('I.wav')

ws = [1536, 864]
black = [-1,-1,-1]

def wp(position):
    return [position[0]/ws[0],position[1]/ws[1]]

def drawlines(_lines):
    for line in _lines:
        line.draw()

win = visual.Window(ws,[30,30],color=black, fullscr=True)

stim_text = 'Loud / Small'
message = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = stim_text) 
message.draw()
win.flip()

event.waitKeys()

linelength = 30
lines = [visual.Line(win, start=wp([0,linelength]), end=wp([0,-linelength])),
        visual.Line(win, start=wp([linelength,0]), end=wp([-linelength,0]))]
        
drawlines(lines)
        
win.flip()
nextFlip = win.getFutureFlipTime(clock='ptb')
sample_sound.play(when=nextFlip)

core.wait(2)

select_text = '1 / 2'
select_message = visual.TextStim(win, font='Malgun Gothic', color = 'white', text = select_text) 
select_message.draw()

win.flip()

event.waitKeys()

win.close()