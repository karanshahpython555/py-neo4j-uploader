from neo4j import GraphDatabase
from dotenv import load_dotenv
import json
import os

# Part 3 - Python Driver


def execute_query(
        uri: str,
        username: str,
        password: str,
        query: str,
        params: dict):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        records, summary, keys = driver.execute_query(query, params)
        return summary

# Part 2 - Conversion


def convert_nodes(
    nodes: dict
):

    queries = []  # Store individual queries here
    params = {}

    for node_label, node_data in nodes.items():
        # Generate a unique parameter key for each node
        params[node_label] = node_data
        # Create individual node creation queries
        query = f"""CALL apoc.create.nodes(["{node_label}"], ${node_label});"""
        queries.append(query)

    return queries, params


def convert_relationships(
    relationships: dict
):

    rel_record_list = []
    params = {}

    for rel_type, rel_records in relationships.items():
        for record in rel_records:

            # Get the relationships _uid to distinguish it from other params
            record_key = record.get('_uid')
            params[record_key] = record

            # Get the source and target node _uids
            from_node_uid = record.get('_from__uid')
            to_node_uid = record.get('_to__uid')

            # Create a list of values and parameter keys which will be used to construct the relationship
            item = f"['{rel_type}', '{from_node_uid}', '{
                to_node_uid}', ${record_key}]"

            rel_record_list.append(item)

    # Combine all the lists into a master list
    composite_rel_records_list = ",".join(rel_record_list)

    # Create a single query to process all the Relationship records
    query = f"""WITH [{composite_rel_records_list}] AS rel_data
                UNWIND rel_data AS relationship
                MATCH (n {{`_uid`:relationship[1]}})
                MATCH (n2 {{`_uid`:relationship[2]}})
                CALL apoc.create.relationship(n, relationship[0], relationship[3], n2) YIELD rel
                RETURN rel
    """

    return query, params


# Part 1 - Upload
def upload(
    uri: str,
    username: str,
    password: str,
    data: str
):

    if isinstance(data, str) is True:
        try:
            data = json.loads(data)
        except Exception as e:
            raise Exception(f'Error converting data to json: {e}')

    # Convert the nodes and relationships into cypher queries and params
    node_queries, node_params = convert_nodes(data['nodes'])
    rel_query, rel_params = convert_relationships(data['relationships'])

    # Aggregate them into a single list of queries and merge the params
    queries = node_queries + [rel_query]
    params = node_params
    params.update(rel_params)

    # Execute each query individually
    for query in queries:
        execute_query(uri, username, password, query, params)


# Part 0 - Setup
def setup(uri: str, username: str, password: str, ip_file: str):
    with open(ip_file) as f:
        data = f.read()
    upload(uri, username, password, data)


if __name__ == "__main__":
    load_dotenv()
    setup(
        uri="bolt://localhost:7687",
        username=os.getenv('DB_USER_NAME'),
        password=os.getenv('DB_PASSWORD'),
        ip_file="test_data.json"
    )
