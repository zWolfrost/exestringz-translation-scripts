# This script allows you to create the "stringz_filter.txt" file, starting from the "stringz_full.txt" file (all the game strings).
# The "stringz_filter.txt" file will contain only the target language strings, useful for quickly sorting the strings to be translated.
from lingua import IsoCode639_1, LanguageDetectorBuilder
from utils import get_stringz_full, get_translation, clean_dialog


# Open the files
TRANSLATION_FILEPATH = "../translation.json"
STRINGZ_FULL_FILEPATH = "../stringz_full.txt"
STRINGZ_FILTER_FILEPATH = "../stringz_filter.txt"

try:
	translation, translation_settings = get_translation(TRANSLATION_FILEPATH)
	stringz_offsets, stringz_lines = get_stringz_full(STRINGZ_FULL_FILEPATH)
except FileNotFoundError as e:
	print(f"File '{e.filename}' not found.")
	exit(1)


# Filter the stringz in the desired language
languages = [getattr(IsoCode639_1, code.upper()) for code in translation_settings["possible_languages"]]
detector = LanguageDetectorBuilder.from_iso_codes_639_1(*languages).build()

CHAR_WHITELIST = """\n !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^`abcdefghijklmnopqrstuvwxyz{|}~ ¡ª¿ÀÁÂÃÄÆÇÈÉÊËÍÎÏÑÓÔÕÖÙÚÛÜßàáâãäæçèéêëíîïñóôõöùúûüŒœЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёẞ‐‑‒–—―…⁃"""

with open(STRINGZ_FILTER_FILEPATH, 'a', encoding='utf-8') as stringz_filter:
	stringz_filter.truncate(0)
	stringz_filter.write('_' * 80 + translation_settings.get("description", ""))

	for stringz_index in range(len(stringz_lines)):
		line = stringz_lines[stringz_index]
		if line and line not in translation and all(ch in CHAR_WHITELIST for ch in line):
			confidence = detector.compute_language_confidence_values(clean_dialog(line))[0]
			if confidence.language.iso_code_639_1 == getattr(IsoCode639_1, translation_settings["from_language"].upper()) and confidence.value > 0.5:
				stringz_filter.write(f"\n{stringz_offsets[stringz_index]}___{confidence.value:.2f}\n{line}")

		print(round(stringz_index / len(stringz_lines) * 100), end='%\r')