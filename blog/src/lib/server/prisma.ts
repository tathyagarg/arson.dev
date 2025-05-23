import { PrismaClient, Prisma } from '@prisma/client';

const prisma = globalThis.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalThis.prisma = prisma;

export default prisma;

export type PostRequest = Omit<Prisma.PostCreateInput, 'id'> & { passphrase: string };
