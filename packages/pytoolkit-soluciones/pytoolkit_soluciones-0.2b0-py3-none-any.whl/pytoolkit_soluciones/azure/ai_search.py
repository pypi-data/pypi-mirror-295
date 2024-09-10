from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import QueryType

def search_index(query, min_score=0.2, num_results=3, endpoint=None, index_name=None, api_key=None):
    """
    Performs a search in Azure Cognitive Search and returns results
    filtered by minimum score and the desired number of results.

    Args:
        query (str): The search query.
        min_score (float): The minimum score percentage that the results must meet.
        num_results (int): The maximum number of results to return.
        endpoint (str): The Azure Cognitive Search endpoint URL.
        index_name (str): The name of the Azure Cognitive Search index.
        api_key (str): The API key for Azure Cognitive Search.

    Returns:
        str or dict: Combined content from the filtered results, or the query if no results were found,
                     or a dictionary with 'error' and 'message' keys in case of failure.
    """
    if not endpoint or not index_name or not api_key:
        return {"error": True, "message": "Endpoint, index_name, and api_key must be provided"}

    try:
        # Connect to Azure Cognitive Search
        search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )
    except Exception as e:
        # Handle connection errors
        return {"error": True, "message": f"Failed to connect to Azure Cognitive Search: {str(e)}"}

    try:
        # Perform the search in the Azure index
        search_results = search_client.search(
            search_text=query,
            query_type=QueryType.SIMPLE,
            select=["content"]
        )
    except Exception as e:
        # Handle search query errors
        return {"error": True, "message": f"Failed to perform search: {str(e)}"}

    try:
        # Filter the results with a score higher than min_score
        filtered_results = [
            {
                "content": doc["content"],
                "score": doc["@search.score"]
            }
            for doc in search_results
            if doc["@search.score"] > min_score
        ]

        # If no results are found, return the query as content
        if not filtered_results:
            return query

        # Sort the results by score and select the top results
        filtered_results.sort(key=lambda x: x["score"], reverse=True)
        top_results = filtered_results[:num_results]

        # Combine the content of the selected top results
        search_content = "\n".join([result["content"] for result in top_results])

        return search_content
    except Exception as e:
        # Handle any other errors during processing
        return {"error": True, "message": f"Error processing search results: {str(e)}"}
