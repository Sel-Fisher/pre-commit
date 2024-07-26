import sys
from datetime import datetime as dt
from pathlib import Path
from xml.sax.saxutils import escape


input_data = Path(sys.argv[1]).read_text()

junit_header = """<?xml version="1.0" encoding="utf-8"?>
<testsuites><testsuite name="pytest" errors="{num_of_test}" failures="0"
skipped="0" tests="{num_of_test}" time="0" timestamp="{dt}" hostname="nebula">
"""
junit_case = """
<testcase classname="" name="{file_name}" file="{file_path}" time="0.000">
<error message="code-style">
{diff}
</error></testcase>
"""
junit_footer = """
</testsuite></testsuites>"""

failed_tests = ""
cnt = 0
diff = ""
file_path = ""
file_name = ""
for line in input_data.split("\n"):
    if "diff --git" in line:
        if diff and file_path:
            cnt += 1
            failed_tests += junit_case.format(
                file_name=file_name, file_path=file_path, diff=escape(diff)
            )
        file_path = line.split(" b/")[-1]
        file_name = file_path.split("/")[-1]
        diff = ""
        continue
    diff += line + "\n"

if diff and file_path:
    cnt += 1
    failed_tests += junit_case.format(
        file_name=file_name, file_path=file_path, diff=escape(diff)
    )

print(
    junit_header.format(num_of_test=cnt, dt=dt.now()),
    failed_tests,
    junit_footer,
)
sys.exit(cnt)