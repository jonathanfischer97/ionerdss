import matplotlib.pyplot as plt
import numpy as np
from read_file import read_file

def hist_mean(file_name):
    t_i = 0
    t_f = 1
    hist = read_file(file_name)
    plot_time = []
    plot_conv = []
    for i in hist:
        if t_i <= i[0] <= t_f:
            plot_time.append(i[0])
            plot_conv.append(np.mean(i[2]))
    plt.plot(plot_time, plot_conv)
    plt.title('Maximum Convergence')
    plt.xlabel('Time')
    plt.ylabel('Convergence')
    plt.show()
            
if __name__ == '__main__':
    hist_mean('histogram_complexes_time.dat')          