from flask import Flask, render_template, request
import psycopg
import re

app = Flask(__name__)

# Database connection configuration
DB_HOST = "localhost"
DB_NAME = "video_game_inventory"
DB_USER = "postgres"
DB_PASSWORD = "root"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        # Connect to the PostgreSQL database
        conn = psycopg.connect(f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}')

        # Get the SQL query from the form
        sql_query = request.form['query']

        try:
            # Execute the SQL query and get the results
            with conn.cursor() as cur:
                cur.execute(sql_query)
                # results = cur.fetchall()
                results = cur.fetchmany(100)
                column_names = [desc[0] for desc in cur.description]
                print('cur.description', cur.description)

            # Render the results template and pass the column names and results
            return render_template('results.html', sql_query=sql_query, column_names=column_names, results=results)

        except (Exception, psycopg.Error) as error:
            # Handle errors
            error_message = str(error)
            return render_template('error.html', error_message=error_message)

    # Render the query template for GET requests
    return render_template('query.html')

if __name__ == '__main__':
    app.run(debug=True)