import torch
import numpy as np
from typing import Tuple


class BinaryToOnehotChannelEmbeddings(torch.nn.Module):
    @staticmethod
    def img2embedding(img_BCHW: torch.Tensor) -> Tuple[Tuple[int, int, int, int], torch.Tensor]:
        original_sizes = tuple(img_BCHW.size())
        img_BWHC = img_BCHW.swapaxes(1, 3)
        img_BWH_C = img_BWHC.reshape(-1, original_sizes[1])
        return original_sizes, img_BWH_C

    @staticmethod
    def embedding2img(original_sizes: Tuple[int, int, int, int], img_BWH_C: torch.Tensor) -> torch.Tensor:
        b_sz, c_sz, h_sz, w_sz = original_sizes
        img_BWHC = img_BWH_C.view(b_sz, w_sz, h_sz, c_sz)
        img_BCHW = img_BWHC.swapaxes(1, 3)
        return img_BCHW

    @staticmethod
    def powerset_map(input_length: int) -> list[int]:
        powerset = []
        for n in range(2**input_length):
            powerset.append([(n//(2**k)) % 2 for k in range(0, input_length)])
        return powerset

    def __init__(self, in_channels) -> None:
        super().__init__()
        W = np.array(BinaryToOnehotChannelEmbeddings.powerset_map(in_channels))[:, :, None, None]
        self.linear = torch.nn.Linear(in_channels, 2 ** in_channels, bias=False)
        self.linear.weight.data = torch.tensor(W).float()[:, :, 0, 0]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_sz, x = BinaryToOnehotChannelEmbeddings.img2embedding(x)  # x == x_BC
        margin = -x.sum(dim=1)[:, None] + 1
        x = margin + self.linear(x) - self.linear(1-x)
        res_sz = x_sz[0], 2**x_sz[1], x_sz[2], x_sz[3]
        x = BinaryToOnehotChannelEmbeddings.embedding2img(res_sz, x)
        return x

    @property
    def num_output_channels(self) -> int:
        return self.linear.out_features


# class BinaryToOnehotChannelConvolutions(torch.nn.Module):
#     @staticmethod
#     def powerset_map(input_length) -> list:
#         powerset = []
#         for n in range(2**input_length):
#             powerset.append([(n//(2**k)) % 2 for k in range(0, input_length)])
#         return powerset

#     def __init__(self, in_channels, output_hardness=3.0, input_hardness=3.0,
#                  learn_input_hardness=False, learn_output_hardness=False):
#         super().__init__()
#         W = np.array(BinaryToOnehotChannelConvolutions.powerset_map(in_channels))[:, :, None, None]
#         self.weight = torch.nn.parameter.Parameter(torch.tensor(W, dtype=torch.float32))

#     def forward(self, x):
#         positive = torch.nn.functional.conv2d(x, self.weight)
#         negative = torch.nn.functional.conv2d(1-x, self.weight)
#         result = 1 + positive - negative
#         return result
