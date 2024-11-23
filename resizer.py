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


def resize_stuff(dirpath):
	if not os.path.isdir(dirpath):
		print(f"Not found: '{dirpath}'")
		return

	original_dirpath = os.path.join(dirpath, 'original')
	if not os.path.isdir(original_dirpath):
		print(f"Not found: '{original_dirpath}'")
		return

	file_paths = get_all_file_paths(original_dirpath)
	input_image_file_paths = [p for p in file_paths if p.endswith('.webp')]
	for i, input_image_file_path in enumerate(input_image_file_paths):
		print(f"Image {i+1:03}/{len(input_image_file_paths):03} => {input_image_file_path}")
		path_parts = input_image_file_path.split("/original/")
		if len(path_parts) != 2:
			print(f"\tSkipped: {input_image_file_path}")
			continue

		for j, resolution in enumerate(RESOLUTIONS):
			print(f"\tResolution {j+1:02}/{len(RESOLUTIONS):02} => {resolution}x{resolution}")
			output_image_wrong_path = os.path.join(path_parts[0], str(resolution), path_parts[1])
			output_dirpath = os.path.dirname(output_image_wrong_path)
			if not os.path.isdir(output_dirpath):
				os.makedirs(output_dirpath)
				print(f"\t\tCreated: {output_dirpath}")

			input_filename = os.path.basename(input_image_file_path)
			output_filename = f"{resolution}-x-{resolution}-{input_filename}"
			output_filepath = os.path.join(output_dirpath, output_filename)
			print(f"\t\tOutput: {output_filepath}")
		break


def main():
	args = sys.argv[1:]
	for arg in args:
		resize_stuff(arg)


if __name__ == '__main__':
	main()
