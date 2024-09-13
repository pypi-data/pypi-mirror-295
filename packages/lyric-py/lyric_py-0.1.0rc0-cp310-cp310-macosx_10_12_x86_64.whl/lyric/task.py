import msgpack
from typing import Union
from enum import IntEnum

from ._py_lyric import PyTaskInfo

class DetailType(IntEnum):
    NORMAL_CODE = 0
    SERIALIZING_DATA = 1

class NormalCode:
    def __init__(self, language: int, code: str):
        self.language = language
        self.code = code

class SerializingData:
    def __init__(self, data: bytes):
        self.data = data

class TaskInfo:
    def __init__(
            self,
            task_type: int,
            name: str,
            language: int,
            task_id: bytes,
            detail_type: DetailType,
            detail: Union[NormalCode, SerializingData],
            execute_mode: int,
            env_id: str
    ):
        self.task_type = task_type
        self.name = name
        self.language = language
        self.task_id = task_id
        self.detail_type = detail_type
        self.detail = detail
        self.execute_mode = execute_mode
        self.env_id = env_id

    @classmethod
    def from_core(cls, core_task_info: PyTaskInfo):
        detail_type = DetailType(core_task_info.detail_type)
        detail_data = msgpack.unpackb(bytes(core_task_info.detail))

        print(f"detail_data: {detail_data}")

        if detail_type == DetailType.NORMAL_CODE:
            # ['language', 'code']
            detail = NormalCode(core_task_info.language, detail_data[1])
        elif detail_type == DetailType.SERIALIZING_DATA:
            # ['data']
            detail = SerializingData(bytes(detail_data[0]))
        else:
            raise ValueError(f"Unknown detail type: {detail_type}")

        return cls(
            task_type=core_task_info.task_type,
            name=core_task_info.name,
            language=core_task_info.language,
            task_id=bytes(core_task_info.task_id),
            detail_type=detail_type,
            detail=detail,
            execute_mode=core_task_info.execute_mode,
            env_id=core_task_info.env_id
        )

    def to_core(self) -> PyTaskInfo:
        if isinstance(self.detail, NormalCode):
            detail_data = msgpack.packb({
                'language': self.detail.language,
                'code': self.detail.code
            })
        elif isinstance(self.detail, SerializingData):
            detail_data = msgpack.packb({
                'data': self.detail.data
            })
        else:
            raise TypeError(f"Unsupported detail type: {type(self.detail)}")

        return PyTaskInfo(
            task_type = self.task_type,
            name=self.name,
            language=self.language,
            task_id=list(self.task_id),
            detail_type=int(self.detail_type),
            detail=detail_data,
            execute_mode=self.execute_mode,
            env_id=self.env_id
        )

    def __str__(self):
        return (f"TaskInfo(task_type={self.task_type}, name={self.name}, "
                f"language={self.language}, task_id={self.task_id}, "
                f"detail_type={self.detail_type}, detail={self.detail}, "
                f"execute_mode={self.execute_mode}, env_id={self.env_id})")

class BaseTask:
    def run(self, task_info: TaskInfo):
        raise NotImplementedError

    def __call__(self, task_info: TaskInfo):
        return self.run(task_info)
class MyDummyTask(BaseTask):
    def run(self, task_info: TaskInfo):
        print(f"Running task: {task_info}")
        return "Executed successfully"
