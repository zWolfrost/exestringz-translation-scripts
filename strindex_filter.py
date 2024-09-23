# This script allows you to create the "strindex_filter.txt" which will contain all the target language strings from the "strindex_full.txt" file.
from lingua import IsoCode639_1, LanguageDetectorBuilder
from strindex_utils import get_strindex_full, get_translation, STRINDEX_FULL_FILEPATH, TRANSLATION_FILEPATH
import re


def main():
	# Open the files
	STRINDEX_FILTER_FILEPATH = "./strindex_filter.txt"
	try:
		strindex_offsets, strindex_lines = get_strindex_full(STRINDEX_FULL_FILEPATH)
		translation = get_translation(TRANSLATION_FILEPATH)
	except FileNotFoundError as e:
		print(f"File '{e.filename}' not found.")
		exit(1)


	# Filter the strindex in the desired language
	languages = [getattr(IsoCode639_1, code.upper()) for code in translation["possible_languages"]]
	detector = LanguageDetectorBuilder.from_iso_codes_639_1(*languages).build()

	CHAR_WHITELIST = translation.get("filter_whitelist", None)

	with open(STRINDEX_FILTER_FILEPATH, 'a', encoding='utf-8') as strindex_filter:
		strindex_filter.truncate(0)
		strindex_filter.write('_' * 80 + translation.get("header", "https://github.com/zWolfrost/exestringz_translation_scripts"))

		for strindex_index in range(len(strindex_lines)):
			line = strindex_lines[strindex_index]
			if line and line not in translation["patch"] and (not CHAR_WHITELIST or all(ch in CHAR_WHITELIST for ch in line)):
				line_clean = re.sub(translation.get("filter_pattern", ""), "", line)
				confidence = detector.compute_language_confidence_values(line_clean)[0]
				if confidence.language.iso_code_639_1 == getattr(IsoCode639_1, translation["source_language"].upper()) and confidence.value > 0.5:
					strindex_filter.write(f"\n{strindex_offsets[strindex_index]}___{confidence.value:.2f}\n{line}")

			print(round(strindex_index / len(strindex_lines) * 100), end='%\r')

	print(f"Saved in '{STRINDEX_FILTER_FILEPATH}'.")


if __name__ == "__main__":
	main()