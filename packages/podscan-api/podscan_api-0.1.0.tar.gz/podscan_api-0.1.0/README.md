# Podscan API Client

A Python client for interacting with the Podscan.fm API. This client provides an easy-to-use interface for accessing podcast data, creating alerts, and managing teams.

## Features

- Search for podcasts
- Analyze recent episodes
- Create and manage alerts for podcast mentions
- Retrieve podcast and episode information
- Team management

## Installation

To install the Podscan API client, run:

```bash
pip install podscan-api
```

## Usage

To use the Podscan API client, you need to have an API key. You can get your API key by signing up for an account on the [Podscan website](https://podscan.fm) and then creating an API key in your account settings.

Here's an example of how to use the Podscan API client to search for podcasts:

```python
from podscan_api import PodScanClient

client = PodScanClient(api_key='your_api_key')

# Search for podcasts
results = client.podcasts.search(query='technology')

for podcast in results['podcasts']:
    print(f"Podcast Name: {podcast['podcast_name']}")
    print(f"Podcast Description: {podcast['podcast_description']}")
```

## Documentation

For more details on the API, including available endpoints and parameters, please refer to the [Podscan API documentation](https://podscan.fm/docs/api#/).
