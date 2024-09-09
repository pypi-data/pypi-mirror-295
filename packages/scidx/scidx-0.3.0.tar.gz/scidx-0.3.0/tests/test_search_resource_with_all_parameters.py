import pytest
import string
import random
from scidx.client import sciDXClient
from scidx.client import CSVProcessing

# Helper function to generate a random string
def generate_random_string(length=8):
    """
    Generate a random string of fixed length.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Test for searching resources using all available parameters
def test_search_resource_with_all_parameters():
    """
    Test the ability to search for resources in the system using all available parameters.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Set the token for authentication
    client.token = "test"
    
    # Step 1: Create a random organization to associate with the resource
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

    # Step 2: Create a random resource (e.g., URL dataset)
    resource_name = generate_random_string()
    resource_title = f"Resource Title {resource_name}"
    resource_url = f"http://example.com/{resource_name}"
    resource_description = "This is a test resource for search testing."
    resource_format = "CSV"

    # CSVProcessing for the resource
    csv_processing = CSVProcessing(delimiter=",", header_line=1, start_line=2)

    # Register the URL resource
    response_create_resource = client.register_url(
        resource_name=resource_name,
        resource_title=resource_title,
        owner_org=org_name,
        resource_url=resource_url,
        file_type=resource_format,
        processing=csv_processing,
        notes=resource_description
    )

    # Check if the resource was created successfully
    assert "id" in response_create_resource
    assert response_create_resource.get("id") is not None  # Ensure an ID is returned

    # Step 3: Search for the resource using all parameters
    response_search_resource = client.search_resource(
        dataset_name=resource_name,
        dataset_title=resource_title,
        owner_org=org_name,
        resource_url=resource_url,
        resource_name=resource_name,
        dataset_description=org_description,
        resource_description=resource_description,
        resource_format=resource_format,
        search_term="test"
    )

    # Debugging: Print the search response to inspect it
    print("Search Resource Response:", response_search_resource)

    # Check if the search response contains the expected resource
    assert isinstance(response_search_resource, list)
    
    # The 'resource_name' is inside the 'resources' list within each result
    found = any(
        any(res['name'] == resource_name for res in result['resources'])
        for result in response_search_resource
    )
    
    assert found, f"Resource {resource_name} not found in search results"
    
    # Step 4: Delete the resource
    response_delete_resource = client.delete_resource(resource_name=resource_name)
    assert response_delete_resource.get("message") == f"{resource_name} deleted successfully"

    # Step 5: Delete the organization
    response_delete_org = client.delete_organization(organization_name=org_name)
    assert response_delete_org.get("message") == "Organization deleted successfully"
