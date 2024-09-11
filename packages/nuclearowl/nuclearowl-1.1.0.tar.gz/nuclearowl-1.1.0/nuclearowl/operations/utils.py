import torch
import numpy as np
from scipy.ndimage import label
from nuclearowl.operations.kernels import Kernel3D


def to_cuda(tensor, device_id=0):
    """
    Move a tensor to the specified CUDA device.

    Parameters:
    tensor (torch.Tensor): The tensor to move to CUDA.
    device_id (int, optional): The ID of the CUDA device to move the tensor to. Default is 0.

    Returns:
    torch.Tensor: The tensor moved to the specified CUDA device.
    """
    return tensor.to(device=f"cuda:{device_id}")


def to_cpu(tensor):
    """
    Move a tensor to the CPU.

    Parameters:
    tensor (torch.Tensor): The tensor to move to the CPU.

    Returns:
    torch.Tensor: The tensor moved to the CPU.
    """
    return tensor.to(device="cpu")


def prepare_kernel(kernel_size=1):
    """
    Prepare a 3D cross-shaped kernel for dilation on a CUDA device.

    Parameters:
    kernel_size (int, optional): The size parameter for the cross-shaped kernel. Default is 1.

    Returns:
    torch.Tensor: The prepared 3D cross-shaped kernel on a CUDA device.
    """
    return Kernel3D.cross(kernel_size).to(device="cuda").unsqueeze(0).unsqueeze(0)


def prepare_mask(mask):
    """
    Transfers data on a CUDA device.

    Parameters:
    mask: A torch tensor.

    Returns:
    torch.Tensor: The tensor on a CUDA device.
    """
    return mask.to(device="cuda")


def find_bdrs_in_dim(mask, dimension):
    """
    Find the boundaries in a specific dimension where the mask is non-zero.

    Parameters:
    mask (torch.Tensor): The input mask.
    dimension (int): The dimension in which to find the boundaries.

    Returns:
    tuple: A tuple containing the indices of the first and last non-zero elements in the specified dimension.
    """
    dims = tuple(i for i in range(3) if i != dimension)
    A = torch.nonzero(torch.any(mask, dim=dims))
    return (A[0].item(), A[-1].item())


def find_bdrs(mask):
    """
    Find the boundaries in all three dimensions where the mask is non-zero.

    Parameters:
    mask (torch.Tensor): The input mask.

    Returns:
    tuple: A tuple containing three tuples, each representing the boundaries in one of the three dimensions.
    """
    bdrs = tuple(find_bdrs_in_dim(mask, i) for i in range(3))
    return bdrs


def find_biforkation_point(mask, dimension=2, BUFFER_THREASHOLD=3):
    """
    Identifies the bifurcation point in a 3D binary mask along a specified dimension.

    The bifurcation point is where exactly two distinct segments (features) appear in a slice of the mask,
    considering a buffer threshold to handle false positives or outliers. The function starts from the topmost
    slice along the specified dimension and moves downward until it finds a slice with exactly two distinct
    segments, adjusted by a buffer threshold to avoid false alarms.

    Args:
        mask (np.ndarray): A 3D binary numpy array (shape: [height, width, depth]) where each voxel is
                           either 0 (background) or 1 (foreground). The function operates along the specified
                           dimension.
        dimension (int, optional): The dimension along which to find the bifurcation point (0 for x, 1 for y, 2 for z).
                                   Defaults to 2, which is the z-dimension.
        BUFFER_THREASHOLD (int, optional): An integer threshold to determine how many slices with false alarms
                                            or outliers can be tolerated before confirming a bifurcation point.
                                            Defaults to 3.

    Returns:
        int: The index of the slice along the specified dimension which is identified as the bifurcation point.
              This is the slice where exactly two distinct features are found, adjusted by the buffer.
    Notes:
        Assumes that there exists a biforcation. In other cases the result of this function might be ill !!!
    Raises:
        ValueError: If the dimension argument is not within the range [0, 2].

    Example:
        mask = np.random.randint(0, 2, size=(100, 100, 50))  # A random binary mask with shape [100, 100, 50]
        dimension = 2
        buffer_threshold = 3
        bifork_point = find_biforkation_point(mask, dimension, buffer_threshold)
        print(f"Bifurcation point along dimension {dimension}: {bifork_point}")
    """
    mask = to_cpu(mask)
    if dimension not in (0, 1, 2):
        raise ValueError(
            "Dimension must be 0 (x-axis), 1 (y-axis), or 2 (z-axis).")

    axes = tuple(i for i in range(3) if i != dimension)
    upper_bound = np.where(np.any(mask, axis=axes))[0][-1]
    BUFFER = 0

    i = upper_bound - 2
    while True:
        labeled_arr, num_features = label(mask.take(i, axis=dimension))

        if num_features == 2 and BUFFER > BUFFER_THREASHOLD:
            break
        elif num_features == 2 and BUFFER <= BUFFER_THREASHOLD:
            BUFFER += 1
        elif num_features == 1 and BUFFER > 0:  # We indeed encountered false alarm
            BUFFER = 0
        i -= 1

    bifork_point = i + BUFFER
    return bifork_point


def get_roi_bdrs(mask, num_vox):
    """
    Get the boundaries of the region of interest (ROI) expanded by a specified number of voxels.

    Parameters:
    mask (torch.Tensor): The input mask.
    num_vox (int): The number of voxels by which to expand the ROI.

    Returns:
    tuple: A tuple containing three tuples, each representing the expanded boundaries in one of the three dimensions.
    """
    shape = mask.shape
    borders = find_bdrs(mask)
    return (
        (max(0, borders[0][0] - num_vox),
         min(shape[0], borders[0][1] + num_vox)),
        (max(0, borders[1][0] - num_vox),
         min(shape[1], borders[1][1] + num_vox)),
        (max(0, borders[2][0] - num_vox),
         min(shape[2], borders[2][1] + num_vox))
    )


def get_roi_size(mask, num_vox):
    """
    Get the size of the region of interest (ROI) expanded by a specified number of voxels.

    Parameters:
    mask (torch.Tensor): The input mask.
    num_vox (int): The number of voxels by which to expand the ROI.

    Returns:
    tuple: A tuple containing the size of the expanded ROI in each of the three dimensions.
    """
    roi = get_roi_bdrs(mask, num_vox)
    return (
        roi[0][1] - roi[0][0],
        roi[1][1] - roi[1][0],
        roi[2][1] - roi[2][0]
    )


def is_small_roi(size, threshold=6):
    """
    Check if the region of interest (ROI) is considered small based on a threshold.

    Parameters:
    size (tuple): The size of the ROI in each of the three dimensions.
    threshold (int, optional): The threshold below which the ROI is considered small. Default is 6.

    Returns:
    bool: True if the ROI is small in any dimension, False otherwise.
    """
    return any(size[i] < threshold for i in range(3))


class Binary:
    @staticmethod
    def check_overlap(mask1, mask2):
        try:
            borders1 = find_bdrs(mask1)  # Might fail if everything is zero
            borders2 = find_bdrs(mask2)
        except:
            return False

        x_overlap = not (borders1[0][1] < borders2[0]
                         [0] or borders1[0][0] > borders2[0][1])
        y_overlap = not (borders1[1][1] < borders2[1]
                         [0] or borders1[1][0] > borders2[1][1])
        z_overlap = not (borders1[2][1] < borders2[2]
                         [0] or borders1[2][0] > borders2[2][1])

        return x_overlap and y_overlap and z_overlap
