"""
common.py

Library code used by many functions.
"""
import logging.config
import subprocess

logger = logging.getLogger(__name__)


def run_command(command):
    """
    Run the command specified and return any output to stdout or stderr as
    a list of strings.
    :param str command: The complete command to run.
    :returns: Any output from the command as a list of strings.
    :raises RuntimeError: If the command did not complete successfully.
    """
    try:
        cmd_out = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                          shell=True)
    except subprocess.CalledProcessError as exc:
        msg = ('Command did not complete sucessfully.\ncommmand:\n{}\n'
               'produced error:\n{}'.format(command, exc.output))
        logger.warning(msg)
        raise RuntimeError(msg)

    if isinstance(cmd_out, str):
        return cmd_out.rstrip().split('\n')
    else:
        return None
