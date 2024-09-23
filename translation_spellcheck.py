# This script will create the "translation_spellcheck.txt" file, that contains spelling and grammar errors in the "translation.json" file.
from language_tool_python import LanguageTool
from strindex_utils import get_translation, TRANSLATION_FILEPATH
import re


def main():
	# Open the files
	TRANSLATION_SPELLCHECK_FILEPATH = "./translation_spellcheck.txt"
	try:
		translation = get_translation(TRANSLATION_FILEPATH)
	except FileNotFoundError as e:
		print(f"File '{e.filename}' not found.")
		exit(1)


	# Find spelling and grammar errors
	lang = LanguageTool(translation["target_language"])
	with open(TRANSLATION_SPELLCHECK_FILEPATH, 'a', encoding='utf-8') as spellcheck:
		spellcheck.truncate(0)
		for line in translation["patch"].values():
			line_clean = re.sub(translation.get("filter_pattern", ""), "", line)
			for error in lang.check(line_clean):
				spellcheck.write('\n'.join(str(error).split('\n')[-3:]) + '\n')

			print(round(list(translation["patch"].values()).index(line) / len(translation["patch"]) * 100), end='%\r')

	print(f"Saved in '{TRANSLATION_SPELLCHECK_FILEPATH}'.")


if __name__ == "__main__":
	main()