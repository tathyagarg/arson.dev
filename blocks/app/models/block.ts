export default interface Block {
  name: string;
  description: string;
  icon: string;
  color: string;
}

export type BlockCategory = {
  color: string;
  blocks: Block[];
};
