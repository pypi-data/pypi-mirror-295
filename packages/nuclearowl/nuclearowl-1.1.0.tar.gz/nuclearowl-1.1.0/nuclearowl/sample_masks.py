import torch
import numpy as np
import nibabel as nib


class Mask2D:
    """
    Provides methods to create various 2D masks using PyTorch tensors.

    This class contains static methods to generate different types of 2D masks, which can be useful for image processing, 
    computer vision tasks, or other applications that require specific 2D patterns.

    Methods:
    - cross(size=(10,10), dtype=torch.float64): Creates a 2D cross-shaped mask.
    - square(size=(10,10), dtype=torch.float64): Creates a 2D square-shaped mask.
    - checkerboard_pattern(size=(10,10), dtype=torch.float64): Creates a 2D checkerboard pattern mask.
    - circle(size=(10,10), dtype=torch.float64): Creates a 2D circular mask.
    """

    @staticmethod
    def cross(size=(10, 10), dtype=torch.float64):
        """
        Creates a 2D cross-shaped mask.

        The cross is centered in the mask with vertical and horizontal lines of 1s spanning a fixed width.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (height, width). Default is (10, 10).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 2D tensor with the cross pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        A[3:6, 4] = 1
        A[4, 3:6] = 1
        return A

    @staticmethod
    def square(size=(10, 10), dtype=torch.float64):
        """
        Creates a 2D square-shaped mask.

        The square is centered in the mask with a fixed size.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (height, width). Default is (10, 10).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 2D tensor with the square pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        A[3:7, 3:7] = 1
        return A

    @staticmethod
    def checkerboard_pattern(size=(10, 10), dtype=torch.float64):
        """
        Creates a 2D checkerboard pattern mask.

        The mask alternates between 1s and 0s in a checkerboard pattern.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (height, width). Default is (10, 10).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 2D tensor with a checkerboard pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        A[::2, ::2] = 1
        return A

    @staticmethod
    def circle(size=(10, 10), dtype=torch.float64):
        """
        Creates a 2D circular mask.

        The circular mask is centered in the mask with a radius that covers a portion of the mask.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (height, width). Default is (10, 10).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 2D tensor with a circular pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 4
        y, x = torch.ogrid[:size[0], :size[1]]
        mask = (x - center[1])**2 + (y - center[0])**2 <= radius**2
        A[mask] = 1
        return A


class Mask3D:
    """
    Provides methods to create various 3D masks using PyTorch tensors.

    This class contains static methods to generate different types of 3D masks, which can be useful for 3D image processing
    or volumetric data.

    Methods:
    - cube(size=(100,100,100), dtype=torch.float64): Creates a 3D cube-shaped mask.
    - corner_cube(size=(100,100,100), dtype=torch.float64): Creates a 3D corner cube mask.
    - checkerboard_pattern(size=(100,100,100), dtype=torch.float64): Creates a 3D checkerboard pattern mask.
    - sphere(size=(100,100,100), dtype=torch.float64): Creates a 3D spherical mask.
    """

    @staticmethod
    def cube(size=(100, 100, 100), dtype=torch.float64):
        """
        Creates a 3D cube-shaped mask.

        The cube is centered in the mask with a fixed size.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (depth, height, width). Default is (100, 100, 100).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 3D tensor with a cube pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        A[30:70, 30:70, 30:70] = 1
        return A

    @staticmethod
    def corner_cube(size=(100, 100, 100), dtype=torch.float64):
        """
        Creates a 3D corner cube mask.

        The corner cube is located at the corner of the mask with a fixed size.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (depth, height, width). Default is (100, 100, 100).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 3D tensor with a corner cube pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        A[0:30, 0:30, 0:30] = 1
        return A

    @staticmethod
    def checkerboard_pattern(size=(100, 100, 100), dtype=torch.float64):
        """
        Creates a 3D checkerboard pattern mask.

        The mask alternates between 1s and 0s in a checkerboard pattern across all three dimensions.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (depth, height, width). Default is (100, 100, 100).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 3D tensor with a checkerboard pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        A[::2, ::2, ::2] = 1
        return A

    @staticmethod
    def sphere(size=(100, 100, 100), dtype=torch.float64):
        """
        Creates a 3D spherical mask.

        The spherical mask is centered in the mask with a radius that covers a portion of the mask.

        Parameters:
        - size: Tuple specifying the dimensions of the mask (depth, height, width). Default is (100, 100, 100).
        - dtype: Data type of the mask tensor. Default is torch.float64.

        Returns:
        - A 3D tensor with a spherical pattern.
        """
        A = torch.zeros(size=size, dtype=dtype)
        center = (size[0] // 2, size[1] // 2, size[2] // 2)
        radius = min(size) // 4
        z, y, x = torch.ogrid[:size[0], :size[1], :size[2]]
        mask = (x - center[0])**2 + (y - center[1])**2 + \
            (z - center[2])**2 <= radius**2
        A[mask] = 1
        return A


