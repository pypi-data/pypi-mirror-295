import json
import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

# BEGIN INIT

load_dotenv()

_api_url = os.getenv("CODEX_API_URL", "wss://api.codexanalytica.com/api/v1/flashcommit")


# END INIT


class RepoDetails(BaseModel):
    url: str
    repository: str
    owner: Optional[str]


class Commit(BaseModel):
    author: str
    committer: str
    message: str
    id: str


class Review(BaseModel):
    path: str
    position: int
    body: str


def get_api_url() -> str:
    return _api_url


class CodexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return vars(obj)
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)
