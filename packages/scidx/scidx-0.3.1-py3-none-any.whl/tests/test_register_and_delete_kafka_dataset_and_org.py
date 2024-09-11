import pytest
import string
import random
from scidx.client import sciDXClient

# Helper function to generate a random string
def generate_random_string(length=8):
    """
    Generate a random string of fixed length.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Test for registering and then deleting a Kafka dataset and its organization
def test_register_and_delete_kafka_dataset_and_org():
    """
    Test the ability to create and then delete a Kafka dataset 
    and the associated organization using the real API.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Set the token for authentication
    client.token = "test"
    
    # Step 1: Create a random organization
    org_name = generate_random_string()
    org_title = f"Title for {org_name}"
    org_description = "This is a test organization created for testing."

    # Register a new organization
    response_create_org = client.register_organization(
        name=org_name,
        title=org_title,
        description=org_description
    )
    
    # Check if the organization was created successfully
    assert "id" in response_create_org
    assert response_create_org.get("id") is not None  # Ensure an ID is returned
    
    # Extract the organization ID
    owner_org = response_create_org.get("id")
    
    # Step 2: Create a random Kafka dataset
    kafka_dataset_name = generate_random_string()
    kafka_dataset_title = f"Kafka Dataset {kafka_dataset_name}"
    kafka_topic = generate_random_string(6)
    kafka_host = "localhost"
    kafka_port = 9092
    kafka_dataset_description = "This is a test Kafka dataset."

    # Register the Kafka dataset
    response_create_kafka = client.register_kafka(
        dataset_name=kafka_dataset_name,
        dataset_title=kafka_dataset_title,
        owner_org=owner_org,
        kafka_topic=kafka_topic,
        kafka_host=kafka_host,
        kafka_port=kafka_port,
        dataset_description=kafka_dataset_description
    )

    # Debugging: Print the Kafka dataset response to inspect it
    print("Create Kafka Dataset Response:", response_create_kafka)

    # Check if the Kafka dataset was created successfully
    assert "id" in response_create_kafka
    assert response_create_kafka.get("id") is not None  # Ensure an ID is returned
    
    # Step 3: Delete the Kafka dataset
    response_delete_kafka = client.delete_resource(resource_name=kafka_dataset_name)
    
    # Check if the Kafka dataset was deleted successfully
    assert response_delete_kafka.get("message") == f"{kafka_dataset_name} deleted successfully"
    
    # Step 4: Delete the organization
    response_delete_org = client.delete_organization(organization_name=org_name)
    
    # Check if the organization was deleted successfully
    assert response_delete_org.get("message") == "Organization deleted successfully"
