from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import (
    define as _attrs_define,
    field as _attrs_field,
)

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.network_service_request_json import NetworkServiceRequestJson


T = TypeVar("T", bound="NetworkServiceRequest")


@_attrs_define
class NetworkServiceRequest:
    """
    Attributes:
        json (NetworkServiceRequestJson):
        name (str):
        orch_id (str):
        workspace_id (int):
        debug (Union[None, Unset, bool]):
        service_name (Union[None, Unset, str]):
        service_port (Union[None, Unset, int]):
        service_protocol (Union[None, Unset, str]):
        timeout (Union[None, Unset, int]):
    """

    json: "NetworkServiceRequestJson"
    name: str
    orch_id: str
    workspace_id: int
    debug: Union[None, Unset, bool] = UNSET
    service_name: Union[None, Unset, str] = UNSET
    service_port: Union[None, Unset, int] = UNSET
    service_protocol: Union[None, Unset, str] = UNSET
    timeout: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        json = self.json.to_dict()

        name = self.name

        orch_id = self.orch_id

        workspace_id = self.workspace_id

        debug: Union[None, Unset, bool]
        if isinstance(self.debug, Unset):
            debug = UNSET
        else:
            debug = self.debug

        service_name: Union[None, Unset, str]
        if isinstance(self.service_name, Unset):
            service_name = UNSET
        else:
            service_name = self.service_name

        service_port: Union[None, Unset, int]
        if isinstance(self.service_port, Unset):
            service_port = UNSET
        else:
            service_port = self.service_port

        service_protocol: Union[None, Unset, str]
        if isinstance(self.service_protocol, Unset):
            service_protocol = UNSET
        else:
            service_protocol = self.service_protocol

        timeout: Union[None, Unset, int]
        if isinstance(self.timeout, Unset):
            timeout = UNSET
        else:
            timeout = self.timeout

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "json": json,
                "name": name,
                "orch_id": orch_id,
                "workspace_id": workspace_id,
            }
        )
        if debug is not UNSET:
            field_dict["debug"] = debug
        if service_name is not UNSET:
            field_dict["service_name"] = service_name
        if service_port is not UNSET:
            field_dict["service_port"] = service_port
        if service_protocol is not UNSET:
            field_dict["service_protocol"] = service_protocol
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.network_service_request_json import NetworkServiceRequestJson

        d = src_dict.copy()
        json = NetworkServiceRequestJson.from_dict(d.pop("json"))

        name = d.pop("name")

        orch_id = d.pop("orch_id")

        workspace_id = d.pop("workspace_id")

        def _parse_debug(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        debug = _parse_debug(d.pop("debug", UNSET))

        def _parse_service_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        service_name = _parse_service_name(d.pop("service_name", UNSET))

        def _parse_service_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        service_port = _parse_service_port(d.pop("service_port", UNSET))

        def _parse_service_protocol(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        service_protocol = _parse_service_protocol(d.pop("service_protocol", UNSET))

        def _parse_timeout(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        timeout = _parse_timeout(d.pop("timeout", UNSET))

        network_service_request = cls(
            json=json,
            name=name,
            orch_id=orch_id,
            workspace_id=workspace_id,
            debug=debug,
            service_name=service_name,
            service_port=service_port,
            service_protocol=service_protocol,
            timeout=timeout,
        )

        network_service_request.additional_properties = d
        return network_service_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
