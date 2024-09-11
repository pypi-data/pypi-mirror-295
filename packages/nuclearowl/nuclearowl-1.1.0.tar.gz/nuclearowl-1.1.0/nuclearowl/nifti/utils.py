import numpy as np
from nuclearowl.nifti.fileIO import get_array_from_nifti, save_nifti
from typing import Tuple
import nibabel as nib


def get_volume_of_voxel(nifti_path: str) -> float:
    """
    Calculates the volume of a voxel in a NIfTI image.

    The volume is computed using the determinant of the affine transformation matrix
    which describes the spatial orientation and resolution of the voxel in the image.

    Parameters:
    - nifti_path (str): Path to the NIfTI file.

    Returns:
    - float: The volume of a single voxel in cubic millimeters (mm³).

    Raises:
    - FileNotFoundError: If the specified NIfTI file does not exist or cannot be accessed.
    - ValueError: If there is an issue with the affine matrix extraction.
    """
    header, affine = get_nifti_options(nifti_path)
    vol = np.linalg.det(affine[:3, :3])
    return vol


def get_nifti_options(nifti_path: str) -> Tuple[nib.Nifti1Header, np.ndarray]:
    """
    Loads a NIfTI file and retrieves the header and affine transformation matrix.

    This function reads the NIfTI file specified by `nifti_path` and returns the header and affine transformation matrix.

    Parameters:
    - nifti_path (str): Path to the NIfTI file.

    Returns:
    - Tuple[nib.Nifti1Header, np.ndarray]: A tuple containing the NIfTI header and the affine transformation matrix.

    Raises:
    - FileNotFoundError: If the specified NIfTI file does not exist or cannot be accessed.
    - nib.filebasedimages.ImageFileError: If the NIfTI file cannot be read or is invalid.
    """
    img = nib.load(nifti_path)
    header = img.header
    affine = img.affine
    return header, affine


def copy_header_from_file(source_nifti_path: str, target_nifti_path: str)->None:
    """
    Copies the header and affine information from the source NIfTI file to the target NIfTI file.

    Parameters:
    - source_nifti_path (str): Path to the source NIfTI file from which the header and affine will be copied.
    - target_nifti_path (str): Path to the target NIfTI file which will receive the header and affine information.

    Returns:
    - None
    """
    header, affine = get_nifti_options(source_nifti_path)
    target_img = get_array_from_nifti(source_nifti_path)
    save_nifti(target_img, target_nifti_path, header, affine)



def get_dimensions_of_nifti_array(nifti_path: str) -> Tuple[int]:
    """ 
    Retrieves the shape of the underlying array.

    Parameters:
    - nifti_path: Path to nifti file.

    Returns:
    - Tuple(3d)

    Raises:
    - FileNotFoundError: If the specified NIfTI file does not exist or cannot be accessed.
    - nib.filebasedimages.ImageFileError: If the NIfTI file cannot be read or is invalid.

    """
    header, affine = get_nifti_options(nifti_path)
    return header.get_data_shape()[-3:]


def get_length_per_pixel(nifti_path: str) -> float:
    """
    Calculates the length of a pixel (voxel side length) in a NIfTI image.

    This function computes the mean length of the voxel edges, assuming that the image is isotropic.
    If the voxel dimensions are non-isotropic (i.e., dimensions vary significantly), an exception is raised.

    Parameters:
    - nifti_path (str): Path to the NIfTI file.

    Returns:
    - float: The mean length of the voxel edges in millimeters (mm).

    Raises:
    - FileNotFoundError: If the specified NIfTI file does not exist or cannot be accessed.
    - ValueError: If the voxel dimensions are non-isotropic (i.e., the standard deviation of voxel dimensions is greater than 0.1).
    """
    header, affine = get_nifti_options(nifti_path)
    S = affine.diagonal()[:-1]
    if np.std(S) > 0.1:
        raise ValueError(
            "Non isotropic NIfTI image: voxel dimensions vary significantly.")
    else:
        return np.mean(S)
