import json

STRINDEX_FULL_FILEPATH = "./strindex_full.txt"
TRANSLATION_FILEPATH = "./translation.json"


def get_strindex_full(filepath: str) -> tuple[list[str], list[str]]:
	with open(filepath, 'r', encoding='utf-8', errors='ignore') as strindex_full:
		strindex_offsets = []
		strindex_lines = []
		for line in strindex_full:
			line = line[:-1]
			if line.startswith('_' * 80):
				strindex_offsets.append(line)
				strindex_lines.append(None)
			elif strindex_lines[-1] is None:
				strindex_lines[-1] = line
			else:
				strindex_lines[-1] += '\n' + line
	return strindex_offsets, strindex_lines


def get_translation(filepath: str) -> tuple[dict[str, str], dict[str, str]]:
	with open(filepath, 'r', encoding='utf-8') as f:
		translation: dict[str, str] = json.loads(f.read())
	return translation


def slice_offsets(offsets: str, start=None, end=None) -> str:
	if start is None and end is None:
		return offsets
	offsets_beg, offsets = offsets.split('-', 1)
	offsets, offsets_end = offsets.rsplit('___', 1)
	offsets = '-'.join(offsets.split('-')[start:end])
	return f"{offsets_beg}-{offsets}___{offsets_end}"


def replace_with_table(string: str, table: dict[str, str]) -> str:
	for key, value in table.items():
		string = string.replace(key, value)
	return string
