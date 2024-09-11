import requests

def create_kafka_stream(self, keywords: list, filter_semantics: dict) -> dict:
    """
    Create a new Kafka stream in the sciDX system.

    Parameters
    ----------
    keywords : list
        A list of keywords to filter the data sources.
    filter_semantics : dict
        A dictionary containing filter semantics to apply to the streams.

    Returns
    -------
    dict
        A dictionary containing the response from the API, including the topic of the created stream.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/stream"
    # Convert the list of keywords to a single comma-separated string
    keywords_str = ','.join(keywords)
    payload = {
        "keywords": keywords_str,
        "filter_semantics": filter_semantics
    }
    headers = self._get_headers()
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    if response.status_code == 201:
        return response.json()
    else:
        error_message = (
            f"Failed to create Kafka stream. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
