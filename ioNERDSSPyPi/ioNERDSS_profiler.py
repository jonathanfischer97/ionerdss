#This is just a workspace to test the speed of functions. Has some NERDSS output files as tests.

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


import ioNERDSS as ion
## CURRENTLY TESTING: something


last = badTimer('start',0)
#ion.save_vars_to_file({"word":[[0,0,0],[0,0,0],[0,0,0],[1,1,1]]})
multi_species = ion.MultiHistogram(FileName="ioNERDSSPyPi\TestingFunctions\histogram_multi\histogram_complexes_time_dode.dat",FileNum=5,InitialTime=0,FinalTime=1,SpeciesList=["A","B"])
result = multi_species.hist_to_csv()
#print(result)
#test.heatmap_complex_dist(xAxis="clat",yAxis="ap2")
#ion.associate_prob_asymmetric(FileName="ioNERDSSPyPi\TestingFunctions\\transition_matrix_time.dat",FileNum=1,InitialTime=0,FinalTime=1,SpeciesName="dode",ShowFig=True,SaveFig=False,SaveVars=True)
#ion.locate_pos_restart(FileNamePdb = "ioNERDSSPyPi\TestingFunctions\\nerdss_output.pdb", NumDict = {"dod":8}, FileNameRestart = "ioNERDSSPyPi\TestingFunctions\\restart.dat",OpName="help") 
#ion.plot_proteins(FileName = "ioNERDSSPyPi\RealClathrinTest\PDB\\25000000.pdb")
#ion.real_PDB_UI()

print()


last = badTimer('start',last)

#ioNERDSSPyPi\TestingFunctions\databse.pdb