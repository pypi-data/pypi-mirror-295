from typing import Any, Dict, Tuple, Union, List
from .srs import MultiRadiusDiffLBP
from .util import pil_image_as_batch
from PIL import Image
import numpy as np
import torch
from collections import defaultdict

TPattern = Union[np.uint64, str, Tuple[int, ...], List[int], np.ndarray, torch.tensor]
TImage = Union[Image.Image, np.ndarray, torch.Tensor, None]


class DenseLBPIndex():
    def __add__(self, other: 'DenseLBPIndex') -> 'DenseLBPIndex':
        assert self.lbp_extractor == other.lbp_extractor and\
            self._do_cache_images == other._do_cache_images and\
            self._do_cache_occurences == other._do_cache_occurences\
            and self._do_cache_stacks == other._do_cache_stacks
        res = DenseLBPIndex(lbp_extractor=self.lbp_extractor,
                            cache_images=self._do_cache_images,
                            cache_occurences=self._do_cache_occurences,
                            cache_stacks=self._do_cache_stacks)
        for lbp_img in self._dense_lbp_images:
            res._dense_lbp_images.append(lbp_img)
            res._ids.append(lbp_img.id)
            res._ids_to_index[lbp_img.id] = len(res._dense_lbp_images) - 1
        for lbp_img in other._dense_lbp_images:
            if lbp_img.id not in self._ids_to_index:
                res._dense_lbp_images.append(lbp_img)
                res._ids.append(lbp_img.id)
                res._ids_to_index[lbp_img.id] = len(res._dense_lbp_images) - 1
            else:
                print(f"__add__ Image with id {lbp_img.id} already exists")
        return res

    def pattern_to_string(self, pattern: TPattern) -> str:
        if isinstance(pattern, str):
            return pattern
        elif isinstance(pattern, (tuple, list, np.ndarray, torch.Tensor)):
            return f"({','.join([str(int(x)) for x in pattern])})"
        else:
            raise ValueError(f'Invalid pattern type {type(pattern)}')

    def pattern_to_tuple(self, pattern: TPattern) -> torch.Tensor:
        if isinstance(pattern, str):
            return tuple([int(p) for p in pattern.strip('()').split(',')])
        elif isinstance(pattern, tuple):
            return pattern
        elif isinstance(pattern, list):
            return tuple(pattern)
        elif isinstance(pattern, np.ndarray):
            return tuple(pattern.reshape(-1))
        elif isinstance(pattern, torch.Tensor):
            return tuple(pattern.cpu().numpy().reshape(-1))
        else:
            raise ValueError(f'Invalid pattern type {type(pattern)}')

    def get_pattern_frequecies(self, return_str: bool = False) -> Union[Dict[str, int], Dict[Tuple[int, ...], int]]:
        occ, _ = self.get_occurence_count()
        freq_pattern = sorted([(v, self.pattern_to_string(k)) for k, v in occ.items()])
        if return_str:
            res = {self.pattern_to_string(p): f for f, p in freq_pattern}
        else:
            res = {self.pattern_to_tuple(p): f for f, p in freq_pattern}
        return res

    def __init__(self, lbp_extractor: MultiRadiusDiffLBP, cache_images: bool = True,
                 cache_stacks: bool = False, cache_occurences: bool = True) -> None:
        if not cache_images and not cache_occurences:
            raise ValueError('Cannot cache neither occurences nor images')
        self.lbp_extractor = lbp_extractor
        self._dense_lbp_images = []
        self._ids = []
        self._ids_to_index: Dict[str, int] = {}
        self._cached_global_occurences = None
        self._cached_per_image_occurences = None
        self._do_cache_stacks = cache_stacks
        self._do_cache_images = cache_images
        self._do_cache_occurences = cache_occurences

    @property
    def radii_count(self) -> int:
        return self.lbp_extractor.radii_count

    def add_image(self, img_id: str, img: TImage = None) -> 'DenseLBPIndex':
        if img_id in self._ids_to_index:
            raise ValueError('Image with id already exists')
        if img is None:
            img = Image.open(img_id)
        lbp_image = DenseImageLBP(id=img_id, img=img, lbp_extractor=self.lbp_extractor,
                                  cache_images=self._do_cache_images, cache_occurences=self._do_cache_occurences,
                                  cache_stack=self._do_cache_stacks)
        self._dense_lbp_images.append(lbp_image)
        self._ids.append(img_id)
        self._ids_to_index[img_id] = len(self._dense_lbp_images) - 1
        self._cached_global_occurences = None
        self._cached_per_image_occurences = None
        return self

    def add_images(self, image_paths) -> 'DenseLBPIndex':
        for image_path in image_paths:
            self.add_image(image_path)
        return self

    def __getitem__(self, pos_or_id: Union[int, str]) -> 'DenseImageLBP':
        if isinstance(pos_or_id, int):
            return self._dense_lbp_images[pos_or_id]
        elif isinstance(pos_or_id, str):
            return self._dense_lbp_images[self._ids_to_index[pos_or_id]]
        else:
            raise ValueError('Invalid index type')

    def __len__(self):
        return len(self._dense_lbp_images)

    def get_occurence_count(self) -> \
            Tuple[Dict[Tuple[int, ...], int], Dict[str, Dict[Tuple[int, ...], int]]]:
        if self._cached_global_occurences is not None and self._cached_per_image_occurences is not None:
            return self._cached_global_occurences, self._cached_per_image_occurences
        global_occurences = defaultdict(lambda: 0)
        per_image_occurences = {}
        for indexed_image in self._dense_lbp_images:
            occurences = indexed_image.occurences
            per_image_occurences[indexed_image.id] = occurences
            for pattern, count in occurences.items():
                global_occurences[pattern] += count
        self._cached_global_occurences = dict(global_occurences)
        self._cached_per_image_occurences = per_image_occurences
        return self._cached_global_occurences, self._cached_per_image_occurences


class FastLBPIndex(DenseLBPIndex):
    def __add__(self, other: 'FastLBPIndex') -> 'FastLBPIndex':
        assert self.lbp_extractor == other.lbp_extractor and\
            self._do_cache_images == other._do_cache_images and\
            self._do_cache_occurences == other._do_cache_occurences\
            and self._do_cache_stacks == other._do_cache_stacks
        res = FastLBPIndex(lbp_extractor=self.lbp_extractor,
                           cache_images=self._do_cache_images,
                           cache_occurences=self._do_cache_occurences,
                           cache_stacks=self._do_cache_stacks)
        for lbp_img in self._dense_lbp_images:
            res._dense_lbp_images.append(lbp_img)
            res._ids.append(lbp_img.id)
            res._ids_to_index[lbp_img.id] = len(res._dense_lbp_images) - 1
        for lbp_img in other._dense_lbp_images:
            if lbp_img.id not in self._ids_to_index:
                res._dense_lbp_images.append(lbp_img)
                res._ids.append(lbp_img.id)
                res._ids_to_index[lbp_img.id] = len(res._dense_lbp_images) - 1
            else:
                print(f"__add__ Image with id {lbp_img.id} already exists")
        return res

    def pattern_to_string(self, pattern: TPattern) -> str:
        if isinstance(pattern, str):
            return pattern
        elif isinstance(pattern, np.uint64):
            return f"{repr(self.decode_pattern(pattern))}"
        elif isinstance(pattern, (tuple, list, np.ndarray, torch.Tensor)):
            return f"({','.join([str(int(x)) for x in pattern])})"
        else:
            raise ValueError(f'Invalid pattern type {type(pattern)}')

    def pattern_to_tuple(self, pattern: TPattern) -> torch.Tensor:
        if isinstance(pattern, str):
            return tuple([int(p) for p in pattern.strip('()').split(',')])
        elif isinstance(pattern, np.uint64):
            return self.decode_pattern(pattern)
        elif isinstance(pattern, tuple):
            return pattern
        elif isinstance(pattern, list):
            return tuple(pattern)
        elif isinstance(pattern, np.ndarray):
            return tuple(pattern.reshape(-1))
        elif isinstance(pattern, torch.Tensor):
            return tuple(pattern.cpu().numpy().reshape(-1))
        else:
            raise ValueError(f'Invalid pattern type {type(pattern)}')

    def encode_pattern(self, pattern: TPattern) -> int:
        pattern = np.array(pattern).reshape(-1)
        if len(pattern) != self.radii_count:
            raise ValueError('Pattern must be convertible to 1D array')
        return (self._pattern_exponents * pattern).sum()

    def decode_pattern(self, pattern: np.uint64) -> Tuple[int, ...]:
        return tuple((pattern // self._pattern_exponents) % 256)

    def __init__(self, lbp_extractor: MultiRadiusDiffLBP, cache_images: bool = True,
                 cache_stacks: bool = False, cache_occurences: bool = True) -> None:
        super().__init__(lbp_extractor=lbp_extractor, cache_images=cache_images, cache_stacks=cache_stacks,
                         cache_occurences=cache_occurences)
        if lbp_extractor.radii_count > 8:
            raise ValueError('FastLBPIndex only supports radii count <= 8')
        self._pattern_exponents = np.array([256 ** i for i in range(lbp_extractor.radii_count)], dtype=np.uint64)

    @property
    def radii_count(self) -> int:
        return self.lbp_extractor.radii_count

    def add_image(self, img_id: str, img: TImage = None) -> 'DenseLBPIndex':
        if img_id in self._ids_to_index:
            raise ValueError('Image with id already exists')
        if img is None:
            img = Image.open(img_id)
        lbp_image = FastImageLBP(id=img_id, img=img, lbp_extractor=self.lbp_extractor,
                                 cache_images=self._do_cache_images, cache_occurences=self._do_cache_occurences,
                                 cache_stack=self._do_cache_stacks)
        self._dense_lbp_images.append(lbp_image)
        self._ids.append(img_id)
        self._ids_to_index[img_id] = len(self._dense_lbp_images) - 1
        self._cached_global_occurences = None
        self._cached_per_image_occurences = None
        return self

    def add_images(self, image_paths) -> 'DenseLBPIndex':
        for image_path in image_paths:
            self.add_image(image_path)
        return self

    def __getitem__(self, pos_or_id: Union[int, str]) -> 'DenseImageLBP':
        if isinstance(pos_or_id, int):
            return self._dense_lbp_images[pos_or_id]
        elif isinstance(pos_or_id, str):
            return self._dense_lbp_images[self._ids_to_index[pos_or_id]]
        else:
            raise ValueError('Invalid index type')

    def get_occurence_count(self) -> \
            Tuple[Dict[int, int], Dict[str, Dict[int, int]]]:
        if self._cached_global_occurences is not None and self._cached_per_image_occurences is not None:
            return self._cached_global_occurences, self._cached_per_image_occurences
        global_occurences = defaultdict(lambda: 0)
        per_image_occurences = {}
        for indexed_image in self._dense_lbp_images:
            occurences = indexed_image.occurences
            per_image_occurences[indexed_image.id] = occurences
            for pattern, count in occurences.items():
                global_occurences[pattern] += count
        self._cached_global_occurences = dict(global_occurences)
        self._cached_per_image_occurences = per_image_occurences
        return self._cached_global_occurences, self._cached_per_image_occurences


class DenseImageLBP():
    @staticmethod
    def resolve_img_type(img: TImage) -> None:
        if isinstance(img, torch.Tensor):
            pt_img = img
            if pt_img.dim() == 3:
                pt_img = pt_img.unsqueeze(0)
            elif pt_img.dim() == 2:
                pt_img = pt_img.unsqueeze(0).unsqueeze(0)
            elif pt_img.dim() != 4:
                raise ValueError('Invalid tensor shape')
            pil_img = Image.fromarray((img[0, 0, :, :].cpu().numpy() * 255.).astype(np.uint8))
        elif isinstance(img, np.ndarray):
            pt_img = torch.tensor(img)
            if pt_img.dim() == 3:
                pt_img = pt_img.unsqueeze(0)
            elif pt_img.dim() == 2:
                pt_img = pt_img.unsqueeze(0).unsqueeze(0)
            elif pt_img.dim() != 4:
                raise ValueError('Invalid tensor shape')
            pil_img = Image.fromarray((img[0, 0, :, :].cpu().numpy() * 255.).astype(np.uint8))
        elif isinstance(img, Image.Image):
            pil_img = img
            pt_img = pil_image_as_batch(img)
        elif isinstance(img, str):
            pil_img = Image.open(img)
            pt_img = pil_image_as_batch(pil_img)
        else:
            raise ValueError(f"Invalid image type {type(img)}")
        return pil_img, pt_img

    def __init__(self, id: str, lbp_extractor: MultiRadiusDiffLBP, img: TImage = None, cache_stack: bool = True,
                 cache_occurences: bool = True, cache_images: bool = True) -> None:
        if not cache_images and not cache_occurences:
            raise ValueError('Cannot cache neither occurences nor images')
        self._lbp_extractor = lbp_extractor
        self._id = id
        self._img = None
        self._cached_stack = None
        self._cached_occurences = None
        self._do_cache_occurences = cache_occurences
        self._do_cache_stack = cache_stack
        if img is None:
            img = id
            pil_img, pt_img = DenseImageLBP.resolve_img_type(img=img)
            self._img = pil_img
        else:
            self._img = img

    @property
    def radii_count(self) -> int:
        return self._lbp_extractor.radii_count

    @property
    def computation_device(self) -> torch.device:
        return self._lbp_extractor.device

    @property
    def id(self) -> str:
        return self._id

    @property
    def stack(self) -> Union[torch.Tensor, None]:
        if self._cached_stack is None:
            _, pt_img = DenseImageLBP.resolve_img_type(img=self._img)
            stack = self._compute_stack(pt_img.to(self.computation_device))
            if self._do_cache_stack:
                self._cached_stack = stack
            return stack
        else:
            return self._cached_stack

    @property
    def occurences(self) -> Dict[Tuple[int, ...], int]:
        stack = self.stack  # caching in case it is not cached
        if self._cached_occurences is None:
            occurences = defaultdict(lambda: 0)
            for x in range(stack.shape[1]):
                for y in range(stack.shape[2]):
                    pattern = tuple(stack[:, x, y])
                    occurences[pattern] += 1
            occurences = dict(occurences)
            if self._do_cache_occurences:
                self._cached_occurences = occurences
            return occurences
        else:
            return self._cached_occurences

    @property
    def img(self) -> Union[Image.Image, None]:
        return self._img

    def _compute_stack(self, pt_img: torch.Tensor) -> np.ndarray:
        res = self._lbp_extractor.compute_lbp_stack(pt_img.to(self.computation_device), return_confidences=False)
        res = res.cpu().numpy().astype(int)
        if len(res.shape) == 4 and res.shape[0] == 1:
            res = res.squeeze(0)
        return res

    def get_similarity_count(self, pattern: TPattern) -> int:
        pattern = np.array(pattern).reshape(-1)[:, None, None]
        if len(pattern.shape) != 3 or pattern.shape[0] != self.radii_count:
            raise ValueError('Pattern must be convertible to 3D array')
        agree = (self.stack == pattern).astype(int).sum(axis=0)
        return agree

    def locate_pattern(self, pattern: TPattern, tolerance=0) -> Tuple[np.ndarray, np.ndarray]:
        correct = self.get_similarity_count(pattern=pattern) >= (self.radii_count - tolerance)
        y, x = np.nonzero(correct)
        return x, y


class FastImageLBP(DenseImageLBP):
    def encode_pattern(self, pattern: TPattern) -> int:
        pattern = np.array(pattern).reshape(-1)
        if len(pattern) != self.radii_count:
            raise ValueError('Pattern must be convertible to 1D array')
        return (self._pattern_exponents * pattern).sum()

    def decode_pattern(self, pattern: int) -> Tuple[int, ...]:
        return tuple((pattern // self._pattern_exponents) % 256)

    def __init__(self, id: str, lbp_extractor: MultiRadiusDiffLBP, img: TImage = None, cache_stack: bool = True,
                 cache_occurences: bool = True, cache_images: bool = True) -> None:
        super().__init__(id=id, lbp_extractor=lbp_extractor, img=img, cache_stack=cache_stack,
                         cache_occurences=cache_occurences, cache_images=cache_images)
        assert lbp_extractor.radii_count <= 8
        self._pattern_exponents = np.array([256 ** i for i in range(lbp_extractor.radii_count)], dtype=np.uint64)

    @property
    def radii_count(self) -> int:
        return self._lbp_extractor.radii_count

    @property
    def computation_device(self) -> torch.device:
        return self._lbp_extractor.device

    @property
    def id(self) -> str:
        return self._id

    @property
    def stack(self) -> Union[torch.Tensor, None]:
        if self._cached_stack is None:
            _, pt_img = DenseImageLBP.resolve_img_type(img=self._img)
            stack = self._compute_stack(pt_img.to(self.computation_device))
            if self._do_cache_stack:
                #print("Caching stack", type(self._cached_stack))
                self._cached_stack = stack
            else:
                pass
                #print("Not Caching stack", type(self._cached_stack))
            return stack
        else:
            return self._cached_stack

    @property
    def occurences(self) -> Dict[int, int]:
        if self._cached_occurences is None:
            stack = self.stack
            patterns, freqs = np.unique(stack, return_counts=True)
            occurences = dict(zip(patterns, freqs))
            if self._do_cache_occurences:
                self._cached_occurences = occurences
            return occurences
        else:
            return self._cached_occurences

    @property
    def img(self) -> Union[Image.Image, None]:
        return self._img

    def _compute_stack(self, pt_img: torch.Tensor) -> np.ndarray:
        stack = self._lbp_extractor.compute_lbp_stack(pt_img.to(self.computation_device), return_confidences=False)
        if len(stack.shape) == 4 and stack.shape[0] == 1:
            stack = stack.squeeze(0)
        stack = (stack.cpu().numpy().astype(np.uint64) * self._pattern_exponents[:, None, None]).sum(axis=0)
        return stack

    def get_similarity_count(self, pattern: TPattern) -> int:
        pattern = self.encode_pattern(pattern)
        if len(pattern.shape) != 3 or pattern.shape[0] != self.radii_count:
            raise ValueError('Pattern must be convertible to 3D array')
        agree = (self.stack == pattern)
        return agree

    def locate_pattern(self, pattern: TPattern, tolerance=0) -> Tuple[np.ndarray, np.ndarray]:
        if tolerance > 0:
            raise NotImplementedError('Tolerance not implemented for FastImageLBP')
        correct = self.get_similarity_count(pattern=pattern) >= (self.radii_count - tolerance)
        y, x = np.nonzero(correct)
        return x, y
