#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import os
import signal
import sys
from argparse import ArgumentParser
from argcomplete import autocomplete
from argparse import Namespace
from al78tools.pysetup.tools import get_file_content
from al78tools.pysetup.first_run import first_run_decorator
from jsongrep.libs.json_filter import JsonFilter, JsonFilterException


APP = "json-grep"
VERSION = get_file_content(os.path.join(os.path.dirname(__file__), "VERSION"))


@first_run_decorator(APP, VERSION)
def _handle_first_run():
    import subprocess
    result = subprocess.run([os.path.join(os.path.dirname(__file__), "postinstall.sh")])
    if result.returncode != 0:
        print("Postinstall script failed. Autocomplete will not work properly.")


def _handle_exit(sig, frame):
    print('Terminated.')
    sys.exit(0)


def _handle_args() -> Namespace:
    
    parser = ArgumentParser(description="JSON GREP v{version} is utility for filtering selected keys from json string piped from STDOUT".format(version=VERSION))
    parser.add_argument("filter_keys", type=str, nargs="+", help=(
        "List of keys which you want to filter from json dict. "
        "If key is in deeper level of tree structure use '.' separator "
        "to specify how deep is key in dict tree structure. You can also use '*' "
        "at the end of key name to filter keys as 'beginning with'. "
        "You can also specify value of item which you want to pass "
        "only by operator '=' or '~'. '~' means "
        "that value is somewhere in string.")
                        )
    parser.add_argument("-e", "--exclude", type=str, dest="exclude_keys", action="append", default=[], help="Exclude lines contains key or key=value combination")
    parser.add_argument("-m", "--multiline-output", dest="multiline_output", default=False, action="store_true", help="Use multiline output for filtered result")
    parser.add_argument("-v", "--values_only", dest="values_only", default=False, action="store_true", help="Show only values without keys description")
    parser.add_argument("-l", "--hl", type=str, dest="highlight", action="append", help="Highlight case sensitively words in filtered results")
    parser.add_argument("-i", "--ihl", type=str, dest="ihighlight", action="append", help="Highlight case insensitively words in filtered results")
    parser.add_argument("-s", "--show-errors", dest="show_errors", default=False, action="store_true", help="Show errors caused by json decode")
    parser.add_argument("-p", "--pass-non-json", dest="pass_non_json", default=False, action="store_true", help="Pass non json lines into stdout")
    parser.add_argument("-f", "--file", type=str, dest="input_file", help="Input file instead of PIPE")

    autocomplete(parser)
    args = parser.parse_args()
    return args


def read_input_file(path: str) -> list[str]:
    with open(path, "r") as f:
        while line := f.readline():
            yield line


def main():
    
    signal.signal(signal.SIGINT, _handle_exit)
    _handle_first_run()
    args = _handle_args()

    json_filter = JsonFilter(args.filter_keys, args.exclude_keys)
    json_filter.multiline_output = args.multiline_output
    json_filter.values_only = args.values_only
    json_filter.highlight_values = args.highlight
    json_filter.ihighlight_values = args.ihighlight
    json_filter.pass_non_json = args.pass_non_json

    try:
        input_lines = read_input_file(args.input_file) if args.input_file else sys.stdin
    except Exception as ex:
        print(f"I/O error: {ex}")
        exit(1)

    for line in input_lines:
        try:
            filtered_data = json_filter.filter_keys_and_values(line)
            if isinstance(filtered_data, dict):
                output = json_filter.format_result(filtered_data)
                sys.stdout.write(output)
            elif isinstance(filtered_data, str):
                sys.stdout.write(filtered_data)
        except JsonFilterException as ex:
            if args.show_errors:
                sys.stderr.write("\33[31mJsonFilterException\33[0m: {}\n".format(ex))
    print("DONE.")


if __name__ == '__main__':
    main()
