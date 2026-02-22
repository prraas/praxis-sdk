from praxis.core.http import HttpClient
from praxis.models.response import Response

class AnalyticsAPI:
    """
    Analytics API to track token usage, cost, and rate limits.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def get_stats(self, days: int = 7, endpoint: str | None = None) -> Response[dict]:
        """
        Get aggregated usage statistics, cost breakdown, and success rates.
        """
        params = {"days": days}
        if endpoint:
            params["endpoint"] = endpoint
            
        return self._http.get("/api/v1/analytics/stats", params=params)

    def get_logs(self, limit: int = 50, endpoint: str | None = None) -> Response[dict]:
        """
        Get detailed recent API usage logs for tracing and auditing.
        """
        params = {"limit": limit}
        if endpoint:
            params["endpoint"] = endpoint
            
        return self._http.get("/api/v1/analytics/logs", params=params)
