import pytest
import torch
import numpy as np
from ptlbp import DiffLBP, TOffsets
import ptlbp
from ptlbp.testing import generate_rect_image, generate_cross_image, generate_cross_and_small, \
    generate_square_and_small, generate_noise_image

from skimage.feature import local_binary_pattern
np.set_printoptions(linewidth=400)

# Debug flags, activate these to see the plots
debug_plots_forward = False
debug_plots_gradient = False
debug_test_generate_gradient = False
debug_plots_supress = False
debug_plots_scikit_image = False
debug_plots_gradient_ascent = False


@pytest.mark.parametrize("point_sample_str, supress_255,  supress_0, num_points, num_output_channels, histogram_size", [
    ("8r1", True, True, 8, 2**8, 2**8 - 2),
    ("8r1", False, True, 8, 2**8, 2**8 - 1),
    ("8r1", True, False, 8, 2**8, 2**8 - 1),
    ("8r1", False, False, 8, 2**8, 2**8),
    ("1r1", False, False, 1, 2**1, 2**1),
    ("3r1", False, False, 3, 2**3, 2**3),
])
def test_difflbp_properties(point_sample_str, supress_255,  supress_0, num_points, num_output_channels, histogram_size):
    lbp = DiffLBP(point_sample_str, supress_full_pattern=supress_255, supress_zero_pattern=supress_0)
    assert lbp.num_points == num_points
    assert lbp.num_output_channels == num_output_channels
    assert lbp.histogram_size == histogram_size


@pytest.mark.parametrize("image, offsets, hist_nonzero", [
    (generate_rect_image(100), "8r1", {0: 9400.0, 2: 1.0, 3: 1.0, 6: 1.0, 8: 1.0, 12: 1.0, 14: 48.0, 24: 1.0,
                                       32: 1.0, 48: 1.0, 56: 48.0, 96: 1.0, 128: 1.0, 129: 1.0, 131: 48.0, 192: 1.0,
                                       224: 48.0}),
    (generate_cross_image(100), "8r1", {0: 9400.0, 2: 2.0, 3: 2.0, 6: 2.0, 8: 2.0, 12: 2.0, 14: 44.0, 24: 2.0,
                                        32: 2.0, 48: 2.0, 56: 44.0, 62: 1.0, 96: 2.0, 128: 2.0, 129: 2.0, 131: 44.0,
                                        143: 1.0, 192: 2.0, 224: 44.0, 227: 1.0, 248: 1.0})
])
def test_DiffLBP_forward(image: torch.Tensor, offsets: TOffsets, hist_nonzero: dict):
    target_hist = torch.zeros(256)
    for k, v in hist_nonzero.items():
        target_hist[k] = v

    # Create an instance of DiffLBP
    diff_lbp = DiffLBP(offsets=offsets, diff_hardness=100., output_hardness=100.)

    # Perform forward pass
    output = diff_lbp(image)

    # Degug print and plot
    if debug_plots_forward:
        from matplotlib import pyplot as plt
        print(output.view(-1).detach().numpy().tolist())
        d = output.view(-1).detach().numpy().tolist()
        print({n: k for n, k in enumerate(d) if k > 0.0005})
        plt.plot(output.view(-1).detach().numpy().tolist())
        plt.show()

        # # Assert the output shape
        assert output.shape == (1, 256, 1, 1)

        # This is how the values for the test were generated
        # h = {}
        # for i in range(256):
        #     count = output[0, i, 0, 0].item()
        #     if count > 0.000000001:
        #         h[i] = count
        # print("H:", repr(h))

    assert torch.allclose(output.view(-1), target_hist.view(-1), atol=1e-7)


@pytest.mark.parametrize("image, offsets, erase_pattern, ignore_zero, small_grad, median_grad, large_grad", [
    (generate_cross_image(100), "8r1", 0, False, -0.8780800700187683, 0.0, 0.8780801296234131),
    (generate_cross_image(100), "8r1", 0, True, 0., 0., 0.),
    (generate_cross_image(100), "8r1", 1, True, -3.87195797e-07, 0., 3.3202590543e-07),
    (generate_cross_image(100), "8r1", 1, False, -3.87195797e-07, 0., 3.3202590543e-07),
    (generate_cross_image(100), "8r1", 2, True, -6.4000669e-05, 0., 6.4000647e-05),
    (generate_cross_image(100), "8r1", 79, True, 0., 0., 0.),
    (generate_cross_image(100), "8r1", 14, True, 0., 0., 0.),
])
def test_gradient(image: torch.Tensor, offsets: str, erase_pattern: int, ignore_zero: bool, small_grad: float,
                  median_grad: float, large_grad: float) -> None:
    diff_lbp = DiffLBP(offsets=offsets, diff_hardness=10., output_hardness=10., pool_pixels="sum")
    image.requires_grad_()
    target_hist = torch.zeros(256)
    output = diff_lbp(image).view(-1)
    target_hist = output.clone().detach()
    target_hist[erase_pattern] = 0
    if ignore_zero:
        loss = ((output[1:] - target_hist[1:])**2).sum()
    else:
        loss = ((output - target_hist)**2).sum()
    loss.backward()
    grad_img = image.grad
    out_small_grad = torch.quantile(grad_img, .02)
    out_median_grad = torch.quantile(grad_img, .5)
    out_large_grad = torch.quantile(grad_img, .98)
    if debug_plots_gradient:
        from matplotlib import pyplot as plt
        plt.imshow(image.grad[0, 0, :, :].detach().numpy())
        plt.colorbar()
        plt.title(f"Erased:{erase_pattern} Zero ignored:{ignore_zero}")
        plt.show()
    # This was used to generate the values
    # print(f"\n{erase_pattern} {ignore_zero}: {out_small_grad}, {out_median_grad}, {out_large_grad}")
    if ignore_zero:
        precision = 1e-5
    else:
        precision = 1e-1
    assert torch.allclose(out_small_grad, torch.tensor(small_grad, dtype=torch.float32), atol=precision)
    assert torch.allclose(out_median_grad, torch.tensor(median_grad, dtype=torch.float32), atol=precision*0.001)
    assert torch.allclose(out_large_grad, torch.tensor(large_grad, dtype=torch.float32), atol=precision)


def test_generate_gradient_image():
    image = generate_cross_image(100)
    diff_lbp = DiffLBP(offsets="8r1", diff_hardness=10, output_hardness=10)
    output = diff_lbp(image)
    # TODO(anguelos) find why removing the epsilon from the output gives a NaN image.
    # The epsilon can be assigned to a single cell of output and it still works
    weak_grad_image = diff_lbp.get_gradient_image(image, output + output * torch.rand_like(output) * .01)
    strong_grad_image = diff_lbp.get_gradient_image(image, torch.ones_like(output))
    if debug_plots_gradient_ascent:
        from matplotlib import pyplot as plt
        print("output: ", output.view(-1).detach().numpy().tolist())
        plt.imshow(strong_grad_image[0, 0, :, :].numpy())
        plt.colorbar()
        plt.title("Strong gradient")
        plt.show(block=False)
        plt.figure()
        plt.imshow(weak_grad_image[0, 0, :, :].numpy())
        plt.colorbar()
        plt.title("Weak gradient")
        plt.show()
    assert weak_grad_image.shape == strong_grad_image.shape == image.shape

    # Very rearelly the following fails randomly. This should be deterministic but
    # maybe numeric instability is not deterministic. Reducing 10 to 5 makes the test pass more often
    # assert (weak_grad_image ** 2).sum() * 10 < (strong_grad_image ** 2).sum()
    assert (weak_grad_image ** 2).sum() * 5 < (strong_grad_image ** 2).sum()
    grad_image = diff_lbp.get_gradient_image(image, torch.ones(256))
    assert grad_image.shape == image.shape

    # TODO(anguelos) test this more extencively
    grad_img = diff_lbp.get_triplet_gradient_image(image, torch.ones(1, 256, 1, 1), torch.ones(1, 256, 1, 1))
    assert grad_img.shape == image.shape
    grad_img = diff_lbp.get_triplet_gradient_image(image, torch.ones(256), torch.ones(256))
    assert grad_img.shape == image.shape


def test_supress():
    """Test the supression of zero and full patterns in the output histogram.
    """
    image = generate_cross_image(100)
    image[:, :, 5, 5] = 1
    image[:, :, 5, 94] = 1
    image[:, :, 94, 5] = 1
    image[:, :, 94, 94] = 1
    diff_lbp_nz_na = DiffLBP(offsets="8r1", diff_hardness=3, output_hardness=3,
                             supress_zero_pattern=True, supress_full_pattern=True)
    diff_lbp_nz_ya = DiffLBP(offsets="8r1", diff_hardness=3, output_hardness=3,
                             supress_zero_pattern=True, supress_full_pattern=False)
    diff_lbp_yz_na = DiffLBP(offsets="8r1", diff_hardness=3, output_hardness=3,
                             supress_zero_pattern=False, supress_full_pattern=True)
    diff_lbp_yz_ya = DiffLBP(offsets="8r1", diff_hardness=3, output_hardness=3,
                             supress_zero_pattern=False, supress_full_pattern=False)
    for variant in [diff_lbp_nz_na, diff_lbp_nz_ya, diff_lbp_yz_na, diff_lbp_yz_ya]:
        target = variant(torch.zeros_like(image))
        grad_image = variant.get_gradient_image(image, target)
        if debug_plots_supress:
            from matplotlib import pyplot as plt
            plt.imshow(grad_image[0, 0, :, :].detach().numpy() ** 2)
            plt.colorbar()
            plt.title(f"Supress zero: {variant.supress_zero_pattern}, Supress full: {variant.supress_full_pattern}")
            plt.show()
        assert grad_image.shape == image.shape


def get_jaccard(lbp_img1, lbp_img2, e=0.000000000000001):
    lab1_sz = int(lbp_img1.max() + 1)  # size of the img1 namespace
    lab2_sz = int(lbp_img2.max() + 1)  # size of the img2 namespace
    labs1, lab1_freqs = np.unique(lbp_img1, return_counts=True)
    labs2, lab2_freqs = np.unique(lbp_img2, return_counts=True)
    joint, joint_freqs = np.unique(lbp_img2.astype("uint32") * lab1_sz + lbp_img1.astype("uint32"), return_counts=True)
    lab1_hist = np.zeros(lab1_sz)
    lab1_hist[labs1.astype("uint32")] = lab1_freqs
    lab2_hist = np.zeros(lab2_sz)
    lab2_hist[labs2.astype("uint32")] = lab2_freqs
    joint_hist = np.zeros(lab1_sz * lab2_sz)
    joint_hist[joint] = joint_freqs
    sparse_union_table = np.zeros([lab1_sz, lab2_sz])
    sparse_intersection_table = np.zeros([lab1_sz, lab2_sz])
    for joint_lab in joint:
        lab1 = joint_lab % lab1_sz
        lab2 = joint_lab // lab1_sz
        sparse_union_table[lab1, lab2] = (lab1_hist[lab1] + lab2_hist[lab2]) - joint_hist[joint_lab]
        sparse_intersection_table[lab1, lab2] = joint_hist[joint_lab]

    # Getting the labels
    lab1 = np.arange(lab1_sz)        
    lab1 = lab1[lab1_hist > 0]
    lab2 = np.arange(lab2_sz)
    lab2 = lab2[lab2_hist > 0]
    intersection_table = sparse_intersection_table[lab1, :][:, lab2]
    union_table = sparse_union_table[lab1, :][:, lab2]

    #  Jaccard of two empty sets is defined as 0 therefor no e goes on the numerator
    return (intersection_table / (union_table + e), intersection_table, union_table,
            lab1, lab2, lab1_hist[lab1], lab2_hist[lab2])


parameters = [
              #  As the diff_harness goes down, the consistency between diff_lbp and sk_lbp goes down
              [100, 100, .97, 1, .78, 1],
              [10, 100, .97, 2, .78, 1],
              [3, 100, .66, 6, .78, 1],  # one patterns missed in a class where 3 occur (rotated 4 times)
              [1, 100, .66, 5, .78, 1],  # 6 becomes 5 because the 0 pattern is no longer created
              [.9, 100, .66, 5, .78, 1],
              [.5, 100, .66, 5, .78, 1],  # Eveything is mapped as the 255 pattern

              [100, .1, .97, 1, .78, 1],  # But we can see that the output_hardness has no effect
              ]


@pytest.mark.parametrize("diff_hardness, output_hardness, diff_min_precision, diff_imprecise_allowed,\
    sk_min_precision, sk_imprecise_allowed", parameters)
def test_scikit_image_agreement(diff_hardness, output_hardness, diff_min_precision,
                                diff_imprecise_allowed, sk_min_precision, sk_imprecise_allowed):
    # TODO (anguelos) merge this with the test in test_binary_to_onehot
    # Scikit image assigns different labels to each pattern but they should be internally coherent
    # A difference between our and the scikit variant is whether we use > cs . >= which allows for some confusion
    # between 0 and 255 patterns
    pt_img = generate_cross_and_small()
    np_img = pt_img.numpy()[0, 0, :, :]
    fulllbp = DiffLBP(offsets="8r1", diff_hardness=diff_hardness, output_hardness=output_hardness,
                      supress_zero_pattern=False, supress_full_pattern=False, pool_pixels=False)
    diff_lbp_img = torch.argmax(fulllbp(pt_img).detach(), dim=1)[0, :, :].numpy().astype("uint8")
    sk_lbp_img = local_binary_pattern(np_img.astype("uint8"), 8, 1, 'default')[1:-1, 1:-1]
    iou, i, u, diff_lab, sk_lab, diff_hist, sk_hist = get_jaccard(diff_lbp_img, sk_lbp_img)

    assert diff_hist.sum() == sk_hist.sum() == i.sum()  # sanity check about get_jaccard

    sk_precision = i.max(axis=0)/i.sum(axis=0)
    assert sk_hist.size == np.unique(sk_lbp_img).size  # sanity check about get_jaccard
    assert sk_precision.size == np.unique(sk_lbp_img).size  # sanity check about get_jaccard

    diff_precision = i.max(axis=1)/i.sum(axis=1)
    assert sk_hist.size == np.unique(sk_lbp_img).size   # sanity check about get_jaccard
    assert diff_precision.size == np.unique(diff_lbp_img).size  # sanity check about get_jaccard

    if debug_plots_scikit_image:
        print(f"Diff Hardnes: {diff_hardness}, Output Hardnes: {output_hardness}")
        print(f"diff_precision : {diff_precision}")
        print(f"sk_precision : {sk_precision}")

    assert diff_precision.min() > diff_min_precision
    assert (diff_precision < 1).sum() <= diff_imprecise_allowed
    assert sk_precision.min() > sk_min_precision
    assert (sk_precision < 1).sum() <= sk_imprecise_allowed

    if debug_plots_scikit_image:
        from matplotlib import pyplot as plt
        fig, axs = plt.subplots(2, 6)
        for n, pattern in enumerate([0, 1, 4, 16, 64, 255]):
            axs[0, n].imshow(diff_lbp_img == pattern)
            axs[1, n].imshow(sk_lbp_img == pattern)
        plt.show()
        plt.imshow(iou)
        plt.colorbar()
        plt.show()


def test_gradient_ascent():
    cross_img = generate_cross_and_small()
    square_img = generate_square_and_small()
    lbp = DiffLBP(offsets="8r1", diff_hardness=10, output_hardness=1,
                  supress_zero_pattern=True, supress_full_pattern=True)
    with torch.no_grad():
        cross_output = lbp(cross_img)
        square_output = lbp(square_img)
    square_grad = lbp.get_gradient_image(square_img, cross_output)
    cross_grad = lbp.get_gradient_image(cross_img, square_output)
    if debug_plots_gradient_ascent:
        from matplotlib import pyplot as plt
        grad_img = torch.cat([square_grad, cross_grad], dim=3)
        plt.imshow(grad_img[0, 0].numpy())
        plt.colorbar()
        plt.show()


@pytest.mark.parametrize("scale, translate, close_mean", [[1., 0., 1.],
                                                          [.7, 0., 1.], [.5, 0., .995],
                                                          [.3, 0., .971], [.1, 0., .75],
                                                          [1.5, 0., .996], [2., 0., 1.],
                                                          [1., .001, 1.], [1., -.5, .75],
                                                          ])
def test_ilumination_invarince(scale, translate, close_mean):
    pt_img = generate_cross_and_small() * .5
    fulllbp = DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                      supress_zero_pattern=False, supress_full_pattern=False, pool_pixels=False)
    gray_lbp_img = torch.argmax(fulllbp(pt_img).detach(), dim=1)[0, :, :].numpy().astype("uint8")
    shifted_lbp_img = torch.argmax(fulllbp(pt_img*scale+translate).detach(), dim=1)[0, :, :].numpy().astype("uint8")
    assert (gray_lbp_img == shifted_lbp_img).mean() >= close_mean


def test_gpu():
    lbp = ptlbp.DiffLBP("8r1")
    assert lbp.device == torch.device('cpu')
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    if torch.cuda.is_available():
        lbp.to('cuda')
        cuda_output = lbp(img.to('cuda'))
        assert torch.allclose(output, cuda_output.cpu(), atol=1e-6)
        assert str(lbp.device).split(':')[0] == 'cuda'
    else:
        with pytest.raises(RuntimeError):
            lbp.to('cuda')
            lbp(generate_noise_image(100, mode_balance=.5, seed=1337).to('cuda'))


def test_diff_pool():
    lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                        supress_zero_pattern=False, supress_full_pattern=False, pool_pixels="sum")
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                        supress_zero_pattern=False, supress_full_pattern=False, pool_pixels="avg")
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                        supress_zero_pattern=False, supress_full_pattern=False, pool_pixels="discrete")
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                        supress_zero_pattern=False, supress_full_pattern=False,
                        pool_pixels=torch.nn.AdaptiveAvgPool2d(1))
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                        supress_zero_pattern=False, supress_full_pattern=False, pool_pixels=None)
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 98, 98)

    with pytest.raises(ValueError):
        lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                            supress_zero_pattern=False, supress_full_pattern=False, pool_pixels="unknown")
        img = generate_noise_image(100, mode_balance=.5, seed=1337)
        output = lbp(img)
        assert output.shape == (1, 256, 1, 1)


def test_diff_comparissons():
    lbp = ptlbp.DiffLBP(offsets="8r1", comparisson="otsu")
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", comparisson="simple")
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", comparisson="quantile")
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    lbp = ptlbp.DiffLBP(offsets="8r1", comparisson=ptlbp.Comparisson())
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    assert output.shape == (1, 256, 1, 1)

    with pytest.raises(ValueError):
        lbp = ptlbp.DiffLBP(offsets="8r1", comparisson=None)
        img = generate_noise_image(100, mode_balance=.5, seed=1337)
        output = lbp(img)
        assert output.shape == (1, 256, 1, 1)


def test_compute_lbp_image():
    lbp = ptlbp.DiffLBP(offsets="8r1", diff_hardness=100, output_hardness=100,
                        supress_zero_pattern=False, supress_full_pattern=False, pool_pixels=False)
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    lbp_img, confidence = lbp.compute_lbp_image(img)
    patterns = np.unique(lbp_img.detach().numpy())
    assert 0 < len(patterns) <= 256
    assert 0 <= confidence.min() <= confidence.max() <= 1


def test_double_onehots():
    img = generate_cross_and_small()

    single = ptlbp.DiffLBP(offsets="8r1", double_onehots=False)
    double = ptlbp.DiffLBP(offsets="8r1", double_onehots=True)
    res_from_double = double(img).float()
    res_from_single = single(img).float()
    assert torch.allclose(res_from_double, res_from_single, atol=30)

    single = ptlbp.DiffLBP(offsets="8r1", double_onehots=False, pool_pixels="avg")
    double = ptlbp.DiffLBP(offsets="8r1", double_onehots=True, pool_pixels="avg")
    res_from_double = double(img).float()
    res_from_single = single(img).float()
    assert torch.allclose(res_from_double, res_from_single, atol=1e-3)


# TODO (anguelos) expand this to test for average pooling
@pytest.mark.parametrize("pool_pixels", ["discrete", "avg"])
def test_forward_sliced(pool_pixels):
    if pool_pixels in ["discrete"]:
        img = generate_cross_and_small()
        assert img.size(3) == img.size(2) == 100
        lbp = ptlbp.DiffLBP(offsets="8r1", pool_pixels=pool_pixels, output_hardness=100, diff_hardness=100)
        double_lbp = ptlbp.DiffLBP(offsets="8r1", double_onehots=True, pool_pixels=pool_pixels)
        output = lbp(img)
        with torch.no_grad():
            sliced_output = lbp.forward_sliced(img, 40)
            double_slice_output = double_lbp.forward_sliced(img, 40)
            pseudo_sliced_output = lbp.forward_sliced(img, 200)
        assert torch.allclose(output, sliced_output, atol=1e-2)
        assert torch.allclose(output, pseudo_sliced_output, atol=1e-2)
        assert torch.allclose(output, double_slice_output, atol=30.)
    else:
        lbp = ptlbp.DiffLBP(offsets="8r1", pool_pixels=pool_pixels, output_hardness=100, diff_hardness=100)
        print("Raisiong:", pool_pixels)
        with pytest.raises(ValueError):
            with torch.no_grad():
                _ = lbp.forward_sliced(generate_cross_and_small(), 40)


def test_block_normalise():
    img = generate_cross_and_small()
    lbp_supr_bn = ptlbp.DiffLBP(offsets="8r1", pool_pixels="discrete", output_hardness=100, diff_hardness=100,
                                supress_full_pattern=True, supress_zero_pattern=True, block_normalise=True)
    lbp_bn = ptlbp.DiffLBP(offsets="8r1", pool_pixels="discrete", output_hardness=100, diff_hardness=100,
                           supress_full_pattern=False, supress_zero_pattern=False, block_normalise=True)
    lbp = ptlbp.DiffLBP(offsets="8r1", pool_pixels="discrete", output_hardness=100, diff_hardness=100,
                        supress_full_pattern=False, supress_zero_pattern=False, block_normalise=False)

    output_supr_bn = lbp_supr_bn(img)
    output_bn = lbp_bn(img)
    output = lbp(img)
    assert output_bn.size() == output.size() and output.size() != output_supr_bn.size()
    assert torch.allclose(output_bn.sum(), output_supr_bn.sum(), atol=1e-7)
    assert torch.allclose(output_bn.sum(), torch.ones(1), atol=1e-7)
    valid_pixels = lbp.valid_pixels_size(img.size())
    valid_pixels = valid_pixels[2] * valid_pixels[3]
    assert .99 * valid_pixels <= output.sum().item() <= 1.01 * valid_pixels
