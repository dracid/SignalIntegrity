'''
Created on Oct 15, 2015

@author: peterp
'''
import xml.etree.ElementTree as et

from PartProperty import *
from PartPicture import *

class Device(object):
    def __init__(self,propertiesList,partPicture):
        if propertiesList==None:
            propertiesList=[]
        self.propertiesList=propertiesList
        self.partPicture=partPicture
        self.selected=False
    def DrawDevice(self,canvas,grid,x,y):
        self.CreateVisiblePropertiesList()
        self.partPicture.current.Selected(self.selected).DrawDevice(canvas,grid,(x,y))
    def IsAt(self,coord):
        return self.partPicture.current.IsAt(coord)
    def WhereInPart(self,coord):
        return self.partPicture.current.WhereInPart(coord)
    def PartPropertyByName(self,name):
        for partProperty in self.propertiesList:
            if partProperty.propertyName == name:
                return partProperty
        return None
    def AddPartProperty(self,PartProperty):
        self.propertiesList=self.propertiesList+[PartProperty]
    def __getitem__(self,item):
        return self.PartPropertyByName(item)
    def NetListLine(self):
        return 'device '+str(self[PartPropertyReferenceDesignator().propertyName].value)+' '+str(self['ports'].value)
    def PinCoordinates(self):
        return self.partPicture.current.PinCoordinates()
    def CreateVisiblePropertiesList(self):
        visiblePartPropertyList=[]
        for partProperty in self.propertiesList:
            propertyString=partProperty.PropertyString()
            if propertyString != '':
                visiblePartPropertyList.append(propertyString)
        self.partPicture.current.InsertVisiblePartProperties(visiblePartPropertyList)
    def xml(self):
        dev = et.Element('device')
        classNameElement = et.Element('class_name')
        classNameElement.text = self.__class__.__name__
        pprope = et.Element('part_properties')
        props = [partProperty.xml() for partProperty in self.propertiesList]
        pprope.extend(props)
        dev.extend([classNameElement,pprope,self.partPicture.xml()])
        return dev
    def Waveform(self):
        return None

class DeviceXMLClassFactory(object):
    def __init__(self,xml):
        propertiesList=[]
        partPicture=None
        className='Device'
        for child in xml:
            if child.tag == 'class_name':
                className=child.text
            if child.tag == 'part_properties':
                for partPropertyElement in child:
                    partProperty=PartPropertyXMLClassFactory(partPropertyElement).result
                    propertiesList.append(partProperty)
            elif child.tag == 'part_picture':
                partPicture=PartPictureXMLClassFactory(child).result
        self.result=eval(className).__new__(eval(className))
        Device.__init__(self.result,propertiesList,partPicture)

class DeviceFile(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,[PartPropertyCategory('Files'),PartPropertyPartName('File'),PartPropertyFileName()]+propertiesList,partPicture)
    def NetListLine(self):
        return Device.NetListLine(self)+' file '+self[PartPropertyFileName().propertyName].value

class DeviceResistor(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,[PartPropertyCategory('Resistors'),PartPropertyPartName('Resistor'),PartPropertyResistance()]+propertiesList,partPicture)
    def NetListLine(self):
        return Device.NetListLine(self)+' R '+self[PartPropertyResistance().propertyName].value

class DeviceCapacitor(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,[PartPropertyCategory('Capacitors'),PartPropertyPartName('Capacitor'),PartPropertyCapacitance()]+propertiesList,partPicture)
    def NetListLine(self):
        return Device.NetListLine(self)+' C '+self[PartPropertyCapacitance().propertyName].value

class DeviceInductor(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,[PartPropertyCategory('Inductors'),PartPropertyPartName('Inductor'),PartPropertyInductance()]+propertiesList,partPicture)
    def NetListLine(self):
        return Device.NetListLine(self)+' L '+self[PartPropertyInductance().propertyName].value

class DeviceMutual(Device):
    def __init__(self):
        Device.__init__(self,[PartPropertyCategory('Inductors'),PartPropertyPartName('Mutual'),PartPropertyPorts(4),PartPropertyInductance(),PartPropertyDescription('Four Port Mutual Inductance')],partPicture=PartPictureVariableMutual())
    def NetListLine(self):
        return Device.NetListLine(self)+' M '+self[PartPropertyInductance().propertyName].value

class Port(Device):
    def __init__(self,portNumber):
        Device.__init__(self,[PartPropertyPartName('Port'),PartPropertyDescription('Port'),PartPropertyPorts(1),PartProperty('portnumber',keyword='',description='Port Number',value=portNumber,visible=True)],partPicture=PartPictureVariablePort())
    def NetListLine(self):
        return 'port '+str(self['portnumber'].value)

class DeviceGround(Device):
    def __init__(self):
        Device.__init__(self,[PartPropertyCategory('Miscellaneous'),PartPropertyPartName('Ground'),PartPropertyDescription('Ground'),PartPropertyPorts(1)],partPicture=PartPictureVariableGround())
    def NetListLine(self):
        return Device.NetListLine(self)+' ground'

class DeviceVoltageSource(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('Voltage Source'),PartPropertyWaveformFileName()]+propertiesList,partPicture)
    def NetListLine(self):
        return 'voltagesource '+str(self[PartPropertyReferenceDesignator().propertyName].value)+' '+str(self['ports'].value)
    def Waveform(self):
        import SignalIntegrity as si
        fileName = self[PartPropertyWaveformFileName().propertyName].value
        waveform = si.td.wf.Waveform().ReadFromFile(fileName)
        return waveform

class DeviceCurrentSource(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('Current Source'),PartPropertyWaveformFileName()]+propertiesList,partPicture)
    def NetListLine(self):
        return 'currentsource '+str(self[PartPropertyReferenceDesignator().propertyName].value)+' '+str(self['ports'].value)

class DeviceMeasurement(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,propertiesList,partPicture)
    def NetListLine(self):
        return 'meas'

class DeviceOutput(Device):
    def __init__(self,propertiesList,partPicture):
        Device.__init__(self,propertiesList,partPicture)
    def NetListLine(self):
        return 'output'

class DeviceMixedModeConverter(Device):
    def __init__(self):
        Device.__init__(self,[PartPropertyCategory('Miscellaneous'),PartPropertyPartName('Mixed Mode Converter'),PartPropertyDescription('Mixed Mode Converter'),PartPropertyPorts(4)],PartPictureVariableMixedModeConverter())
    def NetListLine(self):
        return Device.NetListLine(self)+' mixedmode'

class DeviceVoltageControlledVoltageSourceFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('VoltageControlledVoltageSource'),PartPropertyVoltageGain(1.0)]+propertiesList,PartPictureVariableVoltageControlledVoltageSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' voltagecontrolledvoltagesource '+str(self[PartPropertyVoltageGain().propertyName].value)

class DeviceVoltageAmplifierFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('VoltageAmplifier'),PartPropertyVoltageGain(1.0),PartPropertyInputImpedance(1e8),PartPropertyOutputImpedance(0.)]+propertiesList,PartPictureVariableVoltageControlledVoltageSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' voltageamplifier '+self[PartPropertyVoltageGain().propertyName].NetListProperty()+' '+self[PartPropertyInputImpedance().propertyName].NetListProperty()+' '+self[PartPropertyOutputImpedance().propertyName].NetListProperty()+' '

class DeviceCurrentControlledCurrentSourceFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('CurrentControlledCurrentSource'),PartPropertyCurrentGain(1.0)]+propertiesList,PartPictureVariableCurrentControlledCurrentSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' currentcontrolledcurrentsource '+str(self[PartPropertyCurrentGain().propertyName].value)

class DeviceCurrentAmplifierFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('CurrentAmplifier'),PartPropertyCurrentGain(1.0),PartPropertyInputImpedance(0.),PartPropertyOutputImpedance(1e8)]+propertiesList,PartPictureVariableCurrentControlledCurrentSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' currentamplifier '+self[PartPropertyCurrentGain().propertyName].NetListProperty()+' '+self[PartPropertyInputImpedance().propertyName].NetListProperty()+' '+self[PartPropertyOutputImpedance().propertyName].NetListProperty()+' '

class DeviceVoltageControlledCurrentSourceFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('VoltageControlledCurrentSource'),PartPropertyTransconductance(1.0)]+propertiesList,PartPictureVariableVoltageControlledCurrentSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' voltagecontrolledcurrentsource '+str(self[PartPropertyTransconductance().propertyName].value)

class DeviceTransconductanceAmplifierFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('TransconductanceAmplifier'),PartPropertyTransconductance(1.0),PartPropertyInputImpedance(1e8),PartPropertyOutputImpedance(1e8)]+propertiesList,PartPictureVariableVoltageControlledCurrentSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' transconductanceamplifier '+self[PartPropertyTransconductance().propertyName].NetListProperty()+' '+self[PartPropertyInputImpedance().propertyName].NetListProperty()+' '+self[PartPropertyOutputImpedance().propertyName].NetListProperty()+' '

class DeviceCurrentControlledVoltageSourceFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('CurrentControlledVoltageSource'),PartPropertyTransresistance(1.0)]+propertiesList,PartPictureVariableCurrentControlledVoltageSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' currentcontrolledvoltagesource '+str(self[PartPropertyTransresistance().propertyName].value)

class DeviceTransresistanceAmplifierFourPort(Device):
    def __init__(self,propertiesList):
        Device.__init__(self,[PartPropertyCategory('Sources'),PartPropertyPartName('TransresistanceAmplifier'),PartPropertyTransresistance(1.0),PartPropertyInputImpedance(0.),PartPropertyOutputImpedance(0.)]+propertiesList,PartPictureVariableCurrentControlledVoltageSourceFourPort())
    def NetListLine(self):
        return Device.NetListLine(self)+' transresistanceamplifier '+self[PartPropertyTransresistance().propertyName].NetListProperty()+' '+self[PartPropertyInputImpedance().propertyName].NetListProperty()+' '+self[PartPropertyOutputImpedance().propertyName].NetListProperty()+' '

DeviceList = [
              DeviceFile([PartPropertyDescription('One Port File'),PartPropertyPorts(1)],PartPictureVariableOnePort()),
              DeviceFile([PartPropertyDescription('Two Port File'),PartPropertyPorts(2)],PartPictureVariableTwoPort()),
              DeviceFile([PartPropertyDescription('Three Port File'),PartPropertyPorts(3)],PartPictureVariableThreePort()),
              DeviceFile([PartPropertyDescription('Four Port File'),PartPropertyPorts(4)],PartPictureVariableFourPort()),
              DeviceResistor([PartPropertyDescription('One Port Resistor to Ground'),PartPropertyPorts(1)],PartPictureVariableResistorOnePort()),
              DeviceResistor([PartPropertyDescription('Two Port Resistor'),PartPropertyPorts(2)],PartPictureVariableResistorTwoPort()),
              DeviceCapacitor([PartPropertyDescription('One Port Capacitor to Ground'),PartPropertyPorts(1)],PartPictureVariableCapacitorOnePort()),
              DeviceCapacitor([PartPropertyDescription('Two Port Capacitor'),PartPropertyPorts(2)],PartPictureVariableCapacitorTwoPort()),
              DeviceInductor([PartPropertyDescription('Two Port Inductor'),PartPropertyPorts(2)],PartPictureVariableInductorTwoPort()),
              DeviceMutual(),
              DeviceGround(),
              DeviceVoltageSource([PartPropertyDescription('One Port Voltage Source'),PartPropertyPorts(1)],PartPictureVariableVoltageSourceOnePort()),
              DeviceVoltageSource([PartPropertyDescription('Two Port Voltage Source'),PartPropertyPorts(2)],PartPictureVariableVoltageSourceTwoPort()),
              DeviceCurrentSource([PartPropertyDescription('One Port Current Source'),PartPropertyPorts(1)],PartPictureVariableCurrentSourceOnePort()),
              DeviceCurrentSource([PartPropertyDescription('Two Port Current Source'),PartPropertyPorts(2)],PartPictureVariableCurrentSourceTwoPort()),
              DeviceMeasurement([PartPropertyCategory('Probes'),PartPropertyPartName('Measure'),PartPropertyDescription('Measure')],PartPictureVariableProbe()),
              DeviceOutput([PartPropertyCategory('Probes'),PartPropertyPartName('Output'),PartPropertyDescription('Output')],PartPictureVariableProbe()),
              DeviceMixedModeConverter(),
              DeviceVoltageControlledVoltageSourceFourPort([PartPropertyDescription('Four Port Voltage Controlled Voltage Source'),PartPropertyPorts(4)]),
              DeviceVoltageAmplifierFourPort([PartPropertyDescription('Four Port Voltage Amplifier'),PartPropertyPorts(4)]),
              DeviceCurrentControlledCurrentSourceFourPort([PartPropertyDescription('Four Port Current Controlled Current Source'),PartPropertyPorts(4)]),
              DeviceCurrentAmplifierFourPort([PartPropertyDescription('Four Port Current Amplifier'),PartPropertyPorts(4)]),
              DeviceVoltageControlledCurrentSourceFourPort([PartPropertyDescription('Four Port Voltage Controlled Current Source'),PartPropertyPorts(4)]),
              DeviceTransconductanceAmplifierFourPort([PartPropertyDescription('Four Port Transconductance Amplifier'),PartPropertyPorts(4)]),
              DeviceCurrentControlledVoltageSourceFourPort([PartPropertyDescription('Four Port Current Controlled Voltage Source'),PartPropertyPorts(4)]),
              DeviceTransresistanceAmplifierFourPort([PartPropertyDescription('Four Port Transresistance Amplifier'),PartPropertyPorts(4)])
              ]