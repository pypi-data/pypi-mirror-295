from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas


REQUEST_TIMESTAMP_FIELD_NAME = "request_timestamp"


@dataclass
class RealtimeContext:
    """
    RealtimeContext is a class that is used to pass context metadata such as the request_timestamp
    to the `context` parameter of a Realtime Feature Views.

    :param request_timestamp: For Online Retrieval, this is the timestamp of the request made to the
    Tecton Feature Server. For Offline Retrieval using `get_features_for_events(events), this is the timestamp in the
    `events` dataframe.
    :type request_timestamp: Optional[datetime]
    """

    request_timestamp: Optional[datetime] = None

    def to_pandas(self) -> pandas.DataFrame:
        """Converts the RealtimeContext to a pandas.DataFrame with the Realtime Context field as columns.

        :return: A pandas DataFrame with the RealtimeContext fields as columns.
        """
        return pandas.DataFrame({REQUEST_TIMESTAMP_FIELD_NAME: [self.request_timestamp]})
