import json
import os
import time
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel


class CrawlResponse(BaseModel):
    id: str
    created_at: Optional[str] = None
    state: Optional[str] = None
    base_url: Optional[str] = None
    goal: Optional[str] = None
    children_paths: Optional[List[str]] = None
    json_schema: Optional[str] = None
    errors: Optional[List] = None
    documents: Optional[List[Dict[str, Any]]] = None

    class Config:
        extra = "ignore"


class BriefCrawlInfo(BaseModel):
    id: str
    state: str

    class Config:
        extra = "ignore"


class SaldorClient:
    def __init__(
        self, api_key: Optional[str] = None, base_url="https://api.saldor.com"
    ):
        if not api_key:
            api_key = os.environ.get("SALDOR_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as SALDOR_API_KEY environment variable"
                )

        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"APIKey {api_key}"}

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code >= 400:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        return response.json()["data"]

    def get_crawl(self, crawl_id: str) -> CrawlResponse:
        response = requests.get(
            f"{self.base_url}/crawl/{crawl_id}",
            headers=self.headers,
        )

        data = self._handle_response(response)
        return CrawlResponse(**data)

    def wait_for_crawl(
        self, crawl_id: str, timeout_ms: int = 5000, interval_ms: int = 1000
    ) -> CrawlResponse:
        start_time = time.time()
        while timeout_ms == 0 or time.time() - start_time < timeout_ms / 1000:
            crawl_result = self.get_crawl(crawl_id)
            if crawl_result.state == "completed":
                return crawl_result

            elif crawl_result.state in ["failed", "cancelled"]:
                raise Exception(f"Crawl {crawl_result.state}")

            time.sleep(interval_ms / 1000)
        raise Exception("Crawl timed out")

    def crawl(
        self,
        url: str,
        goal: str = "",
        max_pages: Optional[int] = None,
        max_depth: Optional[int] = None,
        render: Optional[bool] = None,
        children_paths: Optional[List[str]] = None,
        json_schema: Optional[BaseModel] = None,
    ) -> CrawlResponse:
        crawl_job = self.crawl_async(
            url, goal, max_pages, max_depth, render, children_paths, json_schema
        )

        return self.wait_for_crawl(crawl_job.id, timeout_ms=0)

    def crawl_async(
        self,
        url: str,
        goal: str = "",
        max_pages: Optional[int] = None,
        max_depth: Optional[int] = None,
        render: Optional[bool] = None,
        children_paths: Optional[List[str]] = None,
        json_schema: Optional[BaseModel] = None,
    ) -> CrawlResponse:
        payload = {
            "url": url,
            "goal": goal,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "render": render,
            "children_paths": children_paths,
            "json_schema": json.dumps(json_schema.model_json_schema())
            if json_schema
            else None,
        }
        response = requests.post(
            f"{self.base_url}/crawl",
            json=payload,
            headers=self.headers,
        )

        data = self._handle_response(response)
        return CrawlResponse(**data)

    def list_crawls(self, state: str = "") -> List[BriefCrawlInfo]:
        response = requests.get(
            f"{self.base_url}/crawl",
            params={"state": state},
            headers=self.headers,
        )
        data = self._handle_response(response)
        return [BriefCrawlInfo(**crawl) for crawl in data if isinstance(crawl, dict)]
