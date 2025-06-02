export default interface Block {
  name: string;
  description: string;
  icon: string;
  color: string;
}

export const BlockDirectory: Record<string, Block[]> = {
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
}
