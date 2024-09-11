import requests
import json

class Client:
    def __init__(self, api_key, api_url="http://209.237.157.153:8123"):
        """
        Initialize the client with the given API URL and API key.

        Parameters:
        api_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {"X-API-Key": self.api_key}

    def create_index(self, index_name):
        """
        Create a new index with the specified name.

        Parameters:
        index_name (str): The name of the index to be created.

        Returns:
        dict: JSON response indicating success or failure.
        """
        url = f"{self.api_url}/index"
        params = {"index_name": index_name}
        response = requests.post(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_indices(self):
        """
        List all indices.

        Returns:
        dict: JSON response with the current list of indices.
        """
        url = f"{self.api_url}/index"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_videos(self, index_name, query, asset_ids=None, top_k=30, modes=["video", "image"]):
        """
        Search for videos in the specified index using a query.

        Parameters:
        index_name (str): The name of the index to search in.
        query (str): The search query.
        asset_ids (list): List of asset ids to include search through.
        top_k (int): The number of top results to return. Default is 30.
        modes(list): Type of asset to search for (either video or image).

        Returns:
        dict: JSON response containing the search results.
        """
        url = f"{self.api_url}/index/{index_name}/search"
        body = {
            "query": query,
            "top_k": top_k,
            "modes": modes,
        }
        if asset_ids:
            body["asset_ids"] = asset_ids
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_by_image(self, index_name, image_path, top_k=30):
        """
        Search for videos using an image in the specified index.

        Parameters:
        index_name (str): The name of the index to search in.
        image_path (str): The local file path to the image.
        top_k (int): The number of top results to return. Default is 30.

        Returns:
        dict: JSON response containing the search results.
        """
        url = f"{self.api_url}/index/{index_name}/search_image"
        with open(image_path, "rb") as image_file:
            files = {"image_file": image_file}
            params = {"top_k": top_k}
            response = requests.post(url, files=files, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_by_video(self, index_name, video_path, start_seconds=-1, end_seconds=-1, top_k=30):
        """
        Search for videos using a video in the specified index.

        Parameters:
        index_name (str): The name of the index to search in.
        video_path (str): The local file path to the video.
        start_seconds (int): The start time in seconds for the video segment to search. Default is -1 (start of video).
        end_seconds (int): The end time in seconds for the video segment to search. Default is -1 (end of video).
        top_k (int): The number of top results to return. Default is 30.

        Returns:
        dict: JSON response containing the search results.
        """
        url = f"{self.api_url}/index/{index_name}/search_video"
        with open(video_path, "rb") as video_file:
            files = {"video_file": video_file}
            params = {"top_k": top_k, "start_seconds": start_seconds, "end_seconds": end_seconds}
            response = requests.post(url, files=files, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def answer(self, index_name, query, mode='rag', video_ids=[], system_prompt=None, use_markdown=False):
        """
        Get an answer for a query using the specified index and optional parameters.

        Parameters:
        index_name (str): The name of the index to use.
        query (str): The query to answer.
        mode (str): The mode of the answer, default is 'rag'. Available options: ['all', 'rag']
        video_ids (list): List of video IDs to restrict the answer to. Default uses all videos in the index.
        system_prompt (str): Optional system prompt for additional context.
        use_markdown (bool): Whether to use markdown in the response. Default is False.

        Returns:
        dict: JSON response containing the answer.
        """
        url = f"{self.api_url}/index/{index_name}/answer"
        params = {
                "query": query,
                "mode": mode,
                "use_markdown": use_markdown}
        if system_prompt:
            params['system_prompt'] = system_prompt
        if len(video_ids) > 0:
            params['video_ids'] = ','.join(video_ids)
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_search(self, index_name, search_term, max_videos=10, max_duration=600):
        """
        Index videos from a YouTube search query.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        search_term (str): The search term to use for finding videos on YouTube.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        url = f"{self.api_url}/index/{index_name}/youtube/search"
        body = {"search_term": search_term, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_url(self, index_name, url, max_videos=10, max_duration=600):
        """
        Index videos from a specific YouTube URL.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        url (str): The URL of the YouTube video.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        api_url = f"{self.api_url}/index/{index_name}/youtube/url"
        body = {"url": url, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(api_url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_playlist(self, index_name, playlist_url, max_videos=10, max_duration=600):
        """
        Index videos from a YouTube playlist.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        playlist_url (str): The URL of the YouTube playlist.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        api_url = f"{self.api_url}/index/{index_name}/youtube/playlist"
        body = {"playlist_url": playlist_url, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(api_url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_channel(self, index_name, channel_url, max_videos=10, max_duration=600):
        """
        Index videos from a YouTube channel.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        channel_url (str): The URL of the YouTube channel.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        api_url = f"{self.api_url}/index/{index_name}/youtube/channel"
        body = {"channel_url": channel_url, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(api_url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_video(self, index_name, video_path=None, video_url=None, transcript_path=None, metadata={}):
        """
        Index a local video file along with optional transcript and metadata.

        Parameters:
        index_name (str): The name of the index to add the video to.
        video_path (str, optional): The local file path to the video. Default is None.
        video_url (str, optional): The URL of the video. Default is None.
        transcript_path (str, optional): The local file path to the transcript. Default is None.
        metadata (dict): Additional metadata for the video.

        Returns:
        dict: JSON with the video details of the indexed video.

        Raises:
        ValueError: If neither video_path nor video_url is provided.
        """
        url = f"{self.api_url}/index/{index_name}/video"
        files = {}
        params = {}
        if video_path:
            files["video_file"] = open(video_path, "rb")
        elif video_url:
            params["video_url"] = video_url
        else:
            raise ValueError("Either video_path or video_url must be provided.")

        if transcript_path:
            files["transcript"] = open(transcript_path, "rb")

        # Move all non-member metadata to info dictionary.
        info = {}
        for k in list(metadata.keys()):
            if k not in ['url', 'transcript', 'title', 'description']:
                info[k] = metadata.pop(k)
        metadata['info'] = info

        metadata_str = json.dumps(metadata)
        body = {'metadata_str': metadata_str}
        response = requests.post(url, files=files, data=body, params=params, headers=self.headers, stream=True)
        response.raise_for_status()
        return response.json()

    def get_video_metadata(self, index_name, video_id):
        """
        Retrieve video metada corresponding to video_id.

        Parameters:
        index_name (str): The name of the index to add the video to.
        video_id (str): The id of the video.

        Returns:
        dict: JSON with the video metadata.

        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}/metadata"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_video_metadata(self, index_name, video_id, metadata):
        """
        Update video metada corresponding to video_id.

        Parameters:
        index_name (str): The name of the index to add the video to.
        video_id (str): The id of the video.
        metadata (dict): Updated metadata to overwrite.

        Returns:
        dict: JSON with the video metadata.

        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}/metadata"
        response = requests.put(url, json=metadata, headers=self.headers)
        response.raise_for_status()
        return response.json()



    def list_videos(self, index_name):
        """
        List all videos in the specified index.

        Parameters:
        index_name (str): The name of the index.

        Returns:
        dict: JSON that lists all videos in index.
        """
        url = f"{self.api_url}/index/{index_name}/videos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    api_url = "http://127.0.0.1:8123"#"http://73.202.138.16:8888"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlOYW1lIjoidGVzdHMyIiwiaWF0IjoxNzI0ODE4NTkzfQ.o79y6ZjAPzTPvgyePGflmx7ETB0AQm79hBi-IJ0aBlA"

    client = Client(api_key, api_url=api_url)

    # Create an index
    index_name = "coffee"
    #index_name = "cinematic"
    #client.create_index(index_name)

    '''
    vid = client.index_video(
            index_name,
            video_url='https://videos.pexels.com/video-files/2675515/2675515-hd_1920_1080_30fps.mp4')
            #video_url='https://videos.pexels.com/video-files/6060027/6060027-hd_1080_1920_25fps.mp4')
    '''
    # Index videos from a YouTube search
    #search_term = "coffee brewing"
    #client.index_from_youtube_search(index_name, search_term)

    # Search for videos
    query = "how do I make cold brew"
    results = client.search_videos(index_name, query)
    print(results)

    # List indexed videos
    videos = client.list_videos(index_name)
    print(videos)

