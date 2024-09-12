import json
from pathlib import Path
from typing import Any, Dict, Optional, Union, cast

import aiohttp

from ..config import config
from ..logging import internal_logger
from ..schemas.events import AwsWorkloadData


class AWSWorkloadError(Exception):
    pass


class ImdsHttpClient:
    async def get(self, url: str, **requests_kwargs: Any) -> Union[Dict[str, str], str]:
        async with aiohttp.request("GET", url, **requests_kwargs) as response:
            response.raise_for_status()
        return cast(Union[Dict[str, str], str], await response.json())

    async def put(self, url: str, **requests_kwargs: Any) -> str:
        async with aiohttp.request("PUT", url, **requests_kwargs) as response:
            response.raise_for_status()
            return await response.text()


async def get_imds_workload_metadata(imds_client: ImdsHttpClient) -> AwsWorkloadData:
    # get metadata token
    host_url = "http://{}".format(config.aws_metadata_server)
    timeout = None  # type: Optional[Union[aiohttp.ClientTimeout, float]]
    if hasattr(aiohttp, "ClientTimeout"):
        timeout = aiohttp.ClientTimeout(config.aws_metadata_timeout)
    else:
        timeout = config.aws_metadata_timeout

    try:

        token = await imds_client.put(
            "{}/latest/api/token".format(host_url),
            timeout=timeout,
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        )
    except Exception as error:
        raise AWSWorkloadError(
            "Could not retrieve instance metadata token: {}".format(error)
        ) from error

    token_headers = {"X-aws-ec2-metadata-token": token}

    # get instance identity
    try:
        identity = await imds_client.get(
            "{}/latest/dynamic/instance-identity/document".format(host_url),
            timeout=timeout,
            headers=token_headers,
        )
    except Exception as error:
        raise AWSWorkloadError(
            "Could not retrieve instance identity document: {}".format(error)
        ) from error
    if not isinstance(identity, dict):
        raise AWSWorkloadError("Instance identity is not a dictionary")

    # get instance life cycle
    try:
        life_cycle_data = await imds_client.get(
            "{}/latest/meta-data/instance-life-cycle".format(host_url),
            timeout=timeout,
            headers=token_headers,
        )
    except Exception as error:
        raise AWSWorkloadError(
            "Could not retrieve instance life cycle: {}".format(error)
        ) from error
    if not isinstance(life_cycle_data, str):
        raise AWSWorkloadError("Instance life cycle is not a string")

    return AwsWorkloadData(
        ami_id=identity["imageId"],
        launched_date=identity["pendingTime"],
        life_cycle=life_cycle_data,
        region=identity["region"],
        workload_id=identity["instanceId"],
        workload_instance_type=identity["instanceType"],
    )


def get_local_aws_workload_metadata() -> AwsWorkloadData:
    local_metadata = Path(config.aws_local_metadata_file).read_text(encoding="utf8")
    local_metadata_parsed = json.loads(local_metadata)
    identity_parsed = local_metadata_parsed["ds"]["dynamic"]["instance-identity"][
        "document"
    ]
    return AwsWorkloadData(
        ami_id=identity_parsed["imageId"],
        launched_date=identity_parsed["pendingTime"],
        life_cycle=local_metadata_parsed["ds"]["meta-data"]["instance-life-cycle"],
        region=identity_parsed["region"],
        workload_id=identity_parsed["instanceId"],
        workload_instance_type=identity_parsed["instanceType"],
    )


async def get_aws_workload_metadata(
    imds_client: ImdsHttpClient,
) -> Optional[AwsWorkloadData]:
    try:
        return get_local_aws_workload_metadata()
    except Exception as err:
        internal_logger.debug(
            "Failed to get workload metadata from local file with error: {}".format(err)
        )
    try:
        return await get_imds_workload_metadata(imds_client)
    except Exception as err:
        internal_logger.debug(
            "Failed to get workload metadata from IMDS with error: {}".format(err)
        )
    return None
