"""
Preprocessing functions: Crop, downsize, decrease resolution, etc.

This gives us more flexibility to preprocess our own images rather than always using the default
one in the pre-built ProSR architecture
"""

from PIL import Image
import glob, os
import numpy as np
import cv2


def crop_all_center(dir_path, save_to, half_w, half_h):
	"""
	Crops all images in the given directory from the center.
	We want to get a smaller, lower-res image from the larger images so we can run it through
	the ProSR model without the default downsampling.

	:param dir_path: Path of directory containing images (a video, where each frame must be cropped
	from the same location)
	:param save_to: Path where we want to save the cropped images (under the same name)
	:return: None
	"""
	for filename in glob.glob(dir_path + '/*.jpg'):
		head, tail = os.path.split(filename)
		im = Image.open(filename)
		w, h = im.size
		area = (w/2 - half_w, h/2 - half_h, w/2 + half_w, h/2 + half_h)
		cropped_im = im.crop(area)
		cropped_im.save(save_to + '/' + tail)


def get_time_slices(dir_path, save_to):
	"""
	Stack frames of a video and turn it into a 3d array.
	Then take slices of the array across another dimention (capture time).

	Purpose: Try using ProSR to upsample wrt time. (Turn low FPS video into high FPS vifro
	:param dir_path: Path of dir containing low FPS frames
	:param save_to: Path where we want to save the new time-series frames
	:return: None
	"""
	all_imgs = []
	for filename in glob.glob(dir_path + '/*.png'):
		img = cv2.imread(filename, 0)  # use greyscale
		all_imgs.append(img)

	dim1 = all_imgs[0].shape[0]
	dim2 = all_imgs[0].shape[1]
	stack = np.array(all_imgs).reshape((len(all_imgs), dim1, dim2))

	for i in range(dim1):
		time_slice = stack[:, i, :]
		img = Image.fromarray(time_slice, 'L')
		img.save(save_to + '/' + 'time_slice_{:04}'.format(i) + '.png')


