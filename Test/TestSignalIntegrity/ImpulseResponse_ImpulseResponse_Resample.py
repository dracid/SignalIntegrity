class ImpulseResponse(Waveform):
...
    def Resample(self,td):
        fr=self.FrequencyResponse()
        return fr.ImpulseResponse(td)
...
