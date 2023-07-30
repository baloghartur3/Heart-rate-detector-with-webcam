import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

num=50
vid = cv2.VideoCapture(0)
x = np.arange(num)
r = np.zeros((num))
g = np.zeros((num))
b = np.zeros((num))
freq = np.fft.fftfreq(num)
fourierTransform = np.zeros((num))

x1,x2,y1,y2 = 100,200,200,380

# Create a figure and separate subplots for each channel
fig, (ax_r, ax_g, ax_b,ax_fft) = plt.subplots(4, 1)
line_r, = ax_r.plot(x, r, 'r', label='Red')
line_g, = ax_g.plot(x, g, 'g', label='Green')
line_b, = ax_b.plot(x, b, 'b', label='Blue')
line_fft, = ax_fft.plot(freq, fourierTransform)

while True:
    ret, frame = vid.read()
    subframe = frame[x1:x2,y1:y2]
    r = np.roll(r, -1)
    g = np.roll(g, -1)
    b = np.roll(b, -1)
    r[-1] = np.mean(subframe[:, :, 2])
    g[-1] = np.mean(subframe[:, :, 1])
    b[-1] = np.mean(subframe[:, :, 0])
    fourierTransform = np.fft.fft(g)

    #For some reason I have to remove the magnitude of the 0Hz component, not entirely sure why yet
    fourierTransform[0]=0 # Why does this work????

    # Update the plot data
    line_r.set_ydata(r)
    line_g.set_ydata(g)
    line_b.set_ydata(b)
    line_fft.set_ydata(np.abs(fourierTransform))
    # Redraw the plot
    fig.canvas.draw()
    # Ensure the lines stay within the plot frame
    ax_r.relim()
    ax_r.autoscale_view()
    ax_g.relim()
    ax_g.autoscale_view()
    ax_b.relim()
    ax_b.autoscale_view()
    ax_fft.relim()
    ax_fft.autoscale_view()

    plt.pause(0.01)
    cv2.rectangle(frame,(y1, x1),(y2, x2), (0, 255, 0), 3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()