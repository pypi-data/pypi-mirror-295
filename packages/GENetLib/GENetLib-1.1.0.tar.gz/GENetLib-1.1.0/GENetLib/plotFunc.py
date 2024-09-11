from GENetLib.plotFD import plotFD


def plotFunc(x, y = None, xlab = None, ylab = None):

    tofunc = x
    if y == None:
        plotFD(tofunc, xlab, ylab)
    else:
        plotFD(tofunc, y, xlab, ylab)

