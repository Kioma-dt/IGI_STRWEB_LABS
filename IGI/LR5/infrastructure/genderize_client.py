import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class GenderResult:
    name: str
    gender: Optional[str]
    probability: float
    count: int


class GenderizeAPIError(Exception):
    pass


class GenderizeClient:
    BASE_URL = "https://api.genderize.io"

    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def get_gender(self, name: str, country_id: str | None = None) -> GenderResult:
        if not name:
            raise ValueError("Name cannot be empty")

        params = {"name": name}

        if country_id:
            params["country_id"] = country_id

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            raise GenderizeAPIError(f"Request failed: {e}")

        if response.status_code != 200:
            raise GenderizeAPIError(
                f"API error: {response.status_code}, body={response.text}"
            )

        data = response.json()

        return GenderResult(
            name=data.get("name"),
            gender=data.get("gender"),
            probability=float(data.get("probability") or 0),
            count=int(data.get("count") or 0),
        )