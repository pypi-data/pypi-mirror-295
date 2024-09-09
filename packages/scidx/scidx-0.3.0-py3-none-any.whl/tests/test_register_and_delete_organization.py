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

# Test for registering and then deleting an organization
def test_register_and_delete_organization():
    """
    Test the ability to create and then delete an organization 
    using the real API.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Set the token for authentication
    client.token = "test"

    # Generate a random organization name
    org_name = generate_random_string()
    org_title = f"Title for {org_name}"
    org_description = "This is a test organization created for testing."

    # Register a new organization
    response_create = client.register_organization(
        name=org_name,
        title=org_title,
        description=org_description
    )
    
    # Debugging: Print the response to inspect it
    print("Create Organization Response:", response_create)

    # Check if the organization was created successfully
    assert "id" in response_create
    assert response_create.get("message") == "Organization created successfully"

    # Now delete the organization
    response_delete = client.delete_organization(organization_name=org_name)

    # Check if the organization was deleted successfully
    assert response_delete.get("message") == "Organization deleted successfully"
