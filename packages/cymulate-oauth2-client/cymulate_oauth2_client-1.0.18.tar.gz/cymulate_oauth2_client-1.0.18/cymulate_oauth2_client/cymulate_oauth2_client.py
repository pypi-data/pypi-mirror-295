import time
import requests
import logging
import re
import atexit
import threading
import aiohttp
import asyncio
from requests.exceptions import RequestException, HTTPError
from urllib.parse import urlparse
from typing import Optional, Dict, Any, final, Union, Self
from tenacity import retry, stop_after_attempt, wait_fixed
from .api_paths import GETPaths, POSTPaths, PUTPaths, DELETEPaths
from .cymulate_decorators import synchronized, log_exceptions, retry_on_failure

JsonResponse = Dict[str, Any]
Headers = Optional[Dict[str, str]]

@final
class CymulateOAuth2Client:
    ISSUER: str = 'cymulate.com'
    AUDIENCE: str = 'cymulate.com'

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_url: str,
            scope: Optional[str] = None,
            max_retries: int = 3,
            retry_delay: int = 2,
            log_level: int = logging.INFO
    ) -> None:
        self._validate_client_id(client_id)
        self._validate_base_url(base_url)

        self.token_lock = threading.Lock()
        self._initialize_credentials(client_id, client_secret, base_url, scope)
        self._initialize_retry_settings(max_retries, retry_delay)
        self._initialize_token_urls(base_url)
        self._initialize_tokens()
        self._setup_logging(log_level)
        self._register_exit_handler()

    def _initialize_credentials(self, client_id: str, client_secret: str, base_url: str, scope: Optional[str]) -> None:
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.base_url: str = base_url.rstrip('/')
        self.scope: Optional[str] = scope

    def _initialize_retry_settings(self, max_retries: int, retry_delay: int) -> None:
        self.max_retries: int = max_retries
        self.retry_delay: int = retry_delay

    def _initialize_token_urls(self, base_url: str) -> None:
        self.token_url: str = f"{self.base_url}/oauth2/token"
        self.revoke_url: str = f"{self.base_url}/oauth2/revoke"

    def _initialize_tokens(self) -> None:
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: float = 0.0
        self.tokens_revoked: bool = False

    def _setup_logging(self, log_level: int) -> None:
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

    def _register_exit_handler(self) -> None:
        atexit.register(self._revoke_tokens_on_exit)

    @staticmethod
    def _validate_client_id(client_id: str) -> None:
        if not re.fullmatch(r"^[a-fA-F0-9]{24}$", client_id):
            raise ValueError(
                f"Invalid client_id: {client_id}. Must be a valid 24-character hexadecimal MongoDB ObjectId."
            )

    @staticmethod
    def _validate_base_url(base_url: str) -> None:
        parsed_url = urlparse(base_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid base_url: {base_url}. Must be a valid URL.")

    def _make_request(self, url: str, data: JsonResponse, headers: Headers = None) -> JsonResponse:
        headers = headers or {}
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()

    async def _make_async_request(self, url: str, data: JsonResponse, headers: Headers = None) -> JsonResponse:
        headers = headers or {}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    @synchronized(threading.Lock())
    def _ensure_valid_token(self) -> None:
        if self.access_token is None or time.time() >= self.token_expires_at - 30:
            if self.refresh_token:
                self._refresh_access_token()
            else:
                self._get_new_tokens()

    async def _ensure_valid_token_async(self) -> None:
        if self.access_token is None or time.time() >= self.token_expires_at - 30:
            if self.refresh_token:
                await self._refresh_async_access_token()
            else:
                await self._get_new_async_tokens()

    def _refresh_access_token(self) -> Self:
        if not self.refresh_token:
            self.logger.info("No refresh token available. Obtaining new tokens.")
            self._get_new_tokens()
            return self

        self.logger.info("Refreshing access token...")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            response_data = self._make_request(self.token_url, data)
            self._set_tokens(response_data)
        except RequestException:
            self.logger.warning("Failed to refresh token, obtaining new tokens.")
            self._get_new_tokens()

        return self

    async def _refresh_async_access_token(self) -> Self:
        if not self.refresh_token:
            self.logger.info("No refresh token available. Obtaining new tokens (async).")
            await self._get_new_async_tokens()
            return self

        self.logger.info("Refreshing access token (async)...")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        try:
            response_data = await self._make_async_request(self.token_url, data)
            self._set_tokens(response_data)
        except RequestException:
            self.logger.warning("Failed to refresh token (async), obtaining new tokens.")
            await self._get_new_async_tokens()

        return self

    def _get_new_tokens(self) -> None:
        """Obtain new tokens synchronously from the OAuth2 server."""
        self.logger.info("Obtaining new access token...")
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.AUDIENCE,
            'issuer': self.ISSUER,
        }
        if self.scope:
            data['scope'] = self.scope

        response_data = self._make_request(self.token_url, data)
        self._set_tokens(response_data)

    async def _get_new_async_tokens(self) -> None:
        """Obtain new tokens asynchronously from the OAuth2 server."""
        self.logger.info("Obtaining new access token (async)...")
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.AUDIENCE,
            'issuer': self.ISSUER,
        }
        if self.scope:
            data['scope'] = self.scope

        response_data = await self._make_async_request(self.token_url, data)
        self._set_tokens(response_data)

    def _set_tokens(self, response_data: Dict[str, Any]) -> None:
        self.access_token = response_data.get('access_token')
        self.refresh_token = response_data.get('refresh_token')
        self.token_expires_at = time.time() + response_data.get('expires_in', 3600)
        self.logger.info("Access token set successfully. Token expires at {}".format(time.ctime(self.token_expires_at)))

    def _prepare_headers(self, headers: Headers) -> Dict[str, str]:
        headers = headers or {}
        headers['Authorization'] = f'Bearer {self.access_token}'
        return headers

    @log_exceptions(logging.getLogger(__name__))
    @retry_on_failure(max_retries=3, delay=2)
    def request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        self._ensure_valid_token()
        headers = self._prepare_headers(kwargs.pop('headers', {}))

        try:
            response = self._perform_request(method, url, headers, **kwargs)
            if response.status_code == 401:
                self.logger.info("Unauthorized. Refreshing token and retrying request.")
                self._refresh_access_token()
                headers['Authorization'] = f'Bearer {self.access_token}'
                response = self._perform_request(method, url, headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Get response body if available, otherwise report 'No response body'
            response_text = e.response.text if hasattr(e, 'response') and e.response else "No response body"
            self.logger.error(
                f"HTTP error {e.response.status_code if e.response else 'Unknown'}: {response_text}, URL: {url}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {type(e).__name__}, URL: {url}, Error: {str(e)}")
            raise

    @log_exceptions(logging.getLogger(__name__))
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    async def async_request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        await self._ensure_valid_token_async()
        headers = self._prepare_headers(kwargs.pop('headers', {}))

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, headers=headers, **kwargs) as response:
                    response.raise_for_status()
                    if response.status == 401:
                        self.logger.info("Unauthorized (async). Refreshing token and retrying request.")
                        await self._refresh_async_access_token()
                        headers['Authorization'] = f'Bearer {self.access_token}'
                        async with session.request(method, url, headers=headers, **kwargs) as retry_response:
                            retry_response.raise_for_status()
                            return await retry_response.json()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                if hasattr(e, 'response') and e.response is not None:
                    response_text = await e.response.text()
                    self.logger.error(f"HTTP error {e.status}: {response_text}, URL: {url}", exc_info=False, stacklevel=0)
                else:
                    self.logger.error(f"HTTP error {e.status}: No response body, URL: {url}", exc_info=False, stacklevel=0)
                raise
            except aiohttp.ClientError as e:
                self.logger.error(f"Client error: {type(e).__name__}, URL: {url}, Error: {str(e)}", exc_info=False, stacklevel=0)
                raise

    def _perform_request(self, method: str, url: str, headers: Headers, **kwargs: Any) -> requests.Response:
        """Internal method to perform a synchronous HTTP request and handle retries."""
        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if isinstance(e, HTTPError) and e.response is not None:
                    self.logger.error(f"HTTP error {e.response.status_code}: {e.response.text}, URL: {url}")
                else:
                    self.logger.warning(f"{type(e).__name__} on attempt {attempt + 1}: {str(e)}")
                if isinstance(e, HTTPError) and e.response is not None and e.response.status_code >= 455:
                    raise
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    async def _perform_async_request(self, method: str, url: str, headers: Headers,
                                     **kwargs: Any) -> aiohttp.ClientResponse:
        """Internal method to perform an async HTTP request and handle retries."""
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(method, url, headers=headers, **kwargs) as response:
                        if response.status != 200:
                            # Capture response body for non-200 responses
                            response_text = await response.text()
                            self.logger.error(f"HTTP error {response.status}: {response_text}, URL: {url}")
                        response.raise_for_status()  # This will raise for any 4xx/5xx errors
                        return response
            except aiohttp.ClientResponseError as e:
                response_text = await e.response.text() if e.response else "No response body"
                self.logger.error(f"HTTP error {e.status}: {response_text}, URL: {url}")
                if e.status >= 455:
                    raise
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise
            except aiohttp.ClientError as e:
                self.logger.warning(f"{type(e).__name__} on attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise

    async def aget(self, path: Union[str, GETPaths], **kwargs: Any) -> Dict[str, Any]:
        return await self.async_request('GET', f"{self.base_url}{path}", **kwargs)

    def get(self, path: Union[str, GETPaths], **kwargs: Any) -> Dict[str, Any]:
        return self.request('GET', f"{self.base_url}{path}", **kwargs)

    async def apost(self, path: Union[str, POSTPaths], data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None,
                    **kwargs: Any) -> Dict[str, Any]:
        return await self.async_request('POST', f"{self.base_url}{path}", data=data, json=json, **kwargs)

    def post(self, path: Union[str, POSTPaths], data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None,
             **kwargs: Any) -> Dict[str, Any]:
        return self.request('POST', f"{self.base_url}{path}", data=data, json=json, **kwargs)

    async def aput(self, path: Union[str, PUTPaths], data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        return await self.async_request('PUT', f"{self.base_url}{path}", data=data, **kwargs)

    def put(self, path: Union[str, PUTPaths], data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        return self.request('PUT', f"{self.base_url}{path}", data=data, **kwargs)

    async def adelete(self, path: Union[str, DELETEPaths], **kwargs: Any) -> Dict[str, Any]:
        return await self.async_request('DELETE', f"{self.base_url}{path}", **kwargs)

    def delete(self, path: Union[str, DELETEPaths], **kwargs: Any) -> Dict[str, Any]:
        return self.request('DELETE', f"{self.base_url}{path}", **kwargs)

    @log_exceptions(logging.getLogger(__name__))
    def revoke_token(self, token: Optional[str] = None, token_type_hint: str = 'access_token') -> None:
        if self.tokens_revoked:
            self.logger.info("Tokens already revoked, skipping further revocation.")
            return

        if not token:
            token = self.refresh_token if token_type_hint == 'refresh_token' else self.access_token
            if not token:
                self.logger.error(f"No {token_type_hint} available to revoke.")
                return

        self.logger.info(f"Revoking {token_type_hint}...")
        data = {
            'token': token,
            'token_type_hint': token_type_hint
        }

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response_data = self._make_request(self.revoke_url, data, headers)
            if 'message' in response_data and response_data['message'] == 'Token revoked successfully':
                self._clear_tokens(token, token_type_hint)
                self.tokens_revoked = True
            else:
                self.logger.error("Failed to revoke token.")
        except Exception as e:
            self.logger.error(f"Failed to revoke {token_type_hint}: {str(e)}")

    def _clear_tokens(self, token: str, token_type_hint: str) -> None:
        if token_type_hint == 'access_token':
            self.access_token = None
        elif token_type_hint == 'refresh_token':
            self.refresh_token = None
        self.token_expires_at = 0
        self.logger.info(f"{token_type_hint.capitalize()} revoked and cleared successfully.")

    @log_exceptions(logging.getLogger(__name__))
    def _revoke_tokens_on_exit(self) -> None:
        if not self.tokens_revoked:
            if self.refresh_token:
                self.logger.info("Revoking refresh_token on script exit...")
                try:
                    self.revoke_token(self.refresh_token, 'refresh_token')
                except Exception as e:
                    self.logger.error(f"Failed to revoke refresh_token: {str(e)}")
                    return

            if self.access_token and not self.tokens_revoked:
                self.logger.info("Revoking access_token on script exit...")
                try:
                    self.revoke_token(self.access_token, 'access_token')
                except Exception as e:
                    self.logger.error(f"Failed to revoke access_token: {str(e)}")
