def badTimer(event,last):
    
    #find the current time
    import time 
    current = time.perf_counter()
    
    #print which event is running
    print(f'\nEvent: {event}')

    #print how long since previous time
    if not last == 0:
        print(f'Time to Run: {current-last}')
    

    #update last time
    last = current
    return last

