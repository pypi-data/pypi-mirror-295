import requests
from typing import List, Optional


def search_kafka(self, dataset_name: Optional[str] = None, dataset_title: Optional[str] = None,
                    owner_org: Optional[str] = None, kafka_host: Optional[str] = None,
                    kafka_port: Optional[str] = None, kafka_topic: Optional[str] = None,
                    dataset_description: Optional[str] = None, search_term: Optional[str] = None) -> List[dict]:
    """
    Search for Kafka datasets based on various parameters.

    Parameters
    ----------
    dataset_name : Optional[str]
        The name of the Kafka dataset.
    dataset_title : Optional[str]
        The title of the Kafka dataset.
    owner_org : Optional[str]
        The name of the organization.
    kafka_host : Optional[str]
        The Kafka host.
    kafka_port : Optional[str]
        The Kafka port.
    kafka_topic : Optional[str]
        The Kafka topic.
    dataset_description : Optional[str]
        The description of the Kafka dataset.
    search_term : Optional[str]
        A term to search across all fields.

    Returns
    -------
    List[dict]
        A list of Kafka datasets that match the search criteria.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/kafka"
    params = {
        "dataset_name": dataset_name,
        "dataset_title": dataset_title,
        "owner_org": owner_org,
        "kafka_host": kafka_host,
        "kafka_port": kafka_port,
        "kafka_topic": kafka_topic,
        "dataset_description": dataset_description,
        "search_term": search_term
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = (
            f"Failed to search Kafka datasets. "
            f"Request URL: {url}\n"
            f"Parameters: {params}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
