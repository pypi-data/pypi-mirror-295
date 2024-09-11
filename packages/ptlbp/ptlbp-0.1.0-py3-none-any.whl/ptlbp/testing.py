import torch
import numpy as np
#  Usefull for testing:


def generate_rect_image(sz) -> torch.Tensor:
    image = torch.zeros([1, 1, sz, sz], dtype=torch.float32)
    image[:, :, sz//4:3*sz//4, sz//4:3*sz//4] = 1
    return image


def generate_cross_image(sz) -> torch.Tensor:
    image = torch.zeros([1, 1, sz, sz], dtype=torch.float32)
    image[:, :, ((3*sz)//8): ((5*sz)//8), ((1*sz)//4):((3*sz)//4)] = 1.
    image[:, :, ((1*sz)//4):((3*sz)//4), ((3*sz)//8): ((5*sz)//8)] = 1.
    return image


def generate_cross_and_small():
    img = np.zeros([100, 100])
    img[20:80, 40:60] = 1  # 5x20x20 = 2000 pixels
    img[40:60, 20:80] = 1
    img[5, 5] = 1
    img[5, 93:96] = 1
    img[93:96, 5] = 1
    return torch.tensor(img[None, None, :, :], dtype=torch.float32)


def generate_square_and_small():
    img = np.zeros([100, 100])
    img[20:80, 40:60] = 1  # 40x50 = 2000 pixels
    img[5, 5] = 1
    img[5, 93:96] = 1
    img[93:96, 5] = 1
    return torch.tensor(img[None, None, :, :], dtype=torch.float32)


def generate_noise_image(sz, mode_balance=.5, small_noise=.1, seed=1337):
    if isinstance(sz, int):
        sz = (sz, sz)
    assert isinstance(sz, tuple)
    torch.manual_seed(seed)
    img = (torch.rand(*sz) > mode_balance).float()
    img[sz[1]//10: 2 * (sz[1]//10), 2 * sz[0]//10: 8 * (sz[0]//10)] = 1
    img[7 * (sz[1]//10): 8 * (sz[1]//10), 2 * sz[0]//10: 8 * (sz[0]//10)] = 0
    img = img * (1-small_noise) + small_noise * torch.rand_like(img)
    return img[None, None, :, :]


def generate_bimodal_image(sz=100, mode1_mean_std=(.4, .2),
                           mode2_mean_std=(.8, .1), mode1_prob=.8, seed=1337) -> torch.Tensor:
    if isinstance(sz, int):
        sz = (sz, sz)
    assert isinstance(sz, tuple)
    torch.manual_seed(seed)
    mode1_pixels = torch.normal(torch.ones(sz) * mode1_mean_std[0], torch.ones(sz) * mode2_mean_std[1])
    mode2_pixels = torch.normal(torch.ones(sz) * mode2_mean_std[0], torch.ones(sz) * mode2_mean_std[1])
    choice = (torch.rand(sz) < mode1_prob).float()
    img = mode1_pixels * choice + mode2_pixels * (1 - choice)
    return img[None, None, :, :]


def generate_image(sz=100):
    if isinstance(sz, int):
        sz = (sz, sz)
    assert isinstance(sz, tuple)
    w, h = sz
    img = torch.zeros(sz)
    img[h//10, w//10] = 1
    img[h//10 - 2: h//10 + 2, 9 * (w//10)] = 1
    img[9 * (h//10), w//10-2: w//10+2] = 1

    img[2*(h//10): 8*(h//10), 4*(w//10): 6*(w//10)] = 1
    img[4*(h//10): 6*(h//10), 2*(w//10): 8*(w//10)] = 1

    img[2*(h//10): 5*(h//10), 2*(w//10): 3*(w//10)] = 1
    img[2*(h//10): 3*(h//10), 2*(w//10): 5*(w//10)] = 1
    return img[None, None, :, :]
