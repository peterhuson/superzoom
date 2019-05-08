from img_preprocessing import crop_all_center, get_time_slices

def main():

    # small video of road
    # crop_all_center('data/video/vid1_short', 'data/video/vid1_short_cropped', 300, 100)
    # crop_all_center('data/video/vid1_short', 'data/video/vid1_short_cropped', 300, 100)
	#
    # # larger video of road
    # crop_all_center('data/video/vid1_short', 'data/video/vid1_round2_cropped', 600, 200)

    get_time_slices('data/video/low_fps', 'data/video/time_slices')
    # uncomment this and change to slice on second dimension in array ('dim1') to get new upsampled frames
    # get_time_slices('data/video/time_slices_upsample_x2', 'data/video/high_fps')


if __name__ == "__main__":
    main()

