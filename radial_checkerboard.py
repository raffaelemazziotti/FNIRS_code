
# lsl: https://github.com/sccn/labstreaminglayer
from pylsl import StreamInfo, StreamOutlet
import time

# LabStreming Layer initialization to send events to NIRSport
info = StreamInfo(name="Trigger", type="Markers",
                  channel_count=1, channel_format='int32',
                  source_id='Example')
outlet = StreamOutlet(info)

# psychopy: https://www.psychopy.org/
from psychopy import visual, core, event
import movie_utils as utils

trial_number = 20 # Total Number of trials (* events) in sec
time_stim = 5 # Duration of checkerboard event in sec
time_blank = 10  # duration of intertrial time in sec
freq = 4 # Contrast reversal frequency in Hz 

events = [0,1] # events ID
triggers = [[1],[2]] # Trigger Labels for LSL
contrasts = [0, .9] # Stimulus contrast for each event [0 is baseline .9 is 90% contrast]


mywin = visual.Window(monitor="testMonitor", size =[800, 600],
                      units="deg",fullscr=True, color=0,
                      width=None,distance=70,gamma=2.1865)

mywin.mouseVisible = False

stim = visual.RadialStim(win=mywin, units="deg", size=(70, 70),contrast=.9,radialCycles=15, angularCycles=8)
fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)

stimulusTimer = core.Clock()
experimentTimer = core.Clock()


ttl = False
radial = False

trials = utils.trial_manager(ntrial=trial_number,evs=events)
period = 1/freq

# WAITs BEFORE THE START
print("WAIT FOR KEY...")
while True:
    if len(event.getKeys()) > 0:
        break
    event.clearEvents()
    time.sleep(.05)


stimulusTimer.reset()
experimentTimer.reset()
while True:
    exp = experimentTimer.getTime()
    cl = stimulusTimer.getTime()

    if ttl==False and exp >= time_blank:
        ttl = True
        radial = True
        if not trials.hasNext():
            print("End of Stimulation...")
            break
        ev = trials.next()
        stim.setContrast(contrasts[ev])
        outlet.push_sample(triggers[ev])
        print(ev, contrasts[ev])
        experimentTimer.reset()

    elif ttl and exp >= time_stim:
        ttl = False
        radial = False
        experimentTimer.reset()

    if radial:
        if ttl and cl > period:
            stim.setRadialPhase(.5, '+')
            stimulusTimer.reset()
        stim.draw()

    if len(event.getKeys()) > 0:
        break
    fixation.draw()

    mywin.flip()

mywin.mouseVisible = True