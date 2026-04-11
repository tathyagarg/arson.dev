-- CreateTable
CREATE TABLE "User" (
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "permsmissions" TEXT[],

    CONSTRAINT "User_pkey" PRIMARY KEY ("username")
);
