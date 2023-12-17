import sqlalchemy
from sqlalchemy import create_engine

# Create a connection to the PostgreSQL database using the SQLALCHEMY_DATABASE_URI string
# Create a connection to the PostgreSQL database using the SQLALCHEMY_DATABASE_URI string
engine = create_engine('postgresql+psycopg2://maxiq:PgAdminqa_21$@mosaic-k8s-qa-postgres-flexible.postgres.database.azure.com:5432/ai_logistics')

# Open a connection to the database
conn = engine.connect()

# Define the query
query = """
SELECT id,
       split_part(name, '-', 1) AS name_first_part,
       split_part(name, '-', 2) AS name_second_part
FROM nb_docker_image 
WHERE id IN (
  SELECT DISTINCT(nb_docker_image_tag.docker_image_id)
  FROM nb_docker_image_tag
  WHERE docker_image_id IN (
    SELECT id 
    FROM nb_docker_image
    WHERE base_image_id IS NULL 
      AND TYPE='PRE_BUILD' 
      AND kernel_type IN ('rstudio', 'python', 'spark_distributed', 'spark')
      AND NOT EXISTS (
        SELECT 1 
        FROM nb_docker_image_tag
        WHERE nb_docker_image_tag.docker_image_id = nb_docker_image.id
          AND tag LIKE 'version%'
      )
    )
);
"""

# Execute the query and fetch all the results
results = conn.execute(query).fetchall()

# Open a file to write the insert queries
with open('insert_queries.sql', 'w') as f:
    # Loop through the results and write insert queries to the file
    for row in results:
        # Check if row[2] is None or empty
        version = row[2] if row[2] else 'default'
        insert_query = f"INSERT INTO nb_docker_image_tag(id, created_by, tag, updated_by, docker_image_id) VALUES (uuid_generate_v4(), 'system', 'version={version}', 'system', '{row[0]}');\n"
        f.write(insert_query)

        # Execute the insert query
        conn.execute(insert_query)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

