import torch
from .architecture.architecture import *
import cv2
import numpy as np

def esrgan_load_generate(path_to_image, filename, upscaled_path, upscale_level):
    upscale = 4 #4-7
    res_scale = 16#2
    print('upscale is ', upscale_level, 'res_scale', res_scale)
    # device = torch.device('cpu')
    device = torch.device('mps') # using apple silicon
    
    model = RRDB_Net(3, 3, 64, 23, gc=32, upscale=upscale_level, norm_type = None, act_type = 'leakyrelu', \
                            mode = 'CNA', res_scale = res_scale, upsample_mode = 'upconv')
    checkpoint = torch.load('esrgan/models/{:s}'.format('RRDB_ESRGAN_x4_old_arch.pth'))
    model.load_state_dict(checkpoint, strict=True) 

    model.eval()
    for k, v in model.named_parameters():
        v.requires_grad = False
    model = model.to(device)

    img = cv2.imread(path_to_image, cv2.IMREAD_COLOR)
    orig= img
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)
    output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite(upscaled_path, output)
    orig = np.ascontiguousarray(orig)
    output = np.ascontiguousarray(output)
    return orig,output