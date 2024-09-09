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

# Test for registering and then deleting an S3 dataset and its organization
def test_register_and_delete_s3_dataset_and_org():
    """
    Test the ability to create and then delete an S3 dataset 
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
    
    # Step 2: Create a random S3 dataset
    s3_dataset_name = generate_random_string()
    s3_dataset_title = f"S3 Dataset {s3_dataset_name}"
    s3_resource_path = f"s3://bucket/{s3_dataset_name}/data"
    s3_dataset_description = "This is a test S3 dataset."

    # Register the S3 dataset
    response_create_s3 = client.register_s3(
        resource_name=s3_dataset_name,
        resource_title=s3_dataset_title,
        owner_org=owner_org,
        resource_s3=s3_resource_path,
        notes=s3_dataset_description
    )

    # Debugging: Print the S3 dataset response to inspect it
    print("Create S3 Dataset Response:", response_create_s3)

    # Check if the S3 dataset was created successfully
    assert "id" in response_create_s3
    assert response_create_s3.get("id") is not None  # Ensure an ID is returned
    
    # Step 3: Delete the S3 dataset
    response_delete_s3 = client.delete_resource(resource_name=s3_dataset_name)
    
    # Check if the S3 dataset was deleted successfully
    assert response_delete_s3.get("message") == f"{s3_dataset_name} deleted successfully"
    
    # Step 4: Delete the organization
    response_delete_org = client.delete_organization(organization_name=org_name)
    
    # Check if the organization was deleted successfully
    assert response_delete_org.get("message") == "Organization deleted successfully"
