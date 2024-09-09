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

# Test for searching and verifying organization listing
def test_search_organization():
    """
    Test the ability to list all organizations in the system.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Set the token for authentication
    client.token = "test"
    
    # Step 1: Create a random organization to ensure at least one exists
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
    
    # Step 2: Search for organizations
    response_search_org = client.search_organization()
    
    # Debugging: Print the search response to inspect it
    print("Search Organizations Response:", response_search_org)

    # Check if the search response contains a list of organization names (strings)
    assert isinstance(response_search_org, list)

    # Check if the created organization name is in the search results
    assert org_name in response_search_org, f"Organization {org_name} not found in search results"
    
    # Step 3: Delete the organization to clean up
    response_delete_org = client.delete_organization(organization_name=org_name)
    
    # Check if the organization was deleted successfully
    assert response_delete_org.get("message") == "Organization deleted successfully"