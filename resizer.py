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
	webp_file_paths = [p for p in file_paths if p.endswith('.webp')]
	for i, webp_file_path in enumerate(webp_file_paths):
		print(f"Image {i+1:03}/{len(webp_file_paths):03} => {webp_file_path}")
		for j, resolution in enumerate(RESOLUTIONS):
			print(f"\tRes {j+1:02}/{len(RESOLUTIONS):02} => {resolution}x{resolution}")
		break


def main():
	args = sys.argv[1:]
	for arg in args:
		resize_stuff(arg)


if __name__ == '__main__':
	main()
