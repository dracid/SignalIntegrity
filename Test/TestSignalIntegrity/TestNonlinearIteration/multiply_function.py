from SignalIntegrity.Lib.TimeDomain.Waveform.Waveform import Waveform

#Code which will be run by a dependent voltage source to perform voltage transformation
#This simple example will multiply all the passed in waveforms and then multiply by a global scale factor
# inpputs: inputWaveforms - Dictionary of waveforms to utilize
# outputs: outputWaveform - set to transformed Waveform

#Check if scale variable initialized (passed in)
try:
    print(f"Scale factor: {scale}")
except NameError:
    print('Scale not passed in!')
    scale = 1

outputWaveform = VO1 * VO3

outputWaveform = outputWaveform*scale
print('RAN IT')


