import type { Block, BlockType } from './types';

export const BLOCK_TYPES: Record<string, BlockType> = {
  motion: { name: 'motion', color: 'blue' },
  looks: { name: 'looks', color: 'green' },
}

export const BLOCKS: Block[] = [
  { name: 'move', label: 'Move <num> steps', category: BLOCK_TYPES.motion },
  { name: 'turn', label: 'Turn', category: BLOCK_TYPES.motion },
  { name: 'say', label: 'Say', category: BLOCK_TYPES.looks },
  { name: 'think', label: 'Think', category: BLOCK_TYPES.looks },
]
