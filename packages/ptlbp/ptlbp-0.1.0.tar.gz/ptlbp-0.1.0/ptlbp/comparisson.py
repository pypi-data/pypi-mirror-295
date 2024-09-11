import torch
from .histograms import hard_otsu_threshold


class Comparisson(torch.nn.Module):
    def __init__(self, margin: float = .25, learn_margin: bool = False) -> None:
        super().__init__()
        self.margin = torch.nn.parameter.Parameter(torch.tensor(margin, dtype=torch.float32))
        self.margin.requires_grad = learn_margin

    def forward(self, x, offset: torch.Tensor) -> torch.Tensor:
        crop_x = (x.size(2) - offset.size(2)) // 2
        crop_y = (x.size(3) - offset.size(3)) // 2
        return offset - x[:, :, crop_x:-crop_x, crop_y:-crop_y] - self.margin


class ComparissonOtsu(torch.nn.Module):
    def __init__(self,  bins: int = 255, assumed_max: float = 1.0) -> None:
        super().__init__()
        self.bins = bins
        self.assumed_max = assumed_max

    def forward(self, x, offset: torch.Tensor) -> torch.Tensor:
        crop_x = (x.size(2) - offset.size(2)) // 2
        crop_y = (x.size(3) - offset.size(3)) // 2
        diff = offset - x[:, :, crop_x:-crop_x, crop_y:-crop_y]
        # adding 1% noise to avoid quantile problems
        noisy_diff = diff + torch.randn_like(diff) * .01 * (diff.max() - diff.min())
        hist = torch.histc(noisy_diff, bins=self.bins, min=0, max=self.assumed_max)
        quantile_bin_up = (hist.cumsum(0)/hist.sum() < .99).sum().item()
        quantile_bin_down = hist.size(0) - (hist.cumsum(0)/hist.sum() > .01).sum().item()
        # enforce at lest 10 bins to be passed to the histogram
        if quantile_bin_down + 10 >= quantile_bin_up:
            quantile_bin_down -= 10
            quantile_bin_up += 10
            quantile_bin_down = max(1, quantile_bin_down)
            quantile_bin_up = min(self.bins - 1, quantile_bin_up)
        otsu_bin_idx = hard_otsu_threshold(hist[quantile_bin_down:quantile_bin_up]).item() + quantile_bin_down
        #print(otsu_bin_idx)
        #print(self.bins)
        margin = (self.assumed_max / self.bins) * otsu_bin_idx
        #margin = (otsu_bin * self.assumed_max) / self.bins
        #print(margin)
        return diff - margin


class ComparissonQuantile(torch.nn.Module):
    def __init__(self,  bins: int = 255, assumed_max: float = 1.0) -> None:
        super().__init__()
        self.bins = bins
        self.assumed_max = assumed_max

    def forward(self, x, offset: torch.Tensor) -> torch.Tensor:
        crop_x = (x.size(2) - offset.size(2)) // 2
        crop_y = (x.size(3) - offset.size(3)) // 2
        diff = offset - x[:, :, crop_x:-crop_x, crop_y:-crop_y]
        # adding 1% noise to avoid quantile problems
        noisy_diff = diff + torch.randn_like(diff) * .01 * (diff.max() - diff.min())
        hist = torch.histc(noisy_diff, bins=self.bins, min=0, max=self.assumed_max)
        quantile_bin_up = (hist.cumsum(0)/hist.sum() < .99).sum().item()
        quantile_bin_down = hist.size(0) - (hist.cumsum(0)/hist.sum() > .01).sum().item()
        margin = ((quantile_bin_down + quantile_bin_up) / 2) * self.assumed_max / self.bins
        return diff - margin
