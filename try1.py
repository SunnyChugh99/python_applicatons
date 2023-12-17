from sqlalchemy import create_engine
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:admin1234@mosaicai-sandbox.catnchrgoqwp.us-east-1.rds.amazonaws.com:5432/ai_logistics?options=-csearch_path=ai_logistics"
# Connect to the database using SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create a connection
conn = engine.connect()

# Rest of the script...

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Create the uuid-ossp extension if it does not exist
cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

# Define the SQL query
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

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Open a file to write the insert queries
with open('insert_queries.sql', 'w') as f:
    # Loop through the results and write insert queries to the file
    for row in results:
        # Check if row[2] is None or empty
        version = row[2] if row[2] else 'default'
        f.write(f"INSERT INTO nb_docker_image_tag(id, created_by, tag, updated_by, docker_image_id) VALUES (uuid_generate_v4(), 'system', 'version={version}', 'system', '{row[0]}');\n")

# Execute the insert queries
cur.execute(open('insert_queries.sql', 'r').read())

# Commit the changes to the database
conn.commit()

# Close the cursor and database connection
cur.close()
conn.close()
