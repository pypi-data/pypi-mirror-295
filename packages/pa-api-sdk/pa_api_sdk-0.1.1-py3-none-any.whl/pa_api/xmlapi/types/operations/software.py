from dataclasses import dataclass
from datetime import datetime

from pa_api.utils import (
    first,
)
from pa_api.xmlapi.types.utils import (
    mksx,
    pd,
)


@dataclass
class SoftwareVersion:
    # TODO: Use pydantic
    version: str
    filename: str
    released_on: datetime
    downloaded: bool
    current: bool
    latest: bool
    uploaded: bool

    @staticmethod
    def from_xml(xml):
        # TODO: Use correct pydantic functionalities
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        return SoftwareVersion(
            p("./version/text()"),
            p("./filename/text()"),
            p("./released-on/text()", parser=pd),
            p("./downloaded/text()") != "no",
            p("./current/text()") != "no",
            p("./latest/text()") != "no",
            p("./uploaded/text()") != "no",
        )

    @property
    def base_minor_version(self) -> str:
        major, minor, _ = self.version.split(".")
        return f"{major}.{minor}.0"

    @property
    def base_major_version(self) -> str:
        major, _, _ = self.version.split(".")
        return f"{major}.0.0"
