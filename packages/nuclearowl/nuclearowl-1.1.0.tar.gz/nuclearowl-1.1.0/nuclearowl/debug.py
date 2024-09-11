import torch
from nuclearowl.nifti.fileIO import get_tensor_from_nifti
from nuclearowl.wrappers import clean_memory, logger


def areMasksIdentical(mask_a: torch.Tensor, mask_b: torch.Tensor)->bool:
    """
    Compares two tensor masks to determine if they are effectively the same based on the Mean Squared Error (MSE).

    Parameters:
    mask_a (torch.Tensor): The first mask tensor.
    mask_b (torch.Tensor): The second mask tensor.

    Returns:
    bool: True if the MSE between the masks is less than 0.01, indicating they are effectively the same. False otherwise.
    """
    MSE = torch.sum((mask_a - mask_b) ** 2).item()    
    return MSE < 0.01

def areMasksSimilar(mask_a: torch.Tensor, mask_b: torch.Tensor)->bool:
    """
    Compares two tensor masks to determine if they are effectively the same based on the Mean Squared Error (MSE).

    Parameters:
    mask_a (torch.Tensor): The first mask tensor.
    mask_b (torch.Tensor): The second mask tensor.

    Returns:
    bool: True if the MSE between the masks is less than 0.01, indicating they are effectively the same. False otherwise.
    """
    
    median = torch.median(torch.abs(mask_a- mask_b)).item()    
    return median < 0.1

def howDifferentMasks(mask_a: torch.Tensor, mask_b: torch.Tensor)->bool:
    """
    Compares two tensor masks to determine if they are effectively the same based on the Mean Squared Error (MSE).

    Parameters:
    mask_a (torch.Tensor): The first mask tensor.
    mask_b (torch.Tensor): The second mask tensor.

    Returns:
    bool: True if the MSE between the masks is less than 0.01, indicating they are effectively the same. False otherwise.
    """
    MSE = torch.sum((mask_a - mask_b) ** 2).item()    
    return MSE

@clean_memory
def areFilesSimilar(path_a: str, path_b: str, device_id = 0)->bool:
    """
    Compares two NIfTI files to determine if their tensor masks are effectively the same.

    Parameters:
    path_a (str): The file path to the first NIfTI file.
    path_b (str): The file path to the second NIfTI file.

    Returns:
    bool: True if the tensor masks from both files are effectively the same. False otherwise.
    """
    if device_id not in [0,1]:
        cuda = False
    mask_a = get_tensor_from_nifti(path_a, device_id=device_id).to(dtype=torch.float16)
    mask_b = get_tensor_from_nifti(path_b, device_id=device_id).to(dtype=torch.float16)
    diff = torch.abs(mask_a- mask_b)
    diff = diff.to(device="cpu")

    del mask_a, mask_b
    
    median = torch.median(diff).item()    
    return median < 0.1

@clean_memory
def areBinaryFilesSimilar(path_a: str, path_b: str, device_id = 0)->bool:
    """
    Compares two NIfTI files to determine if their tensor masks are effectively the same.

    Parameters:
    path_a (str): The file path to the first NIfTI file.
    path_b (str): The file path to the second NIfTI file.

    Returns:
    bool: True if the tensor masks from both files are effectively the same. False otherwise.
    """
    if device_id not in [0,1]:
        cuda = False
    mask_a = get_tensor_from_nifti(path_a, device_id=device_id).to(dtype=torch.bool)
    mask_b = get_tensor_from_nifti(path_b, device_id=device_id).to(dtype=torch.bool)
    diff = mask_a==mask_b
    
    s1 = torch.sum(mask_a)
    S = torch.sum(diff)

    del mask_a, mask_b
    
    return S/s1<0.05

@clean_memory
def areBinaryFilesIdentical(path_a: str, path_b: str, device_id = 0)->bool:
    """
    Compares two NIfTI files to determine if their tensor masks are effectively the same.

    Parameters:
    path_a (str): The file path to the first NIfTI file.
    path_b (str): The file path to the second NIfTI file.

    Returns:
    bool: True if the tensor masks from both files are effectively the same. False otherwise.
    """
    if device_id not in [0,1]:
        cuda = False
    mask_a = get_tensor_from_nifti(path_a, device_id=device_id).to(dtype=torch.bool)
    mask_b = get_tensor_from_nifti(path_b, device_id=device_id).to(dtype=torch.bool)
    diff = mask_a!=mask_b
    
    s1 = torch.sum(diff).item()
    

    del mask_a, mask_b
    
    return s1==0







def howDifferentFiles(path_a: str, path_b: str)->bool:
    """
    Compares two NIfTI files to determine if their tensor masks are effectively the same.

    Parameters:
    path_a (str): The file path to the first NIfTI file.
    path_b (str): The file path to the second NIfTI file.

    Returns:
    bool: True if the tensor masks from both files are effectively the same. False otherwise.
    """
    mask_a = get_tensor_from_nifti(path_a)
    mask_b = get_tensor_from_nifti(path_b)

    return howDifferentMasks(mask_a, mask_b)
