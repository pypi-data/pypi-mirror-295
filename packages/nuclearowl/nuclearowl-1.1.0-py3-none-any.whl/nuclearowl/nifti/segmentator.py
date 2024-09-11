import subprocess
from typing import List

def total_segmentator(nifti_file: str, output_path: str, segments: List[str] = [], all_in_one:bool = False) -> None:
    """
    Runs the TotalSegmentator tool to perform segmentation on a NIfTI file.

    This function constructs and executes a command to run the TotalSegmentator tool based on the provided NIfTI file.
    It supports segmentation of specified anatomical structures or a full body segmentation.

    Parameters:
    - nifti_file (str): Path to the input NIfTI file that will be segmented.
    - output_path (str): Path where the output segmented file will be saved.
    - segments (List[str], optional): List of anatomical structures to be segmented. If not empty, only the specified
      structures will be segmented. If empty, the full body segmentation is performed. Default is an empty list.

    Returns:
    - None

    Raises:
    - ValueError: If `nifti_file` or `output_path` is an empty string.
    - subprocess.CalledProcessError: If the TotalSegmentator command fails or returns an error.

    Example:
    ```python
    total_segmentator('input_file.nii', 'output_file.nii', segments=['brain', 'heart'])
    ```
    This will segment the 'brain' and 'heart' anatomical structures from 'input_file.nii' and save the result to 'output_file.nii'.

    If `segments` is an empty list:
    ```python
    total_segmentator('input_file.nii', 'output_file.nii')
    ```
    This will perform full body segmentation on 'input_file.nii' and save the result to 'output_file.nii'.
    """
    if not nifti_file or not output_path:
        raise ValueError("Both nifti_file and output_path must be specified.")
    
    if segments:
        print(segments)
        anatomical_structure = " ".join(segments)
        cmd = f"TotalSegmentator -i {nifti_file} -o {output_path} --roi_subset " \
              f"{anatomical_structure} --body_seg"
    else:
        if all_in_one:
            print("This will require a lot of memory (>12GB on your ram)!!!")
            cmd = f"TotalSegmentator -i {nifti_file} -o {output_path} -ml"
        else:
            cmd = f"TotalSegmentator -i {nifti_file} -o {output_path}"

    print(cmd)
    
    subprocess.run(cmd, shell=True, check=True)
