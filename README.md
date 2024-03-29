# py-neo4j-uploader
Upload JSON data to Neo4j using python.

# Neo4j Data Upload Script

This Python script provides functionality to upload data to a Neo4j graph database using the Python Driver provided by Neo4j. It's particularly useful for uploading JSON data representing nodes and relationships into a Neo4j instance.

## Requirements

- Python 3.x
- Neo4j Database
- Python packages: `neo4j`, `python-dotenv`

## Installation

1. Clone or download the script file (`neo4j_data_upload.py`) into your project directory.
2. Install the required Python packages using pip:
    ```
    pip install -r requirements.txt
    ```

## Configuration

Before running the script, make sure to set up your Neo4j database and create a `.env` file in the project directory containing the following environment variables:

DB_USER_NAME=<Neo4j_Username>
DB_PASSWORD=<Neo4j_Password>


Replace `<Neo4j_Username>` and `<Neo4j_Password>` with your Neo4j username and password.

## Usage

1. Prepare your data in JSON format. For example, you can create a file named `test_data.json` containing your node and relationship data.
2. Ensure your Neo4j database is running.
3. Run the script using the following command:
    ```
    python neo4j_uploader.py
    ```

The script will read the data from `test_data.json`, convert it into Cypher queries, and upload it to your Neo4j database.

## Structure

- **Part 0 - Setup**: Sets up the connection to the Neo4j database and reads the input data file.
- **Part 1 - Upload**: Uploads the data to the Neo4j database.
- **Part 2 - Conversion**: Converts the input JSON data into Cypher queries for creating nodes.
- **Part 3 - Python Driver**: Executes the Cypher queries using the Neo4j Python Driver.



