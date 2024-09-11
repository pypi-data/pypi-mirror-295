from chainalysis.sql.sql import Sql
from chainalysis.utils.utils import Utils


class DataSolutionsClient:
    """
    This class provides SDK functions for users to query
    Data Solutions databases.

    The Analytical class queries the Data Solutions Analytical table.
    The Transactional class queries the Data Solutions Postgres table.
    """

    def __init__(
        self,
        api_key: str,
    ):
        self.api_key = api_key

        # Define SDK function classes
        self.sql = Sql(api_key)
        self.utils = Utils()
