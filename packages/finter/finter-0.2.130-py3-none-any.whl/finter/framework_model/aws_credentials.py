import numpy as np
import pandas as pd
import s3fs

from finter.settings import get_api_client, logger
from finter.rest import ApiException
import finter
from finter.log import PromtailLogger


def get_aws_credentials(identity_name):
    api_instance = finter.AWSCredentialsApi(get_api_client())

    try:
        api_response = api_instance.aws_credentials_retrieve(identity_name=identity_name)
        return api_response
    except ApiException as e:
        print("Exception when calling AWSCredentialsApi->aws_credentials_retrieve: %s\n" % e)


def get_parquet_df(identity_name):
    credentials = get_aws_credentials(identity_name)
    fs = s3fs.S3FileSystem(
        key=credentials.aws_access_key_id,
        secret=credentials.aws_secret_access_key,
        token=credentials.aws_session_token,
    )

    s3_bucket_name = "finter-parquet"
    file_name = f"{identity_name}.parquet"
    s3_uri = f"s3://{s3_bucket_name}/{file_name}"

    with fs.open(s3_uri, "rb") as f:
        df = pd.read_parquet(f, engine="pyarrow")

    PromtailLogger.send_log(
        level="INFO",
        message=f"{identity_name}",
        service="finterlabs-jupyterhub",
        user_id=PromtailLogger.get_user_info(),
        operation="load_model_data_parquet",
        status="success",
    )

    if pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = df.index.astype("datetime64[ns]")

    # FL-2089 content model이 아닌 경우 항상 None을 nan으로 변경한다 c2환경에서만 이슈이고 c3에서는 이슈없음
    if not identity_name.startswith("content."):
        df.replace({None: np.nan}, inplace=True)

    return df
