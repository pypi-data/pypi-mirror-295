from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.parsers import parse_folder
from postman_cli_transformer.parsers import parse_request
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.decipherer import LINE_TYPES


class Processor:
    def __init__(self, lines_to_process):
        """Initialize the class with a document already
        converted into an array of the lines in the doc.
        This initializer will parse lines and build out
        the json representation of the input. This will
        be stored in the parsed field. Retrieve the
        results with:
            processor = Processor(lines)
            results = processor.parsed
        """

        # Class property definiing
        self.processing_helper = ProcessingHelper()
        self.parsed = {"collectionName": "", "folders": []}
        self.lines_to_process = lines_to_process

        # Get header info out of the way
        self._process_first_rows()
        self._process_rest_of_lines()

    def _process_first_rows(self):
        # First line is 'postman' followed by empty line
        self.lines_to_process.pop(0)
        self.lines_to_process.pop(0)
        # Next line is the collection name followed by enpty line
        self.parsed["collectionName"] = self.lines_to_process[0].strip()
        self.lines_to_process.pop(0)
        # Next line is empty, so skip
        self.lines_to_process.pop(0)
        self.processing_helper.previous_line_type = LINE_TYPES.EMPTY_LINE

    def _process_rest_of_lines(self):
        for line in self.lines_to_process:
            match line_decipherer(line):
                case LINE_TYPES.EMPTY_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.EMPTY_LINE
                    )
                    if (
                        self.processing_helper.previous_line_type
                        == LINE_TYPES.ERROR_LINE
                    ):
                        error = {
                            "type": self.processing_helper.error_type,
                            "detail": "\n".join(self.processing_helper.error_lines),
                        }

                        error_node = self._search_for_error(
                            self.processing_helper.error_id, self.parsed
                        )

                        error_node["details"] = error

                        self.processing_helper.error_lines = []
                        self.processing_helper.error_type = ""
                        self.processing_helper.error_id = ""

                case LINE_TYPES.FOLDER_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.FOLDER_LINE
                    )
                    folder_json = parse_folder(line)
                    self.parsed["folders"].append(folder_json)
                    self.processing_helper.current_folder += 1
                    self.processing_helper.current_request = -1
                case LINE_TYPES.ROOT_REQUEST_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.ROOT_REQUEST_LINE
                    )
                    if self.processing_helper.root_request_folder == -1:
                        folder_json = parse_folder("❏ <REQUESTS_WITHOUT_FOLDER>")
                        self.parsed["folders"].append(folder_json)
                        self.processing_helper.current_folder += 1
                        self.processing_helper.root_request_folder = (
                            self.processing_helper.current_folder
                        )
                        self.processing_helper.current_request = -1

                    request_json = parse_request(line)
                    self.parsed["folders"][self.processing_helper.root_request_folder][
                        "requests"
                    ].append(request_json)
                    self.processing_helper.current_request += 1
                case LINE_TYPES.REQUEST_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.REQUEST_LINE
                    )
                    request_json = parse_request(line)
                    self.parsed["folders"][self.processing_helper.current_folder][
                        "requests"
                    ].append(request_json)
                    self.processing_helper.current_request += 1
                case LINE_TYPES.URL_LINE:
                    self.processing_helper.update_current_line_type(LINE_TYPES.URL_LINE)
                    url_json = parse_url(line)
                    self.parsed["folders"][self.processing_helper.current_folder][
                        "requests"
                    ][self.processing_helper.current_request]["urls"].append(url_json)
                case LINE_TYPES.TEST_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.TEST_LINE
                    )
                    test_json = parse_test(line)
                    self.parsed["folders"][self.processing_helper.current_folder][
                        "requests"
                    ][self.processing_helper.current_request]["tests"].append(test_json)
                case LINE_TYPES.SUMMARY_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.SUMMARY_LINE
                    )
                    if not self.processing_helper.started_table:
                        self.processing_helper.started_table = True
                        self.parsed["summary"] = {
                            "iterations": {},
                            "requests": {},
                            "test-scripts": {},
                            "prerequest-scripts": {},
                            "assertions": {},
                            "totals": {
                                "totalRunDuration": "",
                                "totalDataReceived": "",
                                "responseTimes": {
                                    "average": "",
                                    "min": "",
                                    "max": "",
                                    "s.d.": "",
                                },
                            },
                        }
                    else:
                        summary_parts = line.split()
                        if "iterations" in line:
                            self._add_summary("iterations", summary_parts)
                        elif "requests" in line:
                            self._add_summary("requests", summary_parts)
                        elif "test-scripts" in line:
                            self._add_summary("test-scripts", summary_parts)
                        elif "prerequest-scripts" in line:
                            self._add_summary("prerequest-scripts", summary_parts)
                        elif "assertions" in line:
                            self._add_summary("assertions", summary_parts)
                        elif "run" in line:
                            self.parsed["summary"]["totals"]["totalRunDuration"] = (
                                summary_parts[4]
                            )
                        elif "data" in line:
                            self.parsed["summary"]["totals"]["totalDataReceived"] = (
                                "%s %s" % (summary_parts[4], summary_parts[5])
                            )
                        elif "response" in line:
                            self.parsed["summary"]["totals"]["responseTimes"] = {
                                "average": summary_parts[4],
                                "min": summary_parts[6].rstrip(","),
                                "max": summary_parts[8].rstrip(","),
                                "s.d.": summary_parts[10].rstrip("]"),
                            }
                case LINE_TYPES.ERROR_HEADER_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.ERROR_HEADER_LINE
                    )

                case LINE_TYPES.ERROR_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.ERROR_LINE
                    )
                    error_parts = line.split()

                    if "AssertionError" in line:
                        self.processing_helper.error_id = error_parts[0].rstrip(".")
                        del error_parts[:2]
                        self.processing_helper.error_type = "AssertionError"

                    error_description = " ".join(error_parts)
                    self.processing_helper.error_lines.append(error_description)

    def _add_summary(self, title, parts):
        self.parsed["summary"][title] = {
            "executed": parts[3],
            "failed": parts[5],
        }

    def _search_for_error(self, error_id, results):
        for folder in results["folders"]:
            for request in folder["requests"]:
                for test in request["tests"]:
                    if test["status"]["error_id"] == error_id:
                        return test["status"]


class ProcessingHelper:
    def __init__(self):
        self.previous_line_type = ""
        self.current_line_type = ""
        self.current_folder = -1
        self.current_request = -1
        self.root_request_folder = -1
        self.started_table = False
        self.error_id = ""
        self.error_lines = []
        self.error_type = ""

    def update_current_line_type(self, new_line_type):
        self.previous_line_type = self.current_line_type
        self.current_line_type = new_line_type
