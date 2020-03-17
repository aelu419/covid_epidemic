import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation

#initilaization
S, I, R, T = [], [], [], []
width = 2.0 #width of the graphed line
delay = 10 #in miliseconds
#https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
fig = plt.figure()
ax = plt.axes()
lineS, = ax.plot([], [], lw=width)
lineI, = ax.plot([], [], lw=width)
lineR, = ax.plot([], [], lw=width)


def refresh(i):
    #get data for frame i
    lineS.set_data(T[0:i], S[0:i])
    lineI.set_data(T[0:i], I[0:i])
    lineR.set_data(T[0:i], R[0:i])

    return lineS, lineI, lineR

def init():
    #get blank graph
    lineS.set_data([], [])
    lineI.set_data([], [])
    lineR.set_data([], [])
    return lineS, lineI, lineR

def sim(s, i, r, a, b, deltaT, step=.1):
    #setup
    global S, I, R, T

    #calculate data
    n = s + i + r
    T = []
    S, I, R = [s], [i], [r]

    ax.set_xlim(0, 1.2 * deltaT)
    ax.set_ylim(0, 1.2 * n)

    fr = int(deltaT / step)
    x = np.linspace(0, deltaT, fr) #generate evenly spaced x values
    for j in x: #for each x value, calculate corresponding SIR values
        k = len(S)
        S.append( S[k-1] - a/n * S[k-1] * I[k-1] * step )
        I.append( I[k-1] + ( a/n * S[k-1] * I[k-1] - b * I[k-1] ) * step )
        R.append( n - S[k] - I [k])
        T.append( j )
        #print(s, i, r, T)

    anim = animation.FuncAnimation(fig, refresh, init_func=init,
                               frames= fr, interval = delay, blit=True)


    plt.title('S-I-R Model'.format(step))


    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, bitrate=1800)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    anim.save('graph_animation.mp4', writer = writer)

    plt.show()

if(__name__=='__main__'):
    sim(10000, 1000, 19000, .618, 1/11, 60)
