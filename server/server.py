from mcp.server.fastmcp import FastMCP
import requests
import pandas as pd

mcp = FastMCP(name="Add", stateless_http=True)

@mcp.tool()
def retrieve_pokemon_data(pokemon: str) -> dict:
    """
    Uses PokeAPI to retrieve Pokemon data based on the Pokemon entered by the user.
    Contain information about the Pokemon such as:
    id, name, base_experience, height, weight, abilities, forms, game indices, location_area_encounters, moves, types, species, stats
    
    """
    pokemon = pokemon.strip().lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    # api call
    response = requests.get(url)

    # format result
    if response.status_code == 200:
        return response.json()
    else:
        return {"message":"Pokemon Not Found","status":response.status_code}

@mcp.tool()
def query_sales_data(year: int, month: int) -> dict:
    """
    Query Sales dataset for sales data in the company.
    Have the following columns: Order ID, amount, profit, quantity, category, state, year-month.
    Able to compute profit and quantity of each category of product sold in each state of the given year and month
    
    """
    # read data
    data = pd.read_csv("Sales Dataset.csv")
    # format and filter based on year month
    data["Year-Month"] = pd.to_datetime(data["Year-Month"], format = "%Y-%m")
    data["Year"] = data["Year-Month"].dt.year
    data["Month"] = data["Year-Month"].dt.month
    data = data[(data["Year"]==year) & (data["Month"]==month)].copy()

    # compute result
    if len(data)>0:
        result = data.groupby(["State","Category"])[["Profit","Quantity"]].sum().to_dict(orient="index")
        result_dict = {"result": result}
        return result_dict
    else:
        return {"messeage": "Provided Filters does not yield any result"}


mcp.run(transport="streamable-http")