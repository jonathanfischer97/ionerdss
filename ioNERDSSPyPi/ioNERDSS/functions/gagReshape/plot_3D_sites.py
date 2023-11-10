import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_3D_sites(positionsVec, COM_index):
    fig = plt.figure(1)
    color_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    ax = plt.axes(projection="3d")
    for i in range(len(COM_index)):
        ax.scatter(positionsVec[COM_index[i]][0], positionsVec[COM_index[i]][1],positionsVec[COM_index[i]][2], color=color_list[i % 9])
        # ax.text(positionsVec[i][0][0], positionsVec[i][0][1],
        #         positionsVec[i][0][2], unique_chain[i], color='k')
        next_COM_index = COM_index[i+1] if i+1 < len(COM_index) else len(positionsVec)
        for j in range(COM_index[i]+1, next_COM_index):
            figure = ax.plot([positionsVec[COM_index[i]][0], positionsVec[j][0]],
                             [positionsVec[COM_index[i]][1], positionsVec[j][1]],
                             [positionsVec[COM_index[i]][2], positionsVec[j][2]], color=color_list[i % 9])
    ax.set_xlabel('x (nm)')
    ax.set_ylabel('y (nm)')
    ax.set_zlabel('z (nm)')
    plt.show()
    return 0