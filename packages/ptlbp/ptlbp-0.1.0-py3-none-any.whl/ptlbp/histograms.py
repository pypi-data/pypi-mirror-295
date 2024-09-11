import torch
from torch import Tensor
from torch.nn import Parameter
import numpy as np
from typing import List, Union, Literal
from numbers import Number


class _DiffBinning(torch.nn.Module):
    """Base class for differentiable binning layers.

    The binned layers are multiplexed as a new dimension in the output tensor.

    """
    def __init__(self, first_bin: Union[None, Number] = None, last_bin: Union[None, Number] = None,
                 nbins: Number = 10, bin_centers: Union[None, Tensor] = None, energy_ratio: Number = 1.) -> None:
        super().__init__()
        if bin_centers is not None:
            if first_bin is not None or last_bin is not None:
                raise ValueError("Cannot specify bin_centers and first_bin/last_bin")
            self.bin_centers: Parameter = Parameter(bin_centers, requires_grad=False)
            self.sigma: float = (bin_centers[1] - bin_centers[0]).item()
            self.er: float = energy_ratio
        else:
            if first_bin is None or last_bin is None:
                raise ValueError("Either bin_centers or first_bin and last_bin must be specified")
            self.bin_centers: Parameter = Parameter(torch.linspace(first_bin, last_bin, nbins), requires_grad=False)
            self.sigma: float = (last_bin - first_bin) / nbins
            self.er: float = energy_ratio

    def forward(self, x: Tensor) -> Tensor:
        ratio = 2.5066  # Manually aproximated this ratio so that the energy is 1
        x = torch.clamp(x, self.bin_centers[0], self.bin_centers[-1])
        if x.dim() == 4:
            bins = self.bin_centers[None, None, None, None, :]
            x = x[:, :, :, :, None]
            return (self.er / ratio) * torch.exp(-((x - bins) ** 2) / (2 * self.sigma ** 2))
        elif x.dim() == 3:
            bins = self.bin_centers[None, None, None, :]
            x = x[:, :, :, None]
            return (self.er / ratio) * torch.exp(-((x - bins) ** 2) / (2 * self.sigma ** 2))
        elif x.dim() == 2:
            bins = self.bin_centers[None, None, :]
            x = x[:, :, None]
            return (self.er / ratio) * torch.exp(-((x - bins) ** 2) / (2 * self.sigma ** 2))
        elif x.dim() == 1:
            bins = self.bin_centers[None, :]
            x = x[:, None]
            return (self.er / ratio) * torch.exp(-((x - bins) ** 2) / (2 * self.sigma ** 2))
        else:
            raise ValueError(f"Unsupported dim {x.dim()}")

    @property
    def bins(self) -> Tensor:
        return self.bin_centers


class DiffHistogram(_DiffBinning):
    def __init__(self, first_bin: Union[None, Number] = None, last_bin: Union[None, Number] = None,
                 nbins: Number = 10, bin_centers: Union[None, Tensor] = None, energy_ratio: Number = 1.,
                 pooling: Union[None, Literal['sum', 'avg'], torch.nn.Module] = None, keepdims: bool = True,
                 pool_dims: List[Number] = [2, 3]):
        super().__init__(first_bin=first_bin, last_bin=last_bin, nbins=nbins, bin_centers=bin_centers,
                         energy_ratio=energy_ratio)
        self.keepdims: bool = keepdims
        self.pool_dims: List[Number] = pool_dims
        self.pooling_method: str = pooling
        if pooling is None:
            self.pooling = lambda x: x  # Identity
        elif pooling == 'sum':
            self.pooling = lambda x: x.sum(dim=pool_dims, keepdims=keepdims)
        elif pooling == 'avg':
            self.pooling = lambda x: x.mean(dim=pool_dims, keepdims=keepdims)
        elif isinstance(pooling, torch.nn.Module):
            self.pooling = pooling
            self.pooling_method = f"custom_{pooling.__class__.__name__}"
        else:
            raise ValueError(f"Unknown pooling method {pooling}")

    def forward(self, x: Tensor) -> Tensor:
        if x.dim() != 4:
            raise ValueError("Input must be a BxCxHxW tensor")
        per_channel = []
        for ch in range(0, x.size(1)):
            b_h_w_bin = super().forward(x[:, ch:ch+1, :, :])[:, 0, :, :, :]  # (B, H, W, BIN)
            b_bin_h_w = b_h_w_bin.permute(0, 3, 1, 2)  # (B, BIN, H, W)
            per_channel.append(b_bin_h_w)
        x = torch.cat(per_channel, dim=1)  # (B, CxBIN, H, W)
        return self.pooling(x)


def get_intraclass_variances(hist: Tensor, levels: Tensor, e=1e-10) -> Tensor:
    """Calculate the weighted intraclass variances.

    Args:
        hist (Tensor): A tensor who has histograms along a dimension.
        levels (Tensor): A tensor with the values the histogram bins. They are assumed to be equidistant.
        e (float, optional): A small value to avoid division by zero. Defaults to 1e-10.

    Returns:
        Tensor: The tensor containing the weighted intraclass variances.
    """
    h_sum = hist.sum(dim=-1, keepdim=True)
    low_coef = hist.cumsum(dim=-1) / h_sum
    low_E_x = ((levels * hist).cumsum(dim=-1) / (hist.cumsum(dim=-1) + e))
    low_var = (((levels - low_E_x) ** 2) * hist).cumsum(dim=-1) / (hist.cumsum(dim=-1) + e)

    f_levels = torch.flip(levels, dims=[0])
    f_hist = torch.flip(hist, dims=[-1])
    f_high_E_x = ((f_levels * f_hist).cumsum(dim=-1) / (f_hist.cumsum(dim=-1) + e))
    f_high_var = (((f_levels - f_high_E_x) ** 2) * f_hist).cumsum(dim=-1) / (f_hist.cumsum(dim=-1) + e)
    high_var = torch.flip(f_high_var, dims=[-1])

    weighted_intraclass_variances = low_var * low_coef + high_var * (1 - low_coef)
    return weighted_intraclass_variances


def hard_otsu_threshold(histograms: Tensor, dim: int = 1, e=1e-10) -> Tensor:
    """
    Applies the hard Otsu thresholding algorithm to the input histograms.

    Args:
        histograms (Tensor): The input histograms. It can be a 1D or higher-dimensional tensor.
        dim (int, optional): The dimension along which the histograms are computed. Default is 1.
        e (float, optional): A small value added to the denominator to avoid division by zero. Default is 1e-10.

    Returns:
        Tensor: An integer tensor with the histogram dimension beeing the index of the Otsu Threhold for the
            respective histogram.

    Raises:
        None

    Examples:
        >>> histograms = torch.tensor([0.7, 0.9, 0.1, 0.6])
        >>> thresholded = hard_otsu_threshold(histograms)
        >>> print(thresholded)
        tensor([2])
    """
    with torch.no_grad():
        device = histograms.device
    if histograms.dim() == 1 and dim != 0:
        histograms = histograms[None, :]
    nb_bins = histograms.size(dim)
    ld_histograms = histograms.swapaxes(dim, -1)  # moving to (..., BIN)
    levels = torch.arange(0, nb_bins, dtype=torch.float, device=device).view(*([1] * (histograms.dim()-1)), -1)
    for chunc_n in range(0, ld_histograms.size(-1)//nb_bins):
        hist = ld_histograms[..., chunc_n*nb_bins:(chunc_n+1)*nb_bins]
        intraclass_variances = get_intraclass_variances(hist, levels=levels, e=e)
    ld_res = torch.argmin(intraclass_variances, dim=-1, keepdim=True)
    return ld_res.swapaxes(-1, dim)


def diff_otsu_threshold(histograms: Tensor, dim: int = 1, t=.01, nb_bins: int = -1, e=1e-10) -> Tensor:
    """
    Compute the differential Otsu threshold for a given histogram.

    Args:
        histograms (Tensor): The input histogram(s) tensor.
        dim (int, optional): The dimension along which the histogram(s) are computed. Defaults to 1.
        t (float, optional): The temperature parameter for softmax. Defaults to 0.01.
        nb_bins (int, optional): The number of bins in the histogram. If -1, it is inferred from the input tensor.
            Defaults to -1.
        e (float, optional): A small value added to the denominator for numerical stability. Defaults to 1e-10.

    Returns:
        Tensor: The differential Otsu threshold tensor.

    Raises:
        ValueError: If the input histogram tensor is not 1-dimensional and `dim` is not 0.

    Examples:
        >>> histograms = torch.rand(3, 128, 100, 101)
        >>> diff_otsu_threshold(histograms).size()
        torch.Size([3, 128, 100, 101])
        >>> torch.torch.aminmax(diff_otsu_threshold(histograms))
        (tensor(0.00...), tensor(.99....))
    """
    device = histograms.device
    if histograms.dim() == 1 and dim != 0:
        histograms = histograms[None, :]
    if nb_bins < 0:
        nb_bins = histograms.size(dim)
    ld_histograms = histograms.swapaxes(dim, -1)
    levels = torch.arange(0, nb_bins, dtype=torch.float, device=device).view(*([1] * (histograms.dim()-1)), -1)
    ld_otsu_chuncs = []
    for chunc_n in range(0, ld_histograms.size(-1)//nb_bins):
        hist = ld_histograms[..., chunc_n*nb_bins:(chunc_n+1)*nb_bins]
        intraclass_variances = get_intraclass_variances(hist, levels=levels, e=e)
        #  Bringing the intraclass variances to a standard normal distribution for a better softmax
        intraclass_variances = intraclass_variances - intraclass_variances.mean(dim=-1, keepdim=True)
        intraclass_variances = intraclass_variances / (intraclass_variances.std(dim=-1, keepdim=True) + e)
        optimal_threshold_prob = (-intraclass_variances / t).softmax(dim=-1)
        ld_otsu_chuncs.append(optimal_threshold_prob)
    ld_otsu_chuncs = torch.cat(ld_otsu_chuncs, dim=-1)
    return ld_otsu_chuncs.swapaxes(-1, dim)


# def otsu_threshold(histograms: Tensor, dim: int = 1, t=.01, nb_bins: int = -1, e=1e-10) -> Tensor:
#     device = histograms.device
#     if histograms.dim() == 1 and dim != 0:
#         histograms = histograms[None, :]
#     if nb_bins < 0:
#         nb_bins = histograms.size(dim)
#     ld_histograms = histograms.swapaxes(dim, -1)
#     levels = torch.arange(0, nb_bins, dtype=torch.float, device=device).view(*([1] * (histograms.dim()-1)), -1)
#     ld_otsu_chuncs = []
#     for chunc_n in range(0, ld_histograms.size(-1)//nb_bins):
#         hist = ld_histograms[..., chunc_n*nb_bins:(chunc_n+1)*nb_bins]
#         h_sum = hist.sum(dim=-1, keepdim=True)
#         low_coef = hist.cumsum(dim=-1)/h_sum
#         high_coef = 1 - low_coef
#         low_E_x = ((levels * hist).cumsum(dim=-1) / (hist.cumsum(dim=-1) + e))
#         low_var = (((levels - low_E_x) ** 2) * hist).cumsum(dim=-1) / (hist.cumsum(dim=-1) + e)

#         f_levels = torch.flip(levels, dims=[0])
#         f_hist = torch.flip(hist, dims=[-1])
#         f_high_E_x = ((f_levels * f_hist).cumsum(dim=-1) / (f_hist.cumsum(dim=-1) + e))
#         f_high_var = (((f_levels - f_high_E_x) ** 2) * f_hist).cumsum(dim=-1) / (f_hist.cumsum(dim=-1) + e)
#         high_var = torch.flip(f_high_var, dims=[-1])

#         intraclass_variances = low_var * low_coef + high_var * high_coef
#         intraclass_variances = intraclass_variances - intraclass_variances.mean(dim=-1, keepdim=True)
#         intraclass_variances = intraclass_variances / (intraclass_variances.std(dim=-1, keepdim=True) + e)
#         optimal_threshold_prob = (-intraclass_variances / t).softmax(dim=-1)
#         ld_otsu_chuncs.append(optimal_threshold_prob)
#     ld_otsu_chuncs = torch.cat(ld_otsu_chuncs, dim=-1)
#     return ld_otsu_chuncs.swapaxes(-1, dim)


class DiffOtsu(torch.nn.Module):
    def __init__(self, first_bin: Union[None, Number] = None, last_bin: Union[None, Number] = None,
                 nbins: Number = 10, bin_centers: Union[None, Tensor] = None, energy_ratio: Number = 1.,
                 temperature: float = .01, e: float = 1e-10) -> None:
        super().__init__()
        self.nbins: int = nbins
        self.t: float = temperature
        self.e: float = e
        self.binning_layer = DiffHistogram(first_bin=first_bin, last_bin=last_bin, nbins=nbins,
                                           bin_centers=bin_centers, energy_ratio=energy_ratio, pooling=None,
                                           keepdims=True)

    def forward(self, x: Tensor) -> Tensor:
        if x.dim() != 4:
            raise ValueError("Input must be a BxCxHxW tensor")
        if x.size(1) != 1:
            # TODO: Implement (cumsum that resets every bins)
            raise NotImplementedError("Number of bins must match the number of channels")
        bins = self.binning_layer.bins[None, :, None, None]
        x = torch.clamp(x, bins.min(), bins.max())
        binned_x = self.binning_layer(x)  # (B, 1xBIN, H, W)
        histogram = binned_x.sum(dim=(2, 3), keepdims=True)  # (B, 1xBIN, 1, 1)
        thr_prob = diff_otsu_threshold(histogram, dim=1, t=self.t, nb_bins=self.nbins, e=self.e)
        result_chunks = []
        for chunk_n in range(0, binned_x.size(1) // self.nbins):
            chunk_start = chunk_n * self.nbins
            chunk_end = (chunk_n + 1) * self.nbins
            binned_chunk = binned_x[:, chunk_start: chunk_end, :, :]
            chunk_cum_prob = thr_prob[:, chunk_start: chunk_end, :, :].cumsum(dim=1)
            result_chunks.append((binned_chunk * chunk_cum_prob).sum(dim=1, keepdims=True))
        return torch.cat(result_chunks, dim=1)


def __avg_pool(x, output_size) -> torch.Tensor:
    return torch.nn.functional.adaptive_avg_pool2d(x, (output_size, output_size))


class DiffHOG(torch.nn.Module):
    def __init__(self, cell_size: Number = 8,
                 pooling: Union[Literal['avg'], Literal['sum'], None, torch.nn.Module] = None,
                 keepdims: bool = True, nbins: int = 9, signed_gradient: bool = False) -> None:
        super().__init__()
        self.cell_size: Number = cell_size
        self.keepdims: bool = keepdims
        self.nbins: int = nbins
        self.signed_gradient: bool = signed_gradient
        angle_bins = torch.linspace(0, 3.14159265359 * (1+signed_gradient), nbins + 1, requires_grad=False)
        angle_bins = (angle_bins[:-1] + angle_bins[1:]) / 2
        self.histogram_layer = DiffHistogram(bin_centers=angle_bins, energy_ratio=1, pooling='None')
        self.grad_filter = torch.nn.Conv2d(1, 2, 3, padding=1, bias=False)
        self.grad_filter.weight[0, 0, :, 0] = [1, 2, 1]
        self.grad_filter.weight[0, 0, :, 2] = [-1, -2, -1]
        self.grad_filter.weight[0, 0, 0, :] = [1, 2, 1]
        self.grad_filter.weight[0, 0, 2, :] = [-1, -2, -1]
        self.pooling_method: str = pooling

        if pooling is None:
            self.pooling = lambda x: x

        elif pooling == 'avg' and cell_size < 0:
            self.pooling = lambda x: x.mean(dim=(2, 3), keepdims=self.keepdims)
        elif pooling == 'avg' and cell_size > 1:
            if int(cell_size) != cell_size:
                raise ValueError("Cell size must be an integer when > 1")
            self.pooling = lambda x: torch.nn.functional.avg_pool2d(x, cell_size, stride=cell_size)
        elif pooling == 'avg' and 0. < cell_size < 1.:
            if (int(1/cell_size) - 1/cell_size) ** 2 > 1e-6:
                raise ValueError("1/cell_size must be an integer when 0 < cell_size < 1")
            else:
                output_size = int(np.round(1/cell_size))
            self.pooling = lambda x: __avg_pool(x, output_size)

        elif pooling == 'sum' and cell_size < 0:
            self.pooling = lambda x: x.sum(dim=(2, 3), keepdims=self.keepdims)
        elif pooling == 'sum' and cell_size > 1:
            if int(cell_size) != cell_size:
                raise ValueError("Cell size must be an integer when > 1")
            self.pooling = lambda x: torch.nn.functional.avg_pool2d(x, cell_size, stride=cell_size)
        elif pooling == 'sum' and 0. < cell_size < 1.:
            if (int(1/cell_size) - 1/cell_size) ** 2 > 1e-6:
                raise ValueError("1/cell_size must be an integer when 0 < cell_size < 1")
            else:
                output_size = int(np.round(1/cell_size))
            self.pooling = lambda x: __avg_pool(x) * output_size ** 2
        elif isinstance(pooling, torch.nn.Module):
            self.pooling = pooling
            self.pooling_method = f"custom_{pooling.__class__.__name__}"
        else:
            raise ValueError(f"Unknown pooling method {pooling}")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() != 4:
            raise ValueError("Input must be a BxCxHxW tensor")
        per_channel = []
        for ch in range(0, x.size(1)):
            ch_x = self.grad_filter(x[:, ch:ch+1, :, :])  # (B, 2, H, W)
            if not self.signed_gradient:
                ch_x = ch_x * torch.tanh(ch_x*10000)  # Approximate abs but differentiable
            magnitude = torch.sqrt(ch_x[:, 0] ** 2 + ch_x[:, 1] ** 2)[:, None, :, :]  # (B, 1, H, W)
            angles = torch.atan2(ch_x[:, 1], ch_x[:, 0])[:, None, :, :]  # (B, 1, H, W)
            binned_angles = self.histogram_layer(angles)  # (B, 1xBIN, H, W)
            binned_magnitudes = binned_angles * magnitude  # (B, 1xBIN, H, W)
            per_channel.append(binned_magnitudes)
        x = torch.cat(per_channel, dim=1)
        del per_channel
        return self.pooling(x)

    @property
    def angle_bins(self) -> torch.Tensor:
        return self.histogram_layer.bins
