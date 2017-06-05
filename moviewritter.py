"""
===========
MovieWriter
===========
This example uses a MovieWriter directly to grab individual frames and write
them to a file. This avoids any event loop integration, but has the advantage
of working with even the Agg backend. This is not recommended for use in an
interactive setting.

"""

import numpy as np # numeric library
import matplotlib # graphic library
matplotlib.use("Agg")
import matplotlib.pyplot as plt # plot library
import matplotlib.animation as manimation # animation library

FFMpegWriter = manimation.writers['ffmpeg'] # requires ffmpeg installed to run
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)


"""
CREATE FIGURE AND SET AXIS LIMITS
"""
fig = plt.figure() # create a figure to draw on
reddata, = plt.plot([], [], 'ro') # plot red particles
bluedata, = plt.plot([], [], 'bo') # plot blue particles

# set axis limits, aspect ratio and title
TITLE = 'Biased Gaussian Random Walkers'
maxX = 10
minX = 0
maxY = 10
minY = 0
plt.xlim(minX, maxX)
plt.ylim(minY, maxY)
plt.gca().set_aspect('equal', adjustable='box')
plt.title(TITLE)

"""
GENERATE DATA
"""
# number of particles
Nred = 50
Nblue = 50

# initial coordinates of red particles
xredvec = (maxX - minX)/2 + (np.random.rand(Nred) - 0.5)*maxX*0.2
yredvec = (maxY - minY)/2 + (np.random.rand(Nred) - 0.5)*maxY*0.2

# initial coordinates of blue particles
xbluevec = (maxX - minX)/2 + (np.random.rand(Nblue) - 0.5)*maxX*0.2
ybluevec = (maxY - minY)/2 + (np.random.rand(Nblue) - 0.5)*maxY*0.2

# distance traveled per tick
redSpeed = 0.05
bluespeed = 0.10
redxbias = 0.01
bluexbias = -0.01


# open output file.
# Parameters are figure to be drawn, filename and dpi (quality, higher = better)
with writer.saving(fig, TITLE, dpi=100):
    for i in range(1000):
        # perform a gaussian random step
        dxredvec = np.random.randn(Nred)*redSpeed + redxbias
        dyredvec = np.random.randn(Nred)*redSpeed
        dxbluevec = np.random.randn(Nblue)*bluespeed + bluexbias
        dybluevec = np.random.randn(Nblue)*bluespeed

        # restrict to square
        for n, (dxred, dyred) in enumerate(zip(dxredvec, dyredvec)):
            newredx = xredvec[n] + dxred
            newredy = yredvec[n] + dyred
            if newredx <= maxX and newredx >= minX:
                xredvec[n] = newredx
            if newredy <= maxY and newredy >= minY:
                yredvec[n] = newredy

        for n, (dxblue, dyblue) in enumerate(zip(dxbluevec, dybluevec)):
            newbluex = xbluevec[n] + dxblue
            newbluey = ybluevec[n] + dyblue
            if newbluex <= maxX and newbluex >= minX:
                xbluevec[n] = newbluex
            if newbluey <= maxY and newbluey >= minY:
                ybluevec[n] = newbluey

        reddata.set_data(xredvec, yredvec)
        bluedata.set_data(xbluevec, ybluevec)

        writer.grab_frame()
