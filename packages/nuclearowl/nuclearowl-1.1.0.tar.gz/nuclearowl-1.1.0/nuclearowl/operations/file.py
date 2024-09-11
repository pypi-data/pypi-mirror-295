from nuclearowl.nifti.fileIO import get_tensor_from_nifti, save_nifti
from nuclearowl.nifti.utils import get_nifti_options
import pickle
from typing import *


class NiftiIO:
    @staticmethod
    def SISO(path_in: str, path_out: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to a single input NIfTI file and save the result to an output NIfTI file.

        This method reads a NIfTI file from `path_in`, applies the `operation` to the loaded data,
        and saves the processed data to `path_out`. The operation should be a callable that takes 
        a NumPy array as input and returns a processed NumPy array.

        Parameters:
        - path_in: Path to the input NIfTI file (string).
        - path_out: Path to the output NIfTI file (string).
        - operation: Callable that takes a NumPy array as input and returns a processed NumPy array.
        - *args: Additional positional arguments to pass to the operation.
        - **kwargs: Additional keyword arguments to pass to the operation.

        Notes:
        - `get_nifti_options` retrieves the header and affine information from the NIfTI file.
        - `get_tensor_from_nifti` loads the NIfTI file into a NumPy array.
        - `save_nifti` saves the processed NumPy array back to a NIfTI file with the given header and affine.
        """
        header, affine = get_nifti_options(path_in)
        mask_in = get_tensor_from_nifti(path_in)
        mask_out = operation(mask_in, *args, **kwargs)
        save_nifti(mask_out, path_out, header, affine)

    @staticmethod
    def SIMO(path_in: str, paths_out: List[str], operation: Callable, *args, **kwargs):
        """
        Apply an operation to a single input NIfTI file and save the results to multiple output NIfTI files.

        This method reads a NIfTI file from `path_in`, applies the `operation` to the loaded data,
        and saves each resulting output to a corresponding path in `paths_out`. The `operation` should 
        be a callable that takes a NumPy array as input and returns a list of processed NumPy arrays.

        Parameters:
        - path_in: Path to the input NIfTI file (string).
        - paths_out: List of paths to the output NIfTI files (list of strings).
        - operation: Callable that takes a NumPy array as input and returns a list of processed NumPy arrays.
        - *args: Additional positional arguments to pass to the operation.
        - **kwargs: Additional keyword arguments to pass to the operation.

        Notes:
        - `get_nifti_options` retrieves the header and affine information from the NIfTI file.
        - `get_tensor_from_nifti` loads the NIfTI file into a NumPy array.
        - `save_nifti` saves each processed NumPy array back to the corresponding NIfTI file with the given header and affine.
        """
        header, affine = get_nifti_options(path_in)
        mask_in = get_tensor_from_nifti(path_in)
        masks_out = operation(mask_in, *args, **kwargs)
        for i, mask_out in enumerate(masks_out):
            save_nifti(mask_out, paths_out[i], header, affine)

    @staticmethod
    def DISO(path_a: str, path_b: str, path_out: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to two input NIfTI files and save the result to an output NIfTI file.

        This method reads two NIfTI files from `path_a` and `path_b`, applies the `operation` to the loaded 
        data, and saves the processed data to `path_out`. The `operation` should be a callable that takes 
        two NumPy arrays as input and returns a processed NumPy array.

        Parameters:
        - path_a: Path to the first input NIfTI file (string).
        - path_b: Path to the second input NIfTI file (string).
        - path_out: Path to the output NIfTI file (string).
        - operation: Callable that takes two NumPy arrays as input and returns a processed NumPy array.
        - *args: Additional positional arguments to pass to the operation.
        - **kwargs: Additional keyword arguments to pass to the operation.

        Notes:
        - `get_nifti_options` retrieves the header and affine information from the first NIfTI file.
        - `get_tensor_from_nifti` loads the NIfTI files into NumPy arrays.
        - `save_nifti` saves the processed NumPy array back to a NIfTI file with the given header and affine.
        """
        header, affine = get_nifti_options(path_a)
        mask_a = get_tensor_from_nifti(path_a)
        mask_b = get_tensor_from_nifti(path_b)
        mask_out = operation(mask_a, mask_b, *args, **kwargs)
        save_nifti(mask_out, path_out, header, affine)

    @staticmethod
    def MISO(paths_in: List[str], path_out: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to multiple input NIfTI files and save the result to an output NIfTI file.

        This method reads multiple NIfTI files from `paths_in`, applies the `operation` to the loaded data,
        and saves the processed data to `path_out`. The `operation` should be a callable that takes a list 
        of NumPy arrays as input and returns a processed NumPy array.

        Parameters:
        - paths_in: List of paths to input NIfTI files (list of strings).
        - path_out: Path to the output NIfTI file (string).
        - operation: Callable that takes a list of NumPy arrays as input and returns a processed NumPy array.
        - *args: Additional positional arguments to pass to the operation.
        - **kwargs: Additional keyword arguments to pass to the operation.

        Notes:
        - `get_nifti_options` retrieves the header and affine information from the first NIfTI file.
        - `get_tensor_from_nifti` loads each NIfTI file into NumPy arrays.
        - `save_nifti` saves the processed NumPy array back to a NIfTI file with the given header and affine.
        """
        header, affine = get_nifti_options(paths_in[0])
        masks_in = [get_tensor_from_nifti(path_in) for path_in in paths_in]
        mask_out = operation(masks_in, *args, **kwargs)
        save_nifti(mask_out, path_out, header, affine)

    @staticmethod
    def MIMO(paths_in: List[str], paths_out: List[str], operation: Callable, *args, **kwargs):
        """
        Apply an operation to multiple input NIfTI files and save the results to multiple output NIfTI files.

        This method reads multiple NIfTI files from `paths_in`, applies the `operation` to the loaded data,
        and saves each resulting output to a corresponding path in `paths_out`. The `operation` should be a 
        callable that takes a list of NumPy arrays as input and returns a list of processed NumPy arrays.

        Parameters:
        - paths_in: List of paths to input NIfTI files (list of strings).
        - paths_out: List of paths to output NIfTI files (list of strings).
        - operation: Callable that takes a list of NumPy arrays as input and returns a list of processed NumPy arrays.
        - *args: Additional positional arguments to pass to the operation.
        - **kwargs: Additional keyword arguments to pass to the operation.

        Notes:
        - `get_nifti_options` retrieves the header and affine information from the first NIfTI file.
        - `get_tensor_from_nifti` loads each NIfTI file into NumPy arrays.
        - `save_nifti` saves each processed NumPy array back to the corresponding NIfTI file with the given header and affine.
        """
        header, affine = get_nifti_options(paths_in[0])
        masks_in = [get_tensor_from_nifti(path_in) for path_in in paths_in]
        masks_out = operation(masks_in, *args, **kwargs)
        for i, mask_out in enumerate(masks_out):
            save_nifti(mask_out, paths_out[i], header, affine)

    class Wrappers:
        @staticmethod
        def SISO(operation: Callable):
            """
            Create a wrapper for the SISO method.

            Parameters:
            - operation: Callable that takes a NumPy array as input and returns a processed NumPy array.

            Returns:
            - A function that applies the operation to a single NIfTI file and saves the result to an output NIfTI file.
            """
            def wrapper(path_in: str, path_out: str, *args, **kwargs):
                NiftiIO.SISO(path_in, path_out, operation, *args, **kwargs)
            return wrapper

        @staticmethod
        def SIMO(operation: Callable):
            """
            Create a wrapper for the SIMO method.

            Parameters:
            - operation: Callable that takes a NumPy array as input and returns a list of processed NumPy arrays.

            Returns:
            - A function that applies the operation to a single NIfTI file and saves each result to a corresponding output NIfTI file.
            """


class MaskI:
    @staticmethod
    def SI(path_in: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to a single input NIfTI file.

        Parameters:
        - path_in: Path to the input NIfTI file.
        - operation: Callable that takes a NumPy array and returns a NumPy array.
        - *args, **kwargs: Additional arguments to pass to the operation.

        Returns:
        - Processed mask as a NumPy array.
        """
        mask_in = get_tensor_from_nifti(path_in)
        mask_out = operation(mask_in, *args, **kwargs)
        return mask_out

    @staticmethod
    def DI(path_a: str, path_b: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to two input NIfTI files.

        Parameters:
        - path_a: Path to the first input NIfTI file.
        - path_b: Path to the second input NIfTI file.
        - operation: Callable that takes two NumPy arrays and returns a NumPy array.
        - *args, **kwargs: Additional arguments to pass to the operation.

        Returns:
        - Processed mask as a NumPy array.
        """
        mask_a = get_tensor_from_nifti(path_a)
        mask_b = get_tensor_from_nifti(path_b)
        mask_out = operation(mask_a, mask_b, *args, **kwargs)
        return mask_out

    @staticmethod
    def MI(paths_in: List[str], operation: Callable, *args, **kwargs):
        """
        Apply an operation to multiple input NIfTI files.

        Parameters:
        - paths_in: List of paths to input NIfTI files.
        - operation: Callable that takes a list of NumPy arrays and returns a NumPy array.
        - *args, **kwargs: Additional arguments to pass to the operation.

        Returns:
        - Processed mask as a NumPy array.
        """
        masks_in = [get_tensor_from_nifti(path_in) for path_in in paths_in]
        mask_out = operation(masks_in, *args, **kwargs)
        return mask_out

    class Wrappers:
        @staticmethod
        def SI(operation: Callable):
            """
            Create a wrapper for the SI method.

            Parameters:
            - operation: Callable that takes a NumPy array and returns a NumPy array.

            Returns:
            - A function that applies the operation to a single NIfTI file.
            """
            def wrapper(path_in: str, *args, **kwargs):
                return MaskI.SI(path_in, operation, *args, **kwargs)
            return wrapper

        @staticmethod
        def DI(operation: Callable):
            """
            Create a wrapper for the DI method.

            Parameters:
            - operation: Callable that takes two NumPy arrays and returns a NumPy array.

            Returns:
            - A function that applies the operation to two NIfTI files.
            """
            def wrapper(path_a: str, path_b: str, *args, **kwargs):
                return MaskI.DI(path_a, path_b, operation, *args, **kwargs)
            return wrapper

        @staticmethod
        def MI(operation: Callable):
            """
            Create a wrapper for the MI method.

            Parameters:
            - operation: Callable that takes a list of NumPy arrays and returns a NumPy array.

            Returns:
            - A function that applies the operation to multiple NIfTI files.
            """
            def wrapper(paths_in: List[str], *args, **kwargs):
                return MaskI.MI(paths_in, operation, *args, **kwargs)
            return wrapper


class AnalysisIO:
    @staticmethod
    def SI(path_in: str, path_out: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to a single input NIfTI file and save the result as a pickle file.

        Parameters:
        - path_in: Path to the input NIfTI file.
        - path_out: Path to the output pickle file.
        - operation: Callable that takes a NumPy array and returns the result.
        - *args, **kwargs: Additional arguments to pass to the operation.
        """
        mask_in = get_tensor_from_nifti(path_in)
        res = operation(mask_in, *args, **kwargs)
        AnalysisIO.save_pickle(res, path_out)

    @staticmethod
    def DI(path_a: str, path_b: str, path_out: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to two input NIfTI files and save the result as a pickle file.

        Parameters:
        - path_a: Path to the first input NIfTI file.
        - path_b: Path to the second input NIfTI file.
        - path_out: Path to the output pickle file.
        - operation: Callable that takes two NumPy arrays and returns the result.
        - *args, **kwargs: Additional arguments to pass to the operation.
        """
        mask_a = get_tensor_from_nifti(path_a)
        mask_b = get_tensor_from_nifti(path_b)
        res = operation(mask_a, mask_b, *args, **kwargs)
        AnalysisIO.save_pickle(res, path_out)

    @staticmethod
    def MI(paths_in: List[str], path_out: str, operation: Callable, *args, **kwargs):
        """
        Apply an operation to multiple input NIfTI files and save the result as a pickle file.

        Parameters:
        - paths_in: List of paths to input NIfTI files.
        - path_out: Path to the output pickle file.
        - operation: Callable that takes a list of NumPy arrays and returns the result.
        - *args, **kwargs: Additional arguments to pass to the operation.
        """
        masks_in = [get_tensor_from_nifti(path_in) for path_in in paths_in]
        res = operation(masks_in, *args, **kwargs)
        AnalysisIO.save_pickle(res, path_out)

    @staticmethod
    def save_pickle(output_file, object):
        """ 
        Helper function, saves the object in binary form as a pickle file.

        Parameters:
        -output_file: Path to the pickle file.
        -object: Datastructure to be saved
        """
        with open(output_file, "wb") as f:
            pickle.dump(object, f)



    class Wrappers:
        @staticmethod
        def SI(operation: Callable):
            """
            Create a wrapper for the SI method.

            Parameters:
            - operation: Callable that takes a NumPy array and returns the result.

            Returns:
            - A function that applies the operation to a single NIfTI file and saves the result.
            """
            def wrapper(path_in: str, path_out: str, *args, **kwargs):
                return AnalysisIO.SI(path_in, path_out, operation, *args, **kwargs)
            return wrapper

        @staticmethod
        def DI(operation: Callable):
            """
            Create a wrapper for the DI method.

            Parameters:
            - operation: Callable that takes two NumPy arrays and returns the result.

            Returns:
            - A function that applies the operation to two NIfTI files and saves the result.
            """
            def wrapper(path_a: str, path_b: str, path_out: str, *args, **kwargs):
                return AnalysisIO.DI(path_a, path_b, path_out, operation, *args, **kwargs)
            return wrapper

        @staticmethod
        def MI(operation: Callable):
            """
            Create a wrapper for the MI method.

            Parameters:
            - operation: Callable that takes a list of NumPy arrays and returns the result.

            Returns:
            - A function that applies the operation to multiple NIfTI files and saves the result.
            """
            def wrapper(paths_in: List[str], path_out: str, *args, **kwargs):
                return AnalysisIO.MI(paths_in, path_out, operation, *args, **kwargs)
            return wrapper
