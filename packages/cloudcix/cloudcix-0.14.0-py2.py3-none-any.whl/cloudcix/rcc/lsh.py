# Local Shell(lsh) for running commands on local machine
import subprocess
from typing import Tuple
# local
from cloudcix.rcc.exceptions import CouldNotExecuteException


def comms_lsh(payload: str) -> Tuple[int, str, str]:
    try:
        # Run the command, capture stdout and stderr
        process = subprocess.Popen(payload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output and error
        exit_code, output, error = process.communicate()

        # Check if there was an error
        if process.returncode != 0:
            err = f'Error executing command "{payload}": {error.decode()}'
            raise CouldNotExecuteException(err)

    except Exception as e:
        err = f'Error executing command "{payload}": {str(e)}'
        raise CouldNotExecuteException(err)

    return exit_code, output.decode(), error.decode()
