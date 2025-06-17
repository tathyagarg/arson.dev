from fastapi import Request
import os
from pathlib import Path
import datetime
from . import HOME, log_event, execute_command
from . import redeploy_fastapi as fastapi_factory
from . import redeploy_pm2 as pm2_factory

LOG_DIR = HOME / 'logs' / 'arson-dev'

fastapi = fastapi_factory(LOG_DIR)
pm2 = pm2_factory(LOG_DIR)

SERVICES = {
    'archive': pm2,
    'blog': pm2,
    'md': fastapi,
    'webhooks': fastapi,
    'cdn': fastapi,
    'uptime': pm2,
    'blocks': pm2,
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
            execution_queue = SERVICES[root](root, logfile, 'arson.dev', execution_queue)

    log_event(f"Redeployment process completed, commands run: {execution_queue}", LOG_DIR / logfile, execution_queue)

    return 200


