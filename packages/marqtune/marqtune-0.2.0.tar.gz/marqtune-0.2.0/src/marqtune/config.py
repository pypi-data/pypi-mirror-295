class Config:
    """
    Client's credentials and configuration parameters
    """

    def __init__(
            self,
            url: str = None,
            api_key: str = None,
            log_waiting: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        url:
            The url to the Marqtune instance (ex: http://localhost:8882)
        """
        self.url = url
        self.api_key = api_key
        self.log_waiting = log_waiting
        # suppress warnings until we figure out the dependency issues:
        # warnings.filterwarnings("ignore")
