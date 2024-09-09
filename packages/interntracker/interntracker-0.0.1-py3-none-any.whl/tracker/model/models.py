from datetime import datetime
from enum import Enum
from typing import List, get_type_hints


class Serializable:
    """
    JSON Serialization
    """

    serialize = {
        datetime: lambda x: datetime.strftime(x, "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    }
    deserialize = {datetime: lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")}

    def __init__(self):
        self.serialize[list] = self.serialize_list
        self.serialize[dict] = self.serialize_dict

    def serialize_attribute(self, value):
        if value is not None and type(value) in self.serialize:
            return self.serialize[type(value)](value)
        else:
            return value

    def serialize_list(self, collections: list):
        result = []
        for item in collections:
            if isinstance(item, Serializable):
                result.append(item.state_dict())
            else:
                value = self.serialize_attribute(item)
                if value is not None:
                    result.append(value)
        return result

    def serialize_dict(self, collections: dict):
        result = {}
        for key, value in collections.items():
            if isinstance(value, Serializable):
                result[key] = value.state_dict()
            else:
                serialized = self.serialize_attribute(value)
                if serialized is not None:
                    result[key] = serialized
        return result

    def state_dict(self):
        result = {}
        for attr in vars(self):
            value = self.serialize_attribute(getattr(self, attr))
            if value is not None:
                result[attr] = value
        return result

    def load_state_dict(self, states: dict):
        annotations = get_type_hints(self.__class__)
        for key, value in states.items():
            if hasattr(self, key) and value is not None:
                if annotations[key] in self.deserialize:
                    setattr(self, key, self.deserialize[annotations[key]](value))
                else:
                    setattr(self, key, value)


class document:
    _id: str = None
    _key: str = None
    _rev: str = None


class Checkpoint(Serializable):
    """
    Checkpoint
    """

    doc: document = None
    config: str = None
    md5: str = None
    path: str = None
    step: int = None
    saveTime: datetime = None
    tokens: int = None
    isDelivery: bool = False
    isRewardModel: bool = False
    isSnapshot: bool = False


class ProcType(Enum):
    RUNNING = "running"
    FAILED = "failed"
    FINISHED = "finished"


class TrainConfig(Serializable):
    """
    Training Config
    """

    doc: document = None
    task: str = None
    loadCkpt: str = None
    configContent: str = None
    dataConfig: str = None
    modelConfig: dict = None
    optimizerConfig: dict = None
    parallelConfig: dict = None
    startStep: int = 0
    startToken: int = 0
    ckpts: List[Checkpoint] = None

    # TrainProc
    cluster: str = None
    envVar: dict = None
    gpuNum: int = None
    startTime: datetime = datetime.now()
    endtime: datetime = None
    state: ProcType = ProcType.RUNNING
    currentStep: int = 0
    totalStep: int = None

    # TrainLog
    configPath: str = None
    logFolder: str = None
    tbFolder: str = None


class TaskType(Enum):
    PRETRAIN = "pretrain"
    RLHF_PPO = "rlhf_ppo"
    RLHF_RM = "rlhf_rm"
    SFT = "sft"


class TrainTask(Serializable):
    """
    Train Task
    """

    doc: document = None
    loadCkpt: str = None
    name: str = None
    type: TaskType = TaskType.PRETRAIN
    desc: str = None
    configs: List[TrainConfig] = None


class ClusterType(Enum):
    ALI = "Ali"
    _910B = "910B"
    A800 = "A800"
    VOLC = "volc"


class TrainProc(Serializable):
    """
    Training Process
    """

    # TrainTask
    name: str = None
    type: TaskType = None
    desc: str = None

    # TrainConfig
    configContent: str = None
    dataConfig: str = None
    modelConfig: dict = None
    optimizerConfig: dict = None
    parallelConfig: dict = None
    startStep: int = 0
    startToken: int = 0

    # TrainProc
    cluster: ClusterType = None
    envVar: dict = None
    gpuNum: int = None
    startTime: datetime = datetime.now()
    endtime: datetime = None
    state: ProcType = ProcType.RUNNING
    currentStep: int = 0
    totalStep: int = None

    # TrainLog
    configPath: str = None
    logFolder: str = None
    tbFolder: str = None

    ckpts: str = []

    def save_local_json(self, ckptMd5: str = None):
        task = TrainTask()
        task.load_state_dict(
            {
                "name": self.name,
                "type": self.type,
                "desc": self.desc,
            }
        )
        config = TrainConfig()
        config.load_state_dict(
            {
                "configContent": self.configContent,
                "dataConfig": self.dataConfig,
                "modelConfig": self.modelConfig,
                "optimizerConfig": self.optimizerConfig,
                "parallelConfig": self.parallelConfig,
                "startStep": self.startStep,
                "startToken": self.startToken,
                "configPath": self.configPath,
                "logFolder": self.logFolder,
                "tbFolder": self.tbFolder,
                "cluster": self.cluster,
                "envVar": self.envVar,
                "gpuNum": self.gpuNum,
                "startTime": self.startTime,
                "endtime": self.endtime,
                "state": self.state,
                "currentStep": self.currentStep,
                "totalStep": self.totalStep,
                "ckpts": self.ckpts,
            }
        )
        if self.name is None:
            task.loadCkpt = ckptMd5
        else:
            config.loadCkpt = ckptMd5
        task.configs = [config]
        return task


def serialize(data):
    if isinstance(data, list):
        return [serialize(d) for d in data]
    elif isinstance(data, dict):
        return {k: serialize(v) for k, v in data.items()}
    elif isinstance(data, Serializable):
        return data.state_dict()
    elif type(data) in Serializable.serialize:
        return Serializable.serialize[type(data)](data)
    elif isinstance(data, Enum):
        return data.value
    else:
        return data
