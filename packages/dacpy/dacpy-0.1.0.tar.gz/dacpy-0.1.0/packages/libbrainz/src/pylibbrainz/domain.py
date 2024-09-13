from functools import lru_cache
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from pylibbrainz import urlutils


class BaseSchema(BaseModel):
    model_config = ConfigDict()


class User(BaseSchema):
    user_name: str
    listen_count: int = 0
    services: list[Literal["spotify"]] = Field(default_factory=list)
    latest_import_timestamp: float = -1
    api_version: Literal["1"] = 1


class Track(BaseSchema):
    album: str
    creator: str
    duration: int
    extension: dict
    identifier: list[str]
    title: str

    @property
    @lru_cache(maxsize=1)
    def mbids(self) -> list[UUID]:
        """MusicBrainz IDs, extracted from `self.identifier`

        Raises:
             ValueError if any of the identifiers cannot be extracted
        """
        mbids = []
        for identifier in self.identifier:
            mbid = urlutils.extract_uuid_from_url(identifier)
            if not mbid:
                raise ValueError(f"Could not extract MusicBrainz ID from {identifier}")
            mbids.append(mbid)
        return mbids


class Playlist(BaseSchema):
    annotation: str
    creator: str
    date: str
    extension: dict
    identifier: str
    title: str
    track: list[Track]

    @property
    @lru_cache(maxsize=1)
    def mbid(self) -> UUID:
        """MusicBrainz ID, extracted from `self.identifier`"""

        mbid = urlutils.extract_uuid_from_url(self.identifier)
        if not mbid:
            raise ValueError(f"Could not extract MusicBrainz ID from {self.identifier}")
        return mbid
