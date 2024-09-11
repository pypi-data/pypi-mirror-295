import torch


class Kernel2D:
    """
    A class to generate and store common 2D kernels for image processing.
    
    Attributes:
    sobel_x (torch.Tensor): 2D Sobel kernel for edge detection in the x-direction.
    sobel_y (torch.Tensor): 2D Sobel kernel for edge detection in the y-direction.
    laplacian (torch.Tensor): 2D Laplacian kernel for edge detection.
    """

    sobel_x = torch.tensor([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]], dtype=torch.float64)

    sobel_y = torch.tensor([[-1, -2, -1],
                            [0,  0,  0],
                            [1,  2,  1]], dtype=torch.float64)

    laplacian = torch.tensor([[[0, -1, 0],
                               [-1, 4, -1],
                               [0, -1, 0]]], dtype=torch.float64)

    @staticmethod
    def create_dilation_kernel(x, type='cross'):
        """
        Create a 2D dilation kernel of a given size and type.

        Parameters:
        x (int): The size parameter for the kernel. The resulting kernel will have dimensions (2x+1, 2x+1).
        type (str): The type of kernel to create. 'cross' for a cross-shaped kernel, any other value for a full kernel.

        Returns:
        torch.Tensor: The generated dilation kernel.
        """
        if type == 'cross':
            return Kernel2D.cross(x)
        else:
            return Kernel2D.full(x)

    @staticmethod
    def full(x):
        """
        Create a full 2D dilation kernel of size (2x+1, 2x+1).

        Parameters:
        x (int): The size parameter for the kernel.

        Returns:
        torch.Tensor: The generated full dilation kernel.
        """
        size = 2 * x + 1
        kernel = torch.zeros((size, size), dtype=torch.float64)

        center = x
        for i in range(size):
            for j in range(size):
                if abs(i - center) <= x and abs(j - center) <= x:
                    kernel[i, j] = 1

        return kernel

    @staticmethod
    def cross(x):
        """
        Create a cross-shaped 2D dilation kernel of size (2x+1, 2x+1).

        Parameters:
        x (int): The size parameter for the kernel.

        Returns:
        torch.Tensor: The generated cross-shaped dilation kernel.
        """
        size = 2 * x + 1
        kernel = torch.zeros((size, size), dtype=torch.float64)

        center = x
        for i in range(size):
            for j in range(size):
                distance = abs(i - center) + abs(j - center)

                if distance <= x:
                    kernel[i, j] = 1

        return kernel


class Kernel3D:
    """
    A class to generate and store common 3D kernels for volumetric data processing.
    
    Attributes:
    laplacian (torch.Tensor): 3D Laplacian kernel for edge detection.
    """

    laplacian = torch.tensor([[[[0, 0, 0], [0, -1, 0], [0, 0, 0]],
                               [[0, -1, 0], [-1, 6, -1], [0, -1, 0]],
                               [[0, 0, 0], [0, -1, 0], [0, 0, 0]]]], dtype=torch.float64)

    @staticmethod
    def create_dilation_kernel(x, type='cross'):
        """
        Create a 3D dilation kernel of a given size and type.

        Parameters:
        x (int): The size parameter for the kernel. The resulting kernel will have dimensions (2x+1, 2x+1, 2x+1).
        type (str): The type of kernel to create. 'cross' for a cross-shaped kernel, any other value for a full kernel.

        Returns:
        torch.Tensor: The generated dilation kernel.
        """
        if type == 'cross':
            return Kernel3D.cross(x)
        else:
            return Kernel3D.full(x)

    @staticmethod
    def full(x):
        """
        Create a full 3D dilation kernel of size (2x+1, 2x+1, 2x+1).

        Parameters:
        x (int): The size parameter for the kernel.

        Returns:
        torch.Tensor: The generated full dilation kernel.
        """
        size = 2 * x + 1
        kernel = torch.zeros((size, size, size), dtype=torch.float64)

        center = x
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if abs(i - center) <= x and abs(j - center) <= x and abs(k - center) <= x:
                        kernel[i, j, k] = 1

        return kernel

    @staticmethod
    def cross(x):
        """
        Create a cross-shaped 3D dilation kernel of size (2x+1, 2x+1, 2x+1).

        Parameters:
        x (int): The size parameter for the kernel.

        Returns:
        torch.Tensor: The generated cross-shaped dilation kernel.
        """
        size = 2 * x + 1
        kernel = torch.zeros((size, size, size), dtype=torch.float64)

        center = x
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    distance = abs(i - center) + abs(j - center) + abs(k - center)

                    if distance <= x:
                        kernel[i, j, k] = 1

        return kernel
