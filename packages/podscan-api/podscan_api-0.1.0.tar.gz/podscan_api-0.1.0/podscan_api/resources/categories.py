from typing import Dict, List


class CategoriesResource:
    def __init__(self, http_client):
        self.http_client = http_client

    def list(self) -> Dict[str, List[Dict]]:
        """List all categories."""
        return self.http_client.get("/categories")
