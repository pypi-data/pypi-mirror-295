# json-verifier

`json-verifier` is a package which allows a test to spot-check various values of a JSON object. 

## Installation

```console
pip install json-verifier
```

## Why do We Need It?

Let's pretend that we are testing an API, which returns a JSON object such as:

```json
{
    "metadata": {
        "name": "sandbox",
        "tags": ["scratch", "pre-production", "experimental"]
    }
}
```

Let say we need to check a few things:

1. The name must be "staging"
2. The description must be "Team sandbox"
3. The first tag must be "testing"
4. The fourth tag must be "non-production"

A typical test then would look like this:

```python
def test_api():
    actual = call_api()
    assert actual["metadata"]["name"] == "staging"
    assert actual["metadata"]["description"] == "Team sandbox"
    assert actual["metadata"]["tags"][0] == "testing"
    assert actual["metadata"]["tags"][3] == "non-production"
```

While this test works, it contains a couple of issues:

1. We want to check for all issues, but the above will stop at the first assertion failure and will not test the rest
2. Notice that the actual value does not contain a "description" value. That means the expression `actual["metadata"]["description"]` will generate a `KeyError` exception
3. Likewise, the expression `actual["metadata"]["tags"][3]` will generate an `IndexError` exception
4. It would be nice to be able to shorthand the keys, especially when dealing with a deeply nested JSON object

`json-verifier` is looking to address these issues. Consider the following test:

```python
from json_verifier import JsonVerifier

def test_api(verifier):
    actual = call_api()
    with JsonVerifier(actual) as verifier:
        verifier.verify_value("metadata.name", "staging")
        verifier.verify_value("metadata.description", "Team sandbox")
        verifier.verify_value("metadata.tags.0", "testing")
        verifier.verify_value("metadata.tags.3", "non-production")
```

Here is a sample `pytest` output:

```none
AssertionError: Verify JSON failed
Object:
{
    "metadata": {
        "name": "sandbox",
        "tags": [
            "scratch",
            "pre-production",
            "experimental"
        ]
    }
}
Errors:
- path='metadata.name', expected='staging', actual='sandbox'
  /home/user/workspace/test_api.py(11) in test_api()
          verifier.verify_value("metadata.name", "staging")

- path='metadata.description', expected='Team sandbox', key error: 'description'
  /home/user/workspace/test_api.py(12) in test_api()
          verifier.verify_value("metadata.description", "Team sandbox")

- path='metadata.tags.0', expected='testing', actual='scratch'
  /home/user/workspace/test_api.py(13) in test_api()
          verifier.verify_value("metadata.tags.0", "testing")

- path='metadata.tags.3', expected='non-production', index error: 3
  /home/user/workspace/test_api.py(14) in test_api()
          verifier.verify_value("metadata.tags.3", "non-production")

This output shows some important information:

1. A formatted dump of the object under test
2. A list of errors. Each complete with filename, line number, the function, the offending line, and why test failed
```


## License

`json-verifier` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
