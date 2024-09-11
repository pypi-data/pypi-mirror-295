import numpy as np
import torch
import pytest
from ptlbp import PointSampler


@pytest.mark.parametrize("offsets, num_points", [([[0, 1], [1, 0]], 2),
                                                 (torch.Tensor([[0, 1], [1, 0]]), 2),
                                                 (np.array([[0, 1], [1, 0]]), 2),
                                                 ("8.5r1", -1),
                                                 ("8r1.5", 8),
                                                 ("3x3", 8),
                                                 (8, 8),
                                                 (5, 5),
                                                 ("WNES", 4),
                                                 (torch.rand(7, 2), 7),
                                                 (np.zeros([3, 2]), 3)])
def test_PointSampler_offsets(offsets, num_points):
    if num_points == -1:
        with pytest.raises(ValueError):
            sampler = PointSampler(1, offsets)
    else:
        sampler = PointSampler(1, offsets)
        assert sampler.weights.shape[0] == num_points
        assert sampler.weights.shape[1] == 1
        assert len(sampler.weights.size()) == 4


@pytest.mark.parametrize("offsets, kernel_size", [
    (torch.tensor([[0.5, 0.5], [1.5, 1.5]]), (3, 3)),
    (torch.tensor([[0.2, 0.2], [0.8, 0.8]]), (2, 2)),
    (torch.tensor([[0.1, 0.1], [0.3, 0.3], [0.5, 0.5], [0.7, 0.7], [-2, -1.5]]), (4, 4))
])
def test_PointSampler_sizes(offsets, kernel_size):
    input_channels = 3
    num_points = offsets.shape[0]
    expected_weight_shape = (num_points * input_channels, input_channels, kernel_size[0], kernel_size[1])
    sampler = PointSampler(input_channels, offsets)
    weight = sampler.weights.detach().numpy()
    assert weight.shape == expected_weight_shape


@pytest.mark.parametrize("input_channels, offsets, impulse_sum", [
    (1, torch.tensor([[0.0, 0.0]]), 1.),
    (1, torch.tensor([[0.5, 0.5], [1.5, 1.5]]), 2.),
    (3, torch.tensor([[0.2, 0.2], [0.8, 0.8]]), 6.),
    (3, torch.tensor([[0.1, 0.1], [0.3, 0.3], [0.5, 0.5], [0.7, 0.7]]), 12.)
])
def test_PointSampler_impulse_sum(input_channels, offsets, impulse_sum):
    sampler = PointSampler(input_channels, offsets)
    image = torch.zeros((1, input_channels, 10, 10))
    image[0, :, 3, 3] = 1.
    output = sampler(image).detach().numpy()
    output_sum = output.sum().item()
    assert np.allclose(output_sum, impulse_sum)


def test_str2offsets():
    simple_r1 = torch.tensor(PointSampler.str2offsets("8r1"), dtype=torch.float32)
    partial_target = torch.tensor([[1, 0], [0, 1], [-1, 0], [0, -1]], dtype=torch.float32)
    assert simple_r1.size(0) == 8 and simple_r1.size(1) == 2
    assert torch.allclose(simple_r1[[0, 2, 4, 6], :], partial_target)  # E,, N,, W,, S,

    v1 = torch.tensor(PointSampler.str2offsets("3x3"), dtype=torch.float32)
    v1_target = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    assert torch.allclose(v1, torch.tensor(v1_target, dtype=torch.float32))

    large_r1 = torch.tensor(PointSampler.str2offsets("16r1"), dtype=torch.float32)
    partial_target = torch.tensor([[1, 0], [0, 1], [-1, 0], [0, -1]], dtype=torch.float32)
    assert large_r1.size(0) == 16 and large_r1.size(1) == 2
    assert torch.allclose(large_r1[[0, 4, 8, 12], :], partial_target)  # E,, N,, W,, S,

    simple_r2 = torch.tensor(PointSampler.str2offsets("8r2"), dtype=torch.float32)
    partial_target = torch.tensor([[1, 0], [0, 1], [-1, 0], [0, -1]], dtype=torch.float32) * 2
    assert simple_r2.size(0) == 8 and simple_r2.size(1) == 2
    assert torch.allclose(simple_r2[[0, 2, 4, 6], :], partial_target)  # E,, N,, W,, S,
