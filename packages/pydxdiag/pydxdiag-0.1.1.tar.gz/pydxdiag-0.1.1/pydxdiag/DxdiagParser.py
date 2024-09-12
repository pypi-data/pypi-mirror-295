from bs4 import BeautifulSoup
from typing import *
from pathlib import Path
import subprocess

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import functions.device.DirectInputDevice as DirectInputDevice
import functions.device.DisplayDevice as DisplayDevice
import functions.device.InputRelatedDevice as InputRelatedDevice
import functions.device.SoundCaptureDevice as SoundCaptureDevice
import functions.device.SoundDevice as SoundDevice
import functions.device.SystemDevice as SystemDevice
import functions.device.VideoCaptureDevice as VideoCaptureDevice
import functions.sz.szByteStreamHandler as szByteStreamHandler
import functions.sz.szEnabledHardwareMFT as szEnabledHardwareMFT
import functions.sz.szMFFileVersions as szMFFileVersions
import functions.sz.szMFTs as szMFTs
import functions.sz.szPreferredMFT as szPreferredMFT
import functions.sz.szSchemeHandlers as szSchemeHandlers
import functions.EnvPowerInformation as EnvPowerInformation
import functions.Filter as Filter
import functions.LogicalDisk as LogicalDisk
import functions.SystemInformation as SystemInformation

class DxdiagParser:
    """
    Basic parser class for DirectX Diagnostic Tool output
    """
    def __init__(self) -> None:
        self.dxXML:BeautifulSoup = None
        # Creating a BeautifulSoup object for the dxdiag output
        self.LoadDXDiag()
        self.GetDirectInputDevices = DirectInputDevice.GetDirectInputDevices
        self.GetDisplayDevices = DisplayDevice.GetDisplayDevices
        self.GetInputRelatedDevicesViaUSBRoot = InputRelatedDevice.GetInputRelatedDevicesViaUSBRoot
        self.GetInputRelatedDeviceViaPS2 = InputRelatedDevice.GetInputRelatedDeviceViaPS2
        self.GetStatusForPollWithInterput = InputRelatedDevice.GetStatusForPollWithInterput
        self.GetSoundCaptureDevices = SoundCaptureDevice.GetSoundCaptureDevices
        self.GetSoundDevices = SoundDevice.GetSoundDevices
        self.GetSystemDevices = SystemDevice.GetSystemDevices
        self.GetVideoCaptureDevices = VideoCaptureDevice.GetVideoCaptureDevices
        self.GetBytesStreamHandlers = szByteStreamHandler.GetBytesStreamHandlers
        self.GetStatufForEnableHardwareMFT = szEnabledHardwareMFT.GetStatufForEnableHardwareMFT
        self.GetMFFileVersions = szMFFileVersions.GetMFFileVersions
        self.GetMFTs = szMFTs.GetMFTs
        self.GetszPreferedMFTs = szPreferredMFT.GetszPreferedMFTs
        self.GetSchemeHandlers = szSchemeHandlers.GetSchemeHandlers
        self.GetEnvPowerInformation = EnvPowerInformation.GetEnvPowerInformation
        self.GetFilters = Filter.GetFilters
        self.GetPreferredDShowFilters = Filter.GetPreferredDShowFilters
        self.GetLogicalDisks = LogicalDisk.GetLogicalDisks
        self.GetOSInformation = SystemInformation.GetOSInformation
        self.GetDirectXDebugLevels = SystemInformation.GetDirectXDebugLevels
        self.GetDxDiagNotes = SystemInformation.GetDxDiagNotes
        self.GetMachineInformation = SystemInformation.GetMachineInformation
    def LoadDXDiag(self) -> None:
        """
        Function to load the dxdiag output into the BeautifulSoup object
        """
        # Running subprocess without shell execution
        subprocess.run(
            ["dxdiag", "-x","dxdiag.xml"],
            shell=False
        )
        # Reading output file then transfer into StringIO Object
        # FIXME: Since dxdiag.exe doesn't support stdout, we have to read the file
        # Probably there is some way that can capture the I/O Buffer while writing?
        with open("dxdiag.xml", "r",encoding="utf-8") as f:
            # Creating an ElementTree object from the StringIO object
              self.dxXML:BeautifulSoup = BeautifulSoup(f, features="xml")
        f.close()
        # Removing the output file
        Path("dxdiag.xml").unlink()

        

    