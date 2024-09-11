from typing import Literal, Optional

from pydantic import AliasPath, ConfigDict, Field

from pa_api.xmlapi.types.utils import List, String, XMLBaseModel


class ProfileSetting(XMLBaseModel):
    groups: List[String] = Field(
        validation_alias=AliasPath("group", "member"), default_factory=list
    )


class Option(XMLBaseModel):
    disable_server_response_inspection: Optional[bool] = Field(
        validation_alias="disable-server-response-inspection", default=None
    )


class Target(XMLBaseModel):
    negate: Optional[bool] = None


class Security(XMLBaseModel):
    model_config = ConfigDict(extra="allow")

    name: String = Field(validation_alias="@name")
    uuid: String = Field(validation_alias="@uuid")
    disabled: Optional[bool] = None

    action: Literal["allow", "deny", "reset-client"]

    to: List[String] = Field(
        validation_alias=AliasPath("to", "member"), default_factory=list
    )
    from_: List[String] = Field(
        validation_alias=AliasPath("from", "member"), default_factory=list
    )
    sources: List[String] = Field(
        validation_alias=AliasPath("source", "member"), default_factory=list
    )
    destinations: List[String] = Field(
        validation_alias=AliasPath("destination", "member"), default_factory=list
    )
    source_users: List[String] = Field(
        validation_alias=AliasPath("source-user", "member"), default_factory=list
    )
    services: List[String] = Field(
        validation_alias=AliasPath("service", "member"), default_factory=list
    )
    applications: List[String] = Field(
        validation_alias=AliasPath("application", "member"), default_factory=list
    )

    description: String = ""
    categories: List[String] = Field(
        validation_alias=AliasPath("category", "member"), default_factory=list
    )
    tags: List[String] = Field(
        validation_alias=AliasPath("tag", "member"), default_factory=list
    )
    group_tag: Optional[String] = Field(validation_alias="group-tag", default=None)

    profile_settings: List[ProfileSetting] = Field(
        validation_alias=AliasPath("profile-settings"), default_factory=list
    )
    target: Optional[Target] = Field(validation_alias=AliasPath("target"), default=None)

    option: Optional[Option] = Field(default=None)
    rule_type: Optional[str] = Field(validation_alias="rule-type", default=None)
    negate_source: Optional[bool] = Field(
        validation_alias="negate-source", default=None
    )
    negate_destination: Optional[bool] = Field(
        validation_alias="negate-destination", default=None
    )
    log_settings: Optional[str] = Field(validation_alias="log-settings", default=None)
    log_start: Optional[bool] = Field(validation_alias="log-start", default=None)
    log_end: Optional[bool] = Field(validation_alias="log-end", default=None)
    icmp_unreachable: Optional[bool] = Field(
        validation_alias="icmp-unreachable", default=None
    )
