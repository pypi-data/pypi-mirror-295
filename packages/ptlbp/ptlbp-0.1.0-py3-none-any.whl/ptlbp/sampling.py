import torch
import numpy as np
import re
from typing import TypeVar


TOffsets = TypeVar('TOffsets', int, list, np.ndarray, torch.Tensor, str)


class PointSampler(torch.nn.Module):
    @staticmethod
    def str2offsets(offsets: str) -> np.ndarray:
        """Converts a string to a numpy array of shape (N, 2) where N is the number of points.

        The string can be: "WNES", "3x3", "NrR", where N is a float or integer  representation of the
        number of points and r is the radius.
        """
        if offsets in ["WNES"]:
            return np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])
        elif offsets == "3x3":
            return np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]])
        elif len(re.findall(r"^\d{1,2}r\d{1,2}(?:\.\d{1,2})?$", offsets)) == 1:
            num_points, r = [eval(k) for k in offsets.split("r")]
            angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
            # angles = angles + (np.pi/16) * (r-1)
            return np.array([[np.cos(a) * r, np.sin(a) * r] for a in angles])
        else:
            raise ValueError("Invalid string for offsets")

    @staticmethod
    def process_offsets(offsets: TOffsets) -> np.ndarray:
        """Converts a string, integer, list, to a numpy array of shape (N, 2) where N is the number of points.

        If the input is already a numpy array, it is returned as is.
        """
        if isinstance(offsets, torch.Tensor):
            return offsets.numpy()
        elif isinstance(offsets, np.ndarray):
            return offsets
        elif isinstance(offsets, list):
            return np.asarray(offsets)
        elif isinstance(offsets, int):
            angles = np.linspace(0, 2*np.pi, offsets, endpoint=False)
            return np.array([[np.cos(a), np.sin(a)] for a in angles])
        elif isinstance(offsets, str):
            return PointSampler.str2offsets(offsets)
        else:
            raise ValueError("Invalid type for offsets")

    def __init__(self, input_channels: int, offsets: TOffsets) -> None:
        super().__init__()
        offsets = PointSampler.process_offsets(offsets)
        X = offsets[:, 0]
        Y = offsets[:, 1]
        num_points = offsets.shape[0]
        left_edge = int(np.floor(X).min())
        right_edge = int(np.ceil(X).max())
        top_edge = int(np.floor(Y).min())
        bottom_edge = int(np.ceil(Y).max())
        kernel_size = (1 + right_edge - left_edge, 1 + bottom_edge - top_edge)
        W = np.zeros((num_points*input_channels, input_channels, kernel_size[0], kernel_size[1]), dtype=np.float32)

        for n in range(num_points):
            left = int(np.floor(offsets[n, 0]))
            left_coef = 1 - (offsets[n, 0]-left)
            if left == offsets[n, 0]:
                right = left
                left_coef = .5
                right_coef = .5
            else:
                right = left + 1
                right_coef = 1 - left_coef

            # centering convolutions
            left = left - left_edge
            right = right - left_edge

            top = int(np.floor(offsets[n, 1]))
            top_coef = 1 - (offsets[n, 1]-top)
            if top == offsets[n, 1]:
                bottom = top
                bottom_coef = .5
                top_coef = .5
            else:
                bottom = top + 1
                bottom_coef = 1 - top_coef

            # centering convolutions
            top = top - top_edge
            bottom = bottom - top_edge

            repr([n, 0, top, left])
            W[n, :, left, top] += top_coef * left_coef
            W[n, :, right, top] += top_coef * right_coef
            W[n, :, left, bottom] += bottom_coef * left_coef
            W[n, :, right, bottom] += bottom_coef * right_coef

        self.weights = torch.nn.parameter.Parameter(torch.tensor(W))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.conv2d(x, self.weights)

    def render_pattern(self, pattern: int, res_width, res_height) -> torch.Tensor:
        with torch.no_grad():
            positive_bin_vector = torch.tensor([pattern // 2**k % 2 for k in range(self.num_points)]).bool()
            negative_bin_vector = ~positive_bin_vector
            res = torch.zeros((1, 1, res_height, res_width), dtype=torch.float32)
            positve_filters = self.weights[positive_bin_vector].sum(dim=0, keepdim=True)
            negative_filters = self.weights[negative_bin_vector].sum(dim=0, keepdim=True)
            assert res.size(2) >= positve_filters.size(2) and res.size(3) >= positve_filters.size(3)
            assert res.size(2) % 2 == 1 and res.size(3) % 2 == 1
            assert positve_filters.size(2) % 2 == 1 and positve_filters.size(3) % 2 == 1
            pad_x = (res.size(2) - positve_filters.size(2)) // 2
            pad_y = (res.size(3) - positve_filters.size(3)) // 2
            res[:, :, pad_x:-pad_x, pad_y:-pad_y] = positve_filters - negative_filters
            return res[0, 0, :, :].detach()

    def valid_pixels_size(self, input_size: tuple) -> tuple:
        border_crop_x = (self.weights.size(2) - 1)
        border_crop_y = (self.weights.size(3) - 1)
        return (input_size[0], self.weights.size(0), input_size[2] - border_crop_x, input_size[3] - border_crop_y)

    @property
    def num_points(self) -> int:
        return self.weights.size(0)//self.weights.size(1)

    @property
    def num_input_channels(self) -> int:
        return self.weights.size(1)


class GaussianPointSampler(PointSampler):
    @staticmethod
    def generate_gaussian_filters(X, Y, point_sigma, point_sum, input_channels=1):
        num_points = X.shape[0]
        if point_sigma < 0:
            point_sigma = X.size(0)
        left_edge = int(np.floor(X - point_sigma).min())
        right_edge = int(np.ceil(X + point_sigma).max())
        top_edge = int(np.floor(Y - point_sigma).min() - point_sigma)
        bottom_edge = int(np.ceil(Y + point_sigma).max())
        kernel_size = (1 + right_edge - left_edge, 1 + bottom_edge - top_edge)
        kernel_orgin = -left_edge, -top_edge
        print((X + point_sigma))
        print(f"X:{X}, Left:{left_edge} Right:{right_edge}, SZ:{kernel_size[0]}\nY:{Y}, Top:{top_edge} Bottom:{bottom_edge}, {kernel_size[1]}")
        W = np.zeros((num_points*input_channels, input_channels, kernel_size[0], kernel_size[1]), dtype=np.float32)
        return W

    def __init__(self, input_channels: int, offsets: TOffsets, point_sigma: float = -1., point_sum: float = 1.) -> None:
        super().__init__(input_channels=input_channels, offsets=offsets)
        offsets = PointSampler.process_offsets(offsets)
        X = offsets[:, 0]
        Y = offsets[:, 1]
        W = GaussianPointSampler.generate_gaussian_filters(X, Y, point_sigma=point_sigma, point_sum=point_sum, input_channels=1)
        self.weights = torch.nn.parameter.Parameter(torch.tensor(W))
