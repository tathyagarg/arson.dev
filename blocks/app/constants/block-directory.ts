import type { BlockCategory } from 'app/types/block';

export type BLOCK_DIRECTORY_TYPE = Record<string, BlockCategory>;

const BLOCK_DIRECTORY: BLOCK_DIRECTORY_TYPE = {
  'default': {
    color: 'gray',
    blocks: [
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
  },
  'media': {
    color: 'purple',
    blocks: [
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
        color: 'orange'
      }
    ],
  },
} as const;

export default BLOCK_DIRECTORY;
