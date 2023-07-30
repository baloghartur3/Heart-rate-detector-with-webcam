import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

vid = cv2.VideoCapture(0)
x = np.linspace(0, 50., num=50)
r = np.zeros((50))
g = np.zeros((50))
b = np.zeros((50))

x1,x2,y1,y2 = 100,200,200,380

# Create a figure and separate subplots for each channel
fig, (ax_r, ax_g, ax_b) = plt.subplots(3, 1, sharex=True)
line_r, = ax_r.plot(x, r, 'r', label='Red')
line_g, = ax_g.plot(x, g, 'g', label='Green')
line_b, = ax_b.plot(x, b, 'b', label='Blue')

while True:
    ret, frame = vid.read()
    subframe = frame[x1:x2,y1:y2]
    r = np.roll(r, -1)
    g = np.roll(g, -1)
    b = np.roll(b, -1)
    r[-1] = np.mean(subframe[:, :, 2])
    g[-1] = np.mean(subframe[:, :, 1])
    b[-1] = np.mean(subframe[:, :, 0])

    # Update the plot data
    line_r.set_ydata(r)
    line_g.set_ydata(g)
    line_b.set_ydata(b)

    # Redraw the plot
    fig.canvas.draw()

    # Ensure the lines stay within the plot frame
    ax_r.relim()
    ax_r.autoscale_view()
    ax_g.relim()
    ax_g.autoscale_view()
    ax_b.relim()
    ax_b.autoscale_view()

    plt.pause(0.01)
    cv2.rectangle(frame,(y1, x1),(y2, x2), (0, 255, 0), 3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()