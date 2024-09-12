import json
import re
from al78tools.cli.cli_colors import BG, CMD, FG


class JsonFilterException(Exception):
    pass


class JsonFilter:
    PARSED_KEY_CACHE = {}

    def __init__(self, filter_keys: list[str], exclude_keys: list[str] = None):
        self.filter_keys = filter_keys
        self.exclude_keys = exclude_keys or []
        self.multiline_output: bool = False
        self.values_only: bool = False
        self.highlight_values: list[str] = []
        self.ihighlight_values: list[str] = []
        self.pass_non_json: bool = False
        self._is_value_operator_used: bool = self._check_is_value_operator_used(self.filter_keys)
        self._is_exclude_value_operator_used: bool = self._check_is_value_operator_used(self.exclude_keys)

    def parse_key(self, key: str) -> (str, str, str):
        if key in self.PARSED_KEY_CACHE:
            return self.PARSED_KEY_CACHE[key]

        rkey: str
        rvalue: str
        operator: str = None
        re_sign = re.search("([=~])", key)
        if re_sign:
            operator = re_sign.group()
        parsed_key: list = str(key).split(operator)
        rkey = parsed_key[0].strip()
        rvalue = parsed_key[1].strip() if len(parsed_key) > 1 else None
        self.PARSED_KEY_CACHE[key] = (rkey, rvalue, operator)
        return rkey, rvalue, operator

    def filter_keys_and_values(self, line: str) -> dict | str:
        result = {}
        is_value_matched = False
        try:
            json_data_tree = json.loads(line)
            json_data_flat = self._flatten_dict(json_data_tree)

            if not isinstance(json_data_flat, dict):
                raise JsonFilterException("JSON data is not dict on line: {}".format(line))

            if self._check_exclude(json_data_flat):
                return None

            result, is_value_matched = self._get_match_result(json_data_flat, self.filter_keys)
        except ValueError as ex:
            if self.pass_non_json:
                return line
            else:
                raise JsonFilterException("Error while decoding jSON line: {} caused by: {}".format(line, ex))
        except Exception as ex:
            raise JsonFilterException("Error while processing line: {} caused by: {}".format(line, ex))
        if self._is_value_operator_used and not is_value_matched:
            return None
        return result

    def _check_exclude(self, json_data_flat: dict) -> bool:
        result, is_value_matched = self._get_match_result(json_data_flat, self.exclude_keys)
        if self._is_exclude_value_operator_used and is_value_matched:
            return True
        return True if result else False

    def _get_match_result(self, json_data_flat: dict, key_list: list) -> (dict, bool):
        result = {}
        is_value_matched = False
        for ikey in key_list:
            key, value, operator = self.parse_key(ikey)
            flat_key: str
            key_matches = [flat_key for flat_key in json_data_flat.keys() if
                           flat_key == key or (key[-1] == "*" and flat_key.startswith(key[:-1]))]
            for key in key_matches:
                if key in json_data_flat:
                    if not value:
                        result[key] = json_data_flat[key]
                    elif operator == "=" and str(value) == str(json_data_flat[key]):
                        result[key] = json_data_flat[key]
                        is_value_matched = True
                    elif operator == "~" and str(value) in str(json_data_flat[key]):
                        result[key] = json_data_flat[key]
                        is_value_matched = True
        return result, is_value_matched

    def _flatten_dict(self, input_dict: dict, parent_key: str = "") -> dict:
        items = []
        for k, v in input_dict.items():
            new_key = "{}.{}".format(parent_key, k) if parent_key else "{}".format(k)
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key).items())
            elif isinstance(v, list):
                new_v = dict(enumerate(v))
                items.extend(self._flatten_dict(new_v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def format_result(self, data: dict) -> str:
        ret = ""
        for key, value in data.items():
            br_line = "\n" if self.multiline_output else " "
            value = self._highlight_value(value) if self.highlight_values else value
            value = self._ihighlight_value(value) if self.ihighlight_values else value
            if self.values_only:
                ret = f"{ret}{FG.cyan}{value}{CMD.reset}{br_line}"
            else:
                ret = f"{ret}\"{FG.green}{CMD.bold}{key}{CMD.reset}\": \"{FG.cyan}{value}{CMD.reset}\"{br_line}"
        return f"{ret}\n"

    def _highlight_value(self, value: str) -> str:
        for highlight in self.highlight_values:
            if found_results := re.findall(f"({highlight})+", value):
                for found in found_results:
                    value = value.replace(found, f"{FG.orange}{BG.lightgrey}{CMD.bold}{found}{CMD.reset}")
        return value

    def _ihighlight_value(self, value: str) -> str:
        for highlight in self.ihighlight_values:
            if found_results := re.findall(f"({highlight})+", value, re.IGNORECASE):
                for found in found_results:
                    value = value.replace(found, f"{FG.orange}{BG.lightgrey}{CMD.bold}{found}{CMD.reset}")
        return value

    def _check_is_value_operator_used(self, key_list: list) -> bool:
        return any([True for key in key_list if self.parse_key(key)[2]])
