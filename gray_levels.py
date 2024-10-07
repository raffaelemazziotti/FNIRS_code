from psychopy import visual, core, event
import numpy as np

# Define the number of steps
number_of_steps = 10  # You can change this value or set it dynamically


win = visual.Window(size=[1920, 1080], fullscr=True, color=[-1, -1, -1], colorSpace='rgb')
instruction_text = visual.TextStim(win, text="Press any key to begin.", pos=(-0.5, -0.9), height=0.05, color=[1, 1, 1], colorSpace='rgb')
instruction_text.draw()
win.flip()
event.waitKeys()

for step in range(1, number_of_steps + 1):
    intensity = (2 * (step - 1) / (number_of_steps - 1)) - 1  
    grey_level = [intensity] * 3
    win.color = grey_level
    step_text = visual.TextStim(win, text=f"Step {step}/{number_of_steps} - Value:{np.round(intensity,2)}", pos=(-0.5, -0.9), height=0.05, color=[1, 1, 1], colorSpace='rgb')
    step_text.draw()
    win.flip()
    event.waitKeys()

win.close()
core.quit()
