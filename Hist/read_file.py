def read_file(file_name):
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
                line = line.strip('. \n').split('	clat: ')
                hist_count.append(int(line[0]))
                hist_conv.append(int(line[1]))
        hist_temp.append(hist_count) 
        hist_temp.append(hist_conv) 
        hist.append(hist_temp)
    return hist

if __name__ == '__main__':
    read_file('histogram_complexes_time.dat')