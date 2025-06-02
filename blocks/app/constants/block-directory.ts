import type { Block } from 'app/types/block';

export type BLOCK_DIRECTORY_TYPE = Record<string, Block[]>;

const BLOCK_DIRECTORY: BLOCK_DIRECTORY_TYPE = {
  'default': [
    {
      name: 'Text',
      description: 'A simple text block',
      icon: 'text',
      color: 'blue'
    },
    {
      name: 'Image',
      description: 'An image block',
      icon: 'image',
      color: 'green'
    }
  ],
  'advanced': [
    {
      name: 'Video',
      description: 'A video block',
      icon: 'video',
      color: 'red'
    },
    {
      name: 'Audio',
      description: 'An audio block',
      icon: 'audio',
      color: 'purple'
    }
  ]
} as const;

export default BLOCK_DIRECTORY;
