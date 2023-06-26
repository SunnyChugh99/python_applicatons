import sqlalchemy
from sqlalchemy import create_engine

# Create a connection to the PostgreSQL database using the SQLALCHEMY_DATABASE_URI string
# Create a connection to the PostgreSQL database using the SQLALCHEMY_DATABASE_URI string
engine = create_engine('postgresql+psycopg2://maxiq:PgAdminqa_21$@mosaic-k8s-qa-postgres-flexible.postgres.database.azure.com:5432/ai_logistics')

# Open a connection to the data

result = engine.execute("SELECT * FROM <table-name>")
for row in result:
    print(row)
