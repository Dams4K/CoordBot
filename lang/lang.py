import csv
import string

class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class _Lang:
    LANG_SEQ = "{LANG_KEY:"

    def __init__(self, file_path="lang/lang.csv") -> None: #TODO: globalize path
        self.file_path = file_path

        with open(self.file_path, newline='') as f:
            self.rows = [row for row in csv.reader(f, delimiter=",", quotechar='"')]


    def get_text(self, text_key: str, lang: str, custom_rows: dict = None, *args, **kwargs) -> str:
        try:
            lang = lang.lower()

            rows = self.rows
            if custom_rows is not None:
                rows = [self.rows[0]]

                for row in self.rows[1:]:
                    key = row[0]
                    if key in custom_rows.keys():
                        rows.append([key] + [custom_rows.get(key)] * (len(row)-1))
                    else:
                        rows.append(row)
                        
            key_row: int = [row for row in range(len(rows)) if rows[row][0].upper() == text_key.upper()][0]
            if lang not in rows[0]:
                lang = "en"
            lang_col: int = rows[0].index(lang.lower())
            text: str = rows[key_row][lang_col]

            start = text.find(_Lang.LANG_SEQ, 0)
            while -1 < start < len(text):
                end = text.find("}", start)

                inner_text_key = text[start+len(_Lang.LANG_SEQ):end]
                if inner_text_key.upper() != text_key.upper():
                    text = text[:start] + self.get_text(inner_text_key, lang, custom_rows=custom_rows, *args, **kwargs) + text[end+1:]

                start = text.find(_Lang.LANG_SEQ, start+1)

            kwargs.setdefault("lang", lang)
            formatter = string.Formatter()
            mapping = FormatDict({str(k): str(v) for k, v in kwargs.items()})

            return formatter.vformat(text, args, mapping)
        except Exception as e:
            print(e)
            return "message not found"
    
    def get_languages(self):
        return self.rows[0][1:]
    def get_keys(self):
        return [self.rows[i][0] for i in range(1, len(self.rows))]
    
    def language_is_translated(self, lang: str):
        return lang.lower() in self.rows[0]


Lang: _Lang = _Lang()

if __name__ == "__main__":
    print(Lang.get_text("TEST_MSG", "fr"))
    print(Lang.get_text("TEST_MSG", "en"))
    print(Lang.get_text("qd", "en"))