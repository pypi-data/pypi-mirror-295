import nibabel as nib
import numpy as np
import subprocess
from nibabel.processing import resample_to_output
from nuclearowl.nifti.fileIO import get_tensor_from_nifti, save_nifti
from nuclearowl.nifti.utils import get_dimensions_of_nifti_array, get_nifti_options
from nuclearowl.operations.mask import Elementary

def create_isotropic_nifti(input: str, output: str) -> None:
    """
    Resamples a NIfTI image to have isotropic voxel dimensions.

    This function adjusts the voxel dimensions of the input NIfTI image to be isotropic by setting all voxel dimensions 
    to the smallest dimension found in the original image. The resampled image is then saved to the specified output path.

    Parameters:
    - input (str): Path to the input NIfTI file.
    - output (str): Path where the resampled NIfTI file will be saved.

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the input NIfTI file does not exist or cannot be accessed.
    - RuntimeError: If there is an error during the resampling or saving process.
    """
    img = nib.load(input)
    pixdim = img.header.get('pixdim')[1:4]
    isotropic_target_spacing = np.min(pixdim)
    target_pixdim = [isotropic_target_spacing] * 3
    resampled_img = resample_to_output(img, voxel_sizes=target_pixdim)
    nib.save(resampled_img, output)


def convert_dicom_to_nifti(dicom_folder: str, output_path: str, name="ct", compress=True) -> None:
    """
    Converts a folder of DICOM images to a NIfTI file using the dcm2niix tool.
    

    This function uses the `dcm2niix` command-line tool to convert DICOM files located in the specified folder into a single NIfTI file.
    It also creates a json file for the meta data and a nifti file for the region of interest.
    The converted NIfTI file is saved to the specified output path.

    Parameters:
    - dicom_folder (str): Path to the folder containing DICOM files.
    - output_path (str): Path where the resulting NIfTI file will be saved.
    - name (str): name of the file. By default its named ct.
    - compress(bool): If true then it compresses the result. The file output is then of type *.nii.gz

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the specified DICOM folder does not exist or cannot be accessed.
    - subprocess.CalledProcessError: If the `dcm2niix` command fails.
    """
    if compress:
        cmd_str = f"dcm2niix -9 -f {name} -o {output_path} -z y {dicom_folder}"
    else:
        cmd_str = f"dcm2niix -f {name} -o {output_path} {dicom_folder}"

    subprocess.run(cmd_str, shell=True, check=True)


def resize_nifti_to_match(source_nifti_path: str, target_nifti_path: str, output_nifti_path: str):
    """
    Resizes the target NIfTI file to match the dimensions of the source NIfTI file and saves the result.

    Parameters:
    - source_nifti_path (str): Path to the source NIfTI file whose dimensions are to be matched.
    - target_nifti_path (str): Path to the target NIfTI file that will be resized.
    - output_nifti_path (str): Path to save the resized NIfTI file.

    Returns:
    - None
    """
    source_size = get_dimensions_of_nifti_array(source_nifti_path)
    header, affine = get_nifti_options(source_nifti_path)
    target_tensor = get_tensor_from_nifti(target_nifti_path)
    resized_target_tensor = Elementary.interpolate(target_tensor, source_size)

    save_nifti(resized_target_tensor, output_nifti_path, header, affine)

