import string


def junit_transform(json_to_transform, time_of_tests):
    transformed = []
    transformed.append('<?xml version="1.0" encoding="UTF-8"?>')
    collection_name = json_to_transform["collectionName"]
    total_tests = get_total_number_of_requests(json_to_transform["folders"])
    total_time = calculate_time(
        json_to_transform["summary"]["totals"]["totalRunDuration"]
    )
    transformed.append(
        '<testsuites name="%s" tests="%s" time="%s">'
        % (collection_name, total_tests, total_time)
    )
    for folder in json_to_transform["folders"]:
        folder_name = folder["name"]
        for request in folder["requests"]:
            test_suite_name = "%s / %s" % (folder_name, request["name"])
            compressed_name = compress(test_suite_name)
            number_of_tests = len(request["tests"])
            number_of_failures = len(
                [
                    test
                    for test in request["tests"]
                    if test["status"]["result"] == "FAILED"
                ]
            )
            request_time = sum(
                [calculate_time(url["response"]["time"]) for url in request["urls"]]
            )
            transformed.append(
                '  <testsuite name="%s" timestamp="%s" tests="%s" failures="%s" errors="0" time="%s">'
                % (
                    test_suite_name,
                    time_of_tests,
                    number_of_tests,
                    number_of_failures,
                    request_time,
                )
            )
            for test in request["tests"]:
                test_name = test["desc"]
                if test["status"]["result"] == "FAILED":
                    transformed.append(
                        '    <testcase name="%s" time="%s" classname="%s">'
                        % (test_name, request_time, compressed_name)
                    )
                    failure_type = test["status"]["details"]["type"]
                    error_details = test["status"]["details"]["detail"].split("\n")
                    test_description = error_details[0]
                    error_message = error_details[1]
                    del error_details[:2]
                    stack_trace = "\n".join(error_details)
                    transformed.append(
                        '      <failure type="%s" message="%s">'
                        % (failure_type, error_message)
                    )

                    transformed.append("        <![CDATA[Failed 1 times.]]>")
                    transformed.append(
                        "        <![CDATA[Collection name: %s.]]>" % collection_name
                    )
                    transformed.append(
                        "        <![CDATA[Request name: %s.]]>" % test_suite_name
                    )
                    transformed.append(
                        "        <![CDATA[Test description: %s.]]>" % test_description
                    )
                    transformed.append(
                        "        <![CDATA[Error message: %s.]]>" % error_message
                    )
                    transformed.append(
                        "        <![CDATA[Stacktrace: %s.]]>" % stack_trace
                    )
                    transformed.append("      </failure>")
                    transformed.append("    </testcase>")
                else:
                    transformed.append(
                        '    <testcase name="%s" time="%s" classname="%s"/>'
                        % (test_name, request_time, compressed_name)
                    )
            transformed.append("  </testsuite>")

    transformed.append("</testsuites>")

    return "\n".join(transformed)


def get_total_number_of_requests(folders):
    request_count = 0
    for folder in folders:
        request_count += len(folder["requests"])

    return request_count


def calculate_time(time_in_ms):
    try:
        stripped_time = time_in_ms.rstrip("ms")
        return int(stripped_time) / 1000
    except (ValueError, Exception):
        return 0


def compress(line):
    forward_slash_removed = line.replace("/", "")
    capitalized = string.capwords(forward_slash_removed)
    strip_space = "".join(capitalized.split())

    return strip_space
