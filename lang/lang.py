import csv
import string

class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class _Lang:
    def __init__(self, file_path="lang/lang.csv") -> None: #TODO: globalize path
        self.file_path = file_path

        with open(self.file_path, newline='') as f:
            self.rows = [row for row in csv.reader(f, delimiter=",", quotechar='"')]


    def get_text(self, text_key: str, lang: str, *args, **kwargs) -> str:
        try:
            lang = lang.lower()
            kwargs.setdefault("lang", lang)

            key_row: int = [row for row in range(len(self.rows)) if self.rows[row][0].upper() == text_key.upper()][0]
            if lang not in self.rows[0]:
                lang = "en"
            lang_col: int = self.rows[0].index(lang.lower())
            text: str = self.rows[key_row][lang_col]

            formatter = string.Formatter()
            mapping = FormatDict({str(k): str(v) for k, v in kwargs.items()})

            return formatter.vformat(text, args, mapping)
        except Exception as e:
            print(e)
            return "message not found"
    
    def get_languages(self):
        return self.rows[0][1:]
    
    def language_is_translated(self, lang: str):
        return lang.lower() in self.rows[0]


Lang: _Lang = _Lang()

if __name__ == "__main__":
    print(Lang.get_text("TEST_MSG", "fr"))
    print(Lang.get_text("TEST_MSG", "en"))
    print(Lang.get_text("qd", "en"))