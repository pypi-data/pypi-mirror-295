from json_verifier import JsonVerifier


def call_api():
    return {"metadata": {"name": "sandbox", "tags": ["scratch", "pre-production", "experimental"]}}


def test_api():
    actual = call_api()
    with JsonVerifier(actual) as verifier:
        verifier.verify_value("metadata.name", "staging")
        verifier.verify_value("metadata.description", "Team sandbox")
        verifier.verify_value("metadata.tags.0", "testing")
        verifier.verify_value("metadata.tags.3", "non-production")
