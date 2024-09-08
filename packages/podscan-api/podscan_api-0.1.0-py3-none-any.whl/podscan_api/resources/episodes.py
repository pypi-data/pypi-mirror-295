from typing import Dict

from ..exceptions import PodScanException


class EpisodesResource:
    def __init__(self, http_client):
        self.http_client = http_client

    def search(self, query: str, page: int = 1, per_page: int = 20, **params) -> Dict:
        """
        Search for episodes.

        Args:
            query (str): The search query.
            page (int, optional): The page number for pagination. Defaults to 1.
            per_page (int, optional): The number of results per page. Defaults to 20.
            **params: Additional parameters to be passed to the API.

        Returns:
            Dict: The search results containing episodes and pagination information.

        Raises:
            PodScanException: If the API request fails.
        """
        params.update({"query": query, "page": page, "per_page": per_page})
        try:
            return self.http_client.get("/episodes/search", params=params)
        except Exception as e:
            raise PodScanException(f"Failed to search episodes: {str(e)}")

    def get_recent(self, page: int = 1, per_page: int = 20, **params) -> Dict:
        """
        Get the most recent episodes.

        Args:
            page (int, optional): The page number for pagination. Defaults to 1.
            per_page (int, optional): The number of results per page. Defaults to 20.
            **params: Additional parameters to be passed to the API.

        Returns:
            Dict: The recent episodes and pagination information.

        Raises:
            PodScanException: If the API request fails.
        """
        params.update({"page": page, "per_page": per_page})
        try:
            return self.http_client.get("/episodes/recent", params=params)
        except Exception as e:
            raise PodScanException(f"Failed to get recent episodes: {str(e)}")

    def get(
        self,
        episode_id: str,
        show_full_podcast: bool = False,
        word_level_timestamps: bool = False,
    ) -> Dict:
        """
        Show a single episode.

        Args:
            episode_id (str): The ID of the episode.
            show_full_podcast (bool, optional): Whether to show the full podcast information. Defaults to False.
            word_level_timestamps (bool, optional): Whether to show word-level timestamps in the transcript. Defaults to False.

        Returns:
            Dict: The episode details.

        Raises:
            PodScanException: If the API request fails.
        """
        params = {
            "show_full_podcast": str(show_full_podcast).lower(),
            "word_level_timestamps": str(word_level_timestamps).lower(),
        }
        try:
            return self.http_client.get(f"/episodes/{episode_id}", params=params)
        except Exception as e:
            raise PodScanException(f"Failed to get episode {episode_id}: {str(e)}")
