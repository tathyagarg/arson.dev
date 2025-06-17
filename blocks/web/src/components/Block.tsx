import type { Block } from 'src/lib/types'
import NumInput from './inputs/NumInput/NumInput'

const parseLabel = (label: string) => {
  // replcae <num> with a number input
  return <div className="flex flex-row gap-2 items-center">
    {label.split(/(<num>)/).map((part, _) => {
      if (part === '<num>') return <NumInput />
      return part
    })}
  </div>
}

const BlockComponent = ({ block }: { block: Block }) => {
  return <div className="cursor-pointer p-4 text-dark-text rounded-md" style={{ backgroundColor: block.category.color }}>
    {parseLabel(block.label)}
  </div>
}

export default BlockComponent;
