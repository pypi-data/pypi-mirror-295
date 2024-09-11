import cc3d
import numpy as np
import torch
from typing import Callable
from nuclearowl.operations.utils import to_cuda, to_cpu
from nuclearowl.operations.mask import Elementary
"""
I want to have a mask as an input and a statistical output (array, number, etc. but not an image)
Also it should not be connected to nifti or any other medical imaging.

"""


def calc_num_lesions(mask):
    """
    Calculate the number of lesions in a given mask.

    This function uses connected component analysis to count the number of distinct lesions in a binary mask.

    Parameters:
    mask (numpy.ndarray or torch.Tensor): Input binary mask where lesions are marked with non-zero values.

    Returns:
    int: The number of distinct lesions in the mask.
    """
    mask = to_cpu(mask)
    lab = cc3d.connected_components(mask)
    return np.max(lab)


def calc_non_zero_voxels(mask):
    """
    Calculate the number of non-zero voxels in a given mask.

    This function creates a binary mask where voxels with non-zero values in the input mask are marked as 1,
    and then counts the total number of such voxels.

    Parameters:
    mask (torch.Tensor): Input mask where non-zero voxels are to be counted.

    Returns:
    int: The number of non-zero voxels in the mask.
    """
    binary_mask = Elementary.get_binary_mask_based_on_condition(mask, lambda x: x != 0)
    return torch.sum(binary_mask).item()


def calc_voxels_above_threshold(mask, threshold, equal=False):
    """
    Calculate the number of voxels in the mask above a given threshold.

    This function counts the number of voxels in the input mask that are above a specified threshold.
    It can optionally include voxels that are equal to the threshold.

    Parameters:
    mask (torch.Tensor): Input mask.
    threshold (float): Threshold value.
    equal (bool, optional): If True, includes voxels equal to the threshold. Default is False.

    Returns:
    int: The number of voxels above (or above and equal to) the threshold.
    """
    mask = to_cuda(mask)
    if equal:
        return torch.sum(mask >= threshold).item()
    else:
        return torch.sum(mask > threshold).item()


def calc_voxels_based_on_condition(mask, condition: Callable):
    """
    Calculate the number of voxels in the mask that satisfy a given condition.

    This function counts the number of voxels in the input mask that meet the criteria defined by the condition function.

    Parameters:
    mask (torch.Tensor): Input mask.
    condition (Callable): A function that takes a voxel value and returns True if the condition is met, and False otherwise.

    Returns:
    int: The number of voxels satisfying the condition.
    """
    return torch.sum(Elementary.get_binary_mask_based_on_condition(mask, condition)).item()


def extract_values_based_on_binary_mask(mask, binary_mask):
    """
    Extract values from the mask based on a binary mask.

    This function extracts the values from the input mask at positions where the binary mask has non-zero values.

    Parameters:
    mask (torch.Tensor): Input mask.
    binary_mask (torch.Tensor): Binary mask indicating the positions to extract values from.

    Returns:
    torch.Tensor: Extracted values from the input mask.
    """
    mask = to_cuda(mask)
    binary_mask = to_cuda(binary_mask)
    vals = mask[binary_mask != 0]
    return vals


def extract_values_based_on_condition(mask, condition: Callable):
    """
    Extract values from the mask based on a condition.

    This function extracts the values from the input mask that satisfy the given condition function.

    Parameters:
    mask (torch.Tensor): Input mask.
    condition (Callable): A function that takes a voxel value and returns True if the condition is met, and False otherwise.

    Returns:
    torch.Tensor: Extracted values from the input mask that satisfy the condition.
    """
    binary_mask = Elementary.get_binary_mask_based_on_condition(mask, condition)
    return mask[binary_mask]
