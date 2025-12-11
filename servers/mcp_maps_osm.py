import requests
from typing import List
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("maps", host="0.0.0.0", port=8001)

@mcp.tool()
def search_restaurants(city_name: str, max_results: int=10) -> List[str]:
    """
        Search for restaurants in a given city using OpenStreetMap data.
        Args:
            city_name: City name to search restaurants in
            max_results: Maximum number of results to retrieve (default: 10)
        Returns:
            List of restaurants found in the city with their details.    
    """

    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    area["name"="{city_name}"]->.searchArea;
    (
      node["amenity"="restaurant"](area.searchArea);
      way["amenity"="restaurant"](area.searchArea);
      relation["amenity"="restaurant"](area.searchArea);
    );
    out center;
    """

    response = requests.post(url, data=query)
    data = response.json()

    restaurants = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        result = json.dumps(tags)

        restaurants.append(result)
        # restaurants.append("name = " + tags.get("name", "N/A") + " cuisine = " + tags.get("cuisine", "N/A") )
        # restaurants.append({
        #     "name": tags.get("name"),
        #     "cuisine": tags.get("cuisine"),
        #     "lat": element.get("lat") or element.get("center", {}).get("lat"),
        #     "lon": element.get("lon") or element.get("center", {}).get("lon")
        # })

    return restaurants[:max_results]


if __name__ == "__main__":
    # results = search_osm_restaurants("San Francisco")
    # print(results[:5])

    mcp.run(transport="sse")
