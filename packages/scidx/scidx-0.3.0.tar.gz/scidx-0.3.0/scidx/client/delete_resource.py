import requests

def delete_resource(self, resource_name: str) -> dict:
    """
    Delete a resource (e.g., Kafka, URL, S3) in the sciDX REST API.

    Parameters
    ----------
    resource_name : str
        The name of the resource to be deleted.

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    # Define the URL for the DELETE request using the resource_name
    url = f"{self.api_url}/{resource_name}"
    
    # Get headers for authorization or other needed parameters
    headers = self._get_headers()

    # Make the DELETE request to the API
    response = requests.delete(url, headers=headers)
    
    # If the response is successful, return the confirmation message
    if response.status_code == 200:
        return response.json()
    # If the resource is not found, raise an HTTPError with a detailed message
    elif response.status_code == 404:
        raise requests.exceptions.HTTPError(
            f"Resource '{resource_name}' not found.", 
            response=response
        )
    # For other cases, raise an HTTPError with a detailed message
    else:
        error_message = (
            f"Failed to delete resource '{resource_name}'. "
            f"Request URL: {url}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
