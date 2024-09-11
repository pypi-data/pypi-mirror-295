import logging
import gc
import torch
from typing import Callable, List
from joblib import Parallel, delayed
import os
import random


def logger(func: Callable):
    """
    Decorator to add logging to a function.

    This decorator logs the completion of a function call with its arguments and logs any exceptions 
    that occur during the function execution. If an exception is caught, it logs the error and returns `None`.

    Parameters:
    - func: The function to be decorated (Callable).

    Returns:
    - A wrapper function that logs function calls and exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logging.info(f"Done with--{args}")
            return result
        except Exception as e:
            logging.error(f"Error with --{args}--{e}")
            return None
    return wrapper


def clean_memory(func: Callable):
    """
    Decorator to clear GPU memory and garbage collect after function execution.

    This decorator ensures that GPU memory is cleared and Python's garbage collector is invoked after 
    the decorated function completes its execution. This is useful for managing memory in long-running 
    processes or when working with large models.

    Parameters:
    - func: The function to be decorated (Callable).

    Returns:
    - A wrapper function that clears memory after the function execution.
    """
    def clean_func(*args, **kwargs):
        result = func(*args, **kwargs)
        torch.cuda.empty_cache()  # Clear GPU cache
        gc.collect()  # Run garbage collection
        return result
    return clean_func


def Sequential(func: Callable, cases: List):
    """
    Decorator to apply a function sequentially over a list of cases.

    This decorator wraps a function and applies it to each case in the `cases` list. It returns a list 
    of results corresponding to each case.

    Parameters:
    - func: The function to be decorated (Callable).
    - cases: A list of cases to which the function will be applied (List).

    Returns:
    - A wrapper function that applies the decorated function to each case sequentially and returns a list of results.
    """
    def wrapper(*args, **kwargs):
        res = []
        for case in cases:
            res.append(func(case, *args, **kwargs))
        return res
    return wrapper


def RunParallel(func: Callable, cases: List[List]=[], n_jobs=4):
    """
    Decorator to apply a function in parallel over a list of cases.

    This decorator wraps a function and applies it to each case in the `cases` list in parallel using
    multiple processes. It returns a list of results, each corresponding to the result of applying the 
    function to a case.

    Parameters:
    - func: The function to be decorated (Callable).
    - cases: A list of cases to which the function will be applied in parallel (List).

    Returns:
    - A wrapper function that applies the decorated function to each case in parallel and returns a list of results.
    """
    def wrapper(*args, **kwargs):
        res = Parallel(n_jobs=n_jobs)(
            delayed(func)(c, d, *args, **kwargs)
            for c in cases[0]
            for d in cases[1]
        )
        return res
    return wrapper



class SpecificStructure:
    """
    A class to handle operations on a specific folder structure.

    Attributes:
    periods (list of str): The list of periods to consider within each subdirectory.
    folder (str): The path to the root folder.
    names (list of str): The list of subdirectory names in the root folder.
    """


    def __init__(self, folder: str) -> None:
        """
        Initializes the SpecificStructure with the specified folder.

        Parameters:
        folder (str): The path to the root folder.
        """
        self.folder = folder
        self.names = os.listdir(folder)
        self.names.sort()
        self.periods = ["initial", "final"]

    def run(self, func: Callable, *args, FOLDER = None, names=None, periods = None,**kwargs):
        """
        Runs a specified function on each combination of name and period.

        Parameters:
        func (Callable): The function to run. It should accept name, period, and any additional arguments.
        *args: Additional positional arguments to pass to the function.
        **kwargs: Additional keyword arguments to pass to the function.
        
        Example:
        def example_func(name, period, extra_arg):
            print(f"Processing {name} during {period} with {extra_arg}")

        structure = SpecificStructure("/path/to/folder")
        structure.run(example_func, "extra_value")
        """
        if FOLDER==None:
            FOLDER = self.folder
        if names==None:
            names = self.names
        if periods==None:
            periods = self.periods

        RES = []
        for name in names:
            for period in periods:
                res = func(FOLDER, name, period, *args, **kwargs)
                RES.append(res)
        return RES
    
    
    def doesFileExist(self, file_name):
        """
        Check whether a specified file exists within a set of directories.

        Parameters:
        -----------
        file_name : str
            The name of the file to check for existence.

        Returns:
        --------
        bool
            True if the file exists in all specified directories, False otherwise.
        """
        
        def does_single_file_exist(folder, name, period, file_name):
            path = os.path.join(folder, name, period, file_name)
            return os.path.exists(path)
        
        res = self.run(does_single_file_exist, file_name)
        return all(res)
    
    def whereFileNotExist(self, file_name):
        """
        Check whether a specified file exists within a set of directories.

        Parameters:
        -----------
        file_name : str
            The name of the file to check for existence.

        Returns:
        --------
        bool
            True if the file exists in all specified directories, False otherwise.
        """
        
        def does_single_file_exist(folder, name, period, file_name):
            path = os.path.join(folder, name, period, file_name)
            if os.path.exists(path):
                return None
            else:
                return (name, period)
        
        return self.run(does_single_file_exist, file_name)       

        


    def run_parallel(self, func: Callable, n_jobs: int, *args, FOLDER = None, names=None, periods = None, **kwargs):
        """
        Runs a specified function in parallel on each combination of name and period.

        Parameters:
        func (Callable): The function to run. It should accept name, period, and any additional arguments.
        n_jobs (int): The number of parallel jobs to run.
        *args: Additional positional arguments to pass to the function.
        **kwargs: Additional keyword arguments to pass to the function.
        
        Returns:
        list: A list of results from the function calls.
        
        Example:
        def example_func(name, period, extra_arg):
            return f"Processed {name} during {period} with {extra_arg}"

        structure = SpecificStructure("/path/to/folder")
        results = structure.run_parallel(example_func, n_jobs=4, extra_arg="extra_value")
        print(results)
        """

        if FOLDER==None:
            FOLDER = self.folder
        if names==None:
            names = self.names
        if periods==None:
            periods = self.periods

        RES = Parallel(n_jobs=n_jobs)(
            delayed(func)(FOLDER, name, period, *args, **kwargs)
            for name in names
            for period in periods
        )
        return RES
    
    # def random_check(self, func:Callable, percentage=0.1):
    #     samp = random.sample(self.names, k = int(percentage*len(self.names)))
    #     self.
        