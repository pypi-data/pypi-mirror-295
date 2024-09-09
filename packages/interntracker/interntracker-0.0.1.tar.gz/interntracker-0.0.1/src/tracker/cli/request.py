import os
from typing import List

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from ..model import Checkpoint, TrainProc, TrainTask, serialize

online_comb_mutation = """
mutation CreateTrainConfig($input: CombinedInputType!, $procMd5: String, $ckptMd5: String) {
  createTrainConfig(input: $input, procMd5: $procMd5, ckptMd5: $ckptMd5) {
    configContent
    dataConfig
    id
    key
    modelConfig
    optimizerConfig
    parallelConfig
    revision
    startStep
    startToken
    task
  }
}
"""


online_ckpt_mutation = """
mutation CreateCheckpoint($input: CkptInput!, $procMd5: String) {
  createCheckpoint(input: $input, procMd5: $procMd5) {
    config
    id
    isDelivery
    isRewardModel
    isSnapshot
    key
    md5
    path
    revision
    saveTime
    step
  }
}
"""


offline_mutation = """
mutation CreateRoadmap($input: [TrainTaskInput!]!) {
  createRoadmap(input: $input) {
    code
    data
    msg
    err
  }
}
"""


async def save_roadmap_offline_mutation(data: List[TrainTask], url=os.getenv("INTERNTRACK_API_URL"), timeout=60):
    transport = AIOHTTPTransport(url=url)
    async with Client(transport=transport, execute_timeout=timeout) as session:
        mutation = gql(offline_mutation)
        result = await session.execute(mutation, {"input": serialize(data)})
        return result


async def save_proc_online_mutation(
    data: TrainProc, procMd5: str, ckptMd5: str = None, url=os.getenv("INTERNTRACK_API_URL"), timeout=60
):
    transport = AIOHTTPTransport(url=url)
    async with Client(transport=transport, execute_timeout=timeout) as session:
        mutation = gql(online_comb_mutation)
        result = await session.execute(mutation, {"input": serialize(data), "procMd5": procMd5, "ckptMd5": ckptMd5})
        return result


async def save_ckpt_online_mutation(data: Checkpoint, procMd5: str, url=os.getenv("INTERNTRACK_API_URL"), timeout=60):
    transport = AIOHTTPTransport(url=url)
    async with Client(transport=transport, execute_timeout=timeout) as session:
        mutation = gql(online_ckpt_mutation)
        result = await session.execute(mutation, {"input": serialize(data), "procMd5": procMd5})
        return result
