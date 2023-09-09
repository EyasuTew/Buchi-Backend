import os

import dotenv
import httpx
import asyncio
from fastapi import HTTPException

dotenv.load_dotenv()
ACCESS_TOKEN = None

async def make_api_call(url, params, headers):
    """
    Helper function to make API calls and handle errors

    Parameters:
    url (str): The URL to make the API call to.
    params (dict): The search parameters for the API call.
    headers (dict): The headers for the API call.

    Returns:
    requests.entities.Response: The API response.
    """
    global ACCESS_TOKEN
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        # tasks = [client.get(f"" + url + "/{url_param}") for url_param in params]
        # response = await asyncio.gather(*tasks)

    if response.status_code == 401 and "expired" in response.json()["detail"]:
        # If access token is expired, generate a new one and make API call again
        print("Access token expired. Regenerating...")
        ACCESS_TOKEN = await get_access_token()
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
        print("Access token regenerated." + "*" * 50)
    elif response.status_code != 200:
        # Raise an exception if the API call failed
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response


async def get_access_token():
    """
    Function to get a new access token from the Petfinder API

    Returns:
    str: The access token
    """
    global ACCESS_TOKEN

    print("Getting access token...")
    url = "https://api.petfinder.com/v2/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("CLIENT_ID","WTbqnSJ2VqHbtG5J1LDuh5uUAQHUGXSoy5QbYao4CShaDhTYP3"),
        "client_secret": os.environ.get("CLIENT_SECRET","AoI3WEOcRD9MgHPmAWoh5y7pcuCENp45oJFBW1X6"),
    }
    print("data = ", data)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        print("respomse...", response)
        response.raise_for_status()
    ACCESS_TOKEN = response.json().get("access_token")
    return ACCESS_TOKEN


async def get_petfinder_results(search):
    """
    Function to get search results from the Petfinder API

    Parameters:
    search (dict): The search parameters for the API call.

    Returns:
    list: A list of dictionaries containing the search results.
    """
    # print("Getting petfinder results...")
    global ACCESS_TOKEN

    if not ACCESS_TOKEN:
        ACCESS_TOKEN = await get_access_token()
    print("ACCESS_TOKEN...",ACCESS_TOKEN)
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = "https://api.petfinder.com/v2/animals"
    response = await make_api_call(url, search, headers=headers)
    data = response.json()["animals"]
    petfinder_results = []
    for pet in data:
        print("pet...",pet)
        petfinder_results.append(
            {
                "pet_id": pet["id"],
                "source": "petfinder",
                "name": pet["name"],
                "type": pet["type"],
                "good_with_children": pet["environment"]["children"],
                "age": pet["age"],
                "gender": pet["gender"],
                "size": pet["size"],
                "photos": pet["photos"],
            }
        )
    return petfinder_results
