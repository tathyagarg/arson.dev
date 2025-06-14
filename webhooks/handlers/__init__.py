from datetime import datetime
import io
import subprocess
from pathlib import Path

HOME = Path.home()


def log_event(event: str, log_file: Path , execution_queue: list[str]):
    with open(log_file, 'a') as log:
        log.write(f"[{len(execution_queue)}] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}\n")

def execute_command(command: str, cwd: Path, log_file: io.TextIOWrapper, execution_queue: list[str]) -> int:
    log_event(f"Executing command: {command} in {cwd}", Path(log_file.name), execution_queue)
    status = subprocess.run(command, shell=True, cwd=cwd, stdout=log_file, stderr=log_file).returncode

    return status


def redeploy_service_factory(steps: list[str]):
    def _factory(log_file_path: Path):
        def redeploy_service(name: str, log_file_name: str, parent_dir: str, execution_queue: list[str]):
            for i, step in enumerate(steps, 1):
                with open(log_file_path / log_file_name, 'a') as log_file:
                    log_file.write(f'Step {i} for {name}: {step.format(name=name)}\n')

                    command = step.format(name=name)

                    execution_queue.append(command)
                    status = execute_command(command, HOME / parent_dir / name, log_file, execution_queue)

                    log_file.write(f'Step {i} for {name} completed with status {status}\n')

            return execution_queue
        
        return redeploy_service

    return _factory


redeploy_sveltekit = redeploy_service_factory(['npm i', 'npm run build', 'pm2 restart {name}'])
redeploy_astro = redeploy_service_factory(['npm i', 'npm run build -- --remote', 'pm2 restart {name}'])
redeploy_fastapi = redeploy_service_factory(['../.venv/bin/python -m pip install -r requirements.txt', 'systemctl --user restart {name}'])

