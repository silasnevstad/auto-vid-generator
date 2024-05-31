import requests
from config.settings import PEXELS_API_KEY


class PexelsAPI:
    def __init__(self):
        self.api_url_photos = "https://api.pexels.com/v1"
        self.api_url_videos = "https://api.pexels.com/videos"
        self.headers = {
            "Authorization": PEXELS_API_KEY
        }
        self.request = None
        self.json = None
        self.page = None
        self.total_results = None
        self.page_results = None
        self.has_next_page = None
        self.has_previous_page = None
        self.next_page = None
        self.prev_page = None

    def search_photos(self, query, orientation=None, size=None, color=None, locale=None, page=1, per_page=15):
        query = query.replace(" ", "+")
        url = f"{self.api_url_photos}/search"
        params = {
            "query": query,
            "orientation": orientation,
            "size": size,
            "color": color,
            "locale": locale,
            "page": page,
            "per_page": per_page
        }
        self.__request(url, params)
        return None if not self.request else self.json

    def search_videos(self, query, orientation=None, size=None, locale=None, page=1, per_page=15):
        query = query.replace(" ", "+")
        url = f"{self.api_url_videos}/search"
        params = {
            "query": query,
            "orientation": orientation,
            "size": size,
            "locale": locale,
            "page": page,
            "per_page": per_page
        }
        self.__request(url, params)
        return None if not self.request else self.json

    def curated_photos(self, page=1, per_page=15):
        url = f"{self.api_url_photos}/curated"
        params = {
            "page": page,
            "per_page": per_page
        }
        self.__request(url, params)
        return None if not self.request else self.json

    def popular_videos(self, min_width=None, min_height=None, min_duration=None, max_duration=None, page=1,
                       per_page=15):
        url = f"{self.api_url_videos}/popular"
        params = {
            "min_width": min_width,
            "min_height": min_height,
            "min_duration": min_duration,
            "max_duration": max_duration,
            "page": page,
            "per_page": per_page
        }
        self.__request(url, params)
        return None if not self.request else self.json

    def get_photo(self, photo_id):
        url = f"{self.api_url_photos}/photos/{photo_id}"
        self.__request(url)
        return None if not self.request else self.json

    def get_video(self, video_id):
        url = f"{self.api_url_videos}/videos/{video_id}"
        self.__request(url)
        return None if not self.request else self.json

    def download_video(self, query, output_path,
                       orientation=None, size=None, locale=None, min_duration=None, max_duration=None):
        video = self.__get_video_with_criteria(query, orientation, size, locale, min_duration, max_duration)
        if not video:
            return None
        with open(output_path, 'wb+') as f:
            f.write(requests.get(video.get("video_files")[0].get("link")).content)

    def __get_video_with_criteria(self, query,
                                  orientation=None, size=None, locale=None, min_duration=None, max_duration=None,
                                  page=1, per_page=15):
        while True:
            videos = self.search_videos(query, orientation, size, locale, page, per_page)
            if not videos:
                return None
            for video in videos['videos']:
                if self.__ensure_video_length(video, min_duration, max_duration):
                    return video
            page += 1

    @staticmethod
    def __ensure_video_length(video, min_duration=None, max_duration=None):
        duration = video.get("duration")
        if min_duration and duration < min_duration:
            return False
        if max_duration and duration > max_duration:
            return False
        return True

    def __request(self, url, params=None):
        try:
            self.request = requests.get(url, headers=self.headers, params=params, timeout=15)
            self.__update_page_properties()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            self.request = None

    def __update_page_properties(self):
        if self.request.ok:
            self.json = self.request.json()
            self.page = self.json.get("page")
            self.total_results = self.json.get("total_results")
            self.page_results = len(self.json.get("photos", []))
            self.next_page = self.json.get("next_page")
            self.has_next_page = self.next_page is not None
            self.prev_page = self.json.get("prev_page")
            self.has_previous_page = self.prev_page is not None
        else:
            print("Error: Check API key")
            print(self.request)
            print("API key:", self.headers["Authorization"])
            self.request = None
