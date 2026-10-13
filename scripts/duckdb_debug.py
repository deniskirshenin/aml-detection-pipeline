import duckdb

con = duckdb.connect('data/raw_data.duckdb')

query = """
    SELECT 
        table_catalog, 
        table_schema, 
        table_name, 
        table_type
    FROM information_schema.tables
    WHERE table_schema != 'information_schema' 
      AND table_schema != 'pg_catalog';
"""

df = con.execute(query).fetchdf()
print(df)