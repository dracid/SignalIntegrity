"""
 Performs Simulations Numerically
"""

# Copyright (c) 2021 Nubis Communications, Inc.
# Copyright (c) 2018-2020 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

from numpy import array,zeros

from SignalIntegrity.Lib.SystemDescriptions.Simulator import Simulator
from SignalIntegrity.Lib.SystemDescriptions.Numeric import Numeric


class SimulatorNumeric(Simulator,Numeric):
    fasterway=True
    """class for performing numeric simulations
    @note For the purposes of this class, the numerical simulation work
    has been performed by returning the transfer matrix.  Transfer matrices
    built over many frequencies are then utilized in the actual waveform
    processing for the simulation."""
    def __init__(self,sd=None):
        """Constructor
        @param sd (optional) instance of class SystemDescription
        """
        Simulator.__init__(self,sd)
    def TransferMatrix(self,Z0=50.):
        """TransferMatrix
        @param Z0 float (optional, defaults to 50.) reference impedance for the calculation
        @return list of list transfer matrix that for O output waveforms
        and I input waveforms is OxI and be considered as multiplied by
        a vector of input waveforms to produce a vector of output waveforms.

        The transfer matrix provided is for a single frequency."""
        self.Check()
        # pragma: silent exclude
        if not self.fasterway:
        # pragma: include outdent
            if not hasattr(self, 'VE_o'):
                self.VE_o=array(self.VoltageExtractionMatrix(self.m_ol))
                self.sm=array(self.SourceToStimsPrimeMatrix(Z0=Z0))
            SIPrime=array(self.SIPrime(Left=self.VE_o))
            Result=[list(v) for v in list(self.VE_o.dot(SIPrime).dot(self.sm))]
        # pragma: silent exclude indent
        else:
            if not hasattr(self, 'VE'):
                self.VE_o=array(self.VoltageExtractionMatrix(self.m_ol))
                self.VE=array(self.VoltageExtractionList(self.m_ol))
                self.sm=array(self.SourceToStimsPrimeMatrix(Z0=Z0))
            SIPrime=array(self.SIPrime(Left=self.VE_o))
            Result=[list(v) for v in list(self.Extract(self.VE,SIPrime).dot(self.sm))]
        # pragma: include
        return Result
