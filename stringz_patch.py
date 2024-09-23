# This script allows you to create the "stringz_patch.txt" file,
# starting from the "stringz_full.txt" file (all the game strings) and the "translation.json" file (the translations of the strings).
from utils import get_stringz_full, get_translation, slice_offsets, replace_with_table


# Open the files
TRANSLATION_FILEPATH = "./translation.json"
STRINGZ_FULL_FILEPATH = "./stringz_full.txt"
STRINGZ_PATCH_FILEPATH = "./stringz_patch.txt"

try:
	translation, translation_settings = get_translation(TRANSLATION_FILEPATH)
	stringz_offsets, stringz_lines = get_stringz_full(STRINGZ_FULL_FILEPATH)
except FileNotFoundError as e:
	print(f"File '{e.filename}' not found.")
	exit(1)


# Check the translation for missing or duplicate lines
translation_counter = {l: 0 for l in translation}
for line in stringz_lines:
	if line in translation:
		translation_counter[line] += 1
for line, count in translation_counter.items():
	if count == 0:
		print(f"The following line doesn't exist:\n{line}\n")
		del translation[line]
	elif count >= 2:
		print(f"The following line is present multiple times:\n{line}\n")


# Create the "stringz_patch.txt" file
with open(STRINGZ_PATCH_FILEPATH, 'a', encoding='utf-8') as stringz_patch:
	stringz_patch.truncate(0)
	stringz_patch.write('_' * 80 + translation_settings.get("description", "https://github.com/zWolfrost/exestringz_translation_scripts"))

	stringz_index = 0
	for line in translation:
		try:
			stringz_index = stringz_lines.index(line, stringz_index + 1)
		except ValueError:
			print(f"The following line is out of order:\n{line}\n")
			continue

		offsets = slice_offsets(stringz_offsets[stringz_index], *translation_settings.get("offsets_slice", {}).get(line, []))
		line_translated = replace_with_table(translation[line], translation_settings.get("dialog_replace", {}))

		stringz_patch.write('\n' + offsets + '\n' + line_translated)

print(f"Saved in '{STRINGZ_PATCH_FILEPATH}'.")