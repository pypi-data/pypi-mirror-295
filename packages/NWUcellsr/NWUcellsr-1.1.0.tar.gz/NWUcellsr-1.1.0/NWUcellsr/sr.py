import argparse
import cv2
import glob
import numpy as np
import os
import torch
from collections import OrderedDict
from NWUcellsr.craft_arch import CRAFT
import pkg_resources  # 用于访问包内资源


def define_model(model_path, scale):
    model = CRAFT(
        upscale=scale,
        in_chans=3,
        img_size=64,
        window_size=16,
        img_range=1.,
        depths=[2, 2, 2, 2],
        embed_dim=48,
        num_heads=[6, 6, 6, 6],
        mlp_ratio=2,
        resi_connection='1conv')

    loadnet = torch.load(model_path)
    keyname = 'params_ema' if 'params_ema' in loadnet else 'params'
    model.load_state_dict(loadnet[keyname], strict=True)

    return model


def process_image(input_folder, output_folder, scale):
    os.makedirs(output_folder, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 获取模型文件的路径
    model_path = pkg_resources.resource_filename(__name__, 'models/sr.pth')
    model = define_model(model_path, scale)
    model.eval()
    model = model.to(device)

    window_size = 16

    input_images = sorted(glob.glob(os.path.join(input_folder, '*')))
    if not input_images:
        print("No images found in the input folder.")
        return

    print(f"Processing {len(input_images)} images...")

    for idx, path in enumerate(input_images):
        print(f"Processing image {idx + 1}/{len(input_images)}: {path}")
        imgname = os.path.splitext(os.path.basename(path))[0]
        img_lq = cv2.imread(path, cv2.IMREAD_COLOR)
        if img_lq is None:
            print(f"Cannot read image at {path}")
            continue
        img_lq = img_lq.astype(np.float32) / 255.0

        img_lq = np.transpose(img_lq if img_lq.shape[2] == 1 else img_lq[:, :, [2, 1, 0]], (2, 0, 1))
        img_lq = torch.from_numpy(img_lq).float().unsqueeze(0).to(device)

        with torch.no_grad():
            _, _, h_old, w_old = img_lq.size()
            h_pad = (h_old // window_size + 1) * window_size - h_old
            w_pad = (w_old // window_size + 1) * window_size - w_old
            img_lq = torch.cat([img_lq, torch.flip(img_lq, [2])], 2)[:, :, :h_old + h_pad, :]
            img_lq = torch.cat([img_lq, torch.flip(img_lq, [3])], 3)[:, :, :, :w_old + w_pad]

            output = model(img_lq)
            output = output[..., :h_old * scale, :w_old * scale]

        output = output.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        if output.ndim == 3:
            output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round().astype(np.uint8)
        output_path = os.path.join(output_folder, f'{imgname}.png')
        cv2.imwrite(output_path, output)
        print(f"Saved super-resolved image to {output_path}")

def run_super_resolution():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='Input low-quality image folder')
    parser.add_argument('--output', type=str, required=True, help='Output folder')
    parser.add_argument('--scale', type=int, default=2, help='Scale factor: 1, 2, 3, 4, 8')
    args = parser.parse_args()

    process_image(args.input, args.output, args.scale)
