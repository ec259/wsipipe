"""
Parent class that contains functionality for reading slides

These are used to render different types of slides into a common format

"""


from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List

import numpy as np
from PIL.Image import Image

from wsipipe.load.slides.region import Region
from wsipipe.utils import Size, Point


class SlideBase(metaclass=ABCMeta):
    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    @property
    @abstractmethod
    def path(self) -> Path:
        raise NotImplementedError

    @property
    @abstractmethod
    def dimensions(self) -> List[Size]:
        """ Gets slide dimensions in pixels for all levels in pyramid
        Returns:
            (List[Size]): A list of sizes
        """
        raise NotImplementedError

    @abstractmethod
    def read_region(self, region: Region) -> Image:
        """Read a region from a WSI

        Returns a PIL image for the region

        Args:
            region (Region): A region of the image
        Returns:
            image (Image): A PIL Image of the specified region 
        """
        raise NotImplementedError

    @abstractmethod
    def read_regions(self, regions: List[Region]) -> List[Image]:
        """Read multiple regions of a WSI

        Returns a PIL image for each region

        Args:
            regions (List[Region]): List of regions
        Returns:
            images (List[Image]): List of Images 
        """
        raise NotImplementedError

    def get_thumbnail(self, level: int) -> np.array:
        """Get thumbnail of whole slide downsized to a level in the pyramid

        Args:
            level (int): Level at which to return thumbnail
        Returns:
            im (np.array): thumbnail as an RGB numpy array 
        """
        # TODO: check this downscaling is ok
        size = self.dimensions[level]
        region = Region(location=Point(0, 0), size=size, level=level)
        im = self.read_region(region)
        im = im.convert("RGB")
        im = np.asarray(im)
        return im