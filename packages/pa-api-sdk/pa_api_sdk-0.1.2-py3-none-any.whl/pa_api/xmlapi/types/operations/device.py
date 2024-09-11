from typing import Optional

from pydantic import AliasPath, ConfigDict, Field

from pa_api.utils import (
    first,
)
from pa_api.xmlapi.types.utils import (
    Datetime,
    XMLBaseModel,
    mksx,
)


class Device(XMLBaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    serial: str
    connected: bool
    unsupported_version: bool = Field(validation_alias="unsupported-version")
    wildfire_rt: bool = Field(validation_alias="wildfire-rt")
    deactivated: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = Field(validation_alias="ip-address", default=None)
    ipv6_address: Optional[str] = Field(validation_alias="ipv6-address", default=None)
    mac_addr: Optional[str] = Field(validation_alias="mac-addr", default=None)
    uptime: Optional[str] = None
    family: Optional[str] = None
    model: Optional[str] = None
    sw_version: Optional[str] = Field(validation_alias="sw-version", default=None)
    app_version: Optional[str] = Field(validation_alias="app-version", default=None)
    av_version: Optional[str] = Field(validation_alias="av-version", default=None)
    device_dictionary_version: Optional[str] = Field(
        validation_alias="device-dictionary-version", default=""
    )
    wildfire_version: Optional[str] = Field(
        validation_alias="wildfire-version", default=None
    )
    threat_version: Optional[str] = Field(
        validation_alias="threat-version", default=None
    )
    url_db: Optional[str] = Field(validation_alias="url-db", default=None)
    url_filtering_version: Optional[str] = Field(
        validation_alias="url-filtering-version", default=None
    )
    logdb_version: Optional[str] = Field(validation_alias="logdb-version", default=None)
    vpnclient_package_version: Optional[str] = Field(
        validation_alias="vpnclient-package-version", default=None
    )
    global_protect_client_package_version: Optional[str] = Field(
        validation_alias="global-protect-client-package-version", default=None
    )
    prev_app_version: Optional[str] = Field(
        validation_alias="prev-app-version", default=None
    )
    prev_av_version: Optional[str] = Field(
        validation_alias="prev-av-version", default=None
    )
    prev_threat_version: Optional[str] = Field(
        validation_alias="prev-threat-version", default=None
    )
    prev_wildfire_version: Optional[str] = Field(
        validation_alias="prev-wildfire-version", default=None
    )
    prev_device_dictionary_version: Optional[str] = Field(
        validation_alias="prev-device-dictionary-version", default=""
    )
    # domain/: str
    # slot_count: str
    # type/: str
    # tag/: str
    # plugin_versions
    # ha_cluster
    ha_peer_serial: Optional[str] = Field(
        validation_alias=AliasPath("ha", "peer", "serial", "#text"), default=None
    )
    vpn_disable_mode: bool = Field(validation_alias="vpn-disable-mode")
    operational_mode: str = Field(validation_alias="operational-mode")
    certificate_status: Optional[str] = Field(
        validation_alias="certificate-status", default=None
    )
    certificate_subject_name: Optional[str] = Field(
        validation_alias="certificate-subject-name", default=None
    )
    certificate_expiry: Optional[Datetime] = Field(
        validation_alias="certificate-expiry", default=None
    )
    connected_at: Optional[Datetime] = Field(
        validation_alias="connected-at", default=None
    )
    custom_certificate_usage: Optional[str] = Field(
        validation_alias="custom-certificate-usage", default=None
    )
    multi_vsys: bool = Field(validation_alias="multi-vsys")
    # vsys
    last_masterkey_push_status: str = Field(
        validation_alias="last-masterkey-push-status"
    )
    last_masterkey_push_timestamp: Optional[str] = Field(
        validation_alias="last-masterkey-push-timestamp", default=None
    )
    express_mode: bool = Field(validation_alias="express-mode")
    device_cert_present: Optional[str] = Field(
        validation_alias="device-cert-present", default=None
    )
    device_cert_expiry_date: str = Field(validation_alias="device-cert-expiry-date")


class VPNFlow(XMLBaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    name: str
    id: int
    gwid: int
    inner_if: str = Field(validation_alias="inner-if")
    outer_if: str = Field(validation_alias="outer-if")
    localip: str
    peerip: str
    state: str
    mon: str
    owner: str


class HAInfo(XMLBaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    enabled: bool
    preemptive: Optional[bool] = None
    mode: Optional[str] = None
    state: Optional[str] = None
    peer_state: Optional[str] = None
    priority: Optional[int] = None
    peer_priority: Optional[int] = None
    is_primary: Optional[bool] = None
    peer_conn_status: Optional[str] = None
    mgmt_ip: Optional[str] = None
    ha1_ipaddr: Optional[str] = None
    ha1_backup_ipaddr: Optional[str] = None
    ha2_ipaddr: Optional[str] = None
    ha1_macaddress: Optional[str] = None
    ha1_backup_macaddress: Optional[str] = None
    ha2_macaddress: Optional[str] = None

    @classmethod
    def from_xml(cls, xml):
        # TODO: Use correct pydantic functionalities
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        priority = p("./group/local-info/priority/text()", parser=int)
        peer_priority = p("./group/peer-info/priority/text()", parser=int)
        is_primary = None
        if priority is not None and peer_priority is not None:
            is_primary = priority < peer_priority
        return HAInfo(
            enabled=p("./enabled/text()"),
            preemptive=p("./group/local-info/preemptive/text()"),
            mode=p("./group/local-info/mode/text()"),
            state=p("./group/local-info/state/text()"),
            peer_state=p("./group/peer-info/state/text()"),
            priority=priority,
            peer_priority=peer_priority,
            is_primary=is_primary,
            peer_conn_status=p("./group/peer-info/conn-status/text()"),
            mgmt_ip=p("./group/local-info/mgmt-ip/text()"),
            ha1_ipaddr=p("./group/local-info/ha1-ipaddr/text()"),
            ha1_backup_ipaddr=p("./group/local-info/ha1-backup-ipaddr/text()"),
            ha2_ipaddr=p("./group/local-info/ha2-ipaddr/text()"),
            ha1_macaddress=p("./group/local-info/ha1-macaddr/text()"),
            ha1_backup_macaddress=p("./group/local-info/ha1-backup-macaddr/text()"),
            ha2_macaddress=p("./group/local-info/ha2-macaddr/text()"),
        )
