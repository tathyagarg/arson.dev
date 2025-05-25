from fastapi import Request
import subprocess
import os
from pathlib import Path

HOME = Path.home()
LOGFILE = HOME / 'logs' / 'arson-dev.log'

def redeploy_service_factory(steps: list[str], log_file_path: Path = LOGFILE):
    def redeploy_service(name: str):
        for i, step in enumerate(steps, 1):
            with open(log_file_path, 'a') as log_file:
                log_file.write(f'Step {i} for {name}: {step}\n')

                status = subprocess.run(step.format(name=name), shell=True, cwd=HOME / 'arson.dev' / name, stdout=log_file, stderr=log_file).returncode

                log_file.write(f'Step {i} for {name} completed with status {status}\n')

    return redeploy_service


redeploy_sveltekit = redeploy_service_factory(['npm i', 'npm run build', 'pm2 restart {name'])
redeploy_fastapi = redeploy_service_factory(['source ../.venv/bin/activate', 'pip install -r requirements.txt', 'systemctl --user restart {name}'])

SERVICES = {
    'archive': redeploy_sveltekit,
    'blog': redeploy_sveltekit,
    'md': redeploy_fastapi,
    'webhooks': redeploy_fastapi,
}


async def handler(request: Request):
    data = await request.json()

    with open(LOGFILE, 'a') as log_file:
        log_file.write(f"Received data: {data}\n")
        subprocess.run("git pull", shell=True, cwd=HOME / 'arson.dev', stdout=log_file, stderr=log_file)

    changed_files = []

    for file in data.get('commits', []):
        for changed_file in file.get('added', []) + file.get('removed', []) + file.get('modified', []):
            changed_files.append(changed_file)

    for file in changed_files:
        root, _ = os.path.split(file)
        if root in SERVICES:
            SERVICES[root](root)

    return 200


