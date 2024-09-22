# This script allows you to find spelling and grammar errors in the "translation.json" file.
from language_tool_python import LanguageTool
from utils import get_translation, clean_dialog


# Open the files
TRANSLATION_FILEPATH = "../translation.json"
SPELLCHECK_FILEPATH = "../spellcheck.txt"

try:
	translation, translation_settings = get_translation(TRANSLATION_FILEPATH)
except FileNotFoundError as e:
	print(f"File '{e.filename}' not found.")
	exit(1)


# Find spelling and grammar errors
lang = LanguageTool(translation_settings["to_language"])
with open(SPELLCHECK_FILEPATH, 'a', encoding='utf-8') as spellcheck:
	spellcheck.truncate(0)
	for line in translation.values():
		for error in lang.check(clean_dialog(line)):
			spellcheck.write('\n'.join(str(error).split('\n')[-3:]) + '\n')

		print(round(list(translation.values()).index(line) / len(translation) * 100), end='%\r')