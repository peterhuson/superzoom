"""
Preprocessing functions: Crop, downsize, decrease resolution, etc.

This gives us more flexibility to preprocess our own images rather than always using the default
one in the pre-built ProSR architecture
"""


def crop_all_center(dir_path):
	"""
	todo
	Crops all images in the given directory from the center.
	We want to get a smaller, lower-res image from the larger images so we can run it through
	the ProSR model without the default downsampling.
	:param dir_path: Path of directory containing images (a video, where each frame must be cropped
	from the same location)
	:return: None
	"""
	pass


