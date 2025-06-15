CREATE TABLE "pings" (
	"id" serial PRIMARY KEY NOT NULL,
	"service" text NOT NULL,
	"status" integer NOT NULL,
	"response_time" integer NOT NULL,
	"created_at" timestamp with time zone DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "services" (
	"id" serial PRIMARY KEY NOT NULL,
	"slug" text NOT NULL,
	"name" text NOT NULL,
	"url" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now(),
	CONSTRAINT "services_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
ALTER TABLE "pings" ADD CONSTRAINT "pings_service_services_slug_fk" FOREIGN KEY ("service") REFERENCES "public"."services"("slug") ON DELETE cascade ON UPDATE no action;