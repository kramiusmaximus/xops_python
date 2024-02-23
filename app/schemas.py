from typing import List
from pydantic import BaseModel, validator, HttpUrl


class UniqueDomainList(BaseModel):
    urls: List[HttpUrl]

    @validator("urls", pre=True)
    def ensure_unique(cls, urls: List[str]) -> List[str]:
        unique_urls = list(set([str(url) for url in urls]))
        return unique_urls

    @property
    def domains(self) -> List[str]:
        return [url.host for url in self.urls]
