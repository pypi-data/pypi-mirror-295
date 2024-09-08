from typing import Dict


class AlertsResource:
    def __init__(self, http_client):
        self.http_client = http_client

    def list(self, team_id: str) -> Dict:
        """List all alerts for a team."""
        return self.http_client.get(f"/teams/{team_id}/alerts")

    def create(self, team_id: str, alert_data: Dict) -> Dict:
        """Create a new alert for the team."""
        return self.http_client.post(f"/teams/{team_id}/alerts", data=alert_data)

    def delete(self, team_id: str, alert_id: str) -> Dict:
        """Delete an alert."""
        return self.http_client.delete(f"/teams/{team_id}/alerts/{alert_id}")

    def update(self, team_id: str, alert_id: str, alert_data: Dict) -> Dict:
        """Update an alert."""
        return self.http_client.put(
            f"/teams/{team_id}/alerts/{alert_id}", data=alert_data
        )

    def get_mentions(self, team_id: str, alert_id: str) -> Dict:
        """Get mentions for an alert."""
        return self.http_client.get(f"/teams/{team_id}/alerts/{alert_id}/mentions")
