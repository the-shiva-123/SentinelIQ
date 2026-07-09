from __future__ import annotations

import logging
from typing import Any, Dict, Optional
import requests
from utils.config import settings

# Setup isolated logger for tracking network anomalies
logger = logging.getLogger("SentinelIQ.APIClient")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class APIClient:
    """Production-grade robust HTTP client wrapper with integrated error tracking."""

    def __init__(self, base_url: Optional[str] = None, timeout: int | None = None) -> None:
        self.base_url = base_url or settings.api_base_url or "http://localhost"
        self.timeout = timeout if timeout is not None else settings.api_timeout_seconds

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        try:
            logger.info(f"Initiating GET request to target: {url}")
            response = requests.get(url, params=params, timeout=self.timeout)
            
            # This triggers an HTTPError automatically for bad status codes (4xx/5xx)
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP Contract Failure on GET {path}: Code {response.status_code} - {http_err}")
            raise http_err
        except requests.exceptions.Timeout:
            logger.error(f"Network Latency Timeout Exceeded ({self.timeout}s) on GET {path}")
            raise TimeoutError(f"Connection timed out while hitting endpoint {path}")
        except requests.RequestException as req_err:
            logger.error(f"Fatal Transport Communication Breakdown on GET {path}: {req_err}")
            raise req_err

    def post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        try:
            logger.info(f"Initiating POST payload distribution to: {url}")
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP Contract Failure on POST {path}: Code {response.status_code} - {http_err}")
            raise http_err
        except requests.exceptions.Timeout:
            logger.error(f"Network Latency Timeout Exceeded ({self.timeout}s) on POST {path}")
            raise TimeoutError(f"Connection timed out while posting to endpoint {path}")
        except requests.RequestException as req_err:
            logger.error(f"Fatal Transport Communication Breakdown on POST {path}: {req_err}")
            raise req_err