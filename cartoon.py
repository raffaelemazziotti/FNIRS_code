# fusion between a cartoon and radstim

# lsl: https://github.com/sccn/labstreaminglayer
from pylsl import StreamInfo, StreamOutlet
info = StreamInfo(name = "Trigger", type = "Markers",
                  channel_count=1, channel_format='int32',
                  source_id='Aurora')
outlet = StreamOutlet(info)
triggers = [[1],[2]]
# ffpyplayer: https://pypi.org/project/ffpyplayer/
from ffpyplayer.player import MediaPlayer
# OpenCV: https://docs.opencv.org/master/d6/d00/tutorial_py_root.html
import cv2
import numpy as np
import movie_utils as utils

#psychopy: https://www.psychopy.org/
from psychopy import core
#matplotlib:
import matplotlib.pyplot as plt
import os


number_of_trials = 20 # Number of stimulations (contrast inversion) and blank (no changes in contrast) trials [the total number of trigger delivered is number_of_trials * 2]
intertrial = 10 # intertrial duration in secs
# stimulation duration in secs
tex_dur = 5 # stimulation duration in secs
start_sec = 1 # Start the movie from  this second

stim_freq = 4  # Frequency in Hz of stimulus contrast inversion
cnt_stim = .9 # image contrast during stimulation [0 to 1]
cnt_baseline = .2 # image contrast during baseline [0 to 1]
luminance = .5 # mean luminance [0 to 1]
gamma = 2.1865 # monitor gamma correction

moviename = "ReLeone_edited" # movie file name [.mp4]
# the script assumes that a folder called 'movies' exists 


#######################################################

filename = r'movies' + os.sep + moviename + ".mp4"
print(filename)

stimulation_duration = ( intertrial + tex_dur ) * number_of_trials * 2

font= cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,400)
fontScale= 1
fontColor= (255,255,255)
lineType= 2


ttl = False
radial = False
ph = False
period = (1/stim_freq)/2
nframe = 0
cnt = cnt_baseline

experiment_time = core.Clock()
tex_time = core.Clock()
loop_time = core.Clock()
total_time = core.Clock()

events = [0,1]
trials = utils.trial_manager(number_of_trials,events)

player = MediaPlayer(filename)

cv2.namedWindow('frame', cv2.WINDOW_FREERATIO)
#cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

intertime = list()
prevframe = None


player.seek(start_sec, accurate=False)
frame, val = player.get_frame()
while frame is None or frame[0] is None:
    frame, val = player.get_frame()
    core.wait(.1)

metadata = player.get_metadata()
print("Total Duration of session in secs: {}".format(stimulation_duration))
print("Movie duration in sec: ", metadata["duration"], "Movie duration in min:", metadata["duration"]/60)
msg = "StD: {} sec - {} min".format(np.round(stimulation_duration,2), np.round(stimulation_duration/60,2))
msg2 = "MoD: {} sec - {} min".format(np.round(metadata["duration"],2), np.round(metadata["duration"]/60,2) )
if stimulation_duration > metadata["duration"]:
    raise Exception('Stimulation duration too long')

img, t = frame
w = img.get_size()[0]
h = img.get_size()[1]
#arr = np.ones((512,512)) * 0.5

arr = np.asarray(frame[0].to_bytearray()[0]).reshape(h, w, 3)
arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
arr = cv2.resize(arr, (512, 512), interpolation=cv2.INTER_AREA)  # resize to 512x512
arr = utils.scale(arr) * luminance
arr = (luminance + (arr * cnt))*255
cv2.putText(arr, "Push SPACE to Start...", (bottomLeftCornerOfText[0], bottomLeftCornerOfText[1]-30), font, fontScale, fontColor, lineType)
cv2.putText(arr, msg, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
cv2.putText(arr, msg2, (bottomLeftCornerOfText[0], bottomLeftCornerOfText[1]+30), font, fontScale, fontColor, lineType)

cv2.imshow('frame', utils.adjust_gamma(arr.astype('uint8'), gamma=gamma))

player.toggle_pause()
while True:
    if cv2.waitKey(10) == 32:
        break
player.toggle_pause()

# load the stimulus in range -1 to 1
radialTexture = utils.radial_checkerboard_mask(res=512)
radialTexture1 = utils.radial_checkerboard_mask(res=512, phi=np.pi)


tex_time.reset()
experiment_time.reset()
loop_time.reset()
while val != 'eof':
    exp = experiment_time.getTime()
    cl = tex_time.getTime()

    frame, val = player.get_frame()
    if frame is None:
        print("is_none")
        continue
    else:
        img, t = frame
        prevframe = img

    if w==None or h==None:
        w = img.get_size()[0]
        h = img.get_size()[1]

    arr = np.asarray(frame[0].to_bytearray()[0]).reshape(h, w, 3)
    arr = cv2.resize(arr, (512, 512), interpolation=cv2.INTER_AREA)  # resize to 512x512

    if radial:
        arr = utils.auto_canny(arr) / 255   # Edge detection
        arr = arr.astype(float)  # Float tranform
    else:
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        arr = utils.scale(arr) * luminance

    if ttl == False and exp >= intertrial: # at the end of baseline
        ttl = True
        experiment_time.reset()
        if not trials.hasNext():
            break #
        ev = trials.next()
        outlet.push_sample(triggers[ev])
        if ev==1:
            cnt = cnt_stim
            radial = True
    elif ttl and exp >= tex_dur and ph==False: # at the end of stimulation
        ttl = False
        experiment_time.reset()
        cnt = cnt_baseline # unComment this for abrupt return to baseline contrast
        radial = False

    if radial:
        if ttl and cl > period:
            ph = not ph
            tex_time.reset()

        if ph:
            texture = radialTexture * luminance
        else:
            texture = radialTexture1 * luminance
    else:
        if cnt > cnt_baseline:
            cnt -= 0.01


    if radial:
        arr = arr * texture * -1  # edges of the opposite polarity respect to texture
        arr = np.where(arr == 0, texture, arr)


    arr = (luminance + (arr * cnt)) * 255

    cv2.imshow('frame', utils.adjust_gamma(arr.astype('uint8'), gamma=gamma))
    ltime =int( 40-loop_time.getTime() )
    intertime.append(loop_time.getTime())
    loop_time.reset()
    key = cv2.waitKey(ltime if ltime > 0 else 1)
    if key == 27: # ESC
        break
    elif key == 32:
        player.toggle_pause()
        while True:
            if cv2.waitKey(10) == 32:
                break
        player.toggle_pause()
        ttl = False
        experiment_time.reset()
        radial = False


cv2.waitKey(10)
cv2.destroyAllWindows()

plt.plot(intertime)
plt.show()

