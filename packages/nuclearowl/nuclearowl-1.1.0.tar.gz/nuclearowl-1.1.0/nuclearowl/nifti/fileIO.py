import nibabel as nib
import numpy as np
import torch
from nuclearowl.operations.utils import to_cpu


def get_array_from_nifti(nifti_path: str) -> np.ndarray:
    """
    Loads a NIfTI file and extracts the image data as a NumPy array.

    This function reads the NIfTI file specified by `nifti_path` and returns the image data as a NumPy array.

    Parameters:
    - nifti_path (str): Path to the NIfTI file.

    Returns:
    - np.ndarray: The image data from the NIfTI file as a NumPy array.

    Raises:
    - FileNotFoundError: If the specified NIfTI file does not exist or cannot be accessed.
    - nib.filebasedimages.ImageFileError: If the NIfTI file cannot be read or is invalid.
    """
    obj = nib.load(nifti_path)
    return obj.get_fdata()


def get_tensor_from_nifti(nifti_path: str, cuda=True, device_id=0) -> torch.Tensor:
    """
    Loads a NIfTI file and converts the image data to a PyTorch tensor.

    This function reads the NIfTI file specified by `nifti_path`, extracts the image data as a NumPy array, and then
    converts it to a PyTorch tensor.

    Parameters:
    - nifti_path (str): Path to the NIfTI file.

    Returns:
    - torch.Tensor: The image data from the NIfTI file as a PyTorch tensor.

    Raises:
    - FileNotFoundError: If the specified NIfTI file does not exist or cannot be accessed.
    - nib.filebasedimages.ImageFileError: If the NIfTI file cannot be read or is invalid.
    """
    if cuda:
        return torch.tensor(get_array_from_nifti(nifti_path)).to(device=f"cuda:{device_id}")
    else:
        return torch.tensor(get_array_from_nifti(nifti_path))


def save_nifti(mask_out: torch.Tensor, path_out: str, header: nib.Nifti1Header, affine: np.ndarray) -> None:
    """
    Saves a PyTorch tensor as a NIfTI file.

    This function converts the given PyTorch tensor to a NumPy array, then creates a NIfTI image using the provided
    header and affine transformation matrix, and saves it to the specified output path.

    Parameters:
    - mask_out (torch.Tensor): The image data to be saved as a NIfTI file.
    - path_out (str): Path where the NIfTI file will be saved.
    - header (nib.Nifti1Header): The header to be used for the NIfTI file.
    - affine (np.ndarray): The affine transformation matrix to be used for the NIfTI file.

    Returns:
    - None

    Raises:
    - TypeError: If `mask_out` is not a PyTorch tensor or cannot be converted to a NumPy array.
    - ValueError: If `header` or `affine` is not in the correct format or cannot be used to create a NIfTI file.
    - RuntimeError: If there is an error during the saving process.
    """
    mask_out = to_cpu(mask_out)
    out_img = nib.Nifti1Image(mask_out.numpy(), affine=affine, header=header)
    nib.save(out_img, path_out)


def save_tensor_as_nifti(tensor: torch.Tensor, filename: str) -> None:
    """
    Saves a PyTorch tensor as a NIfTI file with an identity affine matrix.

    This function converts the given PyTorch tensor to a NumPy array and creates a NIfTI image using an identity
    affine matrix. The resulting NIfTI file is saved to the specified filename.

    Parameters:
    - tensor (torch.Tensor): The image data to be saved as a NIfTI file.
    - filename (str): Path where the NIfTI file will be saved.

    Returns:
    - None

    Raises:
    - TypeError: If `tensor` is not a PyTorch tensor or cannot be converted to a NumPy array.
    - RuntimeError: If there is an error during the NIfTI file creation or saving process.
    """
    tensor = np.array(tensor, dtype=np.float64)
    nifti_img = nib.Nifti1Image(tensor, affine=np.eye(4))
    nib.save(nifti_img, filename)



