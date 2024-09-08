from typing import Dict, List


class TeamsResource:
    def __init__(self, http_client):
        self.http_client = http_client

    def list(self) -> Dict[str, List[Dict]]:
        """List all teams."""
        return self.http_client.get("/teams")

    def get(self, team_id: str) -> Dict:
        """Show a single team."""
        return self.http_client.get(f"/teams/{team_id}")

    def create(self, team_data: Dict) -> Dict:
        """Create a new team."""
        return self.http_client.post("/teams", data=team_data)
