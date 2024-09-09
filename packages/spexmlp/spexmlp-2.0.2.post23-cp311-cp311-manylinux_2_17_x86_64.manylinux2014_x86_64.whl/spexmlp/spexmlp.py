import time,random,os


# =============== slinear and encrypt =================
from torch import nn
import numpy as np
import spexmlp_cuda,torch
from ._autocast_utils import _cast_if_autocast_enabled
license_loaded=[False]

def _fused_dense(input, weight, bias,id1):
    assert license_loaded[0]
    args = _cast_if_autocast_enabled(input.contiguous(), weight, bias,id1)
    with torch.cuda.amp.autocast(enabled=False),torch.no_grad():
        return spexmlp_cuda.slinear_bias_forward(*args)

def _fused_dense_gelu_dense(input, weight, bias1, bias2,id1):
    assert license_loaded[0]
    args = _cast_if_autocast_enabled(input.contiguous(), weight, bias1, bias2,id1)
    with torch.cuda.amp.autocast(enabled=False):
        return spexmlp_cuda.slinear_gelu_linear_forward(*args)


class sFusedDense(nn.Module):
    def __init__(self, module:nn.Linear, encrypt_function, id1):
        super(sFusedDense, self).__init__()
        self.in_features = module.in_features
        self.out_features = module.out_features
        self.weight = nn.Parameter(encrypt_function(module.weight.data, id1))
        self.bias = module.bias
        self.id1 = id1

    def forward(self, input):
        return _fused_dense(input, self.weight.data, self.bias.data,self.id1)

class sFusedConv1x1(nn.Module):
    def __init__(self, module:nn.Conv2d, encrypt_function, id1):
        super(sFusedConv1x1, self).__init__()
        self.in_features = module.in_channels
        self.out_features = module.out_channels
        self.weight = nn.Parameter(encrypt_function(module.weight.data, id1))
        self.bias = module.bias
        self.id1 = id1

    def forward(self, input):
        input = input.permute(0,2,3,1)
        result = _fused_dense(input, self.weight.data, self.bias.data,self.id1)
        return result.permute(0,3,1,2)


class sFusedDenseGeluDense(nn.Module):
    def __init__(self, module:nn.Module,encrypt_function, id1):
        super(sFusedDenseGeluDense, self).__init__()
        weight = torch.cat([module.fc1.weight.data.flatten(),module.fc2.weight.data.flatten()],0)
        self.weight = nn.Parameter(encrypt_function(weight,id1))
        self.bias1 = module.fc1.bias
        self.bias2 = module.fc2.bias
        self.id1=id1

    def forward(self, input):
        return _fused_dense_gelu_dense(input, self.weight.data, self.bias1.data, self.bias2.data,self.id1)

def load_license(model=None,path=None,sec_message=None,device='cuda'):
    # provide a license path, list containing the license message, or model that encrypted by the license,
    # load license into gpu.
    if path is not None:
        with open(path,'r') as f:
            sec_message = [int(t) for t in f.readlines() if len(t.strip())>0]
    elif model is not None:
        sec_message = model.lyyLicense
    sec_message = np.array([sec_message],dtype=np.uint64).astype(np.int64)
    sec_message = torch.as_tensor(sec_message,dtype=torch.int64,device=device)
    license_loaded[0] = True
    output = spexmlp_cuda.check_sec_forward(sec_message)
    if output[0] == 500:
        raise ImportError('model license has expired!')
    elif output[0] == 300:
        raise ImportError('invalid model license!')
    elif output[0] == 404:
        raise ImportError('un-authorized device!')
    elif output[0] == 301:
        raise ImportError('different version of licenses detected, which is not supported!')
    elif output[0] != 1:
        raise ImportError('failed to load model license')