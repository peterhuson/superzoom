from img_preprocessing import crop_all_center, get_time_slices

def main():

    # small video of road (we ended up not using this in our final results)
    # crop_all_center('data/application_video/vid1_short', 'data/application_video/vid1_short_cropped', 300, 100)
    # crop_all_center('data/application_video/vid1_short', 'data/application_video/vid1_short_cropped', 300, 100)
    # crop_all_center('data/application_video/vid1_short', 'data/application_video/vid1_round2_cropped', 600, 200)

    # get time slices from a directory of low rate frames
    # get_time_slices('data/application_video/time/low_fps_frames', 'data/application_video/time/time_slices_original')

    # uncomment this and change to slice on second dimension in array ('dim1') to get new upsampled frames
    # get_time_slices('data/application_video/time/time_slice_upsample_x4', 'data/application_video/time/high_fps_frame_x4')


if __name__ == "__main__":
    main()

