from functools import lru_cache

import pandas as pd


@lru_cache(maxsize=None)
def read_gbq(query: str) -> pd.DataFrame:
    """Query job result."""
    from google.cloud import bigquery
    default_project_id = 'just-data'
    client = bigquery.Client(project=default_project_id)
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query, job_config=job_config)
    return query_job.result().to_dataframe()
