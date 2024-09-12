import logging
import subprocess
from collections import defaultdict
from pathlib import Path
import platform

from click import command, option
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler())

@command()
@option('--all', is_flag=True, help='See all processes.')
@option('--include-ports', "-i", default='', help='Comma-separated list of ports to include.')
@option('--exclude-ports', "-x", default='', help='Comma-separated list of ports to exclude.')
@option('--page', is_flag=True, help='Page the output.')
@option("--log-level", "-l", default="info")
def cli(all, include_ports, exclude_ports, page, log_level: str) -> None:
    logging.basicConfig(level=log_level.upper())
    include_ports = set(include_ports.split(',')) if include_ports else set()
    exclude_ports = set(exclude_ports.split(',')) if exclude_ports else set()

    output = subprocess.check_output(["lsof", "-i", "-P", "-n"], text=True)
    lines = output.splitlines()[1:]  # Skip the header line

    table = Table(show_header=True, header_style="bold magenta", padding=(1, 1))

    table.add_column("Process", style="bold green")
    table.add_column("Ports", style="bold yellow")
    table.add_column("Path")
    table.add_column("Command Line", style="blue")

    data = defaultdict(lambda: {"ports": set(), "path": "N/A", "cmdline": "N/A"})
    pid_to_process = {}

    for line in lines:
        parts = line.split()
        logger.debug(parts)
        if len(parts) > 8 and ':' in parts[8]:
            pid = parts[1]
            process_name = parts[0]
            port = parts[8].split(':')[-1]
            if (include_ports and port not in include_ports) or (exclude_ports and port in exclude_ports):
                continue
            data[process_name]["ports"].add(port)
            pid_to_process[pid] = process_name

    if platform.system() == "Linux":
        for pid, process_name in pid_to_process.items():
            try:
                cmdline_output = subprocess.check_output(["ps", "-p", pid, "-o", "command="], text=True).strip()
                path = Path(f"/proc/{pid}/exe").resolve() if Path(f"/proc/{pid}/exe").exists() else "N/A"
                data[process_name]["cmdline"] = cmdline_output
                data[process_name]["path"] = str(path)
            except Exception as e:
                logger.error(f"Error processing PID {pid}: {e}")
    elif platform.system() == "Darwin":  # macOS
        try:
            lsof_output = subprocess.check_output(["lsof", "-p", ",".join(pid_to_process.keys()), "-Fn"], text=True).strip().split('\n')
            current_pid = None
            for line in lsof_output:
                if line.startswith('p'):
                    current_pid = line[1:]
                elif line.startswith('n') and current_pid:
                    path = line[1:]
                    process_name = pid_to_process[current_pid]
                    data[process_name]["path"] = path
            ps_output = subprocess.check_output(["ps", "-p", ",".join(pid_to_process.keys()), "-o", "pid,command="], text=True).strip().split('\n')
            for line in ps_output[1:]:
                parts = line.split(maxsplit=1)
                pid = parts[0]
                cmdline = parts[1]
                process_name = pid_to_process[pid]
                data[process_name]["cmdline"] = cmdline
        except Exception as e:
            logger.error(f"Error processing PIDs: {e}")

    for process_name, info in data.items():
        table.add_row(process_name, ', '.join(sorted(info["ports"])), info["path"], info["cmdline"])

    console = Console()
    if page:
        with console.pager():
            console.print(table)
    else:
        console.print(table)

if __name__ == '__main__':
    cli()