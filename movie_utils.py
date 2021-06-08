from psychopy.visual import filters
from psychopy import visual, event, core
import numpy as np
import cv2
import random


def radial_checkerboard_mask(phi=0, rcycles=8, tcycles=20, res=1024):
    radius = filters.makeRadialMatrix(res)
    #radius = filters.maskMatrix(radius,) # circular radius mask
    [x, y] = np.meshgrid(np.linspace(-1, 1, res), np.linspace(-1, 1, res))
    checks = np.sign(np.sin(radius * 2 * np.pi * rcycles / 2)) * np.sign(np.sin(np.arctan2(x, y) * tcycles / 2 + phi))
    return checks


# Function taken from https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table)

def scale(arr):
    arr = arr - np.mean(arr)
    return arr / np.max(np.abs(arr))

def trials(loops=10,evs=[0,1]):
    t_ev = []
    res = list()
    while True:
        if len(t_ev)==0:
            if loops==0:
                break
            t_ev = evs.copy()
            loops -= 1
        random.shuffle(t_ev)
        res.append(t_ev.pop())
    return res

class trial_manager():

	def __init__(self,ntrial=10,evs=[0,1],verbose=True):
		self.__ntrial = ntrial * len(evs)
		self.__counter = {k:0 for k in evs}
		self.__evs = evs
		self.__trialvec = trials(ntrial,evs)
		self.verbose = verbose

	def next(self):
		self.__ntrial -= 1
		temp = self.__trialvec.pop()
		self.__counter[temp] += 1
		if self.verbose:
			print("Trial: " + str(temp) + " Rep: " + str(self.__counter[temp]) + " ToDo: " + str(self.__ntrial))
		return temp

	def hasNext(self):
		return len(self.__trialvec)>0

	def todo(self):
		return self.__ntrial

	def reps(self,k):
		return self.__counter[k]

# Function taken from https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
def auto_canny(image, sigma=0.99):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged



if __name__ == "__main__":
	tm = trial_manager(10,[1,2])
	while  tm.hasNext():
		print(tm.hasNext())
		val = tm.next()
		print(val,tm.todo(),tm.reps(val))
