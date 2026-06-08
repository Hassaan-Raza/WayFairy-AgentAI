from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults


@tool
def search_web_tool(query: str) -> str:
    """
    Search the web for travel information including hotels, attractions,
    restaurants, routes, visa requirements, and local tips.
    Use simple, specific search queries for best results.
    """
    try:
        search = DuckDuckGoSearchResults(
            num_results=6,
            backend="lite",
            safesearch="Moderate"
        )
        results = search.run(query)

        # if no results, try a simplified query
        if not results or "no results" in results.lower() or "no good" in results.lower():
            simplified = " ".join(query.split()[:5])
            results = search.run(simplified)

        return results if results else "No results found for this query. Try different search terms."

    except Exception as e:
        return f"Search error: {str(e)}. Try a simpler or different query."
