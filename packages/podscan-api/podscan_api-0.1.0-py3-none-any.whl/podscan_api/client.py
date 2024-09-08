from .http_client import HTTPClient
from .resources.alerts import AlertsResource
from .resources.categories import CategoriesResource
from .resources.episodes import EpisodesResource
from .resources.podcasts import PodcastsResource
from .resources.teams import TeamsResource


class PodScanClient:
    def __init__(self, api_key: str):
        self.http_client = HTTPClient(api_key)
        self.alerts = AlertsResource(self.http_client)
        self.categories = CategoriesResource(self.http_client)
        self.episodes = EpisodesResource(self.http_client)
        self.podcasts = PodcastsResource(self.http_client)
        self.teams = TeamsResource(self.http_client)
