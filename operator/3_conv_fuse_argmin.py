import torch
from torch.nn import Conv2d, Module
from utils import input_spatials, format_list
import pdb
import os

class Model(Module):
    def __init__(self, inc, outc, k, s, p, d, g):
        super().__init__()
        self.m = Conv2d(inc, outc, k, s, p, d, g)
        # self.m = Conv2d(inc, outc, 3)
        
    def forward(self, x):
        return torch.argmin(self.m(x))

def work(workdir: str):
    inchannels = [3]
    outchannels = [1, 64, 512]
    kernels = [3]
    strides = [1]
    pads = [0]
    dilations = [1]
    
    ret = []

    for inc in inchannels:
        for outc in outchannels:
            
            groups = [1]
            if inc > 16 and outc > 16:
                groups.append(int(inc/16))
            
            for g in groups:
                for k in kernels:
                    for s in strides:
                        for p in pads:
                            for d in dilations:
                                m = Model(inc, outc, k, s, p, d, g)
                                
                                key = 'conv{}s{}p{}d{}ic{}oc{}g{}.argmin'.format(k,s,p,d,inc,outc,g)

                                filename = os.path.join(workdir, '{}.onnx'.format(key))
                                
                                input_ = torch.rand(1, inc, 224, 224)
                                out = m(input_)
                                torch.onnx.export(model=m, args=(input_), f=filename, verbose=False, input_names=['input'], output_names=['output'])
                                
                                print('{} input={}'.format(key, format_list(input_.shape)))
                                ret.append((key, filename))
    return ret

if __name__ == '__main__':
    ret = work('onnx/argmin/')
    print(len(ret))
