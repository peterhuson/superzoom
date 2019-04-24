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

