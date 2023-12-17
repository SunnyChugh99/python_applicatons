import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="refract.cqkkwwmb5gtj.us-east-1.rds.amazonaws.com",
    database="ai_logistics",
    user="postgres",
    password="R_PgcoL5yVz2r7_T",
    options=f"-c search_path=ai_logistics"
)

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
for row in results:
    print(row[0], row[1], row[2])
# Loop through the results and insert a new record with a random UUID and the version number
for row in results:
    # Define the SQL query to insert a new record with a random UUID and the version number
    insert_query = f"""
        INSERT INTO nb_docker_image_tag(id, created_by, tag, updated_by, docker_image_id)
        VALUES (uuid_generate_v4(), 'system', 'version={row[2]}', 'system', '{row[0]}');
    """
    # Execute the insert query
    cur.execute(insert_query)

# Commit the changes to the database
conn.commit()

# Close the cursor and database connection
cur.close()
conn.close()
