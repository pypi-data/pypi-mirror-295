import types
import re

from postman_cli_transformer.unicode_constants import BOX_ICON
from postman_cli_transformer.unicode_constants import CHECKMARK_ICON
from postman_cli_transformer.unicode_constants import ENTER_ICON
from postman_cli_transformer.unicode_constants import RIGHT_ARROW_ICON
from postman_cli_transformer.unicode_constants import TABLE_PARTS_LIST


LINE_TYPES = types.SimpleNamespace()
LINE_TYPES.FOLDER_LINE = "FOLDER"
LINE_TYPES.TEST_LINE = "TEST"
LINE_TYPES.REQUEST_LINE = "REQUEST"
LINE_TYPES.URL_LINE = "URL"
LINE_TYPES.ROOT_REQUEST_LINE = "ROOT_REQUEST"
LINE_TYPES.EMPTY_LINE = "EMPTY"
LINE_TYPES.SUMMARY_LINE = "SUMMARY"
LINE_TYPES.ERROR_HEADER_LINE = "ERROR_HEADER"
LINE_TYPES.ERROR_LINE = "ERROR"
LINE_TYPES.INFO_LINE = "INFO"
LINE_TYPES.UNKNOWN_LINE = "UNKNOWN"

http_verbs = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]


def line_decipherer(line):
    line = strip_ansi_color_codes(line)

    if line.strip() == "":
        return LINE_TYPES.EMPTY_LINE

    if line[0] == BOX_ICON:
        return LINE_TYPES.FOLDER_LINE

    start_of_test_line = "  " + CHECKMARK_ICON
    if line[:3] == start_of_test_line:
        return LINE_TYPES.TEST_LINE

    # This regex looks at the start of the line for a failed test which could
    # count up to 999 followed by a period. If it is the first failed test it
    # would look like '<space><space>1.' the 100th failed test would look like
    # '100.' so the regex looks for space or digit in the first 2 columns and
    # 0-9 in third followed by a period
    if re.search(r"^[\s\d][\s\d][0-9].", line):
        return LINE_TYPES.TEST_LINE

    if line[0] == ENTER_ICON:
        return LINE_TYPES.REQUEST_LINE

    if line[0] == RIGHT_ARROW_ICON:
        return LINE_TYPES.ROOT_REQUEST_LINE

    if line[0] in TABLE_PARTS_LIST:
        return LINE_TYPES.SUMMARY_LINE

    if line[:12].strip() == "#  failure":
        return LINE_TYPES.ERROR_HEADER_LINE

    # This regex looks at the start of the line for a test error result which
    # could count up to 99 followed by a period. If it is the first error
    # result it would look like '<space>1.  Assertion' the 90th failed test
    # would look like '90.  Assertion' so the regex looks for space or digit
    # in the first column and 0-9 in second followed by a period and the word
    # Assertion. NEED TO DOUBLE CHECK IF IT WILL ALWAYS BE AN ASSERTION ERROR
    # HERE
    if re.search(r"^[\s\d][0-9].  Assertion", line):
        return LINE_TYPES.ERROR_LINE

    if len(line.split()) >= 2:
        if "Error" in line.split()[1]:
            return LINE_TYPES.ERROR_LINE

    if line[:21] == "                     ":
        return LINE_TYPES.ERROR_LINE

    if line[:20] == "Postman CLI run data":
        return LINE_TYPES.INFO_LINE

    if line[:20] == "You can view the run":
        return LINE_TYPES.INFO_LINE

    line_parts = line.split(" ")
    if line_parts[0] == "" and line_parts[1] == "" and line_parts[2] in http_verbs:
        return LINE_TYPES.URL_LINE

    return LINE_TYPES.UNKNOWN_LINE


def strip_ansi_color_codes(text):
    """Removes ANSI color codes from a string."""
    return re.sub(r"\x1b\[[0-9;]*[mG]", "", text)
