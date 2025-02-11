from typing import Any, Dict, List, Tuple, TYPE_CHECKING

import re

if TYPE_CHECKING:
    from qfit.models.measurement_data import MeasDataType
    from scqubits.core.hilbert_space import HilbertSpace
    from qfit.models.data_structures import CaliTableRowParam, FitParam, SliderParam


def parseRegDict(
    registryDict: Dict[str, Any],
) -> Dict[str, Any]:
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
        version = "1.0.0"  # the version that we haven't stored the version number

    major, minor, micro = version.split(".")[:3]
    major, minor, micro = int(major), int(minor), int(micro)

    if major == 1 and minor == 0:
        return _parseRegDict10x_20x(registryDict)

    elif major >= 2:
        return registryDict

    else:
        raise ValueError(
            f"File version {version} is no longer supported. "
            f"Please contact the developer for retrieving the data."
        )


# 1.0.x --> 2.0.x =============================================================
def _parseRegDict10x_20x(registryDict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the measurement data unpickled from the file with version 1.0.x.

    Parameters
    ----------
    measData : MeasDataType
        the measurement data un
    """

    # handles the missing keys
    keyMap = [
        ("measDataSet.data", "MeasDataSet.data"),
        ("measDataSet.currentRow", "MeasDataSet._currentRow"),
        ("projectFile", "MainWindow._projectFile"),
    ]
    keysDeleted = []
    dictAdded = {
        "MeasDataSet.checkedRawX": [],
        "MeasDataSet.checkedRawY": [],
    }
    for key, newKey in keyMap:
        if key in registryDict:
            registryDict[newKey] = registryDict[key]
            keysDeleted.append(key)
    for key, value in dictAdded.items():
        if key not in registryDict:
            registryDict[key] = value
    for key in keysDeleted:
        del registryDict[key]

    # change attributes of the measurement data
    for measData in registryDict["MeasDataSet.data"]:
        _parseMeasData10x_20x(measData)

    # calibration data need point pair source?
    calibParams = registryDict["CaliParamModel"]
    _parseCalibParam10x_20x(calibParams)

    prefitCaliParams = registryDict["PrefitCaliParams"]
    _parsePrefitCaliParam10x_20x(prefitCaliParams)

    fitCaliParams = registryDict["FitCaliParams"]
    _parseFitCaliParam10x_20x(fitCaliParams)

    return registryDict


def _parseMeasData10x_20x(measData: "MeasDataType"):
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


def _parseCalibParam10x_20x(caliParams: Dict[str, Dict[str, "CaliTableRowParam"]]):
    nameMap = [
        ("pointPairSource", "DATA<br>SOURCE"),
    ]

    for parent, caliDict in caliParams.items():
        for key, newKey in nameMap:
            if key in caliDict:
                caliDict[newKey] = caliDict.pop(key)
        # replace keys that takes shape <parent>.<param> to (<param>)<br><parent>
        for key in list(caliDict.keys()):
            if re.match(r"^\w+\.\w+$", key):
                newKey = f"{key.split('.')[1]}<br>({'.'.join(key.split('.')[:-1])})"
                caliDict[newKey] = caliDict.pop(key)


def _parseFitCaliParam10x_20x(caliParams: Dict[str, Dict[str, "FitParam"]]):

    for parent, caliDict in caliParams.items():
        # replace keys that takes shape <parent>.<param> to (<param>)<br><parent>
        for key in list(caliDict.keys()):
            if re.match(r"^\w+\.\w+$", key):
                newKey = f"{key.split('.')[1]}<br>({'.'.join(key.split('.')[:-1])})"
                caliDict[newKey] = caliDict.pop(key)


def _parsePrefitCaliParam10x_20x(caliParams: Dict[str, Dict[str, "SliderParam"]]):

    for parent, caliDict in caliParams.items():
        # replace keys that takes shape <parent>.<param> to (<param>)<br><parent>
        for key in list(caliDict.keys()):
            if re.match(r"^\w+\.\w+$", key):
                newKey = f"{key.split('.')[1]}<br>({'.'.join(key.split('.')[:-1])})"
                caliDict[newKey] = caliDict.pop(key)
