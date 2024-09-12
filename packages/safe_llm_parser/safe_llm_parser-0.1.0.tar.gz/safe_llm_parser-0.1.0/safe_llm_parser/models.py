from time import gmtime, strftime

from pydantic import BaseModel


class Log(BaseModel):
    input: str
    output: str
    error: str
    timestamp: str = strftime("%Y-%m-%d %H:%M:%S", gmtime())


class LLMLog(Log):
    correctness_prompt: str
    correctness_output: str
