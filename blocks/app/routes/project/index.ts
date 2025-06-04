import Route from '@ember/routing/route';
import type BlockCategory from 'app/types/block';
import BLOCK_DIRECTORY from '@constants/block-directory';

export default class ProjectRoute extends Route {
  model(): { blocks: Record<string, BlockCategory> } {
    return {blocks: BLOCK_DIRECTORY as Record<string, BlockCategory>};
  }
}
