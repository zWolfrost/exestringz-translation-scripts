# This script allows you to create the "strindex_filter.txt" file, starting from the "strindex_full.txt" file (all the game strings).
# The "strindex_filter.txt" file will contain only the target language strings, useful for quickly sorting the strings to be translated.
import re
from lingua import IsoCode639_1, LanguageDetectorBuilder
from utils import get_strindex_full, get_translation


# Open the files
TRANSLATION_FILEPATH = "./translation.json"
STRINDEX_FULL_FILEPATH = "./strindex_full.txt"
STRINDEX_FILTER_FILEPATH = "./strindex_filter.txt"

try:
	translation, translation_settings = get_translation(TRANSLATION_FILEPATH)
	strindex_offsets, strindex_lines = get_strindex_full(STRINDEX_FULL_FILEPATH)
except FileNotFoundError as e:
	print(f"File '{e.filename}' not found.")
	exit(1)


# Filter the strindex in the desired language
languages = [getattr(IsoCode639_1, code.upper()) for code in translation_settings["possible_languages"]]
detector = LanguageDetectorBuilder.from_iso_codes_639_1(*languages).build()

CHAR_WHITELIST = translation_settings.get("dialog_char_whitelist", None)

with open(STRINDEX_FILTER_FILEPATH, 'a', encoding='utf-8') as strindex_filter:
	strindex_filter.truncate(0)
	strindex_filter.write('_' * 80 + translation_settings.get("description", "https://github.com/zWolfrost/exestringz_translation_scripts"))

	for strindex_index in range(len(strindex_lines)):
		line = strindex_lines[strindex_index]
		if line and line not in translation and (not CHAR_WHITELIST or all(ch in CHAR_WHITELIST for ch in line)):
			line_clean = re.sub(translation_settings.get("dialog_remove_pattern", ""), "", line)
			confidence = detector.compute_language_confidence_values(line_clean)[0]
			if confidence.language.iso_code_639_1 == getattr(IsoCode639_1, translation_settings["from_language"].upper()) and confidence.value > 0.5:
				strindex_filter.write(f"\n{strindex_offsets[strindex_index]}___{confidence.value:.2f}\n{line}")

		print(round(strindex_index / len(strindex_lines) * 100), end='%\r')

print(f"Saved in '{STRINDEX_FILTER_FILEPATH}'.")