import pytest
import torch
from ptlbp import PointSampler, Comparisson, ComparissonOtsu, ComparissonQuantile
import ptlbp
from ptlbp.testing import generate_rect_image, generate_noise_image, generate_bimodal_image


print_plot_debug = False


@pytest.mark.parametrize(["img", "pointsampler", "comparisson", "true_count_range"], [

    (generate_rect_image(100), PointSampler(1, "8r1"), Comparisson(), (580, 600)),
    (generate_rect_image(100), PointSampler(1, "8r1"), ComparissonOtsu(), (580, 600)),
    (generate_rect_image(100), PointSampler(1, "8r1"), ComparissonQuantile(), (580, 600)),

    (torch.zeros(1, 1, 100, 100), PointSampler(1, "8r1"), Comparisson(), (0, 0)),
    (torch.ones(1, 1, 100, 100), PointSampler(1, "8r1"), Comparisson(), (0, 0)),

    (torch.zeros(1, 1, 100, 100), PointSampler(1, "8r1"), ComparissonOtsu(), (0, 0)),
    (torch.ones(1, 1, 100, 100), PointSampler(1, "8r1"), ComparissonOtsu(), (0, 0)),

    (torch.zeros(1, 1, 100, 100), PointSampler(1, "8r1"), ComparissonQuantile(), (0, 0)),
    (torch.ones(1, 1, 100, 100), PointSampler(1, "8r1"), ComparissonQuantile(), (0, 0)),

    (generate_noise_image(100), PointSampler(1, "8r1"), Comparisson(), (19000, 19100)),
    (generate_noise_image(100), PointSampler(1, "8r1"), ComparissonOtsu(), (560, 600)),
    (generate_noise_image(100), PointSampler(1, "8r1"), ComparissonQuantile(), (15200, 15300)),

    (generate_bimodal_image(100), PointSampler(1, "8r1"), Comparisson(), (9800, 10200)),
    (generate_bimodal_image(100), PointSampler(1, "8r1"), ComparissonOtsu(), (400, 600)),
    (generate_bimodal_image(100), PointSampler(1, "8r1"), ComparissonQuantile(), (6800, 7200)),

    (1 - generate_bimodal_image(100), PointSampler(1, "8r1"), Comparisson(), (11200, 12200)),
    (1 - generate_bimodal_image(100), PointSampler(1, "8r1"), ComparissonOtsu(), (12200, 12300)),
    (1 - generate_bimodal_image(100), PointSampler(1, "8r1"), ComparissonQuantile(), (8350, 8750)),
    ][-3:])
def test_comparisson(img, pointsampler: PointSampler, comparisson: torch.nn.Module, true_count_range: tuple):
    torch.manual_seed(1337)
    x = img
    offsets = pointsampler(x)
    soft_output = comparisson(x, offsets)
    harder_output = torch.tanh(100. * soft_output) * .5 + .5
    hard_output = (harder_output > .5).float()
    if print_plot_debug:
        ptlbp.util.plot_img(img, title=f"Input {type(comparisson)}", block=False)
        ptlbp.util.plot_img(soft_output[:, :1, :, :], title=f"Slice 0, Soft {type(comparisson)}", block=False)
        ptlbp.util.plot_img(harder_output[:, :1, :, :], title=f"Slice 0, Harder {type(comparisson)}", block=True)
        print(comparisson, harder_output.sum(), harder_output.mean())
    assert true_count_range[0] <= hard_output.sum().item() <= true_count_range[1]


def test_zeros():
    x = torch.zeros(1, 1, 100, 100)
    pointsampler = PointSampler(1, "8r1")
    comparisson = ComparissonOtsu()
    offsets = pointsampler(x)
    comparissons = comparisson(x, offsets)
    assert (comparissons < 0).float().mean().item() == 1.
