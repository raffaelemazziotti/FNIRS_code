# FNIRS Stimulation Routines

This is the code used to stimulate adults and children with radial checkerboard blended with animated cartoons.

## Requirements

This code relies on a number of external libraries:

* [OpenCV](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
* [ffpyplayer](https://pypi.org/project/ffpyplayer/)
* [LabStreaming Layer](https://github.com/sccn/labstreaminglayer)
* [Psychopy](https://www.psychopy.org/)
* [Numpy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)

Prior to run the code all the libraries should be installed.
The recording system must be connected on the same network to be visible. Connection should be set up in accordance with the recording system configuration.
We use a NIRSport 8x8 with Aurora Software 14.0.
This is the configuration for our system:

```python
info = StreamInfo(name = "Trigger", type = "Markers",
                  channel_count=1, channel_format='int32',
                  source_id='Aurora')
outlet = StreamOutlet(info)
```

With this configuration you can send triggers to the recording system using the command:

```python
outlet.push_sample(['event name'])
```

![radial checkerboard]( "Contrast reversal radial checkerboard stimulus")