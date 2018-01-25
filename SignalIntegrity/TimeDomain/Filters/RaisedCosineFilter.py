'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from FirFilter import FirFilter
from FilterDescriptor import FilterDescriptor
import math

class RaisedCosineFilter(FirFilter):
    def __init__(self,S=1):
        L=2*S+1
        w=[math.cos(2*math.pi*(k-S)/L)*0.5+0.5 for k in range(L)]
        Scale=sum(w)
        w=[tap/Scale for tap in w]
        FirFilter.__init__(self,FilterDescriptor(1,S,2*S),w)