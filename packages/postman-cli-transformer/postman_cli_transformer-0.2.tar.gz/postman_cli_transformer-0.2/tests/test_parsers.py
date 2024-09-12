from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.parsers import parse_folder
from postman_cli_transformer.parsers import parse_request


def test_successful_test_parsing():
    test_line = "  \u2713  Response status code is 200\n"
    assert parse_test(test_line) == {
        "desc": "Response status code is 200",
        "status": {
            "result": "SUCCESS",
            "error_id": "",
            "details": {},
        },
    }


def test_failed_test_parsing():
    test_line = "  1. Region object structure is as expected\n"
    assert parse_test(test_line) == {
        "desc": "Region object structure is as expected",
        "status": {
            "result": "FAILED",
            "error_id": "1",
            "details": {},
        },
        # Note: actual order details get added at the end of the doc parsing
    }


def test_url_parsing():
    url_line = "  GET https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota [200 OK, 1.82kB, 83ms]\n"
    assert parse_url(url_line) == {
        "url": "https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota",
        "httpVerb": "GET",
        "response": {"code": "200 OK", "size": "1.82kB", "time": "83ms"},
    }


def test_folder_parsing():
    folder_line = "❏ Repeats / Regions Copy\n"
    assert parse_folder(folder_line) == {
        "name": "Repeats / Regions Copy",
        "requests": [],
    }


def test_request_parsing():
    request_line = "↳ Get location and machine counts\n"

    assert parse_request(request_line) == {
        "name": "Get location and machine counts",
        "urls": [],
        "tests": [],
    }
