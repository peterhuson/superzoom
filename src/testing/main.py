from img_preprocessing import crop_all_center

def main():

    # small video of road
    # crop_all_center('data/video/vid1_short', 'data/video/vid1_short_cropped', 300, 100)
    crop_all_center('data/video/vid1_short', 'data/video/vid1_short_cropped', 300, 100)

    # larger video of road
    crop_all_center('data/video/vid1_short', 'data/video/vid1_round2_cropped', 600, 200)


if __name__ == "__main__":
    main()

