from fastapi import Request
import subprocess
import os
from pathlib import Path
import io
import datetime

HOME = Path.home()
LOG_DIR = HOME / 'logs' / 'arson-dev'

def log_event(event: str, log_file: Path , execution_queue: list[str]):
    with open(log_file, 'a') as log:
        log.write(f"[{len(execution_queue)}] - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}\n")

def execute_command(command: str, cwd: Path, log_file: io.TextIOWrapper, execution_queue: list[str]) -> int:
    log_event(f"Executing command: {command} in {cwd}", Path(log_file.name), execution_queue)
    status = subprocess.run(command, shell=True, cwd=cwd, stdout=log_file, stderr=log_file).returncode

    return status

def redeploy_service_factory(steps: list[str], log_file_path: Path = LOG_DIR, execution_queue: list[str] = []):
    def redeploy_service(name: str, log_file_name: str):
        for i, step in enumerate(steps, 1):
            with open(log_file_path / log_file_name, 'a') as log_file:
                log_file.write(f'Step {i} for {name}: {step.format(name=name)}\n')

                command = step.format(name=name)

                execution_queue.append(command)
                status = execute_command(command, HOME / 'arson.dev' / name, log_file, execution_queue)

                log_file.write(f'Step {i} for {name} completed with status {status}\n')

        return execution_queue

    return redeploy_service


redeploy_sveltekit = redeploy_service_factory(['npm i', 'npm run build', 'pm2 restart {name}'])
redeploy_fastapi = redeploy_service_factory(['../.venv/bin/python -m pip install -r requirements.txt', 'systemctl --user restart {name}'])

SERVICES = {
    'archive': redeploy_sveltekit,
    'blog': redeploy_sveltekit,
    'md': redeploy_fastapi,
    'webhooks': redeploy_fastapi,
}


async def handler(request: Request):
    data = await request.json()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os.makedirs(LOG_DIR, exist_ok=True)

    logfile = f'redeploy-{now}.log'

    execution_queue = []

    with open(LOG_DIR / logfile, 'a') as log:
        log_event(f"Received request with data: {data}", LOG_DIR / logfile, execution_queue)

        execution_queue.append('git pull')
        execute_command('git pull', HOME / 'arson.dev', log, execution_queue)

    changed_files = []

    for file in data.get('commits', []):
        for changed_file in file.get('added', []) + file.get('removed', []) + file.get('modified', []):
            changed_files.append(changed_file)

    for file in changed_files:
        root = Path(file).parts[0]

        with open(LOG_DIR / logfile, 'a') as log_file:
            log_file.write(f"Processing file: {file} with root {root!r}\n")

        if root in SERVICES:
            log_event("Redeploying service: {root}", LOG_DIR / logfile, execution_queue)
            execution_queue = SERVICES[root](root, logfile)

    log_event(f"Redeployment process completed, commands run: {execution_queue}", LOG_DIR / logfile, execution_queue)

    return 200


