from praxis.core.http import HttpClient
from praxis.models.response import Response 

class SortingAPI:
    """
    API for logistical sorting skills.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def sort(
            self,
            items: list[dict],
            bins: list[dict],
            criteria: str,
    ) -> Response[dict]:
        """
        Sort items into bins based on a specified attribute.
        """
        payload = {
            "items": items,
            "bins": bins,
            "criteria": criteria
        }

        return self._http.post(
            "/api/v1/skills/sort",
            json=payload,
        )
