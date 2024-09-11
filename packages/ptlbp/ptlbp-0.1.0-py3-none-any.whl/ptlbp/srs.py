from typing import Tuple, Union
import torch
from .diff_lbp import DiffLBP
from .util import conditional_no_grad
from sklearn.decomposition import PCA
import sys
from pathlib import Path
import tqdm


def hellinger_normalise(features):
    #  return torch.sign(features) * torch.abs(features)**.5
    abs_features = (features ** 2) ** .5
    sign = features / (abs_features + 1e-10)
    return sign * (abs_features ** .5)


def l2_normalise(features, epsilon=1e-10):
    return features/(((torch.sum(features**2, dim=1)**.5)+epsilon)[:, None])


# class DiffSRSLBP(torch.nn.Module):
#     def __init__(self, num_components=200, radii=range(1, 12), supress_zero_pattern=True, supress_full_pattern=True,
#                  block_normalise=True, gradient_on_lbp=True, gradient_on_srs=True, apply_helliger=True, apply_l2=True):
#         super().__init__()
#         radii_modules = []
#         for r in radii:
#             radii_modules.append(DiffLBP(f"8r{r}", supress_zero_pattern=supress_zero_pattern,
#                                          supress_full_pattern=supress_full_pattern,
#                                          block_normalise=block_normalise, comparisson="simple"))
#         self.diff_lbp = torch.nn.ModuleList(radii_modules)
#         if num_components <= 0:
#             self.feature_reduction = None
#         else:
#             self.feature_reduction = torch.nn.Linear(self.histograms_size, num_components, bias=False)

#         # We cant have gradient only on early layers
#         assert (gradient_on_srs and gradient_on_lbp) or not gradient_on_srs
#         self.gradient_on_lbp = gradient_on_lbp
#         self.gradient_on_srs = gradient_on_srs

#         self.apply_helliger = apply_helliger
#         self.apply_l2 = apply_l2

#     def __forward_lbp(self, x):
#         with conditional_no_grad(not self.gradient_on_lbp):
#             x = torch.cat([diff_lbp(x) for diff_lbp in self.diff_lbp], dim=1)
#         return x

#     def __forward_features(self, x):
#         with conditional_no_grad(not self.gradient_on_srs):
#             x = x[:, :, 0, 0]
#             if self.feature_reduction is not None:
#                 x = self.feature_reduction(x)
#             x = x[:, :, None, None]
#             if self.apply_helliger:
#                 x = hellinger_normalise(x)
#             if self.apply_l2:
#                 x = l2_normalise(x)
#         return x

#     def forward(self, x):
#         x = self.__forward_lbp(x)
#         x = self.__forward_features(x)
#         return x

#     def train_pca(self, data):
#         assert self.feature_reduction
#         with torch.no_grad():
#             if isinstance(data, torch.utils.data.DataLoader):
#                 features = []
#                 for sample in data:
#                     features.append(torch.cat([diff_lbp(sample) for diff_lbp in self.diff_lbp], dim=1))
#                 block_normalised_features = torch.cat(features, dim=0)
#             elif isinstance(data, torch.Tensor) and data.dim() == 4:
#                 assert data.size(2) == data.size(3) == 1
#                 block_normalised_features = data[:, :, 0, 0]
#             elif isinstance(data, torch.Tensor) and data.dim() == 2:
#                 block_normalised_features = data
#             else:
#                 raise ValueError(f"Data type {type(data)} or size not supported")

#             device = block_normalised_features.device
#             pca = PCA(n_components=self.num_components)
#             if block_normalised_features.size(0) < self.num_components:
#                 replicates = self.num_components // block_normalised_features.size(0) + 1
#                 new_feature_list = []
#                 for _ in range(replicates):
#                     noise = torch.randn_like(block_normalised_features) * .0000001
#                     new_feature_list.append(block_normalised_features + noise)
#                 block_normalised_features = torch.cat(new_feature_list, dim=0)
#             assert block_normalised_features.size(2) == block_normalised_features.size(3) == 1
#             block_normalised_features = block_normalised_features[:, :, 0, 0]
#             pca.fit(block_normalised_features.cpu().numpy())
#             self.feature_reduction.weight.data = torch.tensor(pca.components_).to(device).float()

#     @property
#     def histograms_size(self):
#         return sum(diff_lbp.histogram_size for diff_lbp in self.diff_lbp)

#     @property
#     def num_components(self):
#         if self.feature_reduction is None:
#             return self.histograms_size
#         else:
#             return self.feature_reduction.out_features


class MultiRadiusDiffLBP(torch.nn.Module):
    def embbed_dataset(self, ds, resume_path, device=None, save_freq=1000, progress=True):
        if device is not None:
            self.to(device)
        embeders = self.diff_lbp
        features_labels_filenames = []
        processed_ids = {}
        if Path(resume_path).exists():
            try:
                features_labels_filenames = torch.load(resume_path)
                processed_ids = {id: (feats, label, id) for (feats, label, id) in features_labels_filenames}
                print(f"Resumed {len(processed_ids)} from {resume_path}", file=sys.stderr)
            except Exception:
                print(f"Error loading {resume_path}", file=sys.stderr)
                features_labels_filenames = []
                processed_ids = {}
        ds_ids = ds.get_ids().tolist()
        remaining_indexes = [n for n in range(len(ds_ids)) if ds_ids[n] not in processed_ids]

        with torch.no_grad():
            if progress:
                remaining_indexes = tqdm.tqdm(remaining_indexes)
            for n in remaining_indexes:
                img, label, img_path = ds[n]
                if img.dim() == 3:
                    img = img[None, :, :, :]
                elif img.dim() == 2:
                    img = img[None, None, :, :]
                elif img.dim() == 4:
                    pass
                else:
                    raise ValueError(f"Invalid image shape {img.shape}")
                img = img.to(device)
                try:
                    features = []
                    for embeder in embeders:
                        features.append(embeder.forward_sliced(img, 200).detach().cpu()[0, :, 0, 0])
                    features = torch.cat(features, dim=0)
                    features_labels_filenames.append((features, label, img_path))
                except Exception:
                    print(f"Error in embedding {img_path}", file=sys.stderr)
                if n % save_freq == 0:
                    torch.save(features_labels_filenames, resume_path)
            torch.save(features_labels_filenames, resume_path)

    def __init__(self, radii, offset_pattern="8r{}", **kwargs):
        super().__init__()
        if "pooling" in kwargs:
            if kwargs["pooling"] is None or kwargs["pooling"] is False:
                raise ValueError("A MultiRadiusDiffLBP needs an effective pooling strategy.")
        radii_modules = []
        for radius in radii:
            radii_modules.append(DiffLBP(offsets=offset_pattern.format(radius), **kwargs))
        self.diff_lbp = torch.nn.ModuleList(radii_modules)

    def forward(self, x):
        return torch.cat([diff_lbp(x) for diff_lbp in self.diff_lbp], dim=1)

    def forward_sliced(self, x, col_width=200):
        with torch.no_grad():
            return torch.cat([diff_lbp.forward_sliced(x, col_width) for diff_lbp in self.diff_lbp], dim=1)

    def compute_lbp_stack(self, img, return_confidences=False, output_device='cpu')\
            -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        by_radius = [lbp.compute_lbp_image(img, return_confidences=return_confidences) for lbp in self.diff_lbp]
        if return_confidences:
            by_radius = [(lbp_img.to(output_device), conf.to(output_device)) for lbp_img, conf in by_radius]
            lbp_stack = torch.cat([lbp_img for lbp_img, _ in by_radius], dim=1)
            conf_stack = torch.cat([conf for _, conf in by_radius], dim=1)
            return lbp_stack, conf_stack
        else:
            by_radius = [lbp_img.to(output_device) for lbp_img in by_radius]
            lbp_stack = torch.cat(by_radius, dim=1)
            return lbp_stack

    @property
    def radii_count(self) -> int:
        return len(self.diff_lbp)

    @property
    def histograms_size(self):
        return sum(diff_lbp.histogram_size for diff_lbp in self.diff_lbp)

    @property
    def device(self):
        return next(self.parameters()).device


class DropConnect(torch.nn.Module):
    def __init__(self, p=0.1):
        super(DropConnect, self).__init__()
        self.p = p

    def forward(self, x):
        if self.training:
            mask = torch.rand((x.size(0), 1), device=x.device) > self.p
            return x * mask
        return x


class CompressionLayer(torch.nn.Module):
    def __init__(self, input_size, output_size, hellinger_normalise=False,
                 l2_normalise=False, in_dropout=0.0, out_dropconnect=0.0):
        super().__init__()
        self.in_do = torch.nn.Dropout(in_dropout)
        self.fc1 = torch.nn.Linear(input_size, output_size)
        self.out_do = DropConnect(out_dropconnect)
        self.hellinger_normalise = hellinger_normalise
        self.l2_normalise = l2_normalise
        self.eval()

    def forward(self, x):
        x = self.in_do(x)
        x = self.fc1(x)
        x = self.out_do(x)
        if self.hellinger_normalise:
            x = hellinger_normalise(x)
        if self.l2_normalise:
            x = l2_normalise(x)
        return x

    def train_pca(self, x):
        with torch.no_grad():
            sklearn_pca = PCA(n_components=self.fc1.weight.shape[0])
            count = 0
            # replicating sample + noise to avoid singular matrix
            # maybe getting the number of samples from the number of features is a better idea
            while x.shape[0] < self.fc1.weight.shape[1] and count < 5:
                x = torch.cat([x, x + .0000001 * torch.rand_like(x) * .5], dim=0)
            sklearn_pca.fit(x.cpu().detach().numpy())
            self.fc1.weight.data[:, :] = torch.tensor(sklearn_pca.components_).to(self.fc1.weight.device)
            print("PCA training done!", file=sys.stderr)


class DeepCompressionLayer(torch.nn.Module):
    def __init__(self, input_size, output_size, hellinger_normalise=False,
                 l2_normalise=False, in_dropout=0.0, out_dropconnect=0.0):
        super().__init__()
        self.in_do = torch.nn.Dropout(in_dropout)
        self.fc1 = torch.nn.Linear(input_size, output_size)
        self.fc2 = torch.nn.Linear(output_size, output_size)
        self.fc3 = torch.nn.Linear(output_size, output_size)
        self.out_do = DropConnect(out_dropconnect)
        self.hellinger_normalise = hellinger_normalise
        self.l2_normalise = l2_normalise
        self.eval()

    def forward(self, x):
        x = self.in_do(x)
        x = torch.tanh(self.fc1(x))
        x = self.in_do(x)
        x = torch.tanh(self.fc2(x))
        x = self.in_do(x)
        x = self.fc3(x)
        x = self.out_do(x)
        if self.hellinger_normalise:
            x = hellinger_normalise(x)
        if self.l2_normalise:
            x = l2_normalise(x)
        return x

    def train_pca(self, x):
        raise NotImplementedError("Not implemented for DeepCompressionLayer")
        with torch.no_grad():
            sklearn_pca = PCA(n_components=self.fc1.weight.shape[0])
            count = 0
            # replicating sample + noise to avoid singular matrix
            # maybe getting the number of samples from the number of features is a better idea
            while x.shape[0] < self.fc1.weight.shape[1] and count < 5:
                x = torch.cat([x, x + .0000001 * torch.rand_like(x) * .5], dim=0)
            sklearn_pca.fit(x.cpu().detach().numpy())
            self.fc1.weight.data[:, :] = torch.tensor(sklearn_pca.components_).to(self.fc1.weight.device)
            print("PCA training done!", file=sys.stderr)


class HighwayBlock(torch.nn.Module):
    def __init__(self, size, dropout_rate, activation_function=torch.nn.Tanh(), init_bias=-2.0, batch_norm=True):
        super(HighwayBlock, self).__init__()
        self.size = size
        self.activation_function = activation_function
        self.H = torch.nn.Linear(size, size)
        self.T = torch.nn.Linear(size, size)
        self.T.bias.data.fill_(init_bias)
        self.dropout = torch.nn.Dropout(dropout_rate)
        self.batch_norm = torch.nn.BatchNorm1d(size) if batch_norm else None

    def forward(self, x):
        H_out = self.activation_function(self.H(x))
        H_out = self.dropout(H_out)
        T_out = torch.sigmoid(self.T(x))
        if self.batch_norm:
            H_out = self.batch_norm(H_out)
        C_out = 1 - T_out
        return H_out * T_out + x * C_out


class DeepResCompressionLayer(torch.nn.Module):
    def __init__(self, input_size, output_size, depth=5, hellinger_normalise=False,
                 l2_normalise=False, in_dropout=0.0, out_dropconnect=0.0, init_highway_bias=-2.0):
        super().__init__()
        self.in_do = torch.nn.Dropout(in_dropout)
        self.fc1 = torch.nn.Linear(input_size, output_size)
        highway_blocks = [HighwayBlock(output_size, in_dropout, init_bias=init_highway_bias) for _ in range(depth)]
        self.highway_blocks = torch.nn.Sequential(*highway_blocks)

        self.out_do = DropConnect(out_dropconnect)
        self.hellinger_normalise = hellinger_normalise
        self.l2_normalise = l2_normalise
        self.eval()

    def forward(self, x):
        x = self.in_do(torch.tanh(self.fc1(x)))
        x = self.highway_blocks(x)
        x = self.out_do(x)
        if self.hellinger_normalise:
            x = hellinger_normalise(x)
        if self.l2_normalise:
            x = l2_normalise(x)
        return x

    def train_pca(self, x):
        raise NotImplementedError("Not implemented for DeepCompressionLayer")


class DiffSRSLBP(torch.nn.Module):
    def __init__(self, radii=list(range(1, 12)), num_components=200, **kwargs) -> None:
        super().__init__()
        self.multi_radius_diff_lbp = MultiRadiusDiffLBP(radii, **kwargs)
        self.compression_layer = CompressionLayer(self.multi_radius_diff_lbp.histograms_size, num_components)
        self.eval()

    def forward(self, x):
        x = self.multi_radius_diff_lbp(x)
        x = self.compression_layer(x)
        return x

    def train_pca(self, data):
        self.compression_layer.train_pca(data)
