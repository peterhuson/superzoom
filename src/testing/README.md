## Testing The Network

When we want to test the network, we should refer to the wealth of information in the [ProGanSR issues page](https://github.com/fperazzi/proSR/issues). 

I was able to run the `test.py` file successfully using the following example command: 
```
python test.py --checkpoint data/checkpoints/proSR.pth --target data/datasets/DIV2K/DIV2K_valid_HR --scale 8 -o just_work_pls
```

I tried to run the `test.py` file on a few inputs of my own, but I wasn't able to get past the following error:
```
RuntimeError: CUDNN_STATUS_NOT_SUPPORTED. This error may appear if you passed in a non-contiguous input.
```
I thought it was because I was giving it `.jpeg` rather than `.png` but it still errored. 30 seconds of googling gets me [here](Someone should look into this.)

#### Testing *Very* Large Images:
According to [this](https://github.com/fperazzi/proSR/issues/9) issue, it is best to split up large images into tiles of smaller size and then run each one through the image individually. This will save memory. 


### Upsampling (Cropped) Videos
1. Turn video into frames of images using ffmpeg (Peter did this part; not super sure what command he used)
2. Crop each video using `crop_all_center` function in `img_preprocessing.py`
3. Upsample cropped images using ```python test.py --checkpoint data/checkpoints/proSR.pth -i [LR FRAMES DIR PATH] --scale [CHOOSE 2, 4, OR 8] -o [HR FRAMES DIR PATH]```
4. Create video from upsampled frames. Run this ffmpeg command in the directory containing all the upsampled frames ```ffmpeg -pattern_type glob -i '*.jpg' [OUTPUT VID NAME + PATH]```
5. Change size of video to original (ProSR upsamples and for some reason also scales the size up by that factor, so we need to downscale it to get something that's comparable to the original) ```ffmpeg -i [LARGE OUTPUT VID] -vf "scale=iw*[DECIMAL, 0.5, 0.25, or 0.125]:ih*[DECIMAL, 0.5, 0.25, or 0.125]" [RESIZED OUTPUT VID PATH]```
6. Pull up original and new resized video. These should be the same size. Compare.

