from typing import Any, Dict, List, Tuple
from qfit.models.measurement_data import MeasDataType
from scqubits.core.hilbert_space import HilbertSpace

def parseRegDict(
    self, 
    registryDict: Dict[str, Any], 
) -> Tuple[Dict[str, Any], "HilbertSpace", List["MeasDataType"]]:
    """
    Parse the registry dictionary from different versions of the app 
    and return the up-to-date registry dictionary, HilbertSpace, and
    measurementData.

    Internal note: 
    When a micro version is updated, the way of storing and reading the 
    data should not be changed. Otherwise, when the mjor or minor version
    is updated, we will need to write a new function to parse the registry
    dictionary.

    Parameters
    ----------
    registryDict : Dict[str, Any]
        the registry dictionary
    """
    try:
        version = registryDict["version"]
    except KeyError:
        version = "1.0.0"   # the version that we haven't stored the version number
        
    major, minor, micro = version.split(".")
    major, minor, micro = int(major), int(minor), int(micro)

    if major == 1 and minor == 0:
        hilbertSpace = registryDict["HilbertSpace"]
        measurementData: List[MeasDataType] = registryDict["measDataSet.data"]

        for measData in measurementData:
            self._parseRegDict10x_20x(measData)

        return registryDict, hilbertSpace, measurementData
    
    elif major >= 2:
        hilbertSpace = registryDict["HilbertSpace"]
        measurementData = registryDict["measDataSet.data"]
        return registryDict, hilbertSpace, measurementData
    
    else:
        raise ValueError(f"File version {version} is no longer supported. "
                            f"Please contact the developer for retrieving the data.")  
    
# 1.0.x --> 2.0.x =============================================================
def _parseRegDict10x_20x(
    registryDict: Dict[str, Any]
) -> Tuple[Dict[str, Any], "HilbertSpace", List["MeasDataType"]]:
    """
    Parse the measurement data unpickled from the file with version 1.0.x.

    Parameters
    ----------
    measData : MeasDataType
        the measurement data un
    """
    hilbertSpace = registryDict["HilbertSpace"]
    measurementData: List[MeasDataType] = registryDict["measDataSet.data"]

    for measData in measurementData:
        _parseMeasData10x_20x(measData)

    # calibration data need point pair source?

    return registryDict, hilbertSpace, measurementData

def _parseMeasData10x_20x(measData: MeasDataType):
    measDict = measData.__dict__

    measData.file = "unKnown"
    measData.zCandidates = measDict["_zCandidates"]
    measData.xCandidates = measDict["rawX"]
    measData.yCandidates = measDict["rawY"]
    measData._rawXNames = measDict["xCandidates"].keyList
    measData._rawYNames = measDict["yCandidates"].keyList

    measData._principalZ = measDict["_currentZ"]
    measData._principalX = measDict["_currentX"]
    measData._principalY = measDict["_currentY"]

    measData._initFilters() 