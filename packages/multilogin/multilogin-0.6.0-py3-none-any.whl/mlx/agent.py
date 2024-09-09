import datetime as dt
import tempfile
from functools import wraps
import contextlib
import logging
import time
import os
import subprocess

import psutil
from rich import print


from rich.console import Console
from rich.table import Table


import pdb

from mlx.misc.util import non_recursive


if "DEBUG" in os.environ:

    def handle_exception(exc_type, exc_value, exc_traceback):
        pdb.post_mortem(exc_traceback)

    import sys

    # Set the custom exception handler
    sys.excepthook = handle_exception


@contextlib.contextmanager
def suppress_output():
    """
    Suppress the output of the rich library
    """
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        yield


@non_recursive
def pid_pprint(func):
    console = Console()

    @wraps(func)
    def wrapper(*args, **kwargs):
        import humanize

        # Run the wrapped function and capture the main process PID
        pid = func(*args, **kwargs)

        # pid might be a proc
        if hasattr(pid, "pid"):
            pid = pid.pid

        # Use psutil to get the parent process and all its child processes
        if not pid:
            return
        try:
            parent = psutil.Process(int(pid))
            children = parent.children(recursive=True)  # Get all children recursively

            # Create a table for the parent process
            parent_table = Table(title="Main Process")
            parent_table.add_column(
                "Attribute", justify="right", style="cyan", no_wrap=True
            )
            parent_table.add_column("Value", style="magenta")

            parent_table.add_row("PID", str(parent.pid))
            parent_table.add_row("Name", parent.name())
            parent_table.add_row("Command Line", " ".join(parent.cmdline()))
            parent_table.add_row("Status", parent.status())
            parent_table.add_row(
                "Started at",
                humanize.naturaltime(dt.datetime.fromtimestamp(parent.create_time())),
            )

            # Print the parent process details
            console.print(parent_table)

            # Create a table for child processes
            if children:
                children_table = Table(title="Child Processes")
                children_table.add_column(
                    "PID", justify="right", style="cyan", no_wrap=True
                )
                children_table.add_column("Name", style="magenta")
                children_table.add_column("Command Line", style="green")
                children_table.add_column("Status", style="yellow")
                children_table.add_column("Started at", style="blue")

                for child in children:
                    children_table.add_row(
                        str(child.pid),
                        child.name(),
                        " ".join(child.cmdline()),
                        child.status(),
                        humanize.naturaltime(
                            dt.datetime.fromtimestamp(child.create_time())
                        ),
                    )

                # Print the child processes details
                console.print(children_table)
            else:
                console.print("[bold red]No child processes found.[/bold red]")

        except psutil.NoSuchProcess:
            console.print(f"[bold red]No process found with PID {pid}[/bold red]")

        return pid

    return wrapper


class AgentController:
    """
    Controls the MLX agent process.
    """

    def path(self, path="/opt/mlx/agent.bin"):
        """
        Configured agent path
        """
        return path

    # @pid_detach
    @pid_pprint
    def start(self, xvfb_run=False, timeout=3):
        """
        Start the MLX agent daemon.
        """
        if os.geteuid() == 0:
            raise RuntimeError(
                "This script should not be run as root. Please run as a regular user."
            )

        if pid := self.status():
            return

        if not self.path():
            raise RuntimeError("Agent path not set.")

        print("Starting MLX agent{}...".format(" with xvfb-run" if xvfb_run else ""))
        command = [self.path()]
        command = ["xvfb-run"] + command if xvfb_run else command

        log_file = tempfile.mktemp(
            prefix="mlx-cli-agent", dir=os.path.expanduser("~/mlx/logs/")
        )
        stderr = proc = subprocess.Popen(
            ["nohup", *command],
            cwd="/",
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=open(
                log_file,
                "a",
            ),
            preexec_fn=os.setpgrp,
            close_fds=True,
            # shell=False,
            # close_fds=True,
            # start_new_session=True,  # Creates a new session (detaches from controlling terminal)
            # universal_newlines=True,
        )

        started_at = time.time()

        with open(log_file, "r") as stderr:
            while (exit_code := proc.poll()) is None:
                if time.time() - started_at >= timeout:
                    break
            else:
                if stderr_output := stderr.read():
                    print("MLX Agent error:", stderr_output)
                    if "cannot open display" in stderr_output and not xvfb_run:
                        return self.start(xvfb_run=True)
                raise RuntimeError("Process exited with code", exit_code)

            return proc

    def stop(self):
        """
        Stop the MLX agent process.
        """
        import signal

        # Disable rich printing

        with suppress_output():
            pid = self.status()
        # Get the agent PID
        if pid:
            os.killpg(os.getpgid(int(pid)), signal.SIGTERM)
            print("Agent stopped successfully")
        else:
            print("Agent not running")

    def restart(self):
        """
        Restart the MLX agent process.
        """
        self.stop()
        self.start()

    def logs(self):
        """
        Get the logs from the MLX agent process.
        """
        import os
        import subprocess

        # Define the directory containing logs
        log_dir = os.path.expanduser("~/mlx/logs/")

        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            raise FileNotFoundError(f"Log directory {log_dir} does not exist")

        # Get all files in the log directory
        log_files = os.listdir(log_dir)

        # Filter for files that match the "agent*.log" pattern
        agent_logs = [
            x for x in log_files if x.startswith("agent") and x.endswith(".log")
        ]

        if not agent_logs:
            raise FileNotFoundError("No agent log files found")

        # Get the latest log file based on modification time
        latest_log = max(
            agent_logs, key=lambda f: os.path.getctime(os.path.join(log_dir, f))
        )

        # Construct full path to the latest log file
        latest_log_path = os.path.join(log_dir, latest_log)

        # Run the tail -F command on the latest log file
        subprocess.run(["tail", "-F", latest_log_path])

    @pid_pprint
    def status(self):
        """
        Shows whether the agent is running and returns the parent PID only.
        """
        import subprocess

        try:
            # Fetch the parent PID by using ps with grep and filtering for the process itself
            pid = (
                subprocess.check_output(["pgrep", "-o", "-f", self.path()])
                .decode()
                .strip()
            )
            print(f"MLX agent running on PID {pid}")
            return pid
        except subprocess.CalledProcessError:
            print("MLX agent NOT running")
            return
