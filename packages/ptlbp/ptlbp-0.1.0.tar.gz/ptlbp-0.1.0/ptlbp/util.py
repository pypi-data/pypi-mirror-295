from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image
import numpy as np
import torch
import matplotlib
from contextlib import nullcontext
import sklearn
import tqdm


def conditional_no_grad(condition):
    if condition:
        return torch.no_grad()
    else:
        return nullcontext()


def sk_mAP(X, y, metric='l1', progress_bar_freq=-1):
    non_singleton_idx = (y[None, :] == y[:, None]).sum(axis=1) > 1
    X, y = X[non_singleton_idx, :], y[non_singleton_idx]
    num_samples = X.shape[0]
    num_estimated_samples = 0
    map_score = 0.0
    top1 = []
    if progress_bar_freq > 0:
        range_iter = tqdm.tqdm(range(num_samples), total=num_samples,
                               desc='mAP', position=0, leave=True, mininterval=1)
    else:
        range_iter = range(num_samples)
    for i in range_iter:
        y_true = (y == y[i]).astype(int)  # Binary relevance: 1 if same class, 0 otherwise
        if metric == 'l1':
            y_score = np.sum(np.abs(X - X[i]), axis=1)  # L1 distances between sample i and all other samples
        elif metric == 'l2':
            y_score = np.sum((X - X[i])**2, axis=1)
        else:
            raise NotImplementedError(f"Metric {metric} not implemented")
        exclude_self = np.arange(num_samples) != i
        y_true, y_score = y_true[exclude_self], y_score[exclude_self]
        if y_true.sum() > 0:
            top1.append(y_true[y_score.argmin()])
            # Negative y_score as sklearn expects higher scores to be better
            map_score += sklearn.metrics.average_precision_score(y_true, -y_score)
            num_estimated_samples += 1
    map_score /= num_estimated_samples
    return map_score, np.array(top1).mean()


def mAP(X, y, metric='l1'):
    gt_table = (y[None, :] == y[:, None]).astype(int)
    dm = sklearn.metrics.pairwise_distances(X, Y=None, metric='euclidean', n_jobs=None, force_all_finite=True)


def pil_image_as_batch(img, add_noise=0, add_large_gradient=0, device='cpu'):
    img = img.convert('L')
    img = np.array(img).astype(float)/255.
    img = img[None, None, :, :]
    res_img = torch.tensor(img).float().to(device)
    if add_noise > 0:
        N = torch.rand_like(res_img)
        res_img = res_img * (1-add_noise) + add_noise * N
    if add_large_gradient > 0:
        a = torch.ones_like(res_img)
        a = torch.cumsum(a, dim=3)
        a = a/a.max()
        res_img = res_img * (1-add_large_gradient) + add_large_gradient * a
    return res_img


def np_image_as_batch(img, add_noise=0, add_large_gradient=0, device='cpu'):
    img = img.astype(float)/255.
    if img.ndim == 2:
        img = img[None, None, :, :]
    elif img.ndim == 3:
        img = img.transpose(2, 0, 1)
        img = img[None, :, :, :]
    res_img = torch.tensor(img).float().to(device)
    if add_noise > 0:
        N = torch.rand_like(res_img)
        res_img = res_img * (1-add_noise) + add_noise * N
    if add_large_gradient > 0:
        a = torch.ones_like(res_img)
        a = torch.cumsum(a, dim=3)
        a = a/a.max()
        res_img = res_img * (1-add_large_gradient) + add_large_gradient * a
    return res_img


def load_image_as_batch(path, add_noise=0, add_large_gradient=0, device='cpu'):
    img = Image.open(path)
    return pil_image_as_batch(img, add_noise=add_noise, add_large_gradient=add_large_gradient, device=device)


def plot_lbp(img, title='', fig=None, block=False):
    if fig is None:
        fig = plt.figure(constrained_layout=False)
    lab_img = img.detach().cpu().numpy()[0, :, :, :].argmax(axis=0)
    plt.imshow(lab_img, cmap='d256')
    plt.xticks([], [])
    if title:
        plt.title(title)
    plt.show(block=block)
    return fig


def plot_img(img, title='', cmap='gray', fig=None, block=False):
    if fig is None:
        fig = plt.figure(constrained_layout=False)
    np_img = img.detach().cpu().numpy()[0, 0, :, :]
    plt.imshow(np_img, cmap='gray')
    plt.colorbar()
    plt.xticks([], [])
    if title:
        plt.title(title)
    plt.show(block=block)


def plot_slices(img, title='', cols=4, cmap='gray', block=False):
    val_min = img.min().item()
    val_max = img.max().item()
    rows = (img.size(1) // cols) + int((img.size(1) % cols) > 0)
    fig = plt.figure(constrained_layout=False)
    widths = (1 * np.ones(cols)).tolist() + [.05]
    heights = (1 * np.ones(rows)).tolist()
    gs = GridSpec(rows, cols+1, figure=fig, width_ratios=widths,
                  height_ratios=heights, left=0.00, right=1., wspace=0.05, hspace=0.05)
    cbar_ax = fig.add_subplot(gs[:, -1])
    for slice in range(img.shape[1]):
        row = slice // cols
        col = slice % cols
        np_img = img.detach().cpu().numpy()[0, slice, :, :]
        ax = fig.add_subplot(gs[row, col])
        imax = ax.imshow(np_img, cmap='gray', extent=[0, 100, 0, 100], vmin=val_min, vmax=val_max)
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        if slice == img.size(1)-1:
            fig.colorbar(imax, cax=cbar_ax)
            pass
    if title:
        fig.suptitle(title)
    plt.show(block=block)


def create_dicrete_colormap(N, pattern0=0):
    patternValues = np.cumsum(np.ones((N + 1), dtype='uint32')) - 1
    resFloatRed = 0.45 * np.mod(patternValues, 2) + \
        0.325 * np.mod(patternValues / 8, 2) + 0.225 * np.mod(patternValues / 64, 2)
    resFloatGreen = 0.45 * np.mod(patternValues / 2, 2) + \
        0.325 * np.mod(patternValues / 16, 2) + 0.225 * np.mod(patternValues / 128, 2)
    resFloatBlue = 0.6 * np.mod(patternValues / 4, 2) + 0.4 * np.mod(patternValues / 32, 2)
    x = np.linspace(0, 1, N)
    rXY0Y1 = np.concatenate((x.reshape(-1, 1), resFloatRed[:-1].reshape(-1, 1),
                             resFloatRed[:-1].reshape(-1, 1)), axis=1)
    r = tuple([tuple(line) for line in list(rXY0Y1)])
    gXY0Y1 = np.concatenate((x.reshape(-1, 1), resFloatGreen[:-1].reshape(-1, 1),
                             resFloatGreen[:-1].reshape(-1, 1)), axis=1)
    g = tuple([tuple(line) for line in gXY0Y1])
    bXY0Y1 = np.concatenate((x.reshape(-1, 1), resFloatBlue[:-1].reshape(-1, 1),
                             resFloatBlue[:-1].reshape(-1, 1)), axis=1)
    b = tuple([tuple(line) for line in bXY0Y1])
    cDict = {'red': r, 'green': g, 'blue': b}
    cMap = matplotlib.colors.LinearSegmentedColormap(f"d{N}", cDict)
    matplotlib.colormaps.register(cMap)
