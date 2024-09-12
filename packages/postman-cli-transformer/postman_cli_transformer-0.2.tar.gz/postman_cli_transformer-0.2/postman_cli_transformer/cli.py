from datetime import datetime
import click
import json
import sys
import io

from postman_cli_transformer.junit_transformer import junit_transform
from postman_cli_transformer.processor import Processor


@click.command()
@click.argument("output", type=click.File("w"), default="-", required=False)
@click.option(
    "--junit-out-file",
    required=False,
    type=click.File("w"),
    help="File location to output junit xml file from transformed CLI results.",
)
@click.version_option()
def cli(output, junit_out_file):
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
    Output json to file foo.json and output junit xml to file bar.xml :
        postman-cli-transformer foo.json --junit-out-file bar.xml

    """

    stdin_data = sys.stdin.read()

    parsed_stdin = parse(stdin_data)

    if junit_out_file:
        current_time_of_test_run = datetime.now().isoformat()

        results = junit_transform(json.loads(parsed_stdin), current_time_of_test_run)
        junit_out_file.write(results)

    output.write(parsed_stdin)
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
