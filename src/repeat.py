from argparse import ArgumentParser
from pprint import pprint
from prosr import Phase
from prosr.data import DataLoader, Dataset, DataChunks
from prosr.logger import info
from prosr.metrics import eval_psnr_and_ssim
from prosr.utils import (get_filenames, IMG_EXTENSIONS, print_evaluation,
                         tensor2im)

import numpy as np
import os
import time
import os.path as osp
import prosr
import skimage.io as io
import torch
import sys
import shutil


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(osp.join(BASE_DIR, 'lib'))


def parse_args(input_folder, output_folder):
    parser = ArgumentParser(description='ProSR')
    parser.add_argument(
        '-d',
        '--downscale',
        help='Bicubic downscaling of input to LR',
        action='store_true')

    parser.add_argument(
        '-mx',
        '--max-dimension',
        help='Split image into chunks of max-dimension.',
        type=int,
        required=False,
        default=0)
    parser.add_argument(
        '--padding',
        help='Pad image when splitting into quadrants.',
        type=int,
        required=False,
        default=0)
    parser.add_argument(
        '-f', '--fmt', help='Image file format', type=str, default='*')
    parser.add_argument(
        '--cpu', help='Use CPU.', action='store_true')

    args = parser.parse_args()

    args.input = get_filenames([], IMG_EXTENSIONS)
    args.target = get_filenames(input_folder, IMG_EXTENSIONS)
    args.output_dir = output_folder

    return args

    
def run_single(input_folder, output_folder):
    # Parse command-line arguments
    args = parse_args(input_folder, output_folder)
    
    arg_checkpoint = "data/checkpoints/proSR.pth"

    if args.cpu:
        checkpoint = torch.load(arg_checkpoint,
                                map_location=lambda storage, loc: storage)
    else:
        checkpoint = torch.load(arg_checkpoint)

    cls_model = getattr(prosr.models, checkpoint['class_name'])

    model = cls_model(**checkpoint['params']['G'])
    model.load_state_dict(checkpoint['state_dict'])

    info('phase: {}'.format(Phase.TEST))
    info('checkpoint: {}'.format(osp.basename(arg_checkpoint)))

    params = checkpoint['params']
    pprint(params)

    model.eval()

    if torch.cuda.is_available() and not args.cpu:
        model = model.cuda()

    dataset = Dataset(
        Phase.TEST,
        args.input,
        args.target,
        8,
        input_size=None,
        mean=params['train']['dataset']['mean'],
        stddev=params['train']['dataset']['stddev'],
        downscale=args.downscale)

    data_loader = DataLoader(dataset, batch_size=1)

    mean = params['train']['dataset']['mean']
    stddev = params['train']['dataset']['stddev']

    if not osp.isdir(args.output_dir):
        os.makedirs(args.output_dir)
    info('Saving images in: {}'.format(args.output_dir))

    with torch.no_grad():
        if len(args.target):
            psnr_mean = 0
            ssim_mean = 0

        for iid, data in enumerate(data_loader):
            tic = time.time()
            # split image in chuncks of max-dimension
            if args.max_dimension:
                data_chunks = DataChunks({'input':data['input']},
                                         args.max_dimension,
                                         args.padding,8)
                for chunk in data_chunks.iter():
                    input = chunk['input']
                    if not args.cpu:
                        input = input.cuda()
                    output = model(input,8)
                    data_chunks.gather(output)
                output = data_chunks.concatenate() + data['bicubic']
            else:
                input = data['input']
                if not args.cpu:
                    input = input.cuda()
                output = model(input,8).cpu() + data['bicubic']
            sr_img = tensor2im(output, mean, stddev)
            toc = time.time()
            if 'target' in data:
                hr_img = tensor2im(data['target'], mean, stddev)
                psnr_val, ssim_val = eval_psnr_and_ssim(
                    sr_img, hr_img, 8)
                print_evaluation(
                    osp.basename(data['input_fn'][0]), psnr_val, ssim_val,
                    iid + 1, len(dataset), toc - tic)
                psnr_mean += psnr_val
                ssim_mean += ssim_val
            else:
                print_evaluation(
                    osp.basename(data['input_fn'][0]), np.nan, np.nan, iid + 1,
                    len(dataset), toc - tic)

            fn = osp.join(args.output_dir, osp.basename(data['input_fn'][0]))
            io.imsave(fn, sr_img)

        if len(args.target):
            psnr_mean /= len(dataset)
            ssim_mean /= len(dataset)
            print_evaluation("average", psnr_mean, ssim_mean)
            
            
if __name__ == '__main__':
    
    loops = 1000
    
    for i in range(loops) :
        run_single("Repeat_Imgs/"+str(i), "Repeat_Imgs/"+str(i+1))
       
    for i in range(loops+1) :
        for file in os.listdir("Repeat_Imgs/"+str(i)) :
            shutil.copyfile("Repeat_Imgs/"+str(i)+"/"+file, "Repeat_Imgs/"+file[:-4]+"_"+str(i)+".png")
            
    for i in range(1, loops+1) :
        for file in os.listdir("Repeat_Imgs/"+str(i)) :
            os.remove("Repeat_Imgs/"+str(i)+"/"+file)
        os.rmdir("Repeat_Imgs/"+str(i))

    
