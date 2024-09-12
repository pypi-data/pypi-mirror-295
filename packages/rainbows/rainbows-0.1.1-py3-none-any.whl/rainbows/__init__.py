# File: rainbows/__init__.py

import os
import requests
from typing import List, Optional, Dict, Any


class Bow:

    def __init__(self,
                 api_url: str = "https://job-api-DavidBudaghyan.replit.app",
                 api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("RAINBOWS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set as RAINBOWS_API_KEY environment variable"
            )
        self.base_url = api_url  # Replace with your actual API URL

    def _make_request(self,
                      method: str,
                      endpoint: str,
                      data: Optional[Dict] = None,
                      params: Optional[Dict] = None):
        headers = {
            "coalition": self.api_key,
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method,
                                    url,
                                    headers=headers,
                                    json=data,
                                    params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error occurred: {e}")
            print(f"Response content: {response.content}")
            raise
        return response.json()

    def get_jobs(self, **kwargs) -> Dict[str, Any]:
        # Convert title_search_criteria if present
        if 'title_search_criteria' in kwargs:
            kwargs['title_search_criteria'] = [{
                'include':
                criteria.get('include'),
                'exclude':
                criteria.get('exclude'),
                'mode':
                criteria.get('mode', 'and')
            } for criteria in kwargs['title_search_criteria']]

        return self._make_request("POST", "get_jobs", data=kwargs)

    def upsert_jobs(self, jobs: List[Dict[str, Any]]) -> Dict[str, str]:
        return self._make_request("POST", "upsert_jobs", data={"jobs": jobs})

    def upsert_from_jsonl(
            self,
            file_path: str,
            jsonl_batch_size: int = 8000,
            upsert_batch_size: Optional[int] = None) -> Dict[str, List[Dict[str, str]]]:
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file, 'application/octet-stream')}
            params = {'jsonl_batch_size': jsonl_batch_size, 'upsert_batch_size': upsert_batch_size}
            headers = {"coalition": self.api_key}
            url = f"{self.base_url}/upsert_from_jsonl"
            response = requests.post(url,
                                     headers=headers,
                                     files=files,
                                     params=params)
            response.raise_for_status()
            return response.json()
