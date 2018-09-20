"""
numeric simulations from netlists
"""
# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
#
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

from SignalIntegrity.Parsers.SimulatorParser import SimulatorParser
from SignalIntegrity.SystemDescriptions import SimulatorNumeric
from SignalIntegrity.FrequencyDomain.TransferMatrices import TransferMatrices
from SignalIntegrity.PySIException import PySIExceptionSimulator
from SignalIntegrity.CallBacker import CallBacker
from SignalIntegrity.ResultsCache import LinesCache

class SimulatorNumericParser(SimulatorParser,CallBacker,LinesCache):
    """performs numeric simulations from netlists"""
    def __init__(self, f=None, args=None,  callback=None, cacheFileName=None):
        """constructor

        frequencies may be provided at construction time (or not for symbolic solutions).

        @param f (optional) list of frequencies
        @param args (optional) string arguments for the circuit.
        @param callback (optional) function taking one argument as a callback
        @param cacheFileName (optional) string name of file used to cache results

        Arguments are provided on a line as pairs of names and values separated by a space.

        The optional callback is used as described in the class CallBacker.

        The use of the cacheFileName is described in the class LineCache

        """
        SimulatorParser.__init__(self, f, args)
        self.transferMatrices = None
        # pragma: silent exclude
        CallBacker.__init__(self,callback)
        LinesCache.__init__(self,'TransferMatrices',cacheFileName)
        # pragma: include
    def TransferMatrices(self):
        """calculates transfer matrices for simulation

        Simulation, insofar as this class is concerned means generating transfer matrices for
        processing waveforms with.

        @return instance of class TransferMatrices

        @remark
        TransferMatrices are used with a TransferMatricesProcessor to process waveforms for
        simulation.
        """
        # pragma: silent exclude
        if not self.transferMatrices is None:
            return self.transferMatrices
        if self.CheckCache():
            self.CallBack(100.0)
            return self.transferMatrices
        # pragma: include
        self.SystemDescription()
        self.m_sd.CheckConnections()
        spc=self.m_spc
        result=[]
        for n in range(len(self.m_f)):
            for d in range(len(self.m_spc)):
                self.m_sd.AssignSParameters(spc[d][0],spc[d][1][n])
            tm=SimulatorNumeric(self.m_sd).TransferMatrix()
            result.append(tm)
            # pragma: silent exclude
            if self.HasACallBack():
                progress = self.m_f[n]/self.m_f[-1]*100.0
                if not self.CallBack(progress):
                    raise PySIExceptionSimulator('calculation aborted')
            # pragma: include
        self.transferMatrices=TransferMatrices(self.m_f,result)
        # pragma: silent exclude
        self.CacheResult()
        # pragma: include
        return self.transferMatrices