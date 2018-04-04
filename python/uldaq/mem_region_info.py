"""
Created on Feb 19, 2018

@author: MCC
"""


class MemRegionInfo:
    """
    Information about a region of memory.

    Args:
        region_type: A :class:`MemRegion` value.
        address: The address of the memory region.
        size: The size of the memory region in bytes.
        access_type: A bit mask of :class:`MemAccessType` values.
    """
    
    def __init__(self, region_type, address, size, access_type):
        self._region_type = region_type
        self._address = address
        self._size = size
        self._access_type = access_type

    def get_region_type(self):
        """
        Gets the region type of the memory region.

        Returns:
            A :class:`MemRegion` value.
        """
        return self._region_type

    def get_address(self):
        """
        Gets the address of the memory region.

        Returns:
            The address of the memory region.
        """
        return self._address

    def get_size(self):
        """
        Gets the size of the memory region.

        Returns:
            The size of the memory region in bytes.
        """
        return self._size

    def get_access_type(self):
        """
        Gets the access type of the memory region.

        Returns:
            A bit mask of :class:`MemAccessType` values.
        """
        return self._access_type
