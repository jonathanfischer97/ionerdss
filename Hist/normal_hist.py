import matplotlib.pyplot as plt
from read_file import read_file

def hist_period(file_name):
    t_i = 0.9
    t_f = 1
    hist = read_file(file_name)
    plot_count = []
    plot_conv = []
    tot = 0
    for i in hist:
        if t_i <= i[0] <= t_f:
            tot += 1
            for j in i[2]:
                if j not in plot_conv:
                    plot_conv.append(j)
                    plot_count.append(i[1][i[2].index(j)])
                else:
                    index = plot_conv.index(j)
                    plot_count[index] += i[1][i[2].index(j)]
    plot_count_mean = []                
    for i in plot_count:
        plot_count_mean.append(i/tot)
    print('Start time(s): ', t_i)
    print('End time(s): ', t_f)
    print('Occurring convergence: ', plot_conv)
    print('Occurring probabilities: ', plot_count_mean)
    plt.bar(plot_conv, plot_count_mean)
    plt.title('Histogram over a Certian Time Period')
    plt.xlabel('Convergence')
    plt.ylabel('Count')
    plt.show()
    
if __name__ == '__main__':
    hist_period('histogram_complexes_time.dat')