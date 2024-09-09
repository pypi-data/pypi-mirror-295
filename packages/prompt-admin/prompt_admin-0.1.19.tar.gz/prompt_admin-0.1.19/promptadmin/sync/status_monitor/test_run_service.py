import os
import subprocess
import uuid

_process = False


class TestRunService:
    def __init__(self):
        if not os.path.exists('test_reports'):
            os.mkdir('test_reports')

    def run_test(self):
        global _process
        if _process:
            return
        _process = True
        try:
            subprocess.Popen(['pytest', '--json-report', f'--json-report-file=test_reports/{uuid.uuid4()}.json'])
        finally:
            _process = False
