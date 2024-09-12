from postman_cli_transformer.processor import Processor

import json


def create_array_from_text(text):
    return text.split("\n")


def test_should_be_able_to_initialize_and_return_json_with_collection_name():
    lines = create_array_from_text("""postman

Pinball Map Collection
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_folders():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions

❏ Machines

❏ Operators""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {"name": "Regions", "requests": []},
            {"name": "Machines", "requests": []},
            {"name": "Operators", "requests": []},
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_urls():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Get location and machine counts

  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]

↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 62ms]

❏ Machines
↳ Fetch all machines

  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Get location and machine counts",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.32kB",
                                    "time": "264ms",
                                },
                            }
                        ],
                        "tests": [],
                    },
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "62ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Fetch all machines",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "65.14kB",
                                    "time": "220ms",
                                },
                            }
                        ],
                        "tests": [],
                    }
                ],
            },
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_tests():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Get location and machine counts

  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields

↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]
  ✓  Response status code is 200
  ✓  Response time is within an acceptable range
  1. Region object structure is as expected
  ✓  All required fields in the 'region' object are present and not empty
  ✓  Region object has correct data types for fields

❏ Machines
↳ Fetch all machines

  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields
  ✓  Response content type is application/json
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Get location and machine counts",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.32kB",
                                    "time": "264ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {
                                    "result": "FAILED",
                                    "error_id": "1",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "All required fields in the 'region' object are present and not empty",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Fetch all machines",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "65.14kB",
                                    "time": "220ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response content type is application/json",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    }
                ],
            },
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_root_level_requests():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Get location and machine counts

  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields

↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  ✓  Response status code is 200
  ✓  Response time is within an acceptable range
  1. Region object structure is as expected
  ✓  All required fields in the region object are present and not empty
  ✓  Region object has correct data types for fields

❏ Machines
↳ Fetch all machines

  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields
  ✓  Response content type is application/json

→ Deactivate a user

  GET https://api.getpostman.com/scim/v2/Users?count=10000 [401 Unauthorized, 485B, 261ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]                                   

→ Change a user

  GET https://api.getpostman.com/scim/v2/Users?count=10000 [401 Unauthorized, 485B, 261ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]                                   
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Get location and machine counts",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.32kB",
                                    "time": "264ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {
                                    "result": "FAILED",
                                    "error_id": "1",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "All required fields in the region object are present and not empty",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Fetch all machines",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "65.14kB",
                                    "time": "220ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response content type is application/json",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "name": "<REQUESTS_WITHOUT_FOLDER>",
                "requests": [
                    {
                        "name": "Deactivate a user",
                        "urls": [
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users?count=10000",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "261ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                    {
                        "name": "Change a user",
                        "urls": [
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users?count=10000",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "261ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                ],
            },
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_the_summary_table():
    lines = create_array_from_text("""postman

Deactivate User Accounts

→ Deactivate a user

  GET https://api.getpostman.com/scim/v2/Users?count=10000 [401 Unauthorized, 485B, 261ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]                                   

→ Change a user

  GET https://api.getpostman.com/scim/v2/Users?count=10000 [401 Unauthorized, 485B, 261ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]                                   

┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                  4 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                  2 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│      prerequest-scripts │                  4 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                  0 │                 0 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 487ms                                        │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 604B (approx)                               │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 103ms [min: 51ms, max: 253ms, s.d.: 86ms] │
└──────────────────────────────────────────────────────────────────┘

Postman CLI run data uploaded to Postman Cloud successfully.
You can view the run data in Postman at: https://go.postman.co/workspace/71a6b37b-a01d-43b4-bcf2-4cc75f1d3d7b/run/33123329-986f44d8-9cda-4445-9179-137678aa1303                             
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Deactivate User Accounts",
        "folders": [
            {
                "name": "<REQUESTS_WITHOUT_FOLDER>",
                "requests": [
                    {
                        "name": "Deactivate a user",
                        "urls": [
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users?count=10000",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "261ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                    {
                        "name": "Change a user",
                        "urls": [
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users?count=10000",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "261ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                ],
            },
        ],
        "summary": {
            "iterations": {"executed": "1", "failed": "0"},
            "requests": {"executed": "4", "failed": "0"},
            "test-scripts": {"executed": "2", "failed": "0"},
            "prerequest-scripts": {"executed": "4", "failed": "0"},
            "assertions": {"executed": "0", "failed": "0"},
            "totals": {
                "totalRunDuration": "487ms",
                "totalDataReceived": "604B (approx)",
                "responseTimes": {
                    "average": "103ms",
                    "min": "51ms",
                    "max": "253ms",
                    "s.d.": "86ms",
                },
            },
        },
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_error_descriptions():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  ✓  Response status code is 200
  ✓  Response time is within an acceptable range
  1. Region object structure is as expected
  ✓  All required fields in the region object are present and not empty
  ✓  Region object has correct data types for fields

❏ Machines
↳ Find if name corresponds to a known region

  GET https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota [200 OK, 1.83kB, 87ms]
  ✓  Response status code is 200
  ✓  Response time is within an acceptable range
  2. Region object structure is as expected
  ✓  All required fields in the region object are present and not empty
  ✓  Region object has correct data types for fields

┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                  4 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                  2 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│      prerequest-scripts │                  4 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                  0 │                 2 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 487ms                                        │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 604B (approx)                               │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 103ms [min: 51ms, max: 253ms, s.d.: 86ms] │
└──────────────────────────────────────────────────────────────────┘

  #  failure                                  detail                                                                                                                                                           
                                                                                                                                                                                                               
 1.  AssertionError                           1Region object structure is as expected                                                                                                                           
                                              2expected null to be a number                                                                                                                                     
                                              xat assertion:2 in test-script                                                                                                                                    
                                              yinside "Regions / Find if name corresponds to a known region"                                                                                                    
                                                                                                                                                                                                               
 2.  AssertionError                           3Region object structure is as expected                                                                                                                           
                                              4expected null to be a number                                                                                                                                     
                                              aat assertion:2 in test-script                                                                                                                                    
                                              binside "Regions / Find if name corresponds to a known region"                                                                                     

Postman CLI run data uploaded to Postman Cloud successfully.
You can view the run data in Postman at: https://go.postman.co/workspace/71a6b37b-a01d-43b4-bcf2-4cc75f1d3d7b/run/33123329-986f44d8-9cda-4445-9179-137678aa1303                             
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {
                                    "result": "FAILED",
                                    "error_id": "1",
                                    "details": {
                                        "type": "AssertionError",
                                        "detail": '1Region object structure is as expected\n2expected null to be a number\nxat assertion:2 in test-script\nyinside "Regions / Find if name corresponds to a known region"',
                                    },
                                },
                            },
                            {
                                "desc": "All required fields in the region object are present and not empty",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Find if name corresponds to a known region",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.83kB",
                                    "time": "87ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {
                                    "result": "FAILED",
                                    "error_id": "2",
                                    "details": {
                                        "type": "AssertionError",
                                        "detail": '3Region object structure is as expected\n4expected null to be a number\naat assertion:2 in test-script\nbinside "Regions / Find if name corresponds to a known region"',
                                    },
                                },
                            },
                            {
                                "desc": "All required fields in the region object are present and not empty",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {
                                    "result": "SUCCESS",
                                    "error_id": "",
                                    "details": {},
                                },
                            },
                        ],
                    },
                ],
            },
        ],
        "summary": {
            "iterations": {"executed": "1", "failed": "0"},
            "requests": {"executed": "4", "failed": "0"},
            "test-scripts": {"executed": "2", "failed": "0"},
            "prerequest-scripts": {"executed": "4", "failed": "0"},
            "assertions": {"executed": "0", "failed": "2"},
            "totals": {
                "totalRunDuration": "487ms",
                "totalDataReceived": "604B (approx)",
                "responseTimes": {
                    "average": "103ms",
                    "min": "51ms",
                    "max": "253ms",
                    "s.d.": "86ms",
                },
            },
        },
    }

    assert json.dumps(results) == json.dumps(expected_results)
