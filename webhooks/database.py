import peewee as pw
from playhouse.migrate import migrate, PostgresqlMigrator
from dotenv import load_dotenv
import os

assert load_dotenv()

DATABASE_NAME: str = os.getenv('DATABASE_NAME', 'webhooks')
DATABASE_USER: str = os.getenv('DATABASE_USER', 'postgres')
DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD', 'unauthenticated')
DATABASE_HOST: str = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT: int = int(os.getenv('DATABASE_PORT', '5432'))

db = pw.PostgresqlDatabase(
    DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT
)

class Listener(pw.Model):
    name = pw.CharField(unique=True)
    verification_type = pw.IntegerField()

    other_data = pw.CharField(null=True)

    class Meta:
        database = db


def migrate_db():
    migrator = PostgresqlMigrator(db)
    migrate(
        migrator.drop_column('listener', 'handler', pw.CharField()),
    )
