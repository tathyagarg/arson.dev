import { readdir, stat, readFile } from 'fs/promises';
import path from 'path';

export async function GET() {
  const dir = path.resolve('static/sites');
  const files = await readdir(dir);

  const data = [];

  for (const file of files) {
    const filePath = path.join(dir, file);
    const stats = await stat(filePath);
    if (stats.isDirectory()) {
      const projectData = await readFile(path.join(filePath, 'project.json'), 'utf-8');
      data.push(JSON.parse(projectData));
    }
  }

  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  })
}
