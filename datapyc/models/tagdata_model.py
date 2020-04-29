# tagdata_models.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


# tagging types (to facility file io, do not use Enum)
import datapyc.io_utils.file_io_serializers as serializers

NO_TAG = 'NO_TAG'
DISPERSIVE_DRESSED = 'DISPERSIVE_DRESSED'
DISPERSIVE_BARE = 'DISPERSIVE_BARE'
CROSSING = 'CROSSING'
CROSSING_DRESSED = 'CROSSING_DRESSED'


# different tag types
# need to store on disk - Enum not a good choice
# store list of tags along with data in AllExtractedDataModel
# do we want separate model for tagging?

class Tag(serializers.Serializable):
    """
    Store a single dataset tag. The tag can be of different types:
    - NO_TAG: user did not tag data
    - DISPERSIVE_DRESSED: transition between two states in the dispersive regime, tagged by dressed-states indices
    - DISPERSIVE_BARE: : transition between two states in the dispersive regime, tagged by bare-states indices
    - CROSSING: avoided crossing, left untagged (fitting should use closest-energy states)
    - CROSSING_DRESSED: avoided crossing, tagged by dressed-states indices

    Parameters
    ----------
    tagType: str
        one of the tag types listed above
    initial, final: int, or tuple of int, or None
        - For NO_TAG and CROSSING, no initial and final state are specified.
        - For DISPERSIVE_DRESSED and CROSSING_DRESSED, initial and final state are specified by an int dressed index.
        - FOR DISPERSIVE_BARE, initial and final state are specified by a tuple of ints (exc. levels of each subsys)
    photons: int or None
        - For NO_TAG, no photon number is specified.
        - For all other tag types, this int specifies the photon number rank of the transition.

    """
    def __init__(self, tagType=NO_TAG, initial=None, final=None, photons=None):
        self.tagType = tagType
        self.initial = initial
        self.final = final
        self.photons = photons


class TagDataModel:
    def __init__(self):
        self.currentTag = Tag()

    def setTag(self, newTag):
        self.currentTag = newTag
