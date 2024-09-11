#!/usr/bin/env python

from PIL import Image
import os
import os.path
import errno
import torch
from io import BytesIO
from torchvision import transforms
import glob
from pathlib import Path
import numpy as np
from collections import defaultdict
import sys
from typing import Tuple, Dict, List, Set
from abc import ABC, abstractmethod
from numpy.random import MT19937, RandomState, SeedSequence
import zipfile
import rarfile
import py7zr
import torchvision
from subprocess import getoutput as shell_stdout
import os


transform_384_train = transforms.Compose([
    transforms.RandomCrop((1024, 384), padding=1, pad_if_needed=True),
    transforms.Resize((512, 192)),
    transforms.Grayscale(),
    transforms.ToTensor(),
])

transform_test = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])


def read_rar_file(rarstream):
    names = rarstream.namelist()
    sample_list = []
    for name in names:
        img = Image.open(BytesIO(rarstream.read(rarstream.getinfo(name)))).copy()
        [writer_id, sample_id] = [int(s) for s in name[:name.find(".")].split("_")]
        language_id = (sample_id-1) / 2  # icdar 2013: english 1,2 and greek 3,4
        sample_list.append((img, (writer_id, language_id, sample_id), name))
    return sample_list


class TextureDs(ABC):
    @abstractmethod
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int, str]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def get_labels(self) -> np.array:
        """Returns the labels (int classes) of each item in the dataset as a numpy array."""
        pass

    @abstractmethod
    def get_ids(self) -> np.array:
        """Returns the string identifiers of each item in the dataset as a numpy array."""
        pass

    def get_ids_to_indexes(self) -> Dict[str, int]:
        return {id: n for n, id in enumerate(self.get_ids())}

    def get_indexes_by_labels(self) -> Dict[int, List[int]]:
        res = defaultdict(lambda: [])
        for n, label in enumerate(self.get_labels()):
            res[label].append(n)
        return res

    def get_unique_labels(self) -> Set[str]:
        return set(self.get_indexes_by_labels().keys())


class TextureSubsetDs(TextureDs):
    def __init__(self, ds: TextureDs, indexes: List[int]):
        self.ds = ds
        self.item_indexes = np.array(indexes)

    def get_ids(self) -> np.array:
        return self.ds.get_ids()[self.item_indexes]

    def get_labels(self) -> np.array:
        return self.ds.get_labels()[self.item_indexes]

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int, str]:
        return self.ds[self.item_indexes[index]]

    def __len__(self) -> int:
        return self.item_indexes.size


class GenericTextureDs(TextureDs):
    def __init__(self, items: List[Tuple[torch.Tensor, int, str]], return_dims: int = 3) -> None:
        super().__init__()
        self.labels = np.array([label for _, label, _ in items])
        self.ids = np.array([id for _, _, id in items])
        if return_dims == 4:
            if items[0][0].dim() == 4:  # assuming batch of images
                self.inputs = [input for input, _, _ in items]
            elif items[0][0].dim() == 3:  # assuming image sample
                self.inputs = [input[None, :, None, None] for input, _, _ in items]
            elif items[0][0].dim() == 2:  # assuming batch of embeddings
                self.inputs = [input[:, :, None, None] for input, _, _ in items]
            elif items[0][0].dim() == 1:
                self.inputs = [input[None, :, None, None] for input, _, _ in items]
            else:
                raise ValueError(f"Invalid input dimension {items[0][0].dim()}")
        elif return_dims == 3:  # assuming image sample
            if items[0][0].dim() == 4:  # assuming batch of images
                if not all(input.size(0) == 1 for input, _, _ in items):
                    raise ValueError("Invalid batch size")
                self.inputs = [input[0] for input, _, _ in items]
            elif items[0][0].dim() == 3:  # assuming image sample
                self.inputs = [input for input, _, _ in items]
            elif items[0][0].dim() == 2:  # assuming batch of embeddings
                if not all(input.size(0) == 1 for input, _, _ in items):
                    raise ValueError("Invalid batch size")
                self.inputs = [input[0, :, None, None] for input, _, _ in items]
            elif items[0][0].dim() == 1:
                self.inputs = [input[None, :, None, None] for input, _, _ in items]
            else:
                raise ValueError(f"Invalid input dimension {items[0][0].dim()}")
        elif return_dims == 2:  # assuming embeddings
            if items[0][0].dim() == 4:
                if not all(input.size(1) == 1 and input.size(2) == 1 for input, _, _ in items):
                    raise ValueError("Invalid batch size")
                self.inputs = [input[:, :, 0, 0] for input, _, _ in items]
            elif items[0][0].dim() == 3:
                if not all(input.size(1) == 1 and input.size(2) == 1 for input, _, _ in items):
                    raise ValueError("Invalid batch size")
                self.inputs = [input[None, :, 0, 0] for input, _, _ in items]
            elif items[0][0].dim() == 2:
                self.inputs = [input for input, _, _ in items]
            elif items[0][0].dim() == 1:
                self.inputs = [input[None, :] for input, _, _ in items]
            else:
                raise ValueError(f"Invalid input dimension {items[0][0].dim()}")
        elif return_dims == 1:
            if items[0][0].dim() == 1:
                self.inputs = [input for input, _, _ in items]
            elif items[0][0].dim() == 2:
                self.inputs = [input[0, :] for input, _, _ in items]
            elif items[0][0].dim() == 3:
                if items[0][0].size(0) == 1:
                    print("Warning: single channel image should not be treated as an embedding", file=sys.stderr)
                if not all(input.size(1) == 1 and input.size(2) == 1 for input, _, _ in items):
                    raise ValueError("Invalid batch size")
                self.inputs = [input[:, 0, 0] for input, _, _ in items]
            elif items[0][0].dim() == 4:
                if items[0][0].size(1) == 1:
                    print("Warning: single channel image should not be treated as an embedding", file=sys.stderr)
                if not all(input.size(2) == 1 and input.size(3) == 1 and input.size(0) == 1 for input, _, _ in items):
                    raise ValueError("Invalid batch size")
                self.inputs = [input[0, :, 0, 0] for input, _, _ in items]
            else:
                raise ValueError(f"Invalid input dimension {items[0][0].dim()}")
        self.return_dims = return_dims

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int, str]:
        return self.inputs[index], self.labels[index], self.ids[index]

    def __len__(self) -> int:
        return len(self.inputs)

    def get_labels(self) -> np.array:
        return self.labels

    def get_ids(self) -> np.array:
        return self.ids


def split_by_labels(ds: TextureDs, label_counts: List[int], seed=-1) -> List[TextureSubsetDs]:
    unique_labels = np.array(list(ds.get_unique_labels()))
    if seed >= 0:
        rs = RandomState(MT19937(SeedSequence(seed)))
        unique_labels = rs.permutation(unique_labels)
    else:
        unique_labels = np.random.permutation(unique_labels)
    indexes_by_labels = ds.get_indexes_by_labels()
    datasets = []
    for label_count in label_counts:
        if label_count == -1:
            return_unique_labels = unique_labels
        else:
            return_unique_labels = unique_labels[:label_count]
            unique_labels = unique_labels[label_count:]
        result_indexes = []
        for label in return_unique_labels:
            result_indexes.extend(indexes_by_labels[label])
        datasets.append(TextureSubsetDs(ds, result_indexes))
    return datasets


class WI2017(TextureDs):
    def __init__(self, ds_root, img_folder="ScriptNet-HistoricalWI-2017-color", transform=None) -> None:
        super().__init__()
        self.transform = transform
        if transform is None:
            transform = transform_test
        self.ids = []
        self.labels = []
        for path in glob.glob(f"{ds_root}/{img_folder}/*.jpg"):
            name = path.split("/")[-1]
            self.ids.append(name)
            self.labels.append(int(name.split("-")[0]))
        print(f"WI2017 Loading {len(self.ids)} samples.", file=sys.stderr)
        self.labels = np.array(self.labels)
        self.ids = np.array(self.ids)
        self.root = ds_root
        self.image_path_pattern = f"{ds_root}/{img_folder}/{{}}"
        self.transform = transform

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int, str]:
        img = Image.open(self.image_path_pattern.format(self.ids[index]))
        img = self.transform(img)
        return img, self.labels[index], self.ids[index]

    def __len__(self) -> int:
        return len(self.ids)

    def get_ids(self) -> np.array:
        return self.ids.copy()

    def get_labels(self) -> np.array:
        return self.labels.copy()


class WI2019(TextureDs):
    def __init__(self, ds_root, train_saples_folder="wi_comp_19_validation",
                 train_labels_csv="wi_comp_19val_ground_truth.csv",
                 test_saples_folder="wi_comp_19_test",
                 test_labels_csv="wi_comp19_test_ground_truth.csv",
                 validation=False, split_images=[1, 1], transform=None) -> None:
        super().__init__()
        if transform is None:
            transform = transform_test
        if validation:
            csv_path = f"{ds_root}/{train_labels_csv}"
            image_folder = train_saples_folder
        else:
            csv_path = f"{ds_root}/{test_labels_csv}"
            image_folder = test_saples_folder
        self.transform = transform
        self.ids = []
        self.labels = []
        self.img_split = split_images
        self.split_count = split_images[0] * split_images[1]
        for line in open(csv_path, "r").readlines():
            line = line.strip()
            if line != "" and line[:4] != "FILE":
                fname, label = line.split(",")[:2]
                for _ in range(self.split_count):
                    self.ids.append(fname)
                    self.labels.append(int(label))
        self.labels = np.array(self.labels)
        self.ids = np.array(self.ids)
        self.root = ds_root
        self.image_path_pattern = f"{ds_root}/{image_folder}/{{}}"

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int, str]:
        img = Image.open(self.image_path_pattern.format(self.ids[index]))
        img = self.transform(img)
        if self.split_count > 1:
            partition = index % self.split_count
            h_partition = partition % self.img_split[0]
            v_partion = partition // self.img_split[0]
            left = h_partition * img.size(2) // self.img_split[0]
            right = (h_partition + 1) * img.size(2) // self.img_split[0]
            top = v_partion * img.size(1) // self.img_split[1]
            bottom = (v_partion + 1) * img.size(1) // self.img_split[1]
            img = img[:, top:bottom, left:right]
        return img, self.labels[index], self.ids[index]

    def __len__(self) -> int:
        return len(self.ids)

    def get_ids(self) -> np.array:
        return self.ids.copy()

    def get_labels(self) -> np.array:
        return self.labels.copy()


class WI2013(TextureDs):
    """Contemporary Writer identification dataset


    Citation: http://users.iit.demokritos.gr/~bgat/ICDAR_2013_Louloudis.pdf
    """
    urls = [
        'http://users.iit.demokritos.gr/~louloud/ICDAR2013WriterIdentificationComp/experimental_dataset_2013.rar',
        'http://users.iit.demokritos.gr/~louloud/ICDAR2013WriterIdentificationComp/icdar2013_benchmarking_dataset.rar'
    ]
    raw_folder = 'raw'
    processed_folder = 'processed'
    training_file = 'training.pt'
    test_file = 'test.pt'

    def __init__(self, root="tmp/wi2013", train=True, transform=transform_test, target_transform=None, download=False,
                 output_class="writer"):
        """Instanciates a pytorch dataset.

        :param root: The directory were everything is stored.
        :param train: Boolean, selects the data-partion and the default preprocessing
        :param transform: Image preprocessing use wi2013.transform_384_train for images of 512x192 obtained by cropping
                randomly and than scaling by 0.5, or wi2013.transform_test for variable sized images.
        :param target_transform: Ground truth preprocessing
        :param download: must be true for the data to download if missing
        :param output_class: This dataset supports different classes "writer":0-99,"sample":0-3 ,"script":0-1
        """
        assert output_class in ("writer", "sample", "script")
        if transform is None:
            if train:
                transform = transform_384_train
            else:
                transform = transform_test
        self.output_select = {"writer": lambda x: (x[0], x[1][0]-1, x[2]),
                              "sample": lambda x: (x[0], x[1][1]-1, x[2]),
                              "script": lambda x: (x[0], x[1][0]-1, x[2])}[output_class]
        self.root = os.path.expanduser(root)
        self.transform = transform
        self.target_transform = target_transform
        self.train = train  # training set or test set

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found.' +
                               ' You can use download=True to download it')

        if self.train:
            self.train_samples = torch.load(
                os.path.join(self.root, self.processed_folder, self.training_file))
        else:
            self.test_samples = torch.load(
                os.path.join(self.root, self.processed_folder, self.test_file))
        if self.train:
            items = self.train_samples
        else:
            items = self.test_samples
        print(f"Loading data: {len(items[0])}")
        img_label_id = [self.output_select(item) for item in items]
        self.labels = np.array([label for _, label, _ in img_label_id])
        self.ids = np.array([id for _, _, id in img_label_id])
        # sorting samples by filename
        id_idx = np.argsort(self.ids)
        self.labels = self.labels[id_idx]
        self.ids = self.ids[id_idx]
        if self.train:
            self.train_samples = [self.train_samples[idx] for idx in id_idx]
        else:
            self.test_samples = [self.test_samples[idx] for idx in id_idx]

    def __getitem__(self, index) -> Tuple[torch.Tensor, int, str]:
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        if self.train:
            img, label, id = self.output_select(self.train_samples[index])
            label = label - 26
        else:
            img, label, id = self.output_select(self.test_samples[index])

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = img  # .fromarray(img.numpy(), mode='L')

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            label = self.target_transform(label)

        return img, label, id

    def __len__(self):
        if self.train:
            return len(self.train_samples)
        else:
            return len(self.test_samples)

    def get_labels(self) -> np.array:
        return self.labels

    def get_ids(self) -> np.array:
        return self.ids

    def _check_exists(self):
        return os.path.exists(os.path.join(self.root, self.processed_folder, self.training_file)) and \
            os.path.exists(os.path.join(self.root, self.processed_folder, self.test_file))

    def download(self):
        """Download the rar files data if it doesn't exist in processed_folder already."""
        import urllib
        import rarfile

        if self._check_exists():
            return

        # download files
        try:
            os.makedirs(os.path.join(self.root, self.raw_folder))
            os.makedirs(os.path.join(self.root, self.processed_folder))
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        for url in self.urls:
            print('Downloading ' + url)
            stream = urllib.request.urlopen(url)
            filename = url.rpartition('/')[-1]
            file_path = os.path.join(self.root, self.raw_folder, filename)
            with open(file_path, 'wb') as f:
                f.write(stream.read())
            with rarfile.RarFile(file_path) as rar_f:
                rar_f.extractall(self.raw_folder)
            # os.unlink(file_path)

        # process and save as torch files
        print('Processing...')
        train_set = read_rar_file(rarfile.RarFile(os.path.join(self.root, self.raw_folder,
                                                               'experimental_dataset_2013.rar')))
        test_set = read_rar_file(
            rarfile.RarFile(os.path.join(self.root, self.raw_folder, 'icdar2013_benchmarking_dataset.rar')))
        with open(os.path.join(self.root, self.processed_folder, self.training_file), 'wb') as f:
            torch.save(train_set, f)
        with open(os.path.join(self.root, self.processed_folder, self.test_file), 'wb') as f:
            torch.save(test_set, f)
        print('Done!')

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of datapoints: {}\n'.format(self.__len__())
        tmp = 'train' if self.train is True else 'test'
        fmt_str += '    Split: {}\n'.format(tmp)
        fmt_str += '    Root Location: {}\n'.format(self.root)
        tmp = '    Transforms (if any): '
        fmt_str += '{0}{1}\n'.format(tmp, self.transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        tmp = '    Target Transforms (if any): '
        fmt_str += '{0}{1}'.format(tmp, self.target_transform.__repr__().replace('\n', '\n' + ' ' * len(tmp)))
        return fmt_str


hisfrag_transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])


class HisFrag20():
    def __init__(self, img_dir, transform=hisfrag_transform, return_writers=True):
        self.image_paths = list(sorted(glob.glob(f"{img_dir}/*.jpg")))
        if len(self.image_paths) == 0:
            raise FileNotFoundError(f"No images found in {img_dir}")
        self.transform = transform
        if return_writers:
            idx = 0
        else:
            idx = 1
        self.labels = np.array([int(Path(img).stem.split('_')[idx]) for img in self.image_paths])
        self.ids = np.array([img_path for img_path in self.image_paths])
        self.unique_labels, self.unique_labels_count = np.unique(self.labels, return_counts=True)
        self.by_label = defaultdict(lambda: [])
        for label, path in zip(self.labels, self.image_paths):
            self.by_label[label].append(path)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, int, str]:
        img = Image.open(self.image_paths[index])
        return self.transform(img), self.labels[index], self.image_paths[index]

    def __len__(self):
        return len(self.image_paths)

    def get_ids(self):
        return self.ids

    def get_labels(self):
        return self.labels


def _warn(*args):
    sys.stderr.write(" ".join([str(arg) for arg in args])+"\n")


def _get_dict(compressed_stream, filter_gt=False, filter_nongt=False):
    assert not (filter_gt and filter_nongt)

    def isimage(x) -> bool:
        return x.split(".")[-1].lower() in ["tiff", "bmp", "jpg", "tif", "jpeg", "png"] and "skel" not in x.lower()

    def isgt(x) -> bool:
        return isimage(x) and ("gt" in x or "GT" in x)

    if isinstance(compressed_stream, py7zr.SevenZipFile):
        compressed_stream.reset()
        res_dict = compressed_stream.readall()
        names = res_dict.keys()
        if filter_gt:
            names = [n for n in names if not isgt(n)]
        if filter_nongt:
            names = [n for n in names if isgt(n)]
        return {name: res_dict[name] for name in names}
    elif isinstance(compressed_stream, rarfile.RarFile) or isinstance(compressed_stream, zipfile.ZipFile):
        names = compressed_stream.namelist()
        names = [n for n in names if isimage(n)]
        if filter_gt:
            names = [n for n in names if not isgt(n)]
        if filter_nongt:
            names = [n for n in names if isgt(n)]
        return {name: BytesIO(compressed_stream.read(compressed_stream.getinfo(name))) for name in names}
    else:
        raise ValueError("Filedescriptor must be one of [rar, zip, 7z]")


def _extract(archive, root=None) -> None:
    if archive.endswith(".tar.gz"):
        if root is None:
            cmd = "tar -xpvzf {}".format(archive)
        else:
            cmd = 'mkdir -p {};tar -xpvzf {} -C{}'.format(root, archive, root)
        _ = shell_stdout(cmd)
    else:
        raise NotImplementedError()


def _check_os_dependencies() -> bool:
    program_list = ["wget"]
    return all([shell_stdout("which "+prog) for prog in program_list])


def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _resumable_download(url, save_dir):
    _mkdir_p(save_dir)
    download_cmd = 'wget --directory-prefix=%s -c %s' % (save_dir, url)
    _warn("Downloading {} ... ".format(url))
    shell_stdout(download_cmd)
    _warn("done")
    return os.path.join(save_dir, url.split("/")[-1])


dibco_transform_gray_input = torchvision.transforms.Compose([
    torchvision.transforms.Grayscale(),
    torchvision.transforms.ToTensor(),
])

dibco_transform_color_input = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor(),
])

dibco_transform_gt = torchvision.transforms.Compose([
    torchvision.transforms.Grayscale(),
    torchvision.transforms.ToTensor(),
])


class Dibco:
    """Provides one or more of the `DIBCO <https://vc.ee.duth.gr/dibco2019/>` datasets.

    Os dependencies: Other than python packages, unrar and arepack CLI tools must be installed.
    In Ubuntu they can be installed with: sudo apt install unrar atool p7zip-full
    In order to concatenate two DIBCO datasets just add them:
    .. source :: python

        trainset = dibco.Dibco.Dibco2009() + dibco.Dibco.Dibco2013()
        valset = dibco.Dibco.Dibco2017() + dibco.Dibco.Dibco209()

    Each item is a tuple of an RGB PIL image and an Binary PIL image. The images are transformed by ``input_transform``
    and ``gt_transform``.
    """
    urls = {
        "2009_HW": ["https://users.iit.demokritos.gr/~bgat/DIBCO2009/benchmark/DIBC02009_Test_images-handwritten.rar",
                    "https://users.iit.demokritos.gr/~bgat/DIBCO2009/benchmark/DIBCO2009-GT-"
                    "Test-images_handwritten.rar"],

        "2009_P": ["https://users.iit.demokritos.gr/~bgat/DIBCO2009/benchmark/DIBCO2009_Test_images-printed.rar",
                   "https://users.iit.demokritos.gr/~bgat/DIBCO2009/benchmark/DIBCO2009-GT-Test-images_printed.rar"],

        "2010": ["http://users.iit.demokritos.gr/~bgat/H-DIBCO2010/benchmark/H_DIBCO2010_test_images.rar",
                 "http://users.iit.demokritos.gr/~bgat/H-DIBCO2010/benchmark/H_DIBCO2010_GT.rar"],

        "2011_P": ["http://utopia.duth.gr/~ipratika/DIBCO2011/benchmark/dataset/DIBCO11-machine_printed.rar"],
        "2011_HW": ["http://utopia.duth.gr/~ipratika/DIBCO2011/benchmark/dataset/DIBCO11-handwritten.rar"],

        "2012": ["http://utopia.duth.gr/~ipratika/HDIBCO2012/benchmark/dataset/H-DIBCO2012-dataset.rar"],

        "2013": ["http://utopia.duth.gr/~ipratika/DIBCO2013/benchmark/dataset/DIBCO2013-dataset.rar"],

        "2014": ["http://users.iit.demokritos.gr/~bgat/HDIBCO2014/benchmark/dataset/original_images.rar",
                 "http://users.iit.demokritos.gr/~bgat/HDIBCO2014/benchmark/dataset/GT.rar"],
        "2016": ["https://vc.ee.duth.gr/h-dibco2016/benchmark/DIBCO2016_dataset-original.zip",
                 "https://vc.ee.duth.gr/h-dibco2016/benchmark/DIBCO2016_dataset-GT.zip"],
        "2017": ["https://vc.ee.duth.gr/dibco2017/benchmark/DIBCO2017_Dataset.7z",
                 "https://vc.ee.duth.gr/dibco2017/benchmark/DIBCO2017_GT.7z"],
        "2018": ["http://vc.ee.duth.gr/h-dibco2018/benchmark/dibco2018_Dataset.zip",
                 "http://vc.ee.duth.gr/h-dibco2018/benchmark/dibco2018-GT.zip"],
        "2019A": ["https://vc.ee.duth.gr/dibco2019/benchmark/dibco2019_dataset_trackA.zip",
                  "https://vc.ee.duth.gr/dibco2019/benchmark/dibco2019_gt_trackA.zip"],
        "2019B": ["https://vc.ee.duth.gr/dibco2019/benchmark/dibco2019_dataset_trackB.zip",
                  "https://vc.ee.duth.gr/dibco2019/benchmark/dibco2019_GT_trackB.zip"]
    }

    # urls = {
    #     "2009_HW": ["http://rr.visioner.ca/assets/dibco_mirror/DIBC02009_Test_images-handwritten.rar",
    #                 "http://rr.visioner.ca/assets/dibco_mirror/DIBCO2009-GT-Test-images_handwritten.rar"],
    #     "2009_P": ["http://rr.visioner.ca/assets/dibco_mirror/DIBCO2009_Test_images-printed.rar",
    #                "http://rr.visioner.ca/assets/dibco_mirror/DIBCO2009-GT-Test-images_printed.rar"],
    #     "2010": ["http://rr.visioner.ca/assets/dibco_mirror/H_DIBCO2010_test_images.rar",
    #              "http://rr.visioner.ca/assets/dibco_mirror/H_DIBCO2010_GT.rar"],
    #     "2011_P": ["http://rr.visioner.ca/assets/dibco_mirror/DIBCO11-machine_printed.rar"],
    #     "2011_HW": ["http://rr.visioner.ca/assets/dibco_mirror/DIBCO11-handwritten.rar"],
    #     "2012": ["http://rr.visioner.ca/assets/dibco_mirror/H-DIBCO2012-dataset.rar"],
    #     "2013": ["http://rr.visioner.ca/assets/dibco_mirror/DIBCO2013-dataset.rar"],
    #     "2014": ["http://rr.visioner.ca/assets/dibco_mirror/original_images.rar",
    #              "http://rr.visioner.ca/assets/dibco_mirror/GT.rar"],
    #     "2016": ["http://rr.visioner.ca/assets/dibco_mirror/DIBCO2016_dataset-original.zip",
    #              "http://rr.visioner.ca/assets/dibco_mirror/DIBCO2016_dataset-GT.zip"],
    #     "2017": ["http://rr.visioner.ca/assets/dibco_mirror/DIBCO2017_Dataset.7z",
    #              "http://rr.visioner.ca/assets/dibco_mirror/DIBCO2017_GT.7z"],
    #     "2018": ["http://rr.visioner.ca/assets/dibco_mirror/dibco2018_Dataset.zip",
    #              "http://rr.visioner.ca/assets/dibco_mirror/dibco2018-GT.zip"],
    #     "2019A": ["http://rr.visioner.ca/assets/dibco_mirror/dibco2019_dataset_trackA.zip",
    #               "http://rr.visioner.ca/assets/dibco_mirror/dibco2019_gt_trackA.zip"],
    #     "2019B": ["http://rr.visioner.ca/assets/dibco_mirror/dibco2019_dataset_trackB.zip",
    #               "http://rr.visioner.ca/assets/dibco_mirror/dibco2019_GT_trackB.zip"]
    # }

    @staticmethod
    def load_single_stream(compressed_stream):
        inname2bs = _get_dict(compressed_stream, filter_gt=True)
        gtname2bs = _get_dict(compressed_stream, filter_nongt=True)
        id2gt = {n.split("/")[-1].split("_")[0].split(".")[0]: Image.open(fd).copy() for n, fd in gtname2bs.items()}
        id2in = {n.split("/")[-1].split("_")[0].split(".")[0]: Image.open(fd).copy() for n, fd in inname2bs.items()}
        assert set(id2gt.keys()) == set(id2in.keys())
        id2in = {k: v.convert("RGB") for k, v in id2in.items()}
        return {k: (id2in[k], id2gt[k]) for k in id2gt.keys()}

    @staticmethod
    def load_double_stream(input_compressed_stream, gt_compressed_stream):
        inname2bs = _get_dict(input_compressed_stream)
        gtname2bs = _get_dict(gt_compressed_stream)
        id2in = {n.split("/")[-1].split("_")[0].split(".")[0]: Image.open(fd).copy() for n, fd in inname2bs.items()}
        id2gt = {n.split("/")[-1].split("_")[0].split(".")[0]: Image.open(fd).copy() for n, fd in gtname2bs.items()}
        assert set(id2gt.keys()) == set(id2in.keys())
        id2in = {k: v.convert("RGB") for k, v in id2in.items()}
        return {k: (id2in[k], id2gt[k]) for k in id2gt.keys()}

    @staticmethod
    def Dibco2009(**kwargs):
        kwargs["partitions"] = ["2009_HW", "2009_P"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2010(**kwargs):
        kwargs["partitions"] = ["2010"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2011(**kwargs):
        kwargs["partitions"] = ["2011_P", "2011_HW"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2012(**kwargs):
        kwargs["partitions"] = ["2012"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2013(**kwargs):
        kwargs["partitions"] = ["2013"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2014(**kwargs):
        kwargs["partitions"] = ["2014"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2016(**kwargs):
        kwargs["partitions"] = ["2016"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2017(**kwargs):
        kwargs["partitions"] = ["2017"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2018(**kwargs):
        kwargs["partitions"] = ["2018"]
        return Dibco(**kwargs)

    @staticmethod
    def Dibco2019(**kwargs):
        kwargs["partitions"] = ["2019A", "2019B"]
        return Dibco(**kwargs)

    def __init__(self, partitions=["2009_HW", "2009_P"], root="./tmp/dibco",
                 input_transform=dibco_transform_gray_input, gt_transform=dibco_transform_gt, add_mask=False):
        self.input_transform = input_transform
        self.gt_transform = gt_transform
        self.root = root
        self.add_mask = add_mask
        data = {}
        for partition in partitions:
            for url in Dibco.urls[partition]:
                archive_fname = root + "/" + url.split("/")[-1]
                if not os.path.isfile(archive_fname):
                    _resumable_download(url, root)
                else:
                    _warn(archive_fname, " found in cache.")
            if len(Dibco.urls[partition]) == 2:
                if Dibco.urls[partition][0].endswith(".rar"):
                    input_rar = rarfile.RarFile(root + "/" + Dibco.urls[partition][0].split("/")[-1])
                    gt_rar = rarfile.RarFile(root + "/" + Dibco.urls[partition][1].split("/")[-1])
                    samples = {partition + "/" + k: v for k, v in Dibco.load_double_stream(input_rar, gt_rar).items()}
                    data.update(samples)
                elif Dibco.urls[partition][0].endswith(".zip") or Dibco.urls[partition][0].endswith(".7z"):
                    zip_input_fname = root + "/" + Dibco.urls[partition][0].split("/")[-1]
                    zip_gt_fname = root + "/" + Dibco.urls[partition][1].split("/")[-1]
                    if zip_input_fname.endswith("7z"):
                        input_zip = py7zr.SevenZipFile(zip_input_fname)
                    else:
                        input_zip = zipfile.ZipFile(zip_input_fname)
                    if zip_gt_fname.endswith("7z"):
                        gt_zip = py7zr.SevenZipFile(zip_gt_fname)
                    else:
                        gt_zip = zipfile.ZipFile(zip_gt_fname)
                    samples = {partition + "/" + k: v for k, v in Dibco.load_double_stream(input_zip, gt_zip).items()}
                    data.update(samples)
                else:
                    raise ValueError("Unknown file type")
            else:
                if Dibco.urls[partition][0].endswith(".rar"):
                    input_rar = rarfile.RarFile(root + "/" + Dibco.urls[partition][0].split("/")[-1])
                    samples = {partition + "/" + k: v for k, v in Dibco.load_single_stream(input_rar).items()}
                    data.update(samples)
                elif Dibco.urls[partition][0].endswith(".zip") or Dibco.urls[partition][0].endswith(".7z"):
                    zip_input_fname = root + "/" + Dibco.urls[partition][0].split("/")[-1]
                    if zip_input_fname.endswith("7z"):
                        # zip_input_fname = zip_input_fname[:-2] + "zip"
                        input_zip = py7zr.SevenZipFile(zip_input_fname)
                    else:
                        input_zip = zipfile.ZipFile(zip_input_fname)
                    samples = {partition + "/" + k: v for k, v in Dibco.load_single_stream(input_zip).items()}
                    data.update(samples)
                else:
                    raise ValueError("Unknown file type")
        id_data = list(data.items())
        self.sample_ids = [sample[0] for sample in id_data]
        self.inputs = [sample[1][0] for sample in id_data]
        self.gt = [sample[1][1] for sample in id_data]

    def __getitem__(self, item):
        input_img = self.input_transform(self.inputs[item])
        gt = self.gt_transform(self.gt[item])
        if self.add_mask:
            return input_img, gt, torch.ones_like(input_img[:1, :, :])
        else:
            return input_img, gt

    def __len__(self):
        return len(self.sample_ids)

    def __add__(self, other):
        res = Dibco(partitions=[])
        res.root = self.root
        res.input_transform = self.input_transform
        res.gt_transform = self.gt_transform
        res.sample_ids = self.sample_ids + other.sample_ids
        res.inputs = self.inputs + other.inputs
        res.gt = self.gt + other.gt
        return res


all_dibco_keys = set(Dibco.urls.keys())


l1out_partitions = {}
for k in all_dibco_keys:
    trainset = sorted(all_dibco_keys - set([k]))
    trainset, validationset = trainset[:-1], trainset[-1:]
    l1out_partitions[k] = {"train": trainset, "val": validationset, "test": k}
