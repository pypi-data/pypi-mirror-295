import pytest
import ptlbp
import torch
import numpy as np
from ptlbp.testing import generate_noise_image, generate_image


debug_test_multiradii = True


@pytest.mark.parametrize("img, radii_count, num_components, out_std", [
    [generate_image(100), 6, 200, .0019],
    [generate_image(100), 3, 200, .0028],
    [generate_image(100), 2, 200, .0033],
    [generate_image(100), 1, 200, .0052],
    [generate_noise_image(100), 1, 200, .0026],
    [generate_noise_image(100), 1, 0, 0.0065]  # No PCA and post-PCA processing
    ])
def test_multiradii(img, radii_count, num_components, out_std):
    torch.manual_seed(1337)
    lbp = ptlbp.DiffSRSLBP(num_components=num_components, radii=range(1, radii_count + 1))
    output = lbp(img)
    if num_components > 0:
        assert output.size(0) == 1 and output.size(1) == num_components and output.size(2) == output.size(3) == 1
    else:
        assert output.size(0) == 1 and output.size(1) == 254 * radii_count and output.size(2) == output.size(3) == 1
    assert np.allclose(output.detach().numpy().std(), out_std, atol=.00015)


#  Test the pca_normalise function
#  Essentially test that after learning the pca components, embeedings from images with similar texture are closer
#  then ones with different texture on 10 reclications and with a margin of other_dist - similar_dist
@pytest.mark.parametrize("mode_balance, far_mode_balance, margin", [
    [.1, .9, .1],
    [.2, .8, .1],
    [.3, .7, .05],
    [.4, .6, .03],
    [.1, .4, .1],  # There is no margin here because the far_mode_balance is too close to the mode_balance
])
def test_train_pca(mode_balance, far_mode_balance, margin):

    def dist(x, y):
        return (((x.view(-1)-y.view(-1))**2).sum()**.5).detach().item()

    lbp = ptlbp.DiffSRSLBP(num_components=200, radii=range(1, 6))
    dataloader = torch.utils.data.DataLoader(
        [generate_noise_image(100, mode_balance=.2+(s/10.) * .6, seed=s)[0] for s in range(10)], batch_size=1)
    lbp.train_pca(dataloader)
    for seed_base in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
        ancor = lbp(generate_noise_image(100, mode_balance=mode_balance, seed=seed_base))
        similar = lbp(generate_noise_image(100, mode_balance=mode_balance, seed=seed_base + 1))
        other = lbp(generate_noise_image(100, mode_balance=far_mode_balance, seed=seed_base + 2))
        assert dist(ancor, similar) + margin < dist(ancor, other)


def test_gpu():
    lbp = ptlbp.DiffSRSLBP(num_components=200, radii=range(1, 6))
    img = generate_noise_image(100, mode_balance=.5, seed=1337)
    output = lbp(img)
    if torch.cuda.is_available():
        lbp.to('cuda')
        cuda_output = lbp(img.to('cuda'))
        assert torch.allclose(output, cuda_output.cpu(), atol=1e-6)
    else:
        with pytest.raises(RuntimeError):
            lbp.to('cuda')
            lbp(generate_noise_image(100, mode_balance=.5, seed=1337).to('cuda'))
