from fastapi import Request

from datetime import datetime
import os

from . import HOME, log_event, execute_command, redeploy_sveltekit

LOG_DIR = HOME / 'logs' / 'dwmun'

async def handler(request: Request):
    data = await request.json()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os.makedirs(LOG_DIR, exist_ok=True)

    logfile = f'redeploy-{now}.log'

    execution_queue = []

    with open(LOG_DIR / logfile, 'a') as log:
        log_event(f"Received request with data: {data}", LOG_DIR / logfile, execution_queue)

        execution_queue.append('git pull')
        execute_command('git pull', HOME / 'dwmun25', log, execution_queue)

    redeploy_sveltekit(LOG_DIR)('dwmun25', logfile, '', execution_queue)

    log_event(f"Redeployment process completed, commands run: {execution_queue}", LOG_DIR / logfile, execution_queue)

    return 200


