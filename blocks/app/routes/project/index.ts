import Route from '@ember/routing/route';
import type Block from 'app/types/block';
import BLOCK_DIRECTORY from '@constants/block-directory';

export default class ProjectRoute extends Route {
  model(): { blocks: Record<string, Block[]> } {
    return {blocks: BLOCK_DIRECTORY as Record<string, Block[]>};
  }
}
