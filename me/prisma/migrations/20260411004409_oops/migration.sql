/*
  Warnings:

  - You are about to drop the column `permsmissions` on the `User` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "User" DROP COLUMN "permsmissions",
ADD COLUMN     "permissions" TEXT[];
