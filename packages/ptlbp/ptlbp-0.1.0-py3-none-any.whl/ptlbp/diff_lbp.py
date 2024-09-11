import torch
from typing import Tuple, Union, Literal, Generator
from .sampling import PointSampler, TOffsets
from .comparisson import Comparisson, ComparissonQuantile, ComparissonOtsu
from .encoding import BinaryToOnehotChannelEmbeddings
import sys


class DiffLBP(torch.nn.Module):
    class DiscretePool(torch.nn.Module):
        def __init__(self, channels: int = 256) -> None:
            super().__init__()
            self.channels = channels

        def forward(self, x) -> torch.Tensor:
            x = torch.argmax(x, dim=1).float()[:, None, :, :]
            histograms = []
            for batch_item in x:
                histograms.append(torch.histc(batch_item, bins=self.channels, min=0, max=self.channels-1))
            return torch.stack(histograms, dim=0)[:, :, None, None]

    def __init__(self, offsets: TOffsets,
                 comparisson: Union[Literal["quantile", "otsu", "simple"], torch.nn.Module] = "quantile",
                 pool_pixels: Union[torch.nn.Module, Literal['sum', False, None, 'avg', 'discrete']] = 'sum',
                 diff_hardness: float = 3.0, learn_input_hardness: bool = False,
                 output_hardness: float = 3.0, learn_output_hardness: bool = False,
                 supress_full_pattern: bool = False, supress_zero_pattern: bool = False,
                 block_normalise: bool = False, double_onehots: bool = False) -> None:
        super().__init__()
        self.point_sampler = PointSampler(input_channels=1, offsets=offsets)

        if comparisson == "otsu":
            self.comparisson = ComparissonOtsu()
        elif comparisson == "simple":
            self.comparisson = Comparisson()
        elif comparisson == "quantile":
            self.comparisson = ComparissonQuantile()
        elif isinstance(comparisson, torch.nn.Module):
            self.comparisson = comparisson
        else:
            raise ValueError("Invalid comparisson")

        self.binary_to_onehot = BinaryToOnehotChannelEmbeddings(self.point_sampler.num_points)

        if pool_pixels == 'sum':
            self.histogram_pool = lambda x: x.sum(dim=2, keepdim=True).sum(dim=3, keepdim=True)
            self.pool_mode = 'sum'

        elif pool_pixels == 'avg':
            self.histogram_pool = torch.nn.AdaptiveAvgPool2d(1)
            self.pool_mode = 'avg'

        elif pool_pixels == 'discrete':
            self.histogram_pool = DiffLBP.DiscretePool(self.binary_to_onehot.num_output_channels)
            self.pool_mode = 'discrete'

        elif pool_pixels is False or pool_pixels is None:
            self.histogram_pool = lambda x: x
            self.pool_mode = None

        elif isinstance(pool_pixels, torch.nn.Module):
            self.histogram_pool = pool_pixels
            self.pool_mode = 'custom'

        else:
            raise ValueError("Invalid pool_pixels")

        self.diff_hardness = torch.nn.parameter.Parameter(torch.tensor(diff_hardness, dtype=torch.float32))
        self.diff_hardness.requires_grad = learn_input_hardness
        self.output_hardness = torch.nn.parameter.Parameter(torch.tensor(output_hardness, dtype=torch.float32))
        self.output_hardness.requires_grad = learn_output_hardness
        self.supress_full_pattern = supress_full_pattern
        self.supress_zero_pattern = supress_zero_pattern
        self.block_normalise = block_normalise
        self.double_onehots = double_onehots

    def compute_lbp_image(self, x: torch.Tensor, slice_width: int = 500,
                          return_confidences=True) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        with torch.no_grad():
            pad = self.point_sampler.weights.size(2) // 2
            pattern_image_slices = []
            confidence_image_slices = []
            for slice, _, _ in self.__forward_pixels_sliced(x, slice_width):
                confidences, patterns = slice.max(dim=1, keepdim=True)
                pattern_image_slices.append(patterns)
                confidence_image_slices.append(confidences)
            pattern_x = torch.cat(pattern_image_slices, dim=3)
            conf_x = torch.cat(confidence_image_slices, dim=3)
            res_pattern_img = torch.zeros_like(x)
            res_confidence_img = torch.zeros_like(x)
            res_pattern_img[:, :, pad:-pad, pad:-pad] = pattern_x
            res_confidence_img[:, :, pad:-pad, pad:-pad] = conf_x
        if return_confidences:
            return res_pattern_img, res_confidence_img
        else:
            return res_pattern_img

    def __forward_pixels(self, x: torch.Tensor) -> torch.Tensor:
        """Computes the forward pass of the model on pixels.

            This is the most memory inefficient part of the the layer.
        """
        x = self.comparisson(x, self.point_sampler(x))
        x = torch.nn.functional.tanh(x * self.diff_hardness) * .5 + .5
        x = self.binary_to_onehot(x)
        if self.double_onehots:
            x = x.double()
        x = torch.nn.functional.softmax(x * self.output_hardness, dim=1)
        return x

    def __forward_pixels_sliced(self, x: torch.Tensor, slice_width: int = 100)\
            -> Generator[Tuple[torch.Tensor, int, int], None, None]:
        """Computes the forward pass of the model on pixels."""
        assert not torch.is_grad_enabled()
        x = self.comparisson(x, self.point_sampler(x))
        x = torch.nn.functional.tanh(x * self.diff_hardness) * .5 + .5
        for i in range(0, x.size(3), slice_width):
            patch_x = self.binary_to_onehot(x[:, :, :, i:i+slice_width])
            pixel_count = patch_x.size(2) * patch_x.size(3)
            if self.double_onehots:
                print("Warning: DiffLbp.forward_pixels_sliced slicing an image and employing\
                    double precision might be wrong.", sys.stderr)
                patch_x = patch_x.double()
            patch_x = torch.nn.functional.softmax(patch_x * self.output_hardness, dim=1)
            yield patch_x, pixel_count, x.size(2) * x.size(3)

    def __forward_histograms(self, x: torch.Tensor) -> torch.Tensor:
        """Postprocesses the histograms after pooling."""
        if self.supress_full_pattern:
            x = x[:, :-1]
        if self.supress_zero_pattern:
            x = x[:, 1:]
        if self.block_normalise:
            x = x / (x.sum(dim=1, keepdim=True) + 1e-10)
        return x

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """This is the forward pass of the model.

        This method:
            computes patterns for every pixel,
            pools pixels into histograms,
            and histograms normalises resulting histograms.
        """
        x = self.__forward_pixels(x)
        x = self.histogram_pool(x)
        x = self.__forward_histograms(x)
        return x

    def forward_sliced(self, x: torch.Tensor, patch_width=1000) -> torch.Tensor:
        # TODO(anguelos) add support for vertical spliting of the image
        # TODO(anguelos) cache the forward pass to enable backward as well
        """Computes the forward pass on images that can't fit memory.

            Attention!!! this does not cache for the backward pass, so it is not suitable for training.
        """
        assert not torch.is_grad_enabled()

        # TODO(anguelos) add support for and None, sum pooling.
        if self.pool_mode not in ["discrete"]:
            raise ValueError("forward_sliced only supports 'discrete' pooling.")
        if patch_width >= x.size(3):
            return self.forward(x)
        x_accumulation = []
        for patch_x, pixel_count, total_forward_pixels in self.__forward_pixels_sliced(x, patch_width):
            patch_x = self.histogram_pool(patch_x)
            x_accumulation.append(patch_x)
        x = torch.cat(x_accumulation, dim=3).sum(dim=3, keepdim=True)
        x = self.__forward_histograms(x)
        return x

    def get_gradient_image(self, image: torch.Tensor, desired_output: torch.Tensor, e=1e-10) -> torch.Tensor:
        """
        Calculates the gradient of the loss function with respect to the input image.

        Args:
            image (torch.Tensor): The input image.
            desired_output (torch.Tensor): The desired output of the model either with dimensions BxCx1x1 or as with a
                                           single dimesion C equal to the histgram size.

        Returns:
            torch.Tensor: The gradient of the loss function with respect to the input image.
        """
        image = image.clone()
        des_output = desired_output.detach()
        tmp_image = image.clone()
        tmp_image.requires_grad_()
        output = self(tmp_image)
        if len(desired_output.size()) == 1:
            des_output = des_output[None, :, None, None]
        loss = (((output - desired_output)**2)**.5).sum()
        # TODO(anguelos) handle when the loss is 0, we get NaN in the image
        loss.backward()
        result = tmp_image.grad.detach()
        return result

    def get_triplet_gradient_image(self, ancor_image: torch.Tensor,
                                   positive_output: torch.Tensor, negative_output) -> torch.Tensor:
        """
        Calculates the gradient of the loss function with respect to the input image.

        Args:
            image (torch.Tensor): The input image.
            desired_output (torch.Tensor): The desired output of the model either with dimensions BxCx1x1 or as with a
                                           single dimesion C equal to the histgram size.

        Returns:
            torch.Tensor: The gradient of the loss function with respect to the input image.
        """
        ancor_image = ancor_image.clone()
        positive_output = positive_output.detach()
        negative_output = negative_output.detach()
        ancor_image.requires_grad_()
        output = self(ancor_image)
        if len(positive_output.size()) == 1:
            positive_output = positive_output[None, :, None, None]
        if len(negative_output.size()) == 1:
            negative_output = negative_output[None, :, None, None]

        positive_output = positive_output[:, 1:-1, :, :]
        negative_output = negative_output[:, 1:-1, :, :]
        output = output[:, 1:-1, :, :]

        positive_diff = (((output - positive_output)**2)).sum()
        negative_diff = (((output - negative_output)**2)).sum()
        loss = (((negative_diff-positive_diff)))
        print(f"Positive: {positive_diff.item():.20f} Negative: {negative_diff.item():.20f} Loss: {loss.item():.20f}")
        loss.backward()
        result = ancor_image.grad.detach()
        return result

    def valid_pixels_size(self, input_size: tuple) -> tuple:
        border_crop_x = (self.point_sampler.weights.size(2) - 1)
        border_crop_y = (self.point_sampler.weights.size(3) - 1)
        return (input_size[0], 2 ** self.point_sampler.weights.size(0),
                input_size[2] - border_crop_x, input_size[3] - border_crop_y)

    @property
    def num_points(self):
        return self.point_sampler.num_points

    @property
    def num_output_channels(self):
        return 2**self.num_points * self.point_sampler.num_input_channels

    @property
    def histogram_size(self):
        return self.num_output_channels - int(self.supress_full_pattern) - int(self.supress_zero_pattern)

    @property
    def device(self):
        return next(self.parameters()).device
