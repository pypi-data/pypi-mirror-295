from __future__ import annotations

import inspect
import io
import json

__all__ = ["JsonVerifier"]


class JsonVerifier:
    """
    Verify a JSON object.

    The caller instantiate an object and use it as a context manager. With
    the context, he/she can perform multiple assertions. Upon exiting
    the context, JsonVerifier will raise a single AssertionError with
    detailed report for all failed assertions.
    """

    def __init__(self, obj, separator="."):
        self.obj = obj
        self.separator = separator
        self._errors = []
        self._context = []

    def verify_value(self, path: str, expected):
        """
        Verify a value exists.

        If there is a problem (key not found, index error, or value is not
        as expected), then a call to tally() will raise the AssertError
        with details to help identifying the problems.

        :param path: A key path, e.g. metadata.name
        :param expected: The expected value
        """
        caller = inspect.stack()[1]
        context = (
            f"{caller.filename}({caller.lineno}) in {caller.function}()",
            *(caller.code_context or []),
        )

        obj = self.obj
        key = ""
        try:
            for key in self.split_path(path):
                obj = obj[int(key)] if isinstance(obj, list) else obj[key]
            if obj != expected:
                self._errors.append(f"{path=}, {expected=}, actual={obj!r}")
                self._context.append(context)
        except KeyError:
            self._errors.append(f"{path=}, {expected=}, key error: {key!r}")
            self._context.append(context)
        except IndexError:
            self._errors.append(f"{path=}, {expected=}, index error: {key}")
            self._context.append(context)
        except ValueError:
            self._errors.append(f"{path=}, {expected=}, index is not int: {key!r}")
            self._context.append(context)

    def tally(self):
        """
        Tally all errors so far.

        If there is at least an error, this function will raise an AssertionError.
        """
        if not self._errors:
            return

        buffer = io.StringIO()
        buffer.write("Verify JSON failed\n")
        buffer.write("Object:\n")
        json.dump(self.obj, buffer, indent=4)
        buffer.write("\nErrors:\n")
        for error, context in zip(self._errors, self._context):
            buffer.write(f"- {error}\n")
            for line in context:
                buffer.write(f"  {line}\n")
        raise AssertionError(buffer.getvalue())

    def split_path(self, path: int | str | list | tuple):
        if isinstance(path, str):
            return path.split(self.separator)

        if isinstance(path, (list, tuple)):
            return path

        # We should not allow set/frozenset as path because the order is
        # non deterministic
        if isinstance(path, (set, frozenset)):
            message = "Set and frozenset are not allowed as path"
            raise TypeError(message)

        # Other scala types
        return [path]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tally()

    @property
    def errors(self):
        """Provide a list of errors incurred."""
        return self._errors[:]
