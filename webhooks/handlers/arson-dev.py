from fastapi import Request
import os

def redeploy_blog():
    os.system('cd /home/tathya/arson.dev/blog && npm run build && pm2 restart blog')


async def handler(request: Request):
    data = await request.json()

    os.system('git pull')

    changed_files = []

    for file in data.get('commits', []):
        for changed_file in file.get('added', []) + file.get('removed', []) + file.get('modified', []):
            changed_files.append(changed_file)

    for file in changed_files:
        if file.startswith('blog/'):
            redeploy_blog()

    return 200


