import csv
import string
import json
import os

class CommandLocalization:
    PATH = "lang/commands/%s.json"

    def __init__(self, filename: str):
        self.filename = filename.lower()
        self.data = {}
        self.load_localization()

    @property
    def path(self) -> str:
        return CommandLocalization.PATH % self.filename

    def load_localization(self) -> None:
        if not os.path.exists(self.path):
            return
        
        with open(self.path, "r") as f:
            self.data = json.load(f)

    @property
    def loc_description(self) -> str:
        return self.data.get("description", None)
    
    @property
    def loc_description_localizations(self) -> dict:
        return self.data.get("description_localizations", None)
    @property
    def loc_name_localizations(self) -> dict:
        return self.data.get("name_localizations", None)

    def get_option_localization(self, name):
        options = self.data.get("options", {})
        return OptionLocalization(options.get(name, {}))

class OptionLocalization:
    def __init__(self, data):
        self.name_localizations = data.get("name_localizations", None)
        self.description = data.get("description", None)
        self.description_localizations = data.get("description_localizations", None)
    
    def add_localization(self, option):
        if self.name_localizations is not None: option.name_localizations = self.name_localizations
        if self.description is not None: option.description = self.description
        if self.description_localizations is not None: option.description_localizations = self.description_localizations

        return option

class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class _Lang:
    LANG_SEQ = "{LANG_KEY:"

    def __init__(self, file_path="lang/lang.csv") -> None: #TODO: globalize path
        self.file_path = file_path

        with open(self.file_path, newline='') as f:
            self.rows = [row for row in csv.reader(f, delimiter=",", quotechar='"')]


    def get_text(self, text_key_informations: str, lang: str, custom_rows: dict = None, *args, **kwargs) -> str:
        """TEXT_KEY:PARAMETER1;PARAMETER2"""
        try:
            splited_text_key_informations = text_key_informations.split(":")
            text_key = splited_text_key_informations[0]
            text_parameters = []
            if len(splited_text_key_informations) > 1:
                text_parameters = splited_text_key_informations[1].split(";")

            lang = lang.lower()

            rows = self.rows
            # Add custom rows
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

                inner_text_key_informations = text[start+len(_Lang.LANG_SEQ):end]
                inner_text_key = inner_text_key_informations.split(":")[0]

                #TODO: infinite loops when key A have key B and key B have key A
                text = text[:start] + self.get_text(inner_text_key_informations, lang, custom_rows=custom_rows, *args, **kwargs) + text[end+1:]

                start = text.find(_Lang.LANG_SEQ, start+1)

            for text_parameter in text_parameters:
                if text_parameter.lower() == "capitalize":
                    text = text[0].upper() + text[1:]
                elif text_parameter.lower() == "casefold":
                    text = text[0].casefold() + text[1:] # casefold because we want ß to become ss

            kwargs.setdefault("lang", lang)
            formatter = string.Formatter()
            mapping = FormatDict({str(k): str(v) for k, v in kwargs.items()})

            return formatter.vformat(text, args, mapping)
        except IndexError:
            print("The", text_key, "key wasn't found")
            return text_key
    
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