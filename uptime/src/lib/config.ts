import fs from 'fs';
import YAML from 'yaml';

let configPath;
try {
  configPath = import.meta.env.PUBLIC_CONFIG_PATH
} catch {
  configPath = process.env.PUBLIC_CONFIG_PATH;
}

const fileContent = fs.readFileSync(configPath, 'utf8');

export const config = YAML.parse(fileContent);

export type Service = {
  name: string;
  url: string;
}
