#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

def getAllUsers( data ):
    """
    From DataFrame return the entity (user, project or directory) names
    """
    users = []
    for ele in data.columns:
       if ele.endswith('_w'):
          users.append( ele[:-2] )
    return users


def getData( histfile ):
    data = pd.read_csv( histfile )
    n = len(data['Year-mon'])
    d = np.arange(0,n)
    yr = []
    yw = []
    yrw = []
    l = []
#   dl = np.char.array( data['Year-mon'] )
    dl = data['Year-mon']
    for usr in getAllUsers( data ):
       yr.append( np.array( data[usr + '_r'] )/1.e+12 )
       yw.append( np.array( data[usr + '_w'] )/1.e+12 )
       yrw.append( np.array( data[usr + '_rw'] )/1.e+12 )
       l.append( usr )
    return d, dl, l, yr, yw, yrw

def plotRW( d, l, yrw ):
    plt.stackplot( d, yrw[:10], labels = l )
    plt.legend(loc='upper right')
    plt.xlim(0,10)
    plt.ylabel('TB')
    plt.xlabel('Months')
    plt.title('Read_time - write_time weighted by amount in TB')
    plt.tight_layout(pad=0)
    plt.show()

def plotW( d, l, yw, dl ):
    plt.stackplot( d, yw[:10], labels = l )
    plt.legend(loc='upper left')
    xmn = 576
    xmx = 600
    plt.xlim(xmn,xmx)
    plt.ylabel('TB')
    plt.xlabel('Yr-month')
    plt.title('Data written over past 12 months')
    plt.xticks(d[xmn:xmx:2],dl[xmn:xmx:2],rotation=25)
    plt.tight_layout(pad=0)
    plt.show()


def parseCmdLine( ):
    import cmdline as cmdl
    parser = cmdl.parserForGplot( )
    args = parser.parse_args()
    histfile = args.histfile
    return histfile


if __name__ == "__main__":
    histfile = parseCmdLine( )
    d, dl, l, yr, yw, yrw = getData( histfile )

    plotRW( d, l, yrw )
#   plotW( d, l, yr, dl )
#   plt.stackplot( d, yrw, labels = l )
#   plt.xlim(0,10)
#   plt.show()
