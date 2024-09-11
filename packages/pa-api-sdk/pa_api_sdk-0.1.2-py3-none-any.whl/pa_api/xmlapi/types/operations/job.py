import enum
import logging
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from pa_api.utils import (
    first,
)
from pa_api.xmlapi.types.utils import (
    mksx,
    parse_datetime,
    parse_time,
    pd,
)


def parse_tdeq(d):
    if "null" in d:
        return None
    try:
        return parse_time(d)
    except Exception as e:
        logging.debug(e)
    return parse_datetime(d)


def parse_progress(progress):
    try:
        return float(progress)
    except Exception as e:
        logging.debug(f"{e} => Fallback to datetime parsing")

    # When finished, progress becomes the date of the end
    if parse_datetime(progress):
        return 100.0
    return None


class JobResult(enum.Enum):
    OK = "OK"
    FAIL = "FAIL"


@dataclass
class Job:
    # TODO: Use pydantic
    tenq: datetime
    tdeq: time
    id: str
    user: str
    type: str
    status: str
    queued: bool
    stoppable: bool
    result: str
    tfin: datetime
    description: str
    position_in_queue: int
    progress: float
    details: str
    warnings: str

    @staticmethod
    def from_xml(xml) -> Optional["Job"]:
        # TODO: Use correct pydantic functionalities
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        return Job(
            p("./tenq/text()", parser=pd),
            p("./tdeq/text()", parser=parse_tdeq),
            p("./id/text()"),
            p("./user/text()"),
            p("./type/text()"),
            p("./status/text()"),
            p("./queued/text()") != "NO",
            p("./stoppable/text()") != "NO",
            p("./result/text()"),
            p("./tfin/text()", parser=pd),
            p("./description/text()"),
            p("./positionInQ/text()", parser=int),
            p("./progress/text()", parser=parse_progress),
            "\n".join(xml.xpath("./details/line/text()")),
            p("./warnings/text()"),
        )
