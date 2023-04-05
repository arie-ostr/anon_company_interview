# import logging
import requests
import time
import pandas
import asyncio
import aiohttp

from data.urls import get_staging_prefix
from infra.utils import remove_keys_from_dict

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.31.3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


class LushaRequest:
    """
    This class encapsulates the request to Lusha APIs
    to be used in tests via function calls

    we can also handle custom headers, QS params, etc.
    """

    def __init__(self, endpoint: str, method: str, payload, headers=HEADERS) -> None:
        # setting the endpoint
        prefix = get_staging_prefix()
        self.url = f"{prefix}/{endpoint}"
        self.endpoint = endpoint

        self.method = method
        self.payload = payload
        self.headers = headers

        self.already_executed = False
        self.dataframe = None

        self._response_json = None
        self._status_code = None

    def execute_request(self):
        """
        Here I might add calls for endpoint via all methods, in a test.
        """
        if self.already_executed:
            raise ValueError("Request already executed")

        start_time = time.time()

        if self.method is None:
            raise NotImplementedError("we dont have a method")
        if self.method.upper() == "GET":
            self.response = requests.get(self.url, headers=self.headers)
        elif self.method.upper() == "POST":
            self.response = requests.post(
                self.url, json=self.payload, headers=self.headers
            )
        elif self.method.upper() == "PUT":
            self.response = requests.put(
                self.url, json=self.payload, headers=self.headers
            )
        elif self.method.upper() == "DELETE":
            self.response = requests.delete(
                self.url, json=self.payload, headers=self.headers
            )
        elif self.method.upper() == "HEAD":
            self.response = requests.head(self.url, headers=self.headers)
        elif self.method.upper() == "OPTIONS":
            self.response = requests.options(self.url, headers=self.headers)
        else:
            raise ValueError("Unsupported HTTP method")

        elapsed_time = time.time() - start_time
        self.request_latency = elapsed_time * 1000  # store time in ms.

        self.already_executed = True  # to avoid bugs
        return self

    def modify_method(self, method):
        """
        for testing with different methods ["GET","HEAD", "OPTIONS"]
        """
        if method in ["POST", "PUT", "DELETE", "GET", "HEAD", "OPTIONS"]:
            self.method = method
        else:
            raise ValueError("Unsupported HTTP method")



    def get_response_json(self):
        if self._response_json is None and self.response is not None:
            self._response_json = self.response.json()
            return self._response_json
        elif self._response_json is not None:
            return self._response_json
        else:
            raise ValueError("Response is empty")

    def extend_payload(self, payload_extra):
        """
        for testing with extra keys
        """
        self.payload.update(payload_extra)

    def remove_from_payload(self, keys_list):
        """
        for testing with missing keys
        """
        remove_keys_from_dict(self.payload, keys_list)

    def get_response_code(self):
        """
        check cached response, its stored here by asynio requests
        """
        if self._status_code is None and self.response.status_code:
            self._status_code = self.response.status_code
            return self._status_code

        else:
            return self._status_code


    def build_dataframe(self):
        """
        for testing with dataframes
        """
        if self.dataframe is None:
            res = self.get_response_json()

            if not isinstance(res, list):
                raise ValueError("only supported for lists now")

            for item in res:
                if not isinstance(item, dict):
                    raise ValueError("only supported for lists of dicts now")

            self.dataframe = pandas.json_normalize(res)

            return self.dataframe
        else:
            return self.dataframe

    def get_items_in_res(self, by_key):
        """extract a series"""
        if isinstance(by_key,str):
            return list(self.build_dataframe()[by_key])
        elif isinstance(by_key, list):
            df_list = self.build_dataframe()[by_key]
            list_of_tuples = [tuple(row) for row in df_list.itertuples(index=False)]
            return list_of_tuples
        else:
            raise ValueError("unsupported key type")

    @staticmethod
    async def _execute_post_request(url, session, payload, headers):
        async with session.post(url, json=payload, headers=headers) as response:
            jsondata = await response.json()
            status = response.status
            return {"json":jsondata,
                    "status":status,
                    "payload":payload}

    @staticmethod
    async def _execute_requests_async(request_list):
        async with aiohttp.ClientSession() as session:
            tasks = []

            for request in request_list:
                tasks.append(
                    LushaRequest._execute_post_request(
                        request.url, session, request.payload, request.headers
                    )
                )
            responses = await asyncio.gather(*tasks)
            return responses
            
        
    @staticmethod 
    def execute_requests_async(request_list):
        """
        we got to the point where we need to do 100+ requests per test param
        there is no way around it other than to use async
        and gather the results. 
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(LushaRequest._execute_requests_async(request_list))
        responses = loop.run_until_complete(future)

        #lock requests
        for res in request_list:
            res.already_executed = True


        return responses