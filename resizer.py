import os
import sys



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


class MyOriginalImage:
	def __init__(self, image_path, idx, directory):
		self.image_path = image_path
		self.idx = idx
		self.directory = directory
		path_parts = self.image_path.split("/original/")
		if len(path_parts) != 2:
			print(f"\tSkipped: {self.image_path}")
			return

		for j, resolution in enumerate(RESOLUTIONS):
			print(f"\tResolution {j+1:02}/{len(RESOLUTIONS):02} => {resolution}x{resolution}")
			output_image_wrong_path = os.path.join(path_parts[0], str(resolution), path_parts[1])
			output_dirpath = os.path.dirname(output_image_wrong_path)
			if not os.path.isdir(output_dirpath):
				os.makedirs(output_dirpath)
				print(f"\t\tCreated: {output_dirpath}")

			input_filename = os.path.basename(self.image_path)
			output_filename = f"{resolution}-x-{resolution}-{input_filename}"
			output_filepath = os.path.join(output_dirpath, output_filename)
			if os.path.isfile(output_filepath):
				print(f"\t\tExists: {output_filepath}")
			else:
				print(f"\t\tSaved: {output_filepath}")



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
		self.original_images = [MyOriginalImage(x, idx, self) for idx, x in enumerate(self.input_image_file_paths)]
		self.ok = True


def main():
	args = sys.argv[1:]
	for arg in args:
		my_dir = MyImageDirectory(arg)


if __name__ == '__main__':
	main()
