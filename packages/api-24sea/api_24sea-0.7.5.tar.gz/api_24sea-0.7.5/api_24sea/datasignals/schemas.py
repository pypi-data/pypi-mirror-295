# -*- coding: utf-8 -*-
"""Data signals types."""
import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ValidationInfo, field_validator


class Metric(BaseModel):
    """A pydantic schema for the metrics names."""

    start_timestamp: str
    end_timestamp: str
    site: str
    location: str
    data_group: Optional[str]
    metric: str
    statistic: Optional[str]
    short_hand: Optional[str]
    unit_str: Optional[str]
    print_str: Optional[str]
    description: Optional[str]
    crud_privileges: Optional[str]


class Metrics(BaseModel):
    """A pydantic schema for the metrics names."""

    metrics: List[Metric]


class GetData(BaseModel):
    """A pydantic schema for the data signals."""

    start_timestamp: Optional[datetime.datetime]
    end_timestamp: Optional[datetime.datetime]
    sites: Optional[Union[str, List[str]]]
    locations: Optional[Union[str, List[str]]]
    metrics: Optional[Union[str, List[str]]]
    outer_join_on_timestamp: Optional[bool]
    headers: Optional[Dict[str, str]]

    @field_validator("start_timestamp", "end_timestamp", mode="before")
    def validate_timestamp(cls, v: Union[datetime.datetime, str]) -> str:
        """Validate the timestamps."""
        if isinstance(v, str):
            try:
                datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                raise ValueError(
                    "Incorrect start timestamp format, expected ISO 8601."
                )

        if isinstance(v, datetime.datetime):
            # Enforce timezone UTC as well
            return v.strftime("%Y-%m-%dT%H:%M:%SZ")

        return v

    @field_validator("end_timestamp")
    def validate_end_timestamp(cls, v, info: ValidationInfo):
        """Validate the end timestamp."""
        if "start_timestamp" in info.data and v < info.data["start_timestamp"]:
            raise ValueError(
                "End timestamp must be greater than start timestamp."
            )
        return v

    @field_validator("sites", "locations", mode="before")
    def validate_sites_locations(cls, v):
        """Validate and normalize sites and locations."""
        if isinstance(v, str):
            v = [v]
        if isinstance(v, List):
            v = [str(item).lower() for item in v]
        return v

    @field_validator("metrics", mode="before")
    def validate_metrics(cls, v):
        """Validate and normalize metrics."""
        if isinstance(v, str):
            v = [v]
        if isinstance(v, List):
            # fmt: off
            v = [item.replace(" ", ".*")
                     .replace("_", ".*")
                     .replace("-", ".*") for item in v]
            # fmt: on
        return "|".join(v)

    @field_validator("outer_join_on_timestamp", mode="before")
    def validate_outer_join_on_timestamp(cls, v):
        """Validate the outer join on timestamp."""
        if v is None:
            return False
        return v

    @field_validator("headers", mode="before")
    def validate_headers(cls, v):
        """Validate the headers."""
        if v is None:
            return {"accept": "application/json"}
        return v
