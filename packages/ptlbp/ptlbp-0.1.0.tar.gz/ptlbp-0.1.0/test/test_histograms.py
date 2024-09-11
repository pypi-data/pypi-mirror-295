import pytest
import torch
import numpy as np
from ptlbp import _DiffBinning, DiffHistogram, DiffOtsu, hard_otsu_threshold, diff_otsu_threshold
import ptlbp
from ptlbp.testing import generate_bimodal_image
from ptlbp.util import np_image_as_batch, plot_img
from skimage import data
from skimage.filters import threshold_otsu as sk_otsu

np.set_printoptions(linewidth=400)


debug_binning = False
debug_hard_otsu = False
if any([debug_binning, debug_hard_otsu]):
    from matplotlib import pyplot as plt


def test_diffbinning():
    img = np_image_as_batch(data.coins())
    sz = list(img.size())
    bins = torch.linspace(-0.1, 1.1, 100)
    binned = _DiffBinning(bin_centers=bins)(img)
    assert binned.size() == torch.Size(sz + [bins.size(0)])
    binned_sum = binned.sum(dim=-1)
    if debug_binning:
        print(torch.aminmax(img))
        plt.imshow(img[0, 0, :, :].numpy())
        plt.title(f"Input image {torch.aminmax(img)}")
        plt.colorbar()
        plt.show(block=False)
        plt.figure()
        plt.imshow(binned_sum[0, 0, :, :].numpy())
        plt.title(f"Binned sum {torch.aminmax(binned_sum)}")
        plt.colorbar()
        plt.show()
    assert torch.allclose(binned.sum(dim=-1), torch.ones(sz), atol=1e-5)
    # Reconstruction only works well when no clamping is needed
    reconstructed = (binned * bins.view(*([1] * img.dim() + [-1]))).sum(dim=-1)
    assert torch.allclose(reconstructed, img, atol=1e-5)


@pytest.mark.parametrize(["img"], [[data.coins()], [data.camera()], [data.page()],
                                   [np.zeros([100, 100])], [np.ones([100, 100])],
                                   [(np.random.rand(100, 100) * 255).astype(np.uint8)]])
def test_hard_otsu(img):
    img = np_image_as_batch(img)
    hist = torch.histc(img, bins=100, min=0, max=1)
    otsu_thr = hard_otsu_threshold(hist).item() / 100
    sk_thr = sk_otsu(img[0, 0, :, :].numpy())
    if debug_hard_otsu:
        print(f"Mean Hard: {(img > otsu_thr).float().mean().item()} Mean SK{(img > otsu_thr).float().mean().item()}")
        plot_img(img, title="Input image", block=False)
        plot_img(img > otsu_thr, title="My Otsu", block=False)
        plot_img(img > sk_thr, title="SK Otsu", block=True)
    assert (img > otsu_thr).float().mean().item() == (img > otsu_thr).float().mean().item()
