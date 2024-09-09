from torch import nn
import rollcat_cuda
import torch
from ._autocast_utils import _cast_if_autocast_enabled

class RollCatFunc(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, *args):
        ctx.args = args
        output = rollcat_cuda.rollcat_forward(input.contiguous(), *args)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        in_grad = rollcat_cuda.rollcat_backward(grad_output.contiguous(),*ctx.args)
        return in_grad,*(None for _ in ctx.args)

def roll_cat(input,num_batch, height, width,num_heads, head_dim,window_size1,window_size2, shift_size,shift_h):
    return RollCatFunc.apply(input,num_batch, height, width,
                             num_heads, head_dim,window_size1,window_size2, shift_size,shift_h)
