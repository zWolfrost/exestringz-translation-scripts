# This script will create the "strindex_patch.txt" file, patching together "strindex_full.txt" and "translation.json".
from strindex_utils import get_strindex_full, get_translation, slice_offsets, replace_with_table, STRINDEX_FULL_FILEPATH, TRANSLATION_FILEPATH


def main():
	# Open the files
	STRINDEX_PATCH_FILEPATH = "./strindex_patch.txt"
	try:
		strindex_offsets, strindex_lines = get_strindex_full(STRINDEX_FULL_FILEPATH)
		translation = get_translation(TRANSLATION_FILEPATH)
	except FileNotFoundError as e:
		print(f"File '{e.filename}' not found.")
		exit(1)


	# Check the translation for missing or duplicate lines
	translation_counter = {l: 0 for l in translation["patch"]}
	for line in strindex_lines:
		if line in translation["patch"]:
			translation_counter[line] += 1
	for line, count in translation_counter.items():
		if count == 0:
			print(f"The following line doesn't exist:\n{line}\n")
			del translation["patch"][line]
		elif count >= 2:
			print(f"The following line is present multiple times:\n{line}\n")


	# Create the strindex patch
	with open(STRINDEX_PATCH_FILEPATH, 'a', encoding='utf-8') as strindex_patch:
		strindex_patch.truncate(0)
		strindex_patch.write('_' * 80 + translation.get("header", "https://github.com/zWolfrost/exestringz_translation_scripts"))

		strindex_index = 0
		for line in translation["patch"]:
			try:
				strindex_index = strindex_lines.index(line, strindex_index + 1)
			except ValueError:
				print(f"The following line is out of order:\n{line}\n")
				continue

			offsets = slice_offsets(strindex_offsets[strindex_index], *translation.get("patch_offsets", {}).get(line, []))
			line_translated = replace_with_table(translation["patch"][line], translation.get("patch_replace", {}))

			strindex_patch.write('\n' + offsets + '\n' + line_translated)

	print(f"Saved in '{STRINDEX_PATCH_FILEPATH}'.")


if __name__ == "__main__":
	main()