from read_file import read_file

def input_time(file_name):
    hist = read_file(file_name)
    min_time = hist[0][0]
    max_time = hist[-1][0]
    t_i = float(input('\nInput the initial time(input -1 for a full-time period): '))
    if min_time <= t_i <= max_time:
        t_f= float(input('Input the final time: '))
        if t_i <= t_f <= max_time:
            return t_i, t_f
        else:
            choice = str(input('\nInvalid time, re-enter time? (y to re-enter, other keys to quit)'))
            if choice == 'y':
                input_time(file_name)
            else:
                return
    elif t_i == -1:
        return min_time, max_time
    else:
        choice = str(input('\nInvalid time, re-enter time? (y to re-enter, other keys to quit) '))
        if choice == 'y':
            input_time(file_name)
        else:
            return

if __name__ == '__main__':
    print(input_time('histogram_complexes_time.dat'))
