from typing import Dict


class PodcastsResource:
    def __init__(self, http_client):
        self.http_client = http_client

    def suggest(self, url: str) -> Dict:
        """Suggest a podcast to be added to the database."""
        return self.http_client.post("/podcasts/suggest", data={"url": url})

    def search(self, query: str, **params) -> Dict:
        """Search for podcasts."""
        params["query"] = query
        return self.http_client.get("/podcasts/search", params=params)

    def get(self, podcast_id: str) -> Dict:
        """Show a single podcast."""
        return self.http_client.get(f"/podcasts/{podcast_id}")

    def get_related(self, podcast_id: str) -> Dict:
        """List related podcasts."""
        return self.http_client.get(f"/podcasts/{podcast_id}/related_podcasts")

    def get_episodes(self, podcast_id: str, **params) -> Dict:
        """List all episodes for a podcast."""
        return self.http_client.get(f"/podcasts/{podcast_id}/episodes", params=params)
