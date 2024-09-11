from dataclasses import dataclass
import matplotlib.pyplot as plt
from nuclearowl.operations.utils import to_cuda
from nuclearowl.operations.mask import Elementary
from nuclearowl.operations.kernels import Kernel2D
from nuclearowl.nifti.fileIO import get_tensor_from_nifti
from nuclearowl.wrappers import clean_memory
import torch
import torch.nn.functional as F


@dataclass
class Mip:
    """
    A class representing a Maximum Intensity Projection (MIP) with two grayscale images.

    Attributes:
    ----------
    g : torch.Tensor
        The grayscale tensor representing the first MIP image.
    y : torch.Tensor
        The grayscale tensor representing the second MIP image.

    Methods:
    -------
    imagify(percentage=1) -> 'GreyImage':
        Transforms the MIP images into a GreyImage instance using a specific percentage of intensity.

    periphery() -> 'Mip':
        Applies a Sobel filter to the MIP images to detect edges, returning a new Mip instance with the processed images.
    """
    g: torch.Tensor
    y: torch.Tensor

    def imagify(self, percentage=1) -> 'GreyImage':
        """
        Transforms the MIP images into a GreyImage instance using a specific percentage of intensity.

        Parameters:
        ----------
        percentage : float, optional
            The percentage of intensity to use for the transformation (default is 1).

        Returns:
        -------
        GreyImage
            A GreyImage instance with the transformed images.
        """
        return GreyImage(
            imagify_mip(self.g, percentage=percentage),
            imagify_mip(self.y, percentage=percentage)
        )

    def periphery(self) -> 'Mip':
        """
        Applies a Sobel filter to the MIP images to detect edges.

        Returns:
        -------
        Mip
            A new Mip instance with the edge-detected images.
        """
        return Mip(
            sobel_filter(self.g),
            sobel_filter(self.y)
        )


@dataclass
class GreyImage:
    """
    A class representing two grayscale images.

    Attributes:
    ----------
    g : torch.Tensor
        The grayscale tensor representing the first image.
    y : torch.Tensor
        The grayscale tensor representing the second image.

    Methods:
    -------
    stack() -> 'RGBImage':
        Stacks the grayscale images to create an RGBImage instance with three channels.
    """
    g: torch.Tensor
    y: torch.Tensor

    def stack(self) -> 'RGBImage':
        """
        Stacks the grayscale images to create an RGBImage instance with three channels.

        Returns:
        -------
        RGBImage
            An RGBImage instance with the stacked images, creating a three-channel image.
        """
        return RGBImage(
            torch.stack((self.g, self.g, self.g)),
            torch.stack((self.y, self.y, self.y))
        )


@dataclass
class RGBImage:
    """
    A class representing two RGB images.

    Attributes:
    ----------
    g : torch.Tensor
        The RGB tensor representing the first image.
    y : torch.Tensor
        The RGB tensor representing the second image.

    Methods:
    -------
    permute():
        Permutes the dimensions of the RGB images to change the order of axes.
    
    bound():
        Applies a theta function to the RGB images for some image transformation.

    Radd(grey_img: GreyImage):
        Adds the grayscale image to the red channel of the RGB images.

    Gadd(grey_img: GreyImage):
        Adds the grayscale image to the green channel of the RGB images.

    Badd(grey_img: GreyImage):
        Adds the grayscale image to the blue channel of the RGB images.

    Cadd(grey_img: GreyImage, mod: int):
        Adds the grayscale image to the specified channel (0 for red, 1 for green, 2 for blue) of the RGB images.

    cpu():
        Moves the RGB images to the CPU memory.
    """
    g: torch.Tensor
    y: torch.Tensor

    def permute(self):
        """
        Permutes the dimensions of the RGB images to change the order of axes.
        """
        self.g = self.g.permute(1, 2, 0)
        self.y = self.y.permute(1, 2, 0)

    def bound(self):
        """
        Applies a theta function to the RGB images for some image transformation.
        """
        self.g = theta_function_image(self.g)
        self.y = theta_function_image(self.y)

    def Radd(self, grey_img: 'GreyImage'):
        """
        Adds the grayscale image to the red channel of the RGB images.

        Parameters:
        ----------
        grey_img : GreyImage
            The grayscale image to be added to the red channel.
        """
        self.g[0, :, :] += grey_img.g
        self.y[0, :, :] += grey_img.y

    def Gadd(self, grey_img: 'GreyImage'):
        """
        Adds the grayscale image to the green channel of the RGB images.

        Parameters:
        ----------
        grey_img : GreyImage
            The grayscale image to be added to the green channel.
        """
        self.g[1, :, :] += grey_img.g
        self.y[1, :, :] += grey_img.y

    def Badd(self, grey_img: 'GreyImage'):
        """
        Adds the grayscale image to the blue channel of the RGB images.

        Parameters:
        ----------
        grey_img : GreyImage
            The grayscale image to be added to the blue channel.
        """
        self.g[2, :, :] += grey_img.g
        self.y[2, :, :] += grey_img.y

    def Cadd(self, grey_img: 'GreyImage', mod: int):
        """
        Adds the grayscale image to the specified channel (0 for red, 1 for green, 2 for blue) of the RGB images.

        Parameters:
        ----------
        grey_img : GreyImage
            The grayscale image to be added to the specified channel.
        mod : int
            The channel index (0 for red, 1 for green, 2 for blue).
        """
        match mod:
            case 0:
                return self.Radd(grey_img)
            case 1:
                return self.Gadd(grey_img)
            case 2:
                return self.Badd(grey_img)

    def cpu(self):
        """
        Moves the RGB images to the CPU memory.
        """
        self.g = self.g.cpu()
        self.y = self.y.cpu()


def theta_function_image(img):
    """
    Clamps image values to a maximum of 255.

    Parameters:
    ----------
    img : torch.Tensor
        The input image tensor.

    Returns:
    -------
    torch.Tensor
        The clamped image tensor.
    """
    bin = img > 255
    img[bin] = 255
    return img


def create_mips(tensor, device_id=0) -> 'Mip':
    """
    Creates Maximum Intensity Projections (MIPs) from a given tensor.

    Parameters:
    ----------
    tensor : torch.Tensor
        The input tensor.
    device_id : int, optional
        The device ID for CUDA (default is 0).

    Returns:
    -------
    Mip
        The created MIP instance.
    """
    tensor = to_cuda(tensor, device_id)
    return Mip(
        torch.max(tensor, dim=0)[0].permute(1, 0).flip(0),
        torch.max(tensor, dim=1)[0].permute(1, 0).flip(0)
    )


def Create_mips(path: str) -> 'Mip':
    """
    Creates MIPs from a given file path.

    Parameters:
    ----------
    path : str
        The file path to the input data.

    Returns:
    -------
    Mip
        The created MIP instance.
    """
    tensor = get_tensor_from_nifti(path)
    return create_mips(tensor)


def plot_mips(image: 'GreyImage | RGBImage'):
    """
    Plots MIPs using matplotlib.

    Parameters:
    ----------
    image : GreyImage | RGBImage
        The image instance to plot.

    Returns:
    -------
    matplotlib.figure.Figure
        The created figure.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 20))
    ax1.imshow(image.g)
    ax2.imshow(image.y)
    return fig


def show_mips(image: 'GreyImage | RGBImage'):
    """
    Shows MIPs using matplotlib.

    Parameters:
    ----------
    image : GreyImage | RGBImage
        The image instance to show.
    """
    fig = plot_mips(image)
    fig.show()


def save_mips(output_path: str, image: 'GreyImage'):
    """
    Saves MIPs to a file.

    Parameters:
    ----------
    output_path : str
        The file path to save the image.
    image : GreyImage
        The image instance to save.
    """
    fig = plot_mips(image)
    fig.savefig(output_path, dpi=300)




@clean_memory
def lazy_mips(main_path: str, *args: str, output_path: str | None = None, opacity=0.3):
    """
    Creates and processes MIPs (Maximum Intensity Projections) lazily, handling multiple paths and optional output.

    Parameters:
    ----------
    main_path : str
        The main file path for the primary MIP.
    *args : str
        Additional file paths for MIP processing.
    output_path : str | None, optional
        The output file path to save the processed MIPs (default is None).
    opacity : float, optional
        The opacity percentage for the image transformation (default is 0.3).

    Returns:
    -------
    None
    """
    mip = Create_mips(main_path)
    IMG = mip.imagify().stack()

    for i, path in enumerate(args):
        periphery = Create_mips(path).periphery()
        l_img = periphery.imagify(percentage=opacity)

        mod = i % 3
        IMG.Cadd(l_img, mod)

    IMG.permute()
    IMG.bound()
    IMG.cpu()

    print()

    if output_path:
        save_mips(output_path, IMG)
    else:
        show_mips(IMG)


def sobel_filter(image_tensor):
    """
    Applies a Sobel filter to an image tensor to detect edges.

    Parameters:
    ----------
    image_tensor : torch.Tensor
        The input image tensor.

    Returns:
    -------
    torch.Tensor
        The tensor with edges detected using the Sobel filter.
    """
    image_tensor = to_cuda(image_tensor)
    sobel_x = to_cuda(Kernel2D.sobel_x)
    sobel_y = to_cuda(Kernel2D.sobel_y)
    grad_x = Elementary.conv_2d(image_tensor, sobel_x, padding=1)
    grad_y = Elementary.conv_2d(image_tensor, sobel_y, padding=1)
    grad_magnitude = torch.sqrt(grad_x ** 2 + grad_y ** 2)
    edges = (grad_magnitude > 0.1 * grad_magnitude.max()).float()
    return edges


def imagify_mip(mip, percentage=1):
    """
    Transforms a MIP (Maximum Intensity Projection) image tensor to a displayable image format.

    Parameters:
    ----------
    mip : torch.Tensor
        The input MIP image tensor.
    percentage : float, optional
        The percentage of intensity to use for the transformation (default is 1).

    Returns:
    -------
    torch.Tensor
        The transformed image tensor in a displayable format.
    """
    M = mip.max().float()
    m = mip.min().float()
    img = 255 * percentage * (mip - m) / (M - m)
    img = img.to(dtype=torch.int32)
    return img




















