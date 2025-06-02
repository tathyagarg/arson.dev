import Component from '@glimmer/component';
import type Block from 'app/types/block';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import type { BLOCK_DIRECTORY_TYPE } from '@constants/block-directory';

interface BlockBarSignature {
  Args: {
    blocks: BLOCK_DIRECTORY_TYPE;
  };
}

export default class BlockBar extends Component<BlockBarSignature> {
  @tracked selected: keyof BLOCK_DIRECTORY_TYPE = 'default';

  get blocks(): Block[] {
    return this.args.blocks[this.selected] ?? [];
  }

  get selectedBlocks(): Block[] {
    if (!this.selected) {
      return [];
    }

    return this.args.blocks[this.selected] ?? [];
  }

  get categories(): string[] {
    return Object.keys(this.args.blocks);
  }

  @action updateSelectedCategory(category: keyof BLOCK_DIRECTORY_TYPE): void {
    if (this.categories.includes(category)) {
      this.selected = category;
    } else {
      console.warn(`Category "${category}" does not exist in the block directory.`);
    }
  }
}
