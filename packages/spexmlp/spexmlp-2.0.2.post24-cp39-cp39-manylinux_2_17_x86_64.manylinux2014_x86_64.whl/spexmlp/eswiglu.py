from typing import Mapping, Any

import torch,torch.nn as nn
import os,importlib.machinery

import numpy as np

license_loaded=[None]

def import_dylib():
    name = 'spexmlp_swiglu_cuda'
    if torch.__version__ >= '2.4.0':
        name += '_torch24'
    lib_path = importlib.machinery.PathFinder().find_spec(name).origin
    torch.ops.load_library(lib_path)

def load_license(model=None,path=None,license=None,device='cuda', reload=False):
    # provide a license path, list containing the license message, or model that encrypted by the license,
    # load license into gpu.
    if license_loaded[0] is not None and not reload:
        return license_loaded[0]

    import_dylib()

    if model is not None:
        for n,p in model.state_dict().items():
            if 'lyyLicense' in n:
                license=p.to(device)
                break
    elif path is not None and os.path.exists(path):
            with open(path,'r') as f:
                license = [int(t) for t in f.readlines() if len(t.strip())>0]

    assert license is not None
    if not isinstance(license,torch.Tensor):
        license = np.array([license], dtype=np.uint64).astype(np.int64)
        license = torch.as_tensor(license, dtype=torch.int64, device=device)

    license = license.to(device)

    output = torch.ops.spexmlp.check_license(license)
    if output[0] == 500:
        raise ValueError('model license has expired!')
    elif output[0] == 300:
        raise ValueError('invalid model license!')
    elif output[0] == 404:
        raise ValueError('un-authorized device!')
    elif output[0] == 301:
        raise ValueError('different version of licenses detected, which is not supported!')
    elif output[0] != 1:
        raise ValueError('failed to load model license')
    license_loaded[0] = license.flatten()[0].item()
    return license_loaded[0]

class sFusedSwiglu(nn.Module):
    def __init__(self, in_dim=None,hid_dim=None,out_dim=None,
                 w1w2=None, b1b2=None, w3=None, b3=None, tid=None, ln_w=None, ln_b=None, eps=1e-5, subln=True):
        super().__init__()
        if in_dim is not None:
            self.w1w2=nn.Parameter(torch.randn((hid_dim*2,in_dim))*0.02)
            self.b1b2=nn.Parameter(torch.randn((hid_dim*2,))*0.02)
            self.w3 = nn.Parameter(torch.randn((out_dim, hid_dim)) * 0.02)
            self.b3 = nn.Parameter(torch.randn((out_dim, )) * 0.02)
            if subln:
                self.ln_b = nn.Parameter(torch.ones((hid_dim , ),dtype=torch.float32) )
                self.ln_w = nn.Parameter(torch.randn((hid_dim ,)) * 0.0001)
            self.register_buffer('tid_tensor', torch.as_tensor(np.random.randint(1,1<<32),dtype=torch.int64))
            self.tid = self.tid_tensor.item()
            self.eps = eps

        if w1w2 is not None:
            self.register_buffer('tid_tensor',torch.as_tensor(tid,device=w1w2.device))
            self.tid = self.tid_tensor.item()
            for name,param in zip(('w1w2','b1b2','w3','b3','ln_w','ln_b'),
                                  (w1w2,b1b2,w3,b3,ln_w,ln_b)):
                p = None if param is None else nn.Parameter(param)
                self.register_parameter(name,p)
            self.eps=eps

    def _load_from_state_dict(self, state_dict, prefix, local_metadata, strict,
                              missing_keys, unexpected_keys, error_msgs):
        super()._load_from_state_dict(state_dict, prefix, local_metadata, strict,
                              missing_keys, unexpected_keys, error_msgs)
        self.tid=self.tid_tensor.item()

    def forward(self,x):
        raise NotImplementedError('sFusedSwiglu is deprecated, '
                                  'please contact CEPRI to update the models to sFusedSwiglu_v2')

class sFusedSwiglu_v2(nn.Module):
    def __init__(self, in_dim=None,hid_dim=None,out_dim=None,
                 w1w2=None, b1b2=None, w3=None, b3=None, tid=None, ln_w=None, ln_b=None, eps=1e-5, subln=True):
        super().__init__()
        if in_dim is not None:
            self.w1w2=nn.Parameter(torch.randn((hid_dim*2*in_dim))*0.02)
            self.b1b2=nn.Parameter(torch.randn((hid_dim*2,))*0.02)
            self.w3 = nn.Parameter(torch.randn((out_dim, hid_dim)) * 0.02)
            self.b3 = nn.Parameter(torch.randn((out_dim, )) * 0.02)
            if subln:
                self.ln_b = nn.Parameter(torch.ones((hid_dim , ),dtype=torch.float32) )
                self.ln_w = nn.Parameter(torch.randn((hid_dim ,)) * 0.0001)
            self.register_buffer('tid_tensor', torch.as_tensor(np.random.randint(1,1<<32),dtype=torch.int64))
            self.tid = self.tid_tensor.item()
            self.eps = eps

        if w1w2 is not None:
            self.register_buffer('tid_tensor',torch.as_tensor(tid,device=w1w2.device))
            self.tid = self.tid_tensor.item()
            for name,param in zip(('w1w2','b1b2','w3','b3','ln_w','ln_b'),
                                  (w1w2,b1b2,w3,b3,ln_w,ln_b)):
                p = None if param is None else nn.Parameter(param)
                self.register_parameter(name,p)
            self.eps=eps

    def _load_from_state_dict(self, state_dict, prefix, local_metadata, strict,
                              missing_keys, unexpected_keys, error_msgs):
        super()._load_from_state_dict(state_dict, prefix, local_metadata, strict,
                                      missing_keys, unexpected_keys, error_msgs)
        self.tid = self.tid_tensor.item()

    def forward(self,x):
        shape=x.shape[:-1]
        x=x.view(-1,x.shape[-1])
        return torch.ops.spexmlp.eswiglu_packedw_v2(
            x, self.w1w2, self.b1b2, self.w3, self.b3, self.tid, self.ln_w, self.ln_b, self.eps
        ).view(*shape,-1)


class sFusedBottleNeck(nn.Module):
    def __init__(self, dim=None, w=None, b1=None, b2=None, tid=0, modelid=0):
        super().__init__()
        assert modelid < 32
        if dim is not None:
            self.w=nn.Parameter(torch.randn((dim*dim*5))*0.02)
            self.b1=nn.Parameter(torch.randn((dim//2,))*0.02)
            self.b2 = nn.Parameter(torch.randn((dim, )) * 0.02)
            self.register_buffer('tid_tensor', torch.as_tensor(np.random.randint(1,1<<28) * modelid,
                                                                    dtype=torch.int64))
            self.tid = self.tid_tensor.item()

        if w is not None:
            self.register_buffer('tid_tensor',torch.as_tensor(tid,device=w.device))
            self.tid = self.tid_tensor.item()
            for name,param in zip(('w','b1','b2'),
                                  (w,b1,b2)):
                p = None if param is None else nn.Parameter(param)
                self.register_parameter(name,p)

    def _load_from_state_dict(self, state_dict, prefix, local_metadata, strict,
                              missing_keys, unexpected_keys, error_msgs):
        super()._load_from_state_dict(state_dict, prefix, local_metadata, strict,
                                      missing_keys, unexpected_keys, error_msgs)
        self.tid = self.tid_tensor.item()

    def forward(self,x):
        x = x.contiguous(memory_format=torch.channels_last)
        return torch.ops.spexmlp.eneck_op(x, self.w, self.b1, self.b2, self.tid)