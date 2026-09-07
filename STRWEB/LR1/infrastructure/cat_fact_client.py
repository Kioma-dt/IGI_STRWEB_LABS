import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class CatFact:
    fact: str
    length: int


class CatFactAPIError(Exception):
    pass


class CatFactClient:
    BASE_URL = "https://catfact.ninja"

    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def get_random_fact(self, max_length: Optional[int] = None) -> CatFact:

        params = {}

        if max_length is not None:
            params["max_length"] = max_length

        try:
            response = requests.get(
                f"{self.BASE_URL}/fact",
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            raise CatFactAPIError(f"Request failed: {e}")

        if response.status_code != 200:
            raise CatFactAPIError(
                f"API error: {response.status_code}, body={response.text}"
            )

        data = response.json()

        return CatFact(
            fact=data.get("fact", ""),
            length=int(data.get("length", 0)),
        )