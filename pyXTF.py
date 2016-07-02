#name:          pyXTF
#created:       May 2016
#by:            p.kennedy@fugro.com
#description:   script to read an XTF file
#notes:         See main at end of script for example how to use this
#based on XTF version 26 18/12/2008
#version 1.00

# XTF BYTE = 1 byte = "b"
# XTFWORD = signed int 2 bytes = h
# XTFWORD = UNsigned int 2 bytes = H (for unipolar data)
# DWORD = unsigned int 4 bytes = "L"
# short = short integer 2 bytes = "h"
# char = 1 byte = "c"

#DONE
#initial implementation

import pprint
import struct
import os.path

class XTFPINGHEADER:
    def __init__(self, fileptr, XTFFileHdr):
        XTFPingHeader_fmt = '=h2b3hLh6bh2L2fL21f2d2h 4b2f2d4h10flfl4b2hB11b'
        XTFPingHeader_len = struct.calcsize(XTFPingHeader_fmt)
        XTFPingHeader_unpack = struct.Struct(XTFPingHeader_fmt).unpack_from

        data = fileptr.read(XTFPingHeader_len)
        s = XTFPingHeader_unpack(data)

        self.MagicNumber                    = s[0]
        self.HeaderType                     = s[1]
        self.SubChannelNumber               = s[2]
        self.NumChansToFollow               = s[3]
        self.Reserved1                      = s[4]
        self.Reserved2                      = s[5]
        self.NumBytesThisRecord             = s[6]
        self.Year                           = s[7]
        self.Month                          = s[8]
        self.Day                            = s[9]
        self.Hour                           = s[10]
        self.Minute                         = s[11]
        self.Second                         = s[12]
        self.HSeconds                       = s[13]
        self.JulianDays                     = s[14]
        self.EventNumber                    = s[15]
        self.PingNumber                     = s[16]
        self.SoundVelocity                  = s[17]
        self.OceanTide                      = s[18]
        self.Reserved2                      = s[19]
        self.ConductivityFreq               = s[20]
        self.TemperatureFreq                = s[21]
        self.PressureFreq                   = s[22]
        self.PressureTemp                   = s[23]
        self.Conductivity                   = s[24]
        self.WaterTemperature               = s[25]
        self.Pressure                       = s[26]
        self.ComputedSoundVelocity          = s[27]
        self.MagX                           = s[28]
        self.MagY                           = s[29]
        self.MagZ                           = s[30]
        self.AuxVal1                        = s[31]
        self.AuxVal2                        = s[32]
        self.AuxVal3                        = s[33]
        self.AuxVal4                        = s[34]
        self.AuxVal5                        = s[35]
        self.AuxVal6                        = s[36]
        self.SpeedLog                       = s[37]
        self.Turbidity                      = s[38]
        self.ShipSpeed                      = s[39]
        self.ShipGyro                       = s[40]
        self.ShipYcoordinate                = s[41]                        
        self.ShipXcoordinate                = s[42]
        self.ShipAltitiude                  = s[43]
        self.ShipDepth                      = s[44]
        self.FixTimeHour                    = s[45]
        self.FixTimeMinute                  = s[46]
        self.FixTimeSecond                  = s[47]
        self.FixTimeHsecond                 = s[48]
        self.SensorSpeed                    = s[49]
        self.KP                             = s[50]
        self.SensorYcoordinate              = s[51]
        self.SensorXcoordinate              = s[52]
        self.SonarStatus                    = s[53]
        self.RangeToTowFish                 = s[54]
        self.BearingToTowFish               = s[55]
        self.CableOut                       = s[56]
        self.Layback                        = s[57]
        self.CableTension                   = s[58]
        self.SensorDepth                    = s[59]
        self.SensorPrimaryAltitude          = s[60]
        self.SensorAuxAltitude              = s[61]
        self.SensorPitch                    = s[62]
        self.SensorRoll                     = s[63]
        self.SensorHeading                  = s[64]
        self.Heave                          = s[65]
        self.Yaw                            = s[66]
        self.AttitudeTimeTag                = s[67]
        self.DOT                            = s[68]
        self.NavFixMilliseconds             = s[69]
        self.ComputerClockHour              = s[70]
        self.ComputerClockMinute            = s[71]
        self.ComputerClockSecond            = s[72]
        self.ComputerClockHSecond           = s[73]
        self.FishPositionDeltaX             = s[74]
        self.FishPositionDeltaY             = s[75]
        self.FishPositionErrorCode          = s[76]
        self.ReservedSpace2                 = s[77]

        # now read the chaninfo records.  This is more complex than it needs to be, but for now, read six channels
        self.pingChannel =[]
        for i in range(self.NumChansToFollow):
            ping = XTFPINGCHANHEADER(fileptr, XTFFileHdr, i)
            self.pingChannel.append(ping)

    def __str__(self):
        return (pprint.pformat(vars(self)))        
                
class XTFPINGCHANHEADER:
    def __init__(self, fileptr, XTFFileHdr, channelIndex):
        XTFPingChanHeader_fmt = '=2h5f5hLh2bLhf2bfh4b'
        XTFPingChanHeader_len = struct.calcsize(XTFPingChanHeader_fmt)
        XTFPingChanHeader_unpack = struct.Struct(XTFPingChanHeader_fmt).unpack_from

        hdr = fileptr.read(XTFPingChanHeader_len)
        s = XTFPingChanHeader_unpack(hdr)
        self.ChannelNumber                    = s[0]
        self.DownsampleMethod                 = s[1]
        self.SlantRange                       = s[2]
        self.GroundRange                      = s[3]
        self.TimeDelay                        = s[4]
        self.TimeDuration                     = s[5]
        self.SecondsPerPing                   = s[6]
        self.ProcessingFlags                  = s[7]
        self.Frequency                        = s[8]
        self.InitialGainCode                  = s[9]
        self.GainCode                         = s[10]
        self.BandWidth                        = s[11]
        self.ContactNumber                    = s[12]
        self.ContactClassification            = s[13]
        self.ContactSubNumber                 = s[14]
        self.ContactType                      = s[15]
        self.NumSamples                       = s[16]
        self.MillivoltScale                   = s[17]
        self.ContactTimeOffTrack              = s[18]
        self.ContactCloseNumber               = s[19]
        self.Reserved2                        = s[20]
        self.FixedVSOP                        = s[21]
        self.Weight                           = s[22]
        self.ReservedSpace1                   = s[23]
        self.ReservedSpace2                   = s[24]
        self.ReservedSpace3                   = s[25]
        self.ReservedSpace4                   = s[26]

        if XTFFileHdr.XTFChanInfo[channelIndex].UniPolar == 0: #polar mean signed data
            if XTFFileHdr.XTFChanInfo[channelIndex].BytesPerSample == 1: #1 byte per sample
                XTFdata_fmt = '=' + str(self.NumSamples) + 'b'
            else:
                XTFdata_fmt = '=' + str(self.NumSamples) + 'h'                
        else:
            # we are using unipolar data
            if XTFFileHdr.XTFChanInfo[channelIndex].BytesPerSample == 1: #1 byte per sample
                XTFdata_fmt = '=' + str(self.NumSamples) + 'B'
            else:
                XTFdata_fmt = '=' + str(self.NumSamples) + 'H'                
            
        #now read the sonar data
        XTFdata_len = struct.calcsize(XTFdata_fmt)
        XTFdata_unpack = struct.Struct(XTFdata_fmt).unpack_from
        blob = fileptr.read(XTFdata_len)
        self.data = XTFdata_unpack(blob)

        return
        
    def __str__(self):
        return (pprint.pformat(vars(self)))        
        
class XTFCHANINFO:
    def __init__(self, fileptr):
        XTFChanInfo_fmt = '=bb3hl16s11fhb53s'
        XTFChanInfo_len = struct.calcsize(XTFChanInfo_fmt)
        XTFChanInfo_unpack = struct.Struct(XTFChanInfo_fmt).unpack_from

        data = fileptr.read(XTFChanInfo_len)
        s = XTFChanInfo_unpack(data)
        self.TypeOfChannel                    = s[0]
        self.SubChannelNumber                 = s[1]
        self.CorrectionFlags                  = s[2]
        self.UniPolar                         = s[3]
        self.BytesPerSample                   = s[4]
        self.Reserved                         = s[5]
        self.ChannelName                      = s[6].decode('utf-8').rstrip('\x00')
        self.VoltScale                        = s[7]
        self.Frequency                        = s[8]
        self.HorizBeamAngle                   = s[9]
        self.TiltAngle                        = s[10]
        self.BeamWidth                        = s[11]
        self.OffsetX                          = s[12]
        self.OffsetY                          = s[13]
        self.OffsetZ                          = s[14]
        self.OffsetYaw                        = s[15]
        self.OffsetPitch                      = s[16]
        self.OffsetRoll                       = s[17]
        self.BeamsPerArray                    = s[18]
        self.SampleFormat                     = s[19]
        self.ReservedArea2                    = s[20].decode('utf-8').rstrip('\x00')
                        
    def __str__(self):
        return (pprint.pformat(vars(self)))

class XTFFILEHDR:
    def __init__(self, fileptr):
        XTFFileHdr_fmt = '=bb8s8s16sh64s64s3hbbhbbHf12b10bl12f'
        XTFFileHdr_len = struct.calcsize(XTFFileHdr_fmt)
        XTFFileHdr_unpack = struct.Struct(XTFFileHdr_fmt).unpack_from

        data = fileptr.read(XTFFileHdr_len)
        s = XTFFileHdr_unpack(data)
        self.FileFormat                         = s[0]
        self.SystemType                         = s[1]
        self.RecordingProgramName               = s[2].decode('utf-8').rstrip('\x00')
        self.RecordingProgramVersion            = s[3].decode('utf-8').rstrip('\x00')
        self.SonarName                          = s[4].decode('utf-8').rstrip('\x00')
        self.SonarType                          = s[5]
        self.NoteString                         = s[6].decode('utf-8').rstrip('\x00')
        self.ThisFileName                       = s[7].decode('utf-8').rstrip('\x00')
        self.NavUnits                           = s[8]
        self.NumberOfSonarChannels              = s[9]
        self.NumberOfBathymetryChannels         = s[10]
        self.NumberOfSnippetChannels            = s[11]
        self.NumberOfForwardLookArrays          = s[12]
        self.NumberOfInterferometryChannels     = s[13]
        self.Reserved1                          = s[14]
        self.Reserved2                          = s[15]
        self.ReferencePointHeight               = s[16]
        self.ProjectionType                     = s[17]
        self.SpheroidType                       = s[18]
        self.NavigationLatency                  = s[19]
        self.OriginX                            = s[20]
        self.Originy                            = s[21]
        self.NavoffsetX                         = s[22]
        self.NavoffsetY                         = s[23]
        self.NavoffsetZ                         = s[24]
        self.NavoffsetYaw                       = s[25]
        self.NavoffsetX                         = s[26]
        self.MRUoffsetY                         = s[27]
        self.MRUoffsetZ                         = s[28]
        self.MRUoffsetYaw                       = s[29]
        self.MRUoffsetPitch                     = s[30]
        self.MRUoffsetRoll                      = s[31]

        # now read the chaninfo records.  This is more complex than it needs to be, but for now, read six channels
        self.XTFChanInfo =[]
        for i in range(6):
            ch = XTFCHANINFO(fileptr)
            self.XTFChanInfo.append(ch)
            
    def __str__(self):
        return (pprint.pformat(vars(self)))
    
class XTFReader:
    def __init__(self, XTFfileName):
        if not os.path.isfile(XTFfileName):
            print ("file not found:", XTFfileName)
        self.fileName = XTFfileName
        self.fileptr = open(XTFfileName, 'rb')        
        self.fileSize = self.fileptr.seek(0, 2)
        # go back to start of file
        self.fileptr.seek(0, 0)
                
        self.XTFFileHdr = XTFFILEHDR(self.fileptr)
            
    def __str__(self):
        return pprint.pformat(vars(self))
        
    def moreData(self):
        bytesRemaining = self.fileSize - self.fileptr.tell()
        return bytesRemaining
                
    def readPing(self):
        ping = XTFPINGHEADER(self.fileptr, self.XTFFileHdr )
        return ping
    
    def readChannel(self):        
        return XTFPINGCHANHEADER(self.fileptr, self.XTFFileHdr)
         
if __name__ == "__main__":
    r = XTFReader("C:/development/python/SonarNadirCalculator/01064_m66c448_SSS_20151219_205405_HH_HuginES7_GA4450_P_compressed.xtf")
    print (r)
    print (r.XTFFileHdr)
    for ch in range(r.XTFFileHdr.NumberOfSonarChannels):
        print(r.XTFFileHdr.XTFChanInfo[ch])

    while r.moreData():
        pingHdr = r.readPing()
        print (pingHdr.PingNumber,  pingHdr.SensorXcoordinate, pingHdr.SensorYcoordinate)
            
    print("Complete reading XTF file :-)")