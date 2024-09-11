from time import sleep

import pandas as pd
from tqdm import tqdm

from chainalysis.constants import ANALYTICAL_ENDPOINTS, BASE_URL
from chainalysis.util_functions.exceptions import (
    BadRequest,
    DataSolutionsAPIException,
    DataSolutionsSDKException,
    UnhandledException,
)
from chainalysis.util_functions.requests import issue_request


class Analytical:
    """
    This class provides methods to execute SQL queries on Data Solutions
    analytical tables. It supports fetching results as JSON or a
    pandas DataFrame, and provides query execution statistics.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Analytical class with the provided API key.

        :param api_key: The API key for accessing the analytical service.
        :type api_key: str
        """

        self.api_key = api_key

    def __call__(
        self,
        query: str,
        parameters: dict[str] = {},
        polling_interval_sec: int = 5,
        autopaginate: bool = True,
    ):
        """
        Execute a SQL query asynchronously using the provided parameters
        and polling interval.

        Autopagination is enabled by default. If autopagination is enabled,
        the method will fetch all pages of results and return a single
        Analytical object with all results.

        Otherwise, the method will return an Analytical object with the
        first page of results. Use the next_page() method to fetch the
        next page of results and the stats() method to get statistics
        that can help you determine the approach to take to fetch all results.

        :param query: The SQL query to be executed.
        :type query: str
        :param parameters: A dictionary of parameters to be used in the query.
        :type parameters: dict[str], optional
        :param polling_interval_sec: The interval in seconds between status checks. The minimum value is 5 seconds.
        :type polling_interval_sec: int, optional
        :param autopaginate: Whether to automatically full results instead of individual pages.
        :type autopaginate: bool, optional
        :return: An instance of the Analytical class with query results.
        :rtype: Analytical
        """

        self._status_code = 0
        self.results = []
        self._stats = {}
        self.json_response = {}
        self.dataframe_data = None
        self._status = "error"
        self.error_message = ""
        self.error_details = ""
        self.next_url = None
        self._total_pages = 0
        self.query_id = None
        self.exception = UnhandledException()

        if polling_interval_sec < 5:
            polling_interval_sec = 5

        query_execution_url = (
            f"{BASE_URL['base_url']}/{ANALYTICAL_ENDPOINTS['async_query_execution']}"
        )

        body = {
            "sql": query,
            "parameters": parameters,
        }

        async_response = issue_request(
            api_key=self.api_key,
            url=query_execution_url,
            body=body,
            method="POST",
        )

        self.query_id = async_response.get("query_id")
        if not self.query_id:
            raise DataSolutionsAPIException(
                "Unexpected response. Query ID was not returned."
            )
        async_query_status_url = f"{BASE_URL['base_url']}/{ANALYTICAL_ENDPOINTS['async_query_status']}?query_id={self.query_id}"

        try:
            # The query will execute asynchronously. We need to keep polling the status endpoint to check if the query has completed.
            while True:
                self.json_response = issue_request(
                    api_key=self.api_key,
                    url=async_query_status_url,
                    method="GET",
                )

                self._status = self.json_response["status"]

                if self._status == "running" or self._status == "pending":
                    print(
                        f"Query is still {self._status}. Checking status again in {polling_interval_sec} seconds."
                    )
                    sleep(polling_interval_sec)
                elif self._status == "error":
                    self.error_message = self.json_response["message"]
                    self.error_details = self.json_response.get("details")
                    break
                elif self._status == "success":
                    self._status_code = 200
                    self._stats = self.json_response["stats"]
                    self.results = self.json_response["results"]
                    self.next_url = self.json_response["next"]
                    self._total_pages = self._stats["total_pages"]
                    break
            if autopaginate:
                # We make a new list to avoid modifying the original results list
                results = self.results.copy()
                current_page = self._stats["last_processed_page_index"] + 1
                total_pages = self._total_pages

                # tqdm displays a progress bar while fetching data
                with tqdm(total=total_pages, desc="Fetching data", unit="page") as pbar:
                    while self.has_next():
                        _next_page = self.next_page()
                        if _next_page._status != "error":
                            next_page_results = _next_page.results
                            results.extend(
                                next_page_results
                            )  # Keep appending results to the list
                            pbar.update(1)  # Update the progress bar
                            current_page += 1
                        else:
                            raise _next_page.exception
                    pbar.update(1)  # Update the progress bar to 100%
                self.results = results
                self.next_url = None
        except DataSolutionsSDKException as e:
            self._status = "error"
            self.exception = e.get_exception()
            self._status_code = e.status_code
        except Exception as e:
            self._status = "error"
            self.exception = UnhandledException(
                details=e,
            )

        return self

    def next_page(self):
        """
        Fetch the next page of analytical query results.

        :return: An instance of the Analytical class with the next page of results.
        :rtype: Analytical
        """

        if self.next_url:
            self.json_response = issue_request(
                api_key=self.api_key,
                url=self.next_url,
                method="GET",
            )
            self._status = self.json_response["status"]

            if self._status == "error":
                self.error_message = self.json_response["message"]
                self.error_details = self.json_response.get("details")
            elif self._status == "success":
                self._status = self._status
                self._stats = self.json_response["stats"]
                self.results = self.json_response["results"]
                self.next_url = self.json_response["next"]
        else:
            raise BadRequest(
                "No next page available. Use the method has_next() to check if there is a next page that can be retrieved."
            )
        return self

    def json(self):
        """
        Return results as a JSON.

        :raises Exception: Raises an exception if the query resulted in an error.
        :return: Results of the SQL query as a JSON.
        :rtype: dict
        """

        if self._status != "error":
            return self.results
        else:
            raise self.exception

    def df(self):
        """
        Convert query results into a pandas DataFrame.

        :raises Exception: Raises an exception if the query resulted in an error.
        :return: DataFrame containing the results of the SQL query.
        :rtype: pd.DataFrame
        """
        if self._status != "error":
            self.dataframe_data = pd.DataFrame(self.results)
            return self.dataframe_data
        else:
            raise self.exception

    def stats(self):
        """
        Get the statistics of the executed query.

        :return: Statistics of the query execution.
        :rtype: dict
        """

        if self._status != "error":
            return self._stats
        else:
            raise self.exception

    def status_code(self):
        """
        Get the HTTP status code of the response.

        :return: HTTP status code.
        :rtype: int
        """

        return self._status_code

    def was_successful(self):
        """
        Determine if the query executed successfully.

        :return: True if the query was successful, False otherwise.
        :rtype: bool
        """

        if self._status != "error":
            return True
        return False

    def total_pages(self) -> int:
        """
        Return total number of pages.

        :return: Number of pages.
        :rtype: int
        """

        return self._total_pages

    def has_next(self) -> bool:
        """
        Return if the next page exists.

        :return: Whether next page exists.
        :rtype: bool
        """

        if self.next_url:
            return True
        return False
