from chainalysis.sql.analytical import Analytical
from chainalysis.sql.transactional import Transactional


class Sql:
    def __init__(self, api_key: str):
        self.transactional = Transactional(api_key)
        self.analytical = Analytical(api_key)
