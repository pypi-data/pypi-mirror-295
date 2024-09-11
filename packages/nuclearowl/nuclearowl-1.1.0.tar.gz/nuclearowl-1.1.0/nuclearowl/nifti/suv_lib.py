import pydicom
import numpy as np
import nibabel as nib
import os
from datetime import datetime
from nuclearowl.nifti.utils import get_nifti_options, get_array_from_nifti

"A lib mostly implemented by David Haberl"

def get_dicom_tags(dcm):
    """
    Return informative and required DICOM tags for SUV calculation. Missing DICOM tags will be returned as NaNs.
    Note: sex and age is not required but can help for estimations if values are missing (e.g. body weight)
    DICOM tags:
    https://dicom.innolitics.com/ciods
    Args:
        dcm (pydicom.dataset.FileDataset): Loaded DICOM file.
        Example:
            dcm = pydicom.dcmread(path_to_dcm_file)
        pydicom:
        https://pydicom.github.io/pydicom/stable/old/ref_guide.html
    Returns:
        dict: Dictionary with DICOM tags.
    """

    # Ensure input parameter validity
    assert (
        dcm.Modality == "PT"
    ), "Passed DICOM file is not a Positron-Emission-Tomography scan. Check DICOM Modality tag."

    # Get patient age
    try:
        age = dcm.PatientAge
    except AttributeError:
        print("Age is not stored in DICOM file.")
        age = np.nan

    # Get patient sex
    try:
        sex = dcm.PatientSex
    except AttributeError:
        print("Sex is not stored in DICOM file.")
        sex = np.nan

    # Get patient weight
    try:
        weight = dcm.PatientWeight
    except AttributeError:
        print("Weight is not stored in DICOM file.")
        weight = np.nan

    # Get patient height
    try:
        patient_height = dcm.PatientSize
    except AttributeError:
        print("Patient Size is not stored in DICOM file.")
        patient_height = np.nan

    # Get radiopharmaceutical information (radiotracer)
    try:
        tracer = dcm.RadiopharmaceuticalInformationSequence[0].Radiopharmaceutical
    except AttributeError:
        print("Radiopharmaceutical Info is not stored in DICOM file.")
        tracer = np.nan

    # Get scan time
    try:
        scan_time = dcm.AcquisitionTime
    except AttributeError:
        print("Acquisition Time is not stored in DICOM file.")
        scan_time = np.nan

    # Get start time of the radiopharmaceutical injection
    try:
        injection_time = dcm.RadiopharmaceuticalInformationSequence[
            0
        ].RadiopharmaceuticalStartTime
    except AttributeError:
        print("Injection Time is not stored in DICOM file.")
        injection_time = np.nan

    # Get half life of radionuclide
    try:
        half_life = dcm.RadiopharmaceuticalInformationSequence[
            0
        ].RadionuclideHalfLife
    except AttributeError:
        print("Half Life is not stored in DICOM file.")
        half_life = np.nan

    # Get total dose injected for radionuclide
    try:
        injected_dose = dcm.RadiopharmaceuticalInformationSequence[
            0
        ].RadionuclideTotalDose
    except AttributeError:
        print("Injected Dose is not stored in DICOM file.")
        injected_dose = np.nan

    return {
        "age": [age],
        "sex": [sex],
        "weight": [weight],
        "height": [patient_height],
        "tracer": [tracer],
        "scan_time": [scan_time],
        "injection_time": [injection_time],
        "half_life": [half_life],
        "injected_dose": [injected_dose],
    }


def assert_time_format(input):
    """
    Time stamp formatting
    Args:
        time (str): Time stamp from DICOM file.
    Returns:
        time: datetime object
    """
    # Cut off milliseconds
    time = input.split(".")[0]
    time_format = "%H%M%S"
    time = datetime.strptime(time, time_format)

    return time


def compute_suvbw_map(
    img, weight, scan_time, injection_time, half_life, injected_dose
):
    """
    Compute SUVbw map based on given weight and injected dose decay.
    Args:
        img: Input image ndarray. Each pixel/voxel is associated with its radioactivity
        represented as volume concentration MBq/mL.
        weight: Patient body weight in kilograms.
        scan_time (str): Acquisition time (start time of PET). Time stamp from DICOM file.
        injection_time (str): Injection time; time when radiopharmaceutical dose was administered.
        Time stamp from DICOM file.
        half_life: Half life of used radiopharmaceutical in seconds.
        injected_dose: Injected total dose of administered radiopharmaceutical in Mega Becquerel.
    Returns:
        suv_map: Image ndarray. Each pixel/voxel is associated with its SUVbw.
    """

    # Assert time format
    scan_time = assert_time_format(scan_time)
    injection_time = assert_time_format(injection_time)
    # Calculate time in seconds between acqusition time (scan time) and injection time
    time_difference = scan_time - injection_time
    time_difference = time_difference.seconds

    # Ensure parameter validity
    check = [weight, time_difference, half_life, injected_dose]
    for i in check:
        assert i > 0, f"Invalid input. No negative values allowed. Value: {i}"
        assert (
            np.isnan(i) == False
        ), f"Invalid input. No NaNs allowed. Value is NaN: {np.isnan(i)}"

    assert weight < 1000, "Weight exceeds 1000 kg, did you really used kg unit?"

    img = np.asarray(img)

    # Calculate decay for decay correction
    decay = np.exp(-np.log(2) * time_difference / half_life)
    # Calculate the dose decayed during procedure in Bq
    injected_dose_decay = injected_dose * decay

    # Weight in grams
    weight = weight * 1000

    # Calculate SUVbw
    suv_map = img * weight / injected_dose_decay

    return suv_map


def create_suv_pet(dicom_folder:str, pet_nifti_file:str, output_path:str)->None:
    """
    Creates a nifti file with the suv values, based on a pet image, and the dicom files.

    Parameters:
    - dicom_folder (str): Path to the dicom folder.
    - pet_nifti_file (str): Path to the pet file. Can be either a .nii or .nii.gz.
    - output_path (str): Path to to the output_file.

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the specified NIfTI or/and dicom paths do not exist or cannot be accessed.

    """
    A = os.listdir(dicom_folder)
    dicom_file = f"{dicom_folder}/{A[0]}"
    dcm = pydicom.dcmread(dicom_file)
    
    
    TAGS = get_dicom_tags(dcm)

    header, affine = get_nifti_options(pet_nifti_file)
    arr= get_array_from_nifti(pet_nifti_file)

    dcm = pydicom.dcmread(dicom_file)

    new = compute_suvbw_map(arr, TAGS["weight"][0],
                    TAGS["scan_time"][0],
                    TAGS["injection_time"][0],
                    TAGS["half_life"][0],
                    TAGS["injected_dose"][0])

    new_nii = nib.Nifti1Image(new, affine, header)

    nib.save(new_nii, output_path)