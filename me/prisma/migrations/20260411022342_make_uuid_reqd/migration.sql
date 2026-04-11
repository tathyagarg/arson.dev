/*
  Warnings:

  - The primary key for the `User` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - A unique constraint covering the columns `[username]` on the table `User` will be added. If there are existing duplicate values, this will fail.
  - Made the column `uuid` on table `User` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "User" DROP CONSTRAINT "User_pkey",
ALTER COLUMN "uuid" SET NOT NULL,
ADD CONSTRAINT "User_pkey" PRIMARY KEY ("uuid");

-- CreateIndex
CREATE UNIQUE INDEX "User_username_key" ON "User"("username");
