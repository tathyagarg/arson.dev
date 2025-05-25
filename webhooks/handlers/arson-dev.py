from fastapi import Request
import os

HOME = '/home/tathya'

def redeploy_sveltekit(name: str):
    os.system(f'cd {HOME}/{name} && npm run build && pm2 restart {name}')


def redeploy_fastapi(name: str):
    os.system(f"systemctl --user restart {name}")


SERVICES = {
    'archive': redeploy_sveltekit,
    'blog': redeploy_sveltekit,
    'md': redeploy_fastapi,
    'webhooks': redeploy_fastapi,
}


async def handler(request: Request):
    data = await request.json()

    os.system('git pull')

    changed_files = []

    for file in data.get('commits', []):
        for changed_file in file.get('added', []) + file.get('removed', []) + file.get('modified', []):
            changed_files.append(changed_file)

    for file in changed_files:
        root, _ = os.path.split(file)
        if root in SERVICES:
            SERVICES[root](root)

    return 200


