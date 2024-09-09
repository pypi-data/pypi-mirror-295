import logging
import warnings

# May help avoid undefined symbol errors https://pytorch.org/cppdocs/notes/faq.html#undefined-symbol-errors-from-pytorch-aten
import torch
import os

try:
    from .spexmlp import *
except Exception:
    pass

try:
    from .rollcat import *
except Exception:
    pass
from .eswiglu import *
