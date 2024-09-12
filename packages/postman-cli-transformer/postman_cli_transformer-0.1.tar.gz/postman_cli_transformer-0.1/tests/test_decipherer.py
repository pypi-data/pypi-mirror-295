from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.decipherer import LINE_TYPES


def test_identification_of_folder_line():
    folder_line = "❏ Regions\n"
    result = line_decipherer(folder_line)

    assert result == LINE_TYPES.FOLDER_LINE


def test_identification_of_successful_test_line():
    test_line = "  ✓  Response status code is 200\n"
    result = line_decipherer(test_line)

    assert result == LINE_TYPES.TEST_LINE


def test_identification_of_failed_test_line():
    test_line = "  1. Region object structure is as expected\n"
    result = line_decipherer(test_line)

    assert result == LINE_TYPES.TEST_LINE


def test_identification_of_a_request_line():
    request_line = "↳ Fetch all regions\n"
    result = line_decipherer(request_line)

    assert result == LINE_TYPES.REQUEST_LINE


def test_identification_of_a_root_request_line():
    request_line = "→ Deactivate a user\n"
    result = line_decipherer(request_line)

    assert result == LINE_TYPES.ROOT_REQUEST_LINE


def test_identification_of_a_get_url_line():
    url_line = (
        "  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    )
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_a_post_url_line():
    url_line = (
        "  POST https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    )
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_a_put_url_line():
    url_line = (
        "  PUT https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    )
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_a_patch_url_line():
    url_line = (
        "  PATCH https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    )
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_a_delete_url_line():
    url_line = (
        "  DELETE https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    )
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_a_head_url_line():
    url_line = (
        "  HEAD https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    )
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_a_options_url_line():
    url_line = "  OPTIONS https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 114ms]\n"
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.URL_LINE


def test_identification_of_empty_line():
    url_line = "  \n"
    result = line_decipherer(url_line)

    assert result == LINE_TYPES.EMPTY_LINE


def test_identification_of_summary_table_by_table_start():
    table_line = (
        "┌─────────────────────────┬────────────────────┬───────────────────┐\n"
    )
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.SUMMARY_LINE


def test_identification_of_summary_table_by_table_side():
    table_line = (
        "│                         │           executed │            failed │\n"
    )
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.SUMMARY_LINE


def test_identification_of_summary_table_by_table_branch():
    table_line = (
        "├─────────────────────────┼────────────────────┼───────────────────┤\n"
    )
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.SUMMARY_LINE


def test_identification_of_summary_table_by_table_end():
    table_line = (
        "└──────────────────────────────────────────────────────────────────┘\n"
    )
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.SUMMARY_LINE


def test_identification_of_error_header():
    table_line = "  #  failure         detail\n"
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.ERROR_HEADER_LINE


def test_identification_of_start_of_error():
    table_line = " 1.  AssertionError  Region object structure is as expected\n"
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.ERROR_LINE


def test_identification_of_body_of_error():
    table_line = "                     expected null to be a number \n"
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.ERROR_LINE


def test_identification_of_info_result():
    table_line = "Postman CLI run data uploaded to Postman Cloud successfully.\n"
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.INFO_LINE


def test_identification_of_view_result():
    table_line = "You can view the run data in Postman at: https://go.postman.co/workspace/71a6b37b-a01d-43b4-bcf2-4cc75f1d3d7b/run/33123329-bcea4e4e-cb2b-481d-b681-d9db0b00784b\n"
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.INFO_LINE


def test_fallthrough_identification():
    table_line = "askjhfakjsbqjwrebfpqowibaoiwecnnasdh*&&&"
    result = line_decipherer(table_line)

    assert result == LINE_TYPES.UNKNOWN_LINE


def test_run_the_decipherer_against_every_line_in_a_file():
    expected_results = [
        "UNKNOWN",
        "EMPTY",
        "UNKNOWN",
        "EMPTY",
        "FOLDER",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "FOLDER",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "FOLDER",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "TEST",
        "TEST",
        "TEST",
        "EMPTY",
        "FOLDER",
        "REQUEST",
        "EMPTY",
        "URL",
        "TEST",
        "TEST",
        "EMPTY",
        "ROOT_REQUEST",
        "EMPTY",
        "URL",
        "URL",
        "EMPTY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "SUMMARY",
        "EMPTY",
        "ERROR_HEADER",
        "EMPTY",
        "ERROR",
        "ERROR",
        "ERROR",
        "ERROR",
        "EMPTY",
        "ERROR",
        "ERROR",
        "ERROR",
        "ERROR",
        "EMPTY",
        "INFO",
        "INFO",
    ]

    raw_file = []
    results = []

    with open("tests/test_data/postman-cli-run.txt") as file:
        while line := file.readline():
            raw_file.append(line)

    for line in raw_file:
        results.append(line_decipherer(line))

    assert results == expected_results
