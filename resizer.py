import os
import sys

from PIL import Image



RESOLUTIONS = [
	32, 64, 128, 192, 256, 384, 512, 1024
]

def get_all_file_paths(root, sort=False):
	file_paths = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			file_path = os.path.join(path, name)
			file_paths.append(file_path)

	if sort:
		file_paths.sort()
	return file_paths



class MySquareOutputImage:
	def __init__(self, resolution, original):
		self.resolution = resolution
		self.original = original
		self.size = (self.resolution, self.resolution)

		path_parts = self.original.image_path.split("/original/")
		self.output_image_wrong_path = os.path.join(path_parts[0], str(self.resolution), path_parts[1])
		self.output_dirpath = os.path.dirname(self.output_image_wrong_path)
		if not os.path.isdir(self.output_dirpath):
			os.makedirs(self.output_dirpath)
			print(f"\t\tCreated: {self.output_dirpath}")

		input_filename = os.path.basename(self.original.image_path)
		self.output_filename = f"{self.resolution}-x-{self.resolution}-{input_filename}"
		self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)

	def exists(self):
		return True if os.path.isfile(self.output_filepath) else False



class MyOriginalImage:
	def __init__(self, image_path, directory):
		self.ok = False
		self.image_path = image_path
		self.image = None
		self.directory = directory

		path_parts = self.image_path.split("/original/")
		if len(path_parts) != 2:
			print(f"\tSkipped: {self.image_path}")
			return

		self.output_images = [MySquareOutputImage(resolution, self) for resolution in RESOLUTIONS]
		self.ok = True

	def initialize_image_object(self):
		if not self.image:
			print(f"\t\tInitializing Image Object . . .")
			self.image = Image.open(self.image_path)
			w, h = self.image.size
			smaller = min(w, h)
			mid_x = w // 2
			mid_y = h // 2
			offset = smaller // 2

			box = (mid_x-offset, mid_y-offset, mid_x+offset, mid_y+offset)
			self.square_img = self.image.crop(box)

	def produce_output_images(self):
		for idx, output_image in enumerate(self.output_images):
			print(f"\tResolution {idx+1:02}/{len(RESOLUTIONS):02} => {output_image.resolution}x{output_image.resolution}")
			if output_image.exists():
				print(f"\t\tExists: {output_image.output_filepath} {output_image.size}")
			else:
				self.initialize_image_object()
				img = self.square_img.resize(output_image.size, Image.LANCZOS)
				img.save(output_image.output_filepath)
				print(f"\t\tSaved: {output_image.output_filepath} {output_image.size}")



class MyImageDirectory:
	def __init__(self, dirpath):
		self.ok = False
		self.dirpath = dirpath
		if not os.path.isdir(self.dirpath):
			print(f"Not found: '{self.dirpath}'")
			return

		self.original_dirpath = os.path.join(self.dirpath, 'original')
		if not os.path.isdir(self.original_dirpath):
			print(f"Not found: '{self.original_dirpath}'")
			return

		file_paths = get_all_file_paths(self.original_dirpath)
		self.input_image_file_paths = [p for p in file_paths if p.endswith('.webp')]
		self.original_images = [MyOriginalImage(image_path, self) for image_path in self.input_image_file_paths]
		self.ok = True

	def produce_output_images(self):
		for idx, image in enumerate(self.original_images):
			print(f"Image {idx+1:03}/{len(self.original_images):03} => {image.image_path}")
			image.produce_output_images()
			# break



def main():
	args = sys.argv[1:]
	for arg in args:
		my_dir = MyImageDirectory(arg)
		my_dir.produce_output_images()


if __name__ == '__main__':
	main()
