import Component from '@glimmer/component';
import type BlockCategory from 'app/types/block';
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

  get blocks(): Record<string, BlockCategory> {
    const blocks = this.args.blocks as Record<string, BlockCategory>;
    return blocks;
  }

  get selectedBlocks() {
    return this.blocks[this.selected];
  }

  get categories(): { name: keyof BLOCK_DIRECTORY_TYPE; color: string }[] {
    const data = Object.entries(this.blocks).map(([key, value]) => {
      return {
        name: key as keyof BLOCK_DIRECTORY_TYPE,
        color: value.color,
      };
    })

    return data;
  }

  get categoryNames(): string[] {
    return Object.keys(this.blocks);
  }

  @action updateSelectedCategory(category: keyof BLOCK_DIRECTORY_TYPE): void {
    if (this.categoryNames.includes(category)) {
      this.selected = category;
    }
  }
}

