import click
import json
import sys
import io

from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.unicode_constants import *
from postman_cli_transformer.processor import Processor


@click.command()
@click.argument("output", type=click.File("w"), default="-", required=False)
@click.option(
    "-uf",
    "--unicode-out-file",
    required=False,
    type=click.File("w"),
    help="""file location to output unicode codes of characters from STDIN.
              Each charachter is represented as (<original character> - <unicode of character>)
              Line breaks(10) are preserved but not given a representation""",
)
# @click.option(
#     "-t",
#     "--extract-tags",
#     required=False,
#     type=click.BOOL,
#     help="""undeveloped, but will eventually extract tags from tests descriptions""",
# )
@click.version_option()
def cli(output, unicode_out_file):
    """This script will take as input the STDOUT from
    a Postman CLI collection run and transform the
    output text to a file containing the output data
    organized in a JSON format. This JSON data is then
    written into a specific file.

    \b
    Output to stdout:
        postman-cli-transformer

    \b
    Output to file foo.json:
        postman-cli-transformer foo.json

    \b
    Output to file foo.json and extract tags from tests:
        postman-cli-transformer foo.json --extract-tags

    """

    stdin_data = sys.stdin.read()

    parsed_stdin = parse(stdin_data)

    if unicode_out_file:
        process_as_unicode(io.StringIO(stdin_data), unicode_out_file)

    output.write(parsed_stdin)
    output.flush()


def process_as_unicode(file, output):
    for line in file:
        for char in line:
            unicodeInt = ord(char)
            if unicodeInt != 10:
                output.write(" (%c - %s) " % (char, unicodeInt))
            else:
                output.write(char)

    output.flush()


def parse(data):
    raw_lines = []
    data_as_file = io.StringIO(data)
    for line in data_as_file:
        raw_lines.append(line)

    processor = Processor(raw_lines)
    results = processor.parsed

    json_str = json.dumps(results)

    return json_str
