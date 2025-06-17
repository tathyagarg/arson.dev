// import { Link, routes } from '@redwoodjs/router'
import { Metadata } from '@redwoodjs/web'
import { BLOCKS, BLOCK_TYPES } from 'src/lib/blocks';
import { useState } from 'react'
import BlockCategory from 'src/components/BlockCategory'
import BlockComponent from 'src/components/Block';

const ProjectPage = () => {
  let [category, setCategory] = useState('motion')

  return (
    <>
      <Metadata title="Project" description="Project page" />

      <div className="w-screen h-screen grid grid-cols-5 grid-rows-5">
        <div className="bg-red-500 col-start-1 col-span-1 row-start-1 row-span-1 grid grid-rows-2 grid-cols-4 p-4">
          {Object.values(BLOCK_TYPES).map((category) => <BlockCategory category={category} onclick={() => setCategory(category.name)}></BlockCategory>)}
        </div>
        <div className="bg-blue-500 col-start-1 col-span-1 row-start-2 row-span-4 flex flex-col gap-4 p-4">
          {BLOCKS.filter(block => block.category.name === category).map((block) => <BlockComponent block={block}></BlockComponent>)}
        </div>
        <div className="bg-green-500 col-start-2 col-span-2 row-start-1 row-span-5"></div>
        <div className="bg-yellow-500 col-start-4 col-span-2 row-start-1 row-span-3"></div>
        <div className="bg-pink-500 col-start-4 col-span-2 row-start-4 row-span-2"></div>
      </div>
      {/*
          My default route is named `project`, link to me with:
          `<Link to={routes.project()}>Project</Link>`
      */}
    </>
  )
}

export default ProjectPage
