import pytest

from json_verifier import JsonVerifier


def test_split_non_default():
    verifier = JsonVerifier({}, separator="/")
    assert verifier.split_path("a/b.c/d") == ["a", "b.c", "d"]


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        pytest.param(5, [5], id="int"),
        pytest.param(True, [True], id="bool"),
        pytest.param("foo", ["foo"], id="single key"),
        pytest.param("a.b.c", ["a", "b", "c"], id="multiple keys"),
    ],
)
def test_split_path(path, expected):
    verifier = JsonVerifier({})
    assert verifier.split_path(path) == expected


@pytest.mark.parametrize(("path"), [(set("abc")), frozenset("abc")])
def test_set_type(path):
    verifier = JsonVerifier({})
    with pytest.raises(TypeError):
        verifier.split_path(path)
