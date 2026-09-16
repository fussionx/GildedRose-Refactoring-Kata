import io
import sys

from approvaltests import Options, verify
from approvaltests.reporters import PythonNativeReporter

from texttest_fixture import main

# Print the diff to stdout on a mismatch rather than launching a GUI diff tool,
# so the test behaves identically locally, headless and in CI.
REPORTER = PythonNativeReporter()


def test_gilded_rose_approvals():
    orig_sysout = sys.stdout
    try:
        fake_stdout = io.StringIO()
        sys.stdout = fake_stdout
        sys.argv = ["texttest_fixture.py", 30]
        main()
        answer = fake_stdout.getvalue()
    finally:
        sys.stdout = orig_sysout

    verify(answer, options=Options().with_reporter(REPORTER))


if __name__ == "__main__":
    test_gilded_rose_approvals()
