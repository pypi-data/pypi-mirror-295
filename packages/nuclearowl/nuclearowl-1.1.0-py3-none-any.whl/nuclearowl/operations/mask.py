from nuclearowl.operations.utils import *
from nuclearowl.operations.kernels import Kernel2D, Kernel3D
import torch
import torch.nn.functional as F
import SimpleITK as sitk
import sys
from typing import Callable, Tuple

"""
I want to have a mask as an input and output!!!! In this file
Also it should not be connected to nifti or any other medical imaging.

"""


class Binary:
    """
    A class providing binary operations for tensor masks, using floating-point precision handling.

    Attributes:
    - ZERO_p (float): A small positive value used as the threshold for zero in floating-point operations.
    - ZERO_m (float): A small negative value used as the threshold for zero in floating-point operations.
    - ONE_p (float): A small positive value greater than one, used for floating-point comparisons.
    - ONE_m (float): A small negative value less than one, used for floating-point comparisons.
    """

    ZERO_p = sys.float_info.epsilon
    ZERO_m = -sys.float_info.epsilon
    ONE_p = 1.0 + sys.float_info.epsilon
    ONE_m = 1.0 - sys.float_info.epsilon

    @staticmethod
    def addition(*masks: torch.Tensor) -> torch.Tensor:
        """
        Perform element-wise addition of multiple masks and return a binary mask indicating where the sum is greater than zero.

        Parameters:
        - masks (torch.Tensor): Variable number of binary masks (tensors) to be added.

        Returns:
        - torch.Tensor: A binary mask where each element is True if the sum of the corresponding elements in the input masks is greater than zero, otherwise False.

        Example:
        ```python
        mask1 = torch.tensor([[1, 0], [0, 1]])
        mask2 = torch.tensor([[0, 1], [1, 0]])
        result = Binary.addition(mask1, mask2)
        ```
        """
        master = masks[0]
        for mask in masks[1:]:
            master += mask
        return master > Binary.ZERO_p

    @staticmethod
    def subtract(mask_a: torch.Tensor, mask_b: torch.Tensor) -> torch.Tensor:
        """
        Subtract one binary mask from another and return a binary mask indicating where the result is greater than zero.

        Parameters:
        - mask_a (torch.Tensor): The mask to be subtracted from.
        - mask_b (torch.Tensor): The mask to subtract.

        Returns:
        - torch.Tensor: A binary mask where each element is True if the result of the subtraction is greater than zero, otherwise False.

        Example:
        ```python
        mask_a = torch.tensor([[1, 1], [0, 1]])
        mask_b = torch.tensor([[0, 1], [0, 0]])
        result = Binary.subtract(mask_a, mask_b)
        ```
        """
        return (mask_a.float() - mask_b.float()) > Binary.ZERO_p

    @staticmethod
    def voxel_xor(mask_a: torch.Tensor, mask_b: torch.Tensor) -> torch.Tensor:
        """
        Perform element-wise XOR operation on two binary masks.

        Parameters:
        - mask_a (torch.Tensor): The first binary mask.
        - mask_b (torch.Tensor): The second binary mask.

        Returns:
        - torch.Tensor: The result of the XOR operation between the two masks.

        Example:
        ```python
        mask_a = torch.tensor([[1, 0], [0, 1]])
        mask_b = torch.tensor([[0, 1], [1, 0]])
        result = Binary.voxel_xor(mask_a, mask_b)
        ```
        """
        return torch.bitwise_xor(mask_a, mask_b)

    @staticmethod
    def voxel_and(mask_a: torch.Tensor, mask_b: torch.Tensor) -> torch.Tensor:
        """
        Perform element-wise AND operation on two binary masks.

        Parameters:
        - mask_a (torch.Tensor): The first binary mask.
        - mask_b (torch.Tensor): The second binary mask.

        Returns:
        - torch.Tensor: The result of the AND operation between the two masks.

        Example:
        ```python
        mask_a = torch.tensor([[1, 0], [1, 1]])
        mask_b = torch.tensor([[1, 1], [0, 1]])
        result = Binary.voxel_and(mask_a, mask_b)
        ```
        """
        return torch.bitwise_and(mask_a, mask_b)

    @staticmethod
    def voxel_or(mask_a: torch.Tensor, mask_b: torch.Tensor) -> torch.Tensor:
        """
        Perform element-wise OR operation on two binary masks by using the addition method.

        Parameters:
        - mask_a (torch.Tensor): The first binary mask.
        - mask_b (torch.Tensor): The second binary mask.

        Returns:
        - torch.Tensor: A binary mask where each element is True if at least one of the corresponding elements in the input masks is True, otherwise False.

        Example:
        ```python
        mask_a = torch.tensor([[1, 0], [1, 1]])
        mask_b = torch.tensor([[0, 1], [1, 0]])
        result = Binary.voxel_or(mask_a, mask_b)
        ```
        """
        return Binary.addition(mask_a, mask_b)

    @staticmethod
    def voxel_not(mask: torch.Tensor) -> torch.Tensor:
        """
        Perform element-wise NOT operation on a binary mask.

        Parameters:
        - mask (torch.Tensor): The binary mask to be negated.

        Returns:
        - torch.Tensor: A binary mask where each element is True if the corresponding element in the input mask is less than zero, otherwise False.

        Example:
        ```python
        mask = torch.tensor([[1, 0], [0, 1]])
        result = Binary.voxel_not(mask)
        ```
        """
        return mask.float() < Binary.ZERO_m

    @staticmethod
    def count_positive(mask: torch.Tensor) -> int:
        """
        Count the number of positive elements in the binary mask.

        Parameters:
        - mask (torch.Tensor): The binary mask where positive elements are counted.

        Returns:
        - int: The count of elements in the mask that are greater than Binary.ONE_m.

        Example:
        ```python
        mask = torch.tensor([[1, 0], [0, 1]])
        count = Binary.count_positive(mask)
        ```
        """
        return int(torch.sum(mask > Binary.ONE_m).item())

    @staticmethod
    def count_zeros(mask: torch.Tensor) -> int:
        """
        Count the number of zero elements in the binary mask.

        Parameters:
        - mask (torch.Tensor): The binary mask where zero elements are counted.

        Returns:
        - int: The count of elements in the mask that are less than Binary.ZERO_p.

        Example:
        ```python
        mask = torch.tensor([[1, 0], [0, 1]])
        count = Binary.count_zeros(mask)
        ```
        """
        return int(torch.sum(mask < Binary.ZERO_p).item())


class Elementary:
    """
    A class providing elementary operations for tensor masks, including 2D and 3D convolutions,
    mask overlay, and binary mask generation based on conditions.

    Methods:
    - conv_2d(tensor: torch.Tensor, kernel: torch.Tensor, padding: int = 1) -> torch.Tensor
    - conv_3d(tensor: torch.Tensor, kernel: torch.Tensor, padding: int = 1) -> torch.Tensor
    - apply_conv3d(mask: torch.Tensor, kernel: torch.Tensor, num_vox: int) -> torch.Tensor
    - overlay(mask_a: torch.Tensor, mask_b: torch.Tensor) -> torch.Tensor
    - get_binary_mask_based_on_condition(mask: torch.Tensor, condition: Callable[[torch.Tensor], torch.Tensor]) -> torch.Tensor
    - zero_out_slices(mask: torch.Tensor, dimension: int, pixels_from_top: int, pixels_from_bottom: int) -> torch.Tensor
    """

    @staticmethod
    def conv_2d(tensor: torch.Tensor, kernel: torch.Tensor, padding: int = 1) -> torch.Tensor:
        """
        Perform a 2D convolution on a tensor using the specified kernel.

        Parameters:
        - tensor (torch.Tensor): The input tensor to be convolved.
        - kernel (torch.Tensor): The convolution kernel.
        - padding (int, optional): The padding to be added to each side of the tensor. Default is 1.

        Returns:
        - torch.Tensor: The result of the 2D convolution.

        Example:
        ```python
        tensor = torch.randn(5, 5)
        kernel = torch.randn(3, 3)
        result = Elementary.conv_2d(tensor, kernel)
        ```
        """
        dilated_tensor = tensor.unsqueeze(0).unsqueeze(0)
        dilated_kernel = kernel.unsqueeze(0).unsqueeze(0)
        con = F.conv2d(dilated_tensor, dilated_kernel, padding=padding)
        return con.squeeze()

    @staticmethod
    def conv_3d(tensor: torch.Tensor, kernel: torch.Tensor, padding: int = 1) -> torch.Tensor:
        """
        Perform a 3D convolution on a tensor using the specified kernel.

        Parameters:
        - tensor (torch.Tensor): The input tensor to be convolved.
        - kernel (torch.Tensor): The convolution kernel.
        - padding (int, optional): The padding to be added to each side of the tensor. Default is 1.

        Returns:
        - torch.Tensor: The result of the 3D convolution.

        Example:
        ```python
        tensor = torch.randn(5, 5, 5)
        kernel = torch.randn(3, 3, 3)
        result = Elementary.conv_3d(tensor, kernel)
        ```
        """
        dilated_tensor = tensor.unsqueeze(0).unsqueeze(0)
        dilated_kernel = kernel.unsqueeze(0).unsqueeze(0)
        con = F.conv3d(dilated_tensor, dilated_kernel, padding=padding)
        return con.squeeze()

    @staticmethod
    def apply_conv3d(mask: torch.Tensor, kernel: torch.Tensor, num_vox: int) -> torch.Tensor:
        """
        Apply a 3D convolution to a mask multiple times.

        Parameters:
        - mask (torch.Tensor): The input mask to be convolved.
        - kernel (torch.Tensor): The convolution kernel.
        - num_vox (int): The number of times to apply the convolution.

        Returns:
        - torch.Tensor: The result of applying the 3D convolution multiple times.

        Example:
        ```python
        mask = torch.randn(5, 5, 5)
        kernel = torch.randn(3, 3, 3)
        result = Elementary.apply_conv3d(mask, kernel, 3)
        ```
        """
        mask = mask.unsqueeze(0).unsqueeze(0)
        con_image = F.conv3d(mask, kernel, padding=1)
        for _ in range(num_vox - 1):
            con_image = F.conv3d(con_image, kernel, padding=1)
        return con_image
    
    def interpolate(tensor:torch.Tensor, size:Tuple[int], mode="trilinear", align_corners:bool=False):
        """
        Perform interpolation on a tensor using a specific mode.

        Parameters:
        - tensor (torch.Tensor): The input tensor to be interpolated.
        - size (torch.Tensor): The target size of the interpolation.
        - mode (int, optional): The mode of interpolation (default=trilinear)
        - align_corners(bool): Forces the corners of the input and target tensor to be similiar.

        Returns:
        - torch.Tensor: The result of the 3D convolution.

        Example:
        ```python
        tensor = torch.randn(5, 5, 5)
        size = (100, 100, 100)
        result = Elementary.conv_3d(tensor, kernel)
        ```
        """
        tensor = tensor.unsqueeze(0).unsqueeze(0)      
        resized_tensor = F.interpolate(tensor, size=size, mode=mode, align_corners=align_corners)
        return resized_tensor.squeeze()

    @staticmethod
    def overlay(mask_a: torch.Tensor, mask_b: torch.Tensor) -> torch.Tensor:
        """
        Perform element-wise multiplication (overlay) of two masks.

        Parameters:
        - mask_a (torch.Tensor): The first mask.
        - mask_b (torch.Tensor): The second mask.

        Returns:
        - torch.Tensor: The result of element-wise multiplication of the two masks.

        Example:
        ```python
        mask_a = torch.tensor([[1, 0], [1, 1]])
        mask_b = torch.tensor([[0, 1], [1, 0]])
        result = Elementary.overlay(mask_a, mask_b)
        ```
        """
        return mask_a * mask_b

    @staticmethod
    def get_binary_mask_based_on_condition(mask: torch.Tensor, condition: Callable[[torch.Tensor], torch.Tensor]) -> torch.Tensor:
        """
        Generate a binary mask based on a specified condition function applied to the input mask.

        Parameters:
        - mask (torch.Tensor): The input mask to be processed.
        - condition (Callable[[torch.Tensor], torch.Tensor]): A function that takes a tensor and returns a binary mask.

        Returns:
        - torch.Tensor: A binary mask resulting from applying the condition function to the input mask.

        Example:
        ```python
        mask = torch.tensor([[1, 0], [0, 1]])
        condition = lambda x: x > 0
        result = Elementary.get_binary_mask_based_on_condition(mask, condition)
        ```
        """
        return condition(mask)

    def zero_out_slices(mask: torch.Tensor, dimension: int, pixels_from_top: int, pixels_from_bottom: int) -> torch.Tensor:
        """
        Zero out a specified number of slices from the top and bottom in a given dimension.

        Parameters:
        mask (torch.Tensor): The input mask.
        dimension (int): The dimension in which to zero out slices.
        pixels_from_top (int): The number of slices to zero out from the top.
        pixels_from_bottom (int): The number of slices to zero out from the bottom.

        Returns:
        torch.Tensor: The mask with the specified slices zeroed out.
        """
        bdrs = find_bdrs_in_dim(mask, dimension)
        mask.narrow(dimension, bdrs[0], pixels_from_top).zero_()
        mask.narrow(
            dimension, bdrs[1] - pixels_from_bottom + 1, pixels_from_bottom).zero_()
        return mask


class Common:
    """
    A class providing common image processing operations for binary masks, including removal of single islands,
    dilation, erosion, and optimized versions of dilation and erosion.

    Methods:
    - remove_single_islands_2d(tensor: torch.Tensor) -> torch.Tensor
    - remove_single_islands_3d(tensor: torch.Tensor) -> torch.Tensor
    - dilation(mask: torch.Tensor, num_vox: int) -> torch.Tensor
    - erosion(mask: torch.Tensor, num_vox: int) -> torch.Tensor
    - fast_dilation(mask: torch.Tensor, num_vox: int) -> torch.Tensor
    - fast_erosion(mask: torch.Tensor, num_vox: int) -> torch.Tensor
    """

    @staticmethod
    def remove_single_islands_2d(tensor: torch.Tensor) -> torch.Tensor:
        """
        Remove single-pixel islands in a 2D binary mask.

        Parameters:
        - tensor (torch.Tensor): The input 2D binary mask.

        Returns:
        - torch.Tensor: The 2D binary mask with single-pixel islands removed.

        Example:
        ```python
        tensor = torch.tensor([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        result = Common.remove_single_islands_2d(tensor)
        ```
        """
        tensor = to_cuda(tensor)
        con = Elementary.conv_2d(tensor, Kernel2D.cross(1))
        threshold = con >= 2
        return tensor * threshold

    @staticmethod
    def remove_single_islands_3d(tensor: torch.Tensor) -> torch.Tensor:
        """
        Remove single-pixel islands in a 3D binary mask.

        Parameters:
        - tensor (torch.Tensor): The input 3D binary mask.

        Returns:
        - torch.Tensor: The 3D binary mask with single-pixel islands removed.

        Example:
        ```python
        tensor = torch.tensor([[[0, 1, 0], [1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1], [0, 1, 0]]])
        result = Common.remove_single_islands_3d(tensor)
        ```
        """
        tensor = to_cuda(tensor)
        con = Elementary.conv_3d(tensor, Kernel3D.cross(1))
        threshold = con >= 2
        return tensor * threshold

    @staticmethod
    def dilation(mask: torch.Tensor, num_vox: int) -> torch.Tensor:
        """
        Perform dilation on a 3D binary mask using a specified kernel.

        Parameters:
        - mask (torch.Tensor): The input 3D binary mask.
        - num_vox (int): The number of voxels to apply dilation.

        Returns:
        - torch.Tensor: The dilated 3D binary mask.

        Example:
        ```python
        mask = torch.tensor([[[0, 1, 0], [1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1], [0, 1, 0]]])
        result = Common.dilation(mask, 2)
        ```
        """
        kernel = prepare_kernel()
        mask = prepare_mask(mask)
        con_image = Elementary.apply_conv3d(mask, kernel, num_vox)
        return con_image.squeeze() > 0

    @staticmethod
    def erosion(mask: torch.Tensor, num_vox: int) -> torch.Tensor:
        """
        Perform erosion on a 3D binary mask using a specified kernel.

        Parameters:
        - mask (torch.Tensor): The input 3D binary mask.
        - num_vox (int): The number of voxels to apply erosion.

        Returns:
        - torch.Tensor: The eroded 3D binary mask.

        Example:
        ```python
        mask = torch.tensor([[[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]]])
        result = Common.erosion(mask, 2)
        ```
        """
        kernel = prepare_kernel()
        mask = prepare_mask(mask)
        K = kernel.sum().item()
        con_image = Elementary.apply_conv3d(mask, kernel, num_vox)
        return con_image.squeeze() >= K ** num_vox

    @staticmethod
    def fast_dilation(mask: torch.Tensor, num_vox: int) -> torch.Tensor:
        """
        Perform optimized dilation on a 3D binary mask by processing only the region of interest (ROI).

        Parameters:
        - mask (torch.Tensor): The input 3D binary mask.
        - num_vox (int): The number of voxels to apply dilation.

        Returns:
        - torch.Tensor: The dilated 3D binary mask.

        Example:
        ```python
        mask = torch.tensor([[[0, 1, 0], [1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1], [0, 1, 0]]])
        result = Common.fast_dilation(mask, 2)
        ```
        """
        mask = to_cuda(mask)
        roi = get_roi_bdrs(mask, num_vox)
        size = get_roi_size(mask, num_vox)

        if is_small_roi(size):
            return Elementary.dilation(mask, num_vox)

        mask_under_edit = mask[roi[0][0]:roi[0][1], roi[1]
                               [0]:roi[1][1], roi[2][0]:roi[2][1]].clone()
        threshold = Elementary.dilation(mask_under_edit, num_vox)
        mask[roi[0][0]:roi[0][1], roi[1][0]:roi[1]
             [1], roi[2][0]:roi[2][1]] = threshold

        return mask

    @staticmethod
    def fast_erosion(mask: torch.Tensor, num_vox: int) -> torch.Tensor:
        """
        Perform optimized erosion on a 3D binary mask by processing only the region of interest (ROI).

        Parameters:
        - mask (torch.Tensor): The input 3D binary mask.
        - num_vox (int): The number of voxels to apply erosion.

        Returns:
        - torch.Tensor: The eroded 3D binary mask.

        Example:
        ```python
        mask = torch.tensor([[[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]]])
        result = Common.fast_erosion(mask, 2)
        ```
        """
        mask = to_cuda(mask)
        try:
            roi = get_roi_bdrs(mask, num_vox)
        except:
            return torch.zeros_like(mask)

        size = get_roi_size(mask, num_vox)
        if is_small_roi(size):
            return torch.zeros_like(mask)

        mask_under_edit = mask[roi[0][0]:roi[0][1], roi[1]
                               [0]:roi[1][1], roi[2][0]:roi[2][1]].clone()
        threshold = Elementary.erosion(mask_under_edit, num_vox)
        mask[roi[0][0]:roi[0][1], roi[1][0]:roi[1]
             [1], roi[2][0]:roi[2][1]] = threshold

        return mask


class Resample:
    """
    A class for resampling medical images using SimpleITK. The class provides functionality to resample 
    images to match the spacing, size, and direction of a reference image. It supports both binary and 
    non-binary images.

    Attributes:
    - basis (str): The file path to the reference image that provides the target spacing, size, and direction.
    - input (str): The file path to the input image to be resampled.
    - output (str): The file path where the resampled image will be saved.
    - binary (bool): A flag indicating whether the input image is binary (True) or not (False). 

    Methods:
    - __init__(self, basis: str, input: str, output: str, binary: bool = False) -> None
    - _resample_sitk_seg_binary(seg: sitk.Image, reference: sitk.Image) -> sitk.Image
    - _resample_sitk_seg(seg: sitk.Image, reference: sitk.Image, interpolator: sitk.InterpolatorEnum) -> sitk.Image
    - main_resample(basis: str = None, input: str = None, output: str = None, binary: bool = False) -> None
    - __call__(self) -> None

    Example:
    reference = "./iso_ct.nii.gz"
    input = "./pet.nii.gz"
    output = "./iso_pet.nii.gz"
    Resample(reference, input, output)()
    """

    def __init__(self, basis: str, input: str, output: str, binary: bool = False) -> "Resample":
        """
        Initializes the Resample class with the given parameters.

        Parameters:
        - basis (str): The file path to the reference image.
        - input (str): The file path to the input image to be resampled.
        - output (str): The file path to save the resampled image.
        - binary (bool): A flag to indicate if the input image is binary. Default is False.
        """
        self.basis = basis
        self.input = input
        self.output = output
        self.binary = binary
        return self

    @staticmethod
    def _resample_sitk_seg_binary(seg: sitk.Image, reference: sitk.Image) -> sitk.Image:
        """
        Resamples a binary segmentation image to match the spacing, size, and direction of the reference image.

        Parameters:
        - seg (sitk.Image): The binary segmentation image to be resampled.
        - reference (sitk.Image): The reference image providing the target spacing, size, and direction.

        Returns:
        - sitk.Image: The resampled binary segmentation image.
        """
        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputSpacing(reference.GetSpacing())
        resampler.SetSize(reference.GetSize())
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
        resampler.SetOutputOrigin(reference.GetOrigin())
        resampler.SetOutputDirection(reference.GetDirection())
        resampler.SetOutputPixelType(sitk.sitkUInt32)
        resampled = resampler.Execute(seg)
        return resampled

    @staticmethod
    def _resample_sitk_seg(seg: sitk.Image, reference: sitk.Image, interpolator = sitk.sitkLinear) -> sitk.Image:
        """
        Resamples a general image to match the spacing, size, and direction of the reference image.

        Parameters:
        - seg (sitk.Image): The image to be resampled.
        - reference (sitk.Image): The reference image providing the target spacing, size, and direction.
        - interpolator (sitk.InterpolatorEnum): The interpolation method to be used. Default is Linear interpolation.

        Returns:
        - sitk.Image: The resampled image.
        """
        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputSpacing(reference.GetSpacing())
        resampler.SetSize(reference.GetSize())
        resampler.SetInterpolator(interpolator)
        resampler.SetOutputOrigin(reference.GetOrigin())
        resampler.SetOutputDirection(reference.GetDirection())
        resampler.SetOutputPixelType(sitk.sitkFloat32)
        resampled = resampler.Execute(seg)
        return resampled

    @staticmethod
    def main_resample(basis: str = None, input: str = None, output: str = None, binary: bool = False) -> None:
        """
        Main function to perform the resampling process. Reads the input and reference images, performs 
        resampling, and saves the output image.

        Parameters:
        - basis (str): The file path to the reference image.
        - input (str): The file path to the input image to be resampled.
        - output (str): The file path to save the resampled image.
        - binary (bool): A flag to indicate if the input image is binary. Default is False.

        Returns:
        - None
        """
        sitk_img = sitk.ReadImage(basis)
        sitk_seg = sitk.ReadImage(input)
        if binary:
            sitk_out = Resample._resample_sitk_seg_binary(sitk_seg, sitk_img)
        else:
            sitk_out = Resample._resample_sitk_seg(sitk_seg, sitk_img)
        sitk_out.SetDirection(sitk_img.GetDirection())
        sitk_out.SetOrigin(sitk_img.GetOrigin())
        sitk_out.SetSpacing(sitk_img.GetSpacing())
        sitk.WriteImage(sitk_out, output)

    def __call__(self) -> None:
        """
        Calls the main resampling function with the parameters initialized in the class instance.

        Returns:
        - None
        """
        Resample.main_resample(self.basis, self.input,
                               self.output, self.binary)
