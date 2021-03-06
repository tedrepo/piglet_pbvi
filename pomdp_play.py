# -*- encoding: utf-8 -*-
"""Run pbvi and naive_pbvi on a POMDP defined in AIMA."""

# This is messy, because it's my scratch file.

import matplotlib
matplotlib.use('GTK3Agg')
from matplotlib import pyplot as plt
import numpy as np

import pbvi
import naive_pbvi

# POMDP definition adapted from:
# Stuart Russell, Peter Norvig. Artificial Intelligence: A Modern Approach. 3rd
# ed., 2010.

#                s0   s1
cT = np.array([[            # s0
                [0.9, 0.1],     # as
                [0.1, 0.9]],    # ag
               [            # s1
                [0.1, 0.9],     # as
                [0.9, 0.1]]])   # ag

#               as   ag
cR = np.array([[0.0, 0.0],      # s0
               [1.0, 1.0]])     # s1

#                    o0   o1
cOmega = np.array([[            # a0
                    [0.6, 0.4],     # s' = s0
                    [0.4, 0.6]],    #      s1
                   [            # a1
                    [0.6, 0.4],     #      s0
                    [0.4, 0.6]]])   #      s1

gamma = 1.0


apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)

V = np.zeros((1, 2), np.float64)

B = np.array([[0.5, 0.5],
              [0.5, 0.5]])

b1 = np.linspace(0.1, 0.9, 8)
B = np.stack([1 - b1, b1], axis=-1)

if __name__ == '__main__':
    V = pbvi.run(apbvi, V, B, 5, 4)
    fig, ax = plt.subplots()
    for v in V:
        ax.plot([0, 1], v)
    plt.show()


    apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)
    B = np.array([[0.7, 0.3]])

    for _ in xrange(4):
        B = apbvi.expanded_B(B)
        print B

    print 'NAIVE'

    anpbvi = naive_pbvi.NaivePBVI(cT, cOmega, cR, gamma)
    nB = np.array([[0.7, 0.3]])

    for _ in xrange(0):
        nB = anpbvi.expanded_B(nB)
        print nB

    print len(B), len(nB)

    for _ in xrange(0):
        Gamma   = apbvi.Gamma(V)
        Epsi    = apbvi.Epsi(B, Gamma)
        V       = apbvi.V(Epsi, B)
        print V

    anpbvi = naive_pbvi.NaivePBVI(cT, cOmega, cR, gamma)

    nV = np.zeros((1, 2), np.float64)
    V  = np.zeros((1, 2), np.float64)

    for _ in xrange(0):
        nGamma  = anpbvi.Gamma(nV)
        nEpsi   = anpbvi.Epsi(B, nGamma)
        nV      = anpbvi.V(nEpsi, B)

    print "\nV\n", nV

    for i in xrange(0):
        print "\n== Round %d ==" % i
        print "GAMMA"
        nGamma = anpbvi.Gamma(nV)
        print nGamma
        Gamma = apbvi.Gamma(V)
        print Gamma

        print "EPSILON"
        nEpsi = anpbvi.Epsi(B, nGamma)
        print nEpsi
        Epsi = apbvi.Epsi(B, Gamma)
        print Epsi

        print "V"
        nV = anpbvi.V(nEpsi, B)
        print nV
        V = apbvi.V(Epsi, B)
        print V
