import matplotlib.pyplot as plt
import numpy as np

def read_file(file_name, speic_name):
    hist = []
    hist_temp = []
    hist_conv = []
    hist_count = []
    with open(file_name, 'r') as file:
        for line in file.readlines():
            if line[0:4] == 'Time':
                if hist_count != [] and hist_conv != []:
                    hist_temp.append(hist_count) 
                    hist_temp.append(hist_conv) 
                    hist.append(hist_temp)
                hist_count = []
                hist_conv = []
                hist_temp = []
                hist_temp.append(float(line.strip('Time (s): ')))
            else:
                string = '	' + str(speic_name) + ': '
                line = line.strip('. \n').split(string)
                if len(line) != 2:
                    print('Wrong species name!')
                    return 0
                else: 
                    hist_count.append(int(line[0]))
                    hist_conv.append(int(line[1]))
            hist_temp.append(hist_count) 
            hist_temp.append(hist_conv) 
            hist.append(hist_temp)
        return hist

def time_valid(file_name, t_i, t_f, speic_name):
    hist = read_file(file_name, speic_name)
    min_time = hist[0][0]
    max_time = hist[-1][0]
    if t_i == -1 and t_f == -1:
        return min_time, max_time 
    elif min_time <= t_i <= max_time and t_i <= t_f <= max_time:
        return t_i, t_f
    else:
        print('Wrong input time period!')
        return -1.0, -1.0

def hist_temp(file_name, t_i, t_f, speic_name):
    t_i, t_f = time_valid(file_name, t_i, t_f, speic_name)
    if t_i != -1 and t_f != -1:
        hist = read_file(file_name, speic_name)
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
        return plot_conv, plot_count_mean
    else:
        return 0

def hist_3d_time(file_name, t_i, t_f, speic_name, time_bins):
    t_arr = np.arange(t_i, t_f, (t_f-t_i)/time_bins)
    t_arr = np.append(t_arr, t_f)
    max_num = 0
    x_lst = []
    z_lst = []
    t_plt = np.zeros(time_bins)
    i = 0
    for i in range(0, len(t_arr)-1):
        t_plt[i] = (t_arr[i]+t_arr[i+1])/2
        x,z = hist_temp(file_name, t_arr[i], t_arr[i+1], speic_name)
        x_lst.append(x)
        z_lst.append(z)
        if max(x) > max_num:
            max_num = max(x)
    z_plt = np.zeros(shape = (max_num, time_bins))
    k = 0
    for i in x_lst:
        l = 0
        for j in i:
            z_plt[j-1, k] = z_lst[k][l]
            l += 1
        k += 1
    x_plt = np.arange(0, max_num, 1)+1
    
    xx, yy = np.meshgrid(x_plt, t_plt)
    X, Y = xx.ravel(), yy.ravel()
    Z = z_plt.ravel()
    bottom = np.zeros_like(Z)
    width = 1
    depth = 1/time_bins
    
    fig=plt.figure()
    ax=fig.gca(projection='3d')
    ax.bar3d(X, Y, bottom, width, depth, Z, shade=True)
    ax.set_xlabel('# of ' + speic_name + ' in sigle complex')
    ax.set_ylabel('Averaged Time')
    ax.set_zlabel('Count')
    plt.show()

    
hist_3d_time('histogram_complexes_time_dode.dat', 0, 1.0, 'dode', 20)