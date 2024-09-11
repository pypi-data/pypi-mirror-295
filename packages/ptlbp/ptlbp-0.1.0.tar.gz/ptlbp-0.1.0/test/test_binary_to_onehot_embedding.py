import torch
import pytest
from ptlbp import PointSampler, BinaryToOnehotChannelEmbeddings as BinaryToOnehotChannel
from skimage.feature import local_binary_pattern


def test_BinaryToOnehotChannel_encoding():
    bchw = torch.arange(210).view(1, 3, 7, 10)
    sz, bc = BinaryToOnehotChannel.img2embedding(bchw)
    new_bchw = BinaryToOnehotChannel.embedding2img(sz, bc)
    assert new_bchw.size() == bchw.size()
    assert torch.allclose(bchw, new_bchw)


@pytest.mark.parametrize("input_size", [1, 2, 3, 4, 8])
def test_BinaryToOnehotChannel_weightsize(input_size):
    oh = BinaryToOnehotChannel(in_channels=input_size)
    assert oh.linear.weight.size(0) == 2 ** input_size
    assert oh.linear.weight.size(1) == input_size
    assert len(oh.linear.weight.size()) == 2


@pytest.mark.parametrize("vector, maxpos", [[torch.tensor([[0, 0, 0]]), 0],
                                            [torch.tensor([[1, 0, 0]]), 1],
                                            [torch.tensor([[0, 1, 0]]), 2],
                                            [torch.tensor([[1, 1, 0]]), 3],
                                            [torch.tensor([[0, 0, 1]]), 4],
                                            [torch.tensor([[1, 0, 1]]), 5],
                                            [torch.tensor([[0, 1, 1]]), 6],
                                            [torch.tensor([[1, 1, 1]]), 7]])
def test_BinaryToOnehotChannel_powerset(vector, maxpos):
    """Test the powerset matrix generator BinaryToOnehotChannel is correct in the case of 3 bits"""
    W = torch.tensor(BinaryToOnehotChannel.powerset_map(3), dtype=torch.float)
    vector = vector.float()
    output = 1 + (vector @ W.T) - ((1-vector) @ W.T)
    assert list(output.size()) == [1, 8]
    assert torch.argmax(output[0, :]).item() == maxpos


img1 = torch.zeros([1, 3, 10, 11], dtype=torch.float32)
img2 = torch.zeros([1, 3, 10, 11], dtype=torch.float32)
img2[0, 0, :, :] = 1
img3 = torch.zeros([1, 3, 10, 11], dtype=torch.float32)
img3[0, :2, :, :] = 1
img4 = torch.zeros([1, 3, 10, 11], dtype=torch.float32)
img4[0, :, :, :] = 1


@pytest.mark.parametrize("input_img, active_output_channel", [[img1[:, :, :1, :1], 0], [img2[:, :, :1, :1], 1],
                                                              [img3[:, :, :1, :1], 3], [img4[:, :, :1, :1], 7]])
def test_BinaryToOnehotChannel_single_pixel(input_img, active_output_channel):
    """Test if the argmax of the output BinaryToOnehotChannel applied on a single pixel image is the same as the expected output"""
    oh = BinaryToOnehotChannel(in_channels=3)
    output = oh(input_img)
    histogram = output[0, :, 0, 0]
    assert torch.argmax(histogram).item() == active_output_channel


@pytest.mark.parametrize("input_img, active_output_channel", [[img1, 0], [img2, 1], [img3, 3], [img4, 7]])
def test_BinaryToOnehotChannel_pooled(input_img, active_output_channel):
    """Test if the argmax of the output BinaryToOnehotChannel aplied on images with uniform pixels per channel is the 
same as the expected output"""
    oh = BinaryToOnehotChannel(in_channels=3)
    output = oh(input_img)
    histogram = output.sum(dim=2).sum(dim=2)[0, :]
    assert torch.argmax(histogram).item() == active_output_channel


#  TODO(anguelos) find the corespondence between SCIKIT and SRS labels
def test_8bit_patterns():
    ps = PointSampler(1, "8r1")
    oh = BinaryToOnehotChannel(in_channels=8)

    #  This is specifically for 8r1 on a 5x5 image
    def get_center_pixel_pattern(img):
        return torch.argmax(oh(ps(img))[:, :, 1, 1], dim=1).item()

    def get_center_pixel_pattern_skimage(img):
        return local_binary_pattern(img[0, 0, :, :].numpy().astype("uint8"), 8, 1, method='default')[2, 2]

    img = torch.zeros([1, 1, 5, 5], dtype=torch.float32)
    assert get_center_pixel_pattern(img) == 0
    #  assert get_center_pixel_pattern(img) == get_center_pixel_pattern_skimage(img)

    img = torch.zeros([1, 1, 5, 5], dtype=torch.float32)
    img[0, 0, 2, 2] = 1
    assert get_center_pixel_pattern(img) == 0
    assert get_center_pixel_pattern(img) == get_center_pixel_pattern_skimage(img)

    img = torch.ones([1, 1, 5, 5], dtype=torch.float32)
    img[0, 0, 2, 2] = 0
    assert get_center_pixel_pattern(img) == 255
    assert get_center_pixel_pattern(img) == get_center_pixel_pattern_skimage(img)

    img = torch.zeros([1, 1, 5, 5], dtype=torch.float32)
    img[0, 0, 2:, :] = 1
    #  print(local_binary_pattern(img[0, 0, :, :].numpy().astype("uint8"), 8, 1, method='default'))
    assert get_center_pixel_pattern(img) == 199
    #  assert get_center_pixel_pattern(img) == get_center_pixel_pattern_skimage(img)
