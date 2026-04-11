/*
  Warnings:

  - You are about to drop the column `permissions` on the `User` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "User" DROP COLUMN "permissions",
ADD COLUMN     "role" TEXT NOT NULL DEFAULT 'user';
