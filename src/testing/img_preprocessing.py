"""
Preprocessing functions: Crop, downsize, decrease resolution, etc.

This gives us more flexibility to preprocess our own images rather than always using the default
one in the pre-built ProSR architecture
"""

from PIL import Image
import glob, os


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

