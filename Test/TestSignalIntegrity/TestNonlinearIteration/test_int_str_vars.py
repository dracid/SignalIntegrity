from SignalIntegrity.Lib.TimeDomain.Waveform.Waveform import Waveform

#Code which will be run by a dependent voltage source to perform voltage transformation
#This simple explanation will just scale VO3 probe (if VO3 not there, exception occurs which is not well handled)
# inpputs: inputWaveforms - dictionary containing Waveform to utilize
# outputs: outputWaveform - set to transformed Waveform

#Check if scale variable initialized (passed in)
if type(test_int) is not int:
    raise Exception("NOT AN INT")
if type(test_str) is not str:
    raise Exception("NOT A STRING")
inputWaveform = NLS1 #Assuming only 1 waveform input, will pick out that waveform
                                                        #if multiple, then will just pick a random one to scale
                                                        #if multiple, then will just pick a random one to scale
outputWaveform = inputWaveform
print('RAN IT')





