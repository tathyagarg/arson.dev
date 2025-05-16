import fs from 'fs';
import path from 'path';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
  const filePath = path.resolve('static/sites/dwmun/index.html');
  const html = fs.readFileSync(filePath, 'utf-8');

  return new Response(html, {
    headers: { 'Content-Type': 'text/html' }
  });
};

