import { BlockType } from 'src/lib/types';

const BlockCategory = ({ category, onclick }: { category: BlockType, onclick: () => void }) => {
  return <div className="flex flex-col gap-1 text-center cursor-pointer w-fit" onClick={onclick}>
    <div style={{ backgroundColor: category.color }} className="h-14 w-14 rounded-full">
    </div>
    {category.name}
  </div >
}

export default BlockCategory;
