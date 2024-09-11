from google.protobuf import timestamp_pb2 as _timestamp_pb2
import LocationFix_pb2 as _LocationFix_pb2
import Pose_pb2 as _Pose_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigurationSensorPerception(_message.Message):
    __slots__ = ("timestamp", "location", "pose", "view_horizontal_angel_deg", "view_horizontal_start_angel_deg", "view_horizontal_end_angel_deg", "view_vertical_angel_deg", "mode", "mode_timestamp", "other_json")
    class SensorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ConfigurationSensorPerception.SensorType]
        CAMERA: _ClassVar[ConfigurationSensorPerception.SensorType]
        LIDAR: _ClassVar[ConfigurationSensorPerception.SensorType]
        RADAR_MARINE: _ClassVar[ConfigurationSensorPerception.SensorType]
        RADAR_VEHICLE: _ClassVar[ConfigurationSensorPerception.SensorType]
    UNKNOWN: ConfigurationSensorPerception.SensorType
    CAMERA: ConfigurationSensorPerception.SensorType
    LIDAR: ConfigurationSensorPerception.SensorType
    RADAR_MARINE: ConfigurationSensorPerception.SensorType
    RADAR_VEHICLE: ConfigurationSensorPerception.SensorType
    class mode_operating(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RUNNING: _ClassVar[ConfigurationSensorPerception.mode_operating]
        STANDBY: _ClassVar[ConfigurationSensorPerception.mode_operating]
        DISABLED: _ClassVar[ConfigurationSensorPerception.mode_operating]
        OFF: _ClassVar[ConfigurationSensorPerception.mode_operating]
        ERROR: _ClassVar[ConfigurationSensorPerception.mode_operating]
    RUNNING: ConfigurationSensorPerception.mode_operating
    STANDBY: ConfigurationSensorPerception.mode_operating
    DISABLED: ConfigurationSensorPerception.mode_operating
    OFF: ConfigurationSensorPerception.mode_operating
    ERROR: ConfigurationSensorPerception.mode_operating
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    VIEW_HORIZONTAL_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    VIEW_HORIZONTAL_START_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    VIEW_HORIZONTAL_END_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    VIEW_VERTICAL_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OTHER_JSON_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    location: _LocationFix_pb2.LocationFix
    pose: _Pose_pb2.Pose
    view_horizontal_angel_deg: float
    view_horizontal_start_angel_deg: float
    view_horizontal_end_angel_deg: float
    view_vertical_angel_deg: float
    mode: str
    mode_timestamp: str
    other_json: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., location: _Optional[_Union[_LocationFix_pb2.LocationFix, _Mapping]] = ..., pose: _Optional[_Union[_Pose_pb2.Pose, _Mapping]] = ..., view_horizontal_angel_deg: _Optional[float] = ..., view_horizontal_start_angel_deg: _Optional[float] = ..., view_horizontal_end_angel_deg: _Optional[float] = ..., view_vertical_angel_deg: _Optional[float] = ..., mode: _Optional[str] = ..., mode_timestamp: _Optional[str] = ..., other_json: _Optional[str] = ...) -> None: ...
