from .sampling import PointSampler, GaussianPointSampler, TOffsets
from .comparisson import Comparisson, ComparissonQuantile, ComparissonOtsu
from .encoding import BinaryToOnehotChannelEmbeddings
from .diff_lbp import DiffLBP
from .srs import DiffSRSLBP, CompressionLayer, DeepCompressionLayer, DeepResCompressionLayer
from .srs import DropConnect, MultiRadiusDiffLBP
from .srs import hellinger_normalise, l2_normalise
from .losses import CDistLoss, CDistContrastiveLoss, CDistTripletLoss, CDistRatioLoss
from .histograms import DiffHOG, DiffHistogram, DiffOtsu, hard_otsu_threshold, diff_otsu_threshold, _DiffBinning
from . import unpooled_lbp
from . import util
from . import testing
from . import datasets


__all__ = ["DiffLBP", "PointSampler", "BinaryToOnehotChannelEmbeddings", "Comparisson", "ComparissonOtsu",
           "ComparissonQuantile", "util", "testing", "TOffsets", "DiffSRSLBP", "CompressionLayer",
           "DeepCompressionLayer", "DeepResCompressionLayer", "DropConnect", "MultiRadiusDiffLBP",
           "hellinger_normalise", "l2_normalise", "CDistLoss", "CDistContrastiveLoss", "CDistTripletLoss",
           "CDistRatioLoss", "DiffHOG", "DiffHistogram", "DiffOtsu", "hard_otsu_threshold",
           "diff_otsu_threshold", "_DiffBinning", "datasets", "unpooled_lbp", "GaussianPointSampler"]


__version__ = "0.1.0"

# redistering comlormap 'd256' to matplotlib
try:
    util.create_dicrete_colormap(256)
except ValueError:
    # colormap already registered lets fail gracefully in __init__
    pass


# TODO: add retrieval searcher for the classes
