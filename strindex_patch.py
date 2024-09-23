# This script allows you to create the "strindex_patch.txt" file,
# starting from the "strindex_full.txt" file (all the game strings) and the "translation.json" file (the translations of the strings).
from utils import get_strindex_full, get_translation, slice_offsets, replace_with_table


# Open the files
TRANSLATION_FILEPATH = "./translation.json"
STRINDEX_FULL_FILEPATH = "./strindex_full.txt"
STRINDEX_PATCH_FILEPATH = "./strindex_patch.txt"

try:
	translation, translation_settings = get_translation(TRANSLATION_FILEPATH)
	strindex_offsets, strindex_lines = get_strindex_full(STRINDEX_FULL_FILEPATH)
except FileNotFoundError as e:
	print(f"File '{e.filename}' not found.")
	exit(1)


# Check the translation for missing or duplicate lines
translation_counter = {l: 0 for l in translation}
for line in strindex_lines:
	if line in translation:
		translation_counter[line] += 1
for line, count in translation_counter.items():
	if count == 0:
		print(f"The following line doesn't exist:\n{line}\n")
		del translation[line]
	elif count >= 2:
		print(f"The following line is present multiple times:\n{line}\n")


# Create the "strindex_patch.txt" file
with open(STRINDEX_PATCH_FILEPATH, 'a', encoding='utf-8') as strindex_patch:
	strindex_patch.truncate(0)
	strindex_patch.write('_' * 80 + translation_settings.get("description", "https://github.com/zWolfrost/exestringz_translation_scripts"))

	strindex_index = 0
	for line in translation:
		try:
			strindex_index = strindex_lines.index(line, strindex_index + 1)
		except ValueError:
			print(f"The following line is out of order:\n{line}\n")
			continue

		offsets = slice_offsets(strindex_offsets[strindex_index], *translation_settings.get("offsets_slice", {}).get(line, []))
		line_translated = replace_with_table(translation[line], translation_settings.get("dialog_replace", {}))

		strindex_patch.write('\n' + offsets + '\n' + line_translated)

print(f"Saved in '{STRINDEX_PATCH_FILEPATH}'.")