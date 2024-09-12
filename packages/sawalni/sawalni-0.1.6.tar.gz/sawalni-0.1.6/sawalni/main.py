from typing import List, Union, Dict, Any, Optional
import requests
import os

SAWALNI_API_KEY = os.getenv("SAWALNI_API_KEY")


class Sawalni:
    def __init__(
        self, api_key: Optional[str] = None, base_url: str = "https://api.sawalni.com"
    ):
        self.api_key = api_key or SAWALNI_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key must be provided either through the constructor or SAWALNI_API_KEY environment variable."
            )
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _request(
        self, method: str, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json()["data"]

    def embed(
        self, input: Union[str, List[str]], model: str = "madmon"
    ) -> Dict[str, Any]:
        """
        Generate multilingual embeddings for text.

        Args:
            input (Union[str, List[str]]): Single text or list of texts to generate embeddings for.
            model (str, optional): Model to use for embedding generation. Defaults to "madmon".

        Returns:
            Dict[str, Any]: Embeddings response.
        """
        data = {"input": input, "model": model}
        return self._request("POST", "/v1/embeddings", data)

    def identify(
        self, input: Union[str, List[str]], model: str = "gherbal-mini", top: int = 1
    ) -> Dict[str, Any]:
        """
        Identify language of text.

        Args:
            input (Union[str, List[str]]): Single text or list of texts to identify language for.
            model (str, optional): Model to use for language identification. Defaults to "gherbal-mini".
            top (int, optional): Number of top language predictions to return (-1 for all). Defaults to 1.

        Returns:
            Dict[str, Any]: Language identification response.
        """
        data = {"input": input, "model": model, "top": top}
        return self._request("POST", "/v1/language/identify", data)

    def translate(
        self, text: str, source: str, target: str, model: str = "tarjamli-medium"
    ) -> Dict[str, Any]:
        """
        Translate text from one language to another.

        Args:
            text (str): Text to be translated.
            source (str): Source language code.
            target (str): Target language code.
            model (str, optional): Model to use for translation. Defaults to "tarjamli-medium".

        Returns:
            Dict[str, Any]: Translation response.
        """
        data = {"text": text, "source": source, "target": target, "model": model}
        return self._request("POST", "/v1/language/translate", data)


class SawalniAsync:
    def __init__(self, api_key: str, base_url: str = "https://api.sawalni.com"):
        self.api_key = api_key or SAWALNI_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key must be provided either through the constructor or SAWALNI_API_KEY environment variable."
            )
        self.base_url = base_url

    async def _request(
        self, method: str, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        import aiohttp

        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        ) as session:
            async with session.request(method, url, json=data) as response:
                response.raise_for_status()
                return await response.json()["data"]

    async def embed(
        self, input: Union[str, List[str]], model: str = "madmon-mini"
    ) -> Dict[str, Any]:
        data = {"input": input, "model": model}
        return await self._request("POST", "/v1/embeddings", data)

    async def identify(
        self, input: Union[str, List[str]], model: str = "gherbal-mini", top: int = 1
    ) -> Dict[str, Any]:
        data = {"input": input, "model": model, "top": top}
        return await self._request("POST", "/v1/language/identify", data)

    async def translate(
        self, text: str, source: str, target: str, model: str = "tarjamli-medium"
    ) -> Dict[str, Any]:
        data = {"text": text, "source": source, "target": target, "model": model}
        return await self._request("POST", "/v1/language/translate", data)
