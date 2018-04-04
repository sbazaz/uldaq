"""
Created on Feb 19, 2018

@author: MCC
"""

from ctypes import c_longlong, byref
from .ul_enums import MemRegion
from .ul_structs import MemDescriptor
from .ul_exception import ULException
from .mem_region_info import MemRegionInfo
from .ul_c_interface import lib, DevItemInfo
from .utils import enum_mask_to_list


class DevMemInfo:
    """
    Provides information about the reserved memory of the DAQ device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_mem_regions(self):
        # type: () -> list[MemRegion]
        """
        Gets the supported memory regions for the DAQ device's reserved memory.

        Returns:
            A list of supported :class:`MemRegion` objects.

        Raises:
            :class:`ULException`
        """
        memory_regions_mask = c_longlong()
        err = lib.ulDevGetInfo(self.__handle, DevItemInfo.MEM_REGIONS, 0, byref(memory_regions_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(MemRegion, memory_regions_mask.value)

    def get_mem_region_info(self):
        # type: () -> list[MemRegionInfo]
        """
        Gets the list of memory region info objects for the DAQ device's reserved memory.

        Returns:
            A list of supported :class:`MemRegionInfo` objects.

        Raises:
            :class:`ULException`
        """
        mem_regions = self.get_mem_regions()
        
        mem_region_info_list = []
        mem_descriptor = MemDescriptor()
        for mr in mem_regions:
            err = lib.ulMemGetInfo(self.__handle, mr, byref(mem_descriptor))
            if err != 0:
                raise ULException(err)

            mem_region_info = MemRegionInfo(mr, mem_descriptor.address, mem_descriptor.size,
                                            mem_descriptor.access_types)
            mem_region_info_list.append(mem_region_info)
                    
        return mem_region_info_list
