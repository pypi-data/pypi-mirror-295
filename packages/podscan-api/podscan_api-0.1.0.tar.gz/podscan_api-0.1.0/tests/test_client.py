import unittest
from unittest.mock import Mock, patch

from podscan_api import PodScanClient
from podscan_api.client import HTTPClient
from podscan_api.resources.alerts import AlertsResource
from podscan_api.resources.podcasts import PodcastsResource


class TestPodScanClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.client = PodScanClient(self.api_key)

    def test_client_initialization(self):
        self.assertIsInstance(self.client.http_client, HTTPClient)
        self.assertEqual(self.client.http_client.api_key, self.api_key)
        self.assertIsInstance(self.client.alerts, AlertsResource)
        self.assertIsInstance(self.client.podcasts, PodcastsResource)

    @patch("podscan_api.client.HTTPClient")
    def test_client_resources_use_same_http_client(self, mock_http_client):
        client = PodScanClient(self.api_key)
        self.assertIs(client.alerts.http_client, client.podcasts.http_client)


class TestAlertsResource(unittest.TestCase):
    def setUp(self):
        self.http_client = Mock()
        self.alerts = AlertsResource(self.http_client)

    def test_list_alerts(self):
        team_id = "team123"
        self.alerts.list(team_id)
        self.http_client.get.assert_called_once_with(f"/teams/{team_id}/alerts")

    def test_create_alert(self):
        team_id = "team123"
        alert_data = {"name": "Test Alert"}
        self.alerts.create(team_id, alert_data)
        self.http_client.post.assert_called_once_with(
            f"/teams/{team_id}/alerts", data=alert_data
        )

    def test_delete_alert(self):
        team_id = "team123"
        alert_id = "alert456"
        self.alerts.delete(team_id, alert_id)
        self.http_client.delete.assert_called_once_with(
            f"/teams/{team_id}/alerts/{alert_id}"
        )


class TestPodcastsResource(unittest.TestCase):
    def setUp(self):
        self.http_client = Mock()
        self.podcasts = PodcastsResource(self.http_client)

    def test_search_podcasts(self):
        query = "technology"
        params = {"page": 1, "per_page": 20}
        self.podcasts.search(query, **params)
        expected_params = {"query": query, "page": 1, "per_page": 20}
        self.http_client.get.assert_called_once_with(
            "/podcasts/search", params=expected_params
        )

    def test_get_podcast(self):
        podcast_id = "podcast789"
        self.podcasts.get(podcast_id)
        self.http_client.get.assert_called_once_with(f"/podcasts/{podcast_id}")

    def test_get_related_podcasts(self):
        podcast_id = "podcast789"
        self.podcasts.get_related(podcast_id)
        self.http_client.get.assert_called_once_with(
            f"/podcasts/{podcast_id}/related_podcasts"
        )


if __name__ == "__main__":
    unittest.main()
