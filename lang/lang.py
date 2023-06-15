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


    def get_key_datas(self, raw_key_datas: str) -> tuple:
        """Return key datas from string

        Parameters
        ----------
            raw_key_datas: str
                String version of key datas
        
        Returns
        -------
            tuple: (key: str, parameters: set)
        """
        s = raw_key_datas.split(":")
        key = s[0]
        parameters: set = set()
        if len(s) > 1: # There's more to it than the key
            parameters = set(s[1].split(";")) # get all parameters
        return (key, parameters)

    def get_rows(self, custom_rows: dict) -> dict:
        if not custom_rows:
            return self.rows
        
        rows_length = len(self.rows[0])
        # Recreate the rows
        rows = [self.rows[0]] # Languages list

        for row in self.rows[1:]:
            key = row[0]
            if key in custom_rows.keys():
                rows.append([key] + [custom_rows.get(key)] * rows_length-1)
            else:
                rows.append(row)
        return rows

    def apply_parameters(self, text, parameters: list) -> str:
        for parameter in parameters:
            if parameter.lower() == "capitalize":
                text = text[0].upper() + text[1:]
            elif parameter.lower() == "casefold":
                text = text[0].casefold() + text[1:] # casefold because we want ß to become ss

        return text

    def get_text(self, raw_key_datas: str, language: str, custom_rows: dict = None, MAX_ITE = 5, *args, **kwargs) -> str:
        """TEXT_KEY:PARAMETER1;PARAMETER2"""
        if MAX_ITE <= 0: # Stop the recursive loop
            return ""
        MAX_ITE -= 1

        # Add get rows + custom rows
        rows = self.get_rows(custom_rows)

        # Get the guild language index
        available_languages = rows[0]
        if self.language_is_translated(language):
            language_index = available_languages.index(language.lower())
        else:
            language_index = available_languages.index("en")
        
        key, parameters = self.get_key_datas(raw_key_datas)
        try:
            key_index: int = [row for row in range(len(rows)) if rows[row][0].upper() == key.upper()][0]
        except IndexError:
            print("The", key, "key wasn't found")
            return key

        text: str = rows[key_index][language_index]

        start_index = text.find(_Lang.LANG_SEQ, 0)
        # if nothing found, start_index will be -1
        while -1 < start_index < len(text):
            # search the closest "}" from the start_index
            end_index = text.find("}", start_index)
            raw_key_datas = text[start_index+len(_Lang.LANG_SEQ):end_index]
            
            # Add text
            inner_text = self.get_text(raw_key_datas, language, custom_rows=custom_rows, MAX_ITE=MAX_ITE, *args, **kwargs)
            text = text[:start_index] + inner_text + text[end_index+1:]

            # Search next key_datas
            start_index = text.find(_Lang.LANG_SEQ, start_index+1)

        text = self.apply_parameters(text, parameters)

        # Add language value
        # language is a default placeholder always available
        kwargs.setdefault("language", language)
        formatter = string.Formatter()
        mapping = FormatDict({str(k): str(v) for k, v in kwargs.items()})

        return formatter.vformat(text, args, mapping)
    
    def language_is_translated(self, language: str):
        return language.lower() in self.rows[0]

    def get_languages(self):
        return self.rows[0][1:]


Lang: _Lang = _Lang()