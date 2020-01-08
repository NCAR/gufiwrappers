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
    y = []
    l = []
    for usr in getAllUsers( data ):
       y.append( np.array( data[usr + '_rw'] ) )
       l.append( usr )
    return d, y, l



def parseCmdLine( ):
    import cmdline as cmdl
    parser = cmdl.parserForGplot( )
    args = parser.parse_args()
    histfile = args.histfile
    return histfile


if __name__ == "__main__":
    histfile = parseCmdLine( )
    d, y, l = getData( histfile )

    plt.stackplot( d, y, labels = l )
    plt.xlim(0,20)
    plt.show()
