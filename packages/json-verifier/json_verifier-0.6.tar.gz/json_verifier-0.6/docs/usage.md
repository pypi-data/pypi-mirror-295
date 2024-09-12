# Usage

## Sample Test


```python
from json_verifier import JsonVerifier

def test_demo():
    with JsonVerifier({"metadata": {"name": "foo", "version": "1.0"}}) as verifier:
        verifier.verify_value("metadata.name", "foo")
        verifier.verify_value("metadata.version", "1.0")
```

## Specifying a Different Separator

By default, the key path such as "metadata.name" uses a period (dot) as separator. There are cases where we cannot use the period. Consider the following data:

```json
{
    "support": {
        "versions": {
            "1.1": true,
            "1.2": true,
        }
}
```

Since the keys "1.1", "1.2" contains dot, we cannot use the dots as separator. In which case, we should use an alternative:

```python
def test_demo():
    data = {
        "support": {
            "versions": {
                "1.1": True,
                "1.2": True,
            }
    }
    with JsonVerifier(data, separator="/") as verifier:
        verifier.verify_value("support/versions/1.1", True)
        verifier.verify_value("support/versions/1.2", True)
```

## Use List or Tuple as Key Path

In cases where we cannot use any single character as separator, we should use list or tuple as key paths:

```python
def test_demo():
    data = {
        "metadata": {
            "name/id": "foo",
            "user.shell": "bash",
        }
    }
    with JsonVerifier(data) as verifier:
        verifier.verify_data(("metadata", "name/id"), "foo")
        verifier.verify_data(["metadata", "user.shell"], "bash")
```
