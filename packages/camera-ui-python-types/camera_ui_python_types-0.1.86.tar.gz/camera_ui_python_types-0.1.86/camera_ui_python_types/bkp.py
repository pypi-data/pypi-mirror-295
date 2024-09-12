from abc import ABCMeta, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Coroutine
from typing import Any, Callable, Generic, Optional, Union, overload, runtime_checkable

from PIL import Image
from reactivex import Observable
from typing_extensions import (
    Literal,
    NotRequired,
    Protocol,
    TypedDict,
    TypeVar,
)

Callback = Union[
    Callable[..., Any],
    Callable[..., Coroutine[Any, Any, Any]],
]


# schema
JsonSchemaType = Literal["string", "number", "boolean", "object", "array", "button"]


class JsonBaseSchema(TypedDict):
    type: JsonSchemaType
    key: NotRequired[Optional[str]]
    title: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    required: NotRequired[Optional[bool]]
    readonly: NotRequired[Optional[bool]]
    placeholder: NotRequired[Optional[str]]
    hidden: NotRequired[Optional[bool]]
    group: NotRequired[Optional[str]]
    defaultValue: NotRequired[Optional[Union[str, int, bool]]]
    store: NotRequired[Optional[bool]]
    onSet: NotRequired[
        Union[Callable[[Any, Any], Awaitable[Union[None, Any]]], Callable[[Any, Any], Union[None, Any]]]
    ]  # only for plugins
    onGet: NotRequired[
        Union[Callable[[], Awaitable[Union[Any, None]]], Callable[[], Union[Any, None]]]
    ]  # only for plugins


class JsonSchemaString(JsonBaseSchema):
    type: Literal["string"]  # type: ignore
    format: NotRequired[
        Literal["date-time", "date", "time", "email", "uuid", "ipv4", "ipv6", "password", "qrCode", "image"]
    ]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class JsonSchemaNumber(JsonBaseSchema):
    type: Literal["number"]  # type: ignore
    minimum: NotRequired[int]
    maximum: NotRequired[int]
    step: NotRequired[float]


class JsonSchemaBoolean(JsonBaseSchema):
    type: Literal["boolean"]  # type: ignore


class JsonSchemaEnum(JsonBaseSchema):
    type: Literal["string"]  # type: ignore
    enum: list[str]
    multiple: NotRequired[bool]


class JsonSchemaButton(JsonBaseSchema):
    type: Literal["button"]  # type: ignore


class JsonSchemaObject(JsonBaseSchema):
    type: Literal["object"]  # type: ignore
    opened: NotRequired[bool]
    properties: NotRequired["JsonSchemaForm"]


class JsonSchemaArray(JsonBaseSchema):
    type: Literal["array"]  # type: ignore
    opened: NotRequired[bool]
    items: NotRequired["JsonSchema"]


class JsonSchemaObjectButton(TypedDict):
    label: str
    onSubmit: str


class JsonSchemaObjectWithButtons(JsonSchemaObject):
    buttons: list[JsonSchemaObjectButton]


JsonSchema = Union[
    JsonSchemaString,
    JsonSchemaNumber,
    JsonSchemaBoolean,
    JsonSchemaEnum,
    JsonSchemaObject,
    JsonSchemaObjectWithButtons,
    JsonSchemaArray,
    JsonSchemaButton,
]


JsonSchemaForm = dict[str, JsonSchema]


class RootSchema(TypedDict):
    schema: JsonSchemaForm


class SchemaConfig(TypedDict):
    rootSchema: RootSchema
    config: dict[str, Any]


# camera object
class Go2RtcSource(TypedDict):
    name: str
    src: str
    ws: str


class Go2RtcFFMPEGSource(TypedDict):
    aac: Go2RtcSource
    opus: Go2RtcSource


class Go2RtcWSSource(TypedDict):
    webrtc: str


class Go2RtcRTSPSource(TypedDict):
    single: str
    default: str
    mp4: str


class Go2RtcEndpoint(TypedDict):
    webrtc: str
    mse: str
    lmp4: str
    mmp4: str
    mp4: str
    mp4Snapshot: str
    jpegSnapshot: str
    lHlsTs: str
    lHlsFmp4: str
    mHlsFmp4: str
    mjpeg: str
    mjpegHtml: str


class StreamUrls(TypedDict):
    ws: Go2RtcWSSource
    rtsp: Go2RtcRTSPSource
    transcoded: Go2RtcFFMPEGSource
    www: Go2RtcEndpoint


class CameraInput(TypedDict):
    _id: str
    name: str
    roles: list["CameraRoles"]
    urls: StreamUrls


CameraRoles = Literal["high-resolution", "mid-resolution", "low-resolution", "snapshot"]

CameraExtensionWithoutHub = Literal[
    "prebuffer",
    "motionDetection",
    "objectDetection",
    "audioDetection",
    "ptz",
]

CameraExtension = Union[CameraExtensionWithoutHub, Literal["hub"]]


class PluginContract(TypedDict):
    extension: NotRequired[CameraExtension]
    supportAdditionalCameras: NotRequired[bool]
    builtIns: NotRequired[list[CameraExtensionWithoutHub]]
    dependencies: list[str]
    pythonVersion: NotRequired[str]


Point = tuple[float, float]

ZoneType = Literal["intersect", "contain"]

ZoneFilter = Literal["include", "exclude"]


class DetectionZone(TypedDict):
    name: str
    points: list[Point]
    type: ZoneType
    filter: ZoneFilter
    classes: list[str]
    isPrivacyMask: bool


class CameraInformation(TypedDict):
    model: NotRequired[str]
    manufacturer: NotRequired[str]
    hardware: NotRequired[str]
    serialNumber: NotRequired[str]
    firmwareVersion: NotRequired[str]
    supportUrl: NotRequired[str]


class MotionDetectionSettings(TypedDict):
    timeout: int


class ObjectDetectionSettings(TypedDict):
    confidence: float


class CameraActivitySettings(TypedDict):
    motion: MotionDetectionSettings
    object: ObjectDetectionSettings


CameraType = Literal["camera", "doorbell"]

CameraFrameWorkerDecoder = Literal["pillow", "wasm"]

CameraFrameWorkerResolution = Literal[640, 480, 320]


class CameraFrameWorkerSettings(TypedDict):
    decoder: CameraFrameWorkerDecoder
    fps: int
    resolution: CameraFrameWorkerResolution


class Camera(TypedDict):
    _id: str
    nativeId: NotRequired[Optional[str]]
    pluginId: str
    name: str
    disabled: bool
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    info: CameraInformation
    type: CameraType
    activityZones: list[DetectionZone]
    activitySettings: CameraActivitySettings
    hasAudioDetector: bool
    hasMotionDetector: bool
    hasObjectDetector: bool
    hasPrebuffer: bool
    hasPtz: bool
    sources: list[CameraInput]
    frameWorkerSettings: CameraFrameWorkerSettings


CameraPublicProperties = Literal[
    "_id",
    "nativeId",
    "pluginId",
    "name",
    "disabled",
    "isCloud",
    "hasLight",
    "hasSiren",
    "hasBinarySensor",
    "hasBattery",
    "info",
    "type",
    "activityZones",
    "activitySettings",
    "hasAudioDetector",
    "hasMotionDetector",
    "hasObjectDetector",
    "hasPrebuffer",
    "hasPtz",
    "sources",
    "frameWorkerSettings",
]


# camera device
ObjectClass = Literal[
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
    "motion",
]


class Detection(TypedDict):
    id: NotRequired[str]
    label: ObjectClass
    confidence: float
    boundingBox: tuple[float, float, float, float]
    inputWidth: int
    inputHeight: int
    origWidth: int
    origHeight: int


class BaseStateLight(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["LightStateWithoutLastEvent"]]


class BaseStateMotion(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["MotionStateWithoutLastEvent"]]


class BaseStateAudio(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["AudioStateWithoutLastEvent"]]


class BaseStateObject(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["ObjectStateWithoutLastEvent"]]


class BaseStateDoorbell(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["DoorbellStateWithoutLastEvent"]]


class BaseStateSiren(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["SirenStateWithoutLastEvent"]]


class BaseStateBattery(TypedDict):
    timestamp: int
    lastEvent: NotRequired[Optional["BatteryStateWithoutLastEvent"]]


class BaseStateWithoutLastEvent(TypedDict):
    timestamp: int


class MotionSetEvent(TypedDict):
    state: NotRequired[bool]
    detections: list[Detection]


class AudioSetEvent(TypedDict):
    state: bool
    db: NotRequired[Optional[int]]


class ObjectSetEvent(TypedDict):
    detections: list[Detection]


class LightSetEvent(TypedDict):
    state: bool


class DoorbellSetEvent(TypedDict):
    state: bool


class SirenSetEvent(TypedDict):
    state: bool
    level: NotRequired[Optional[int]]


class BatterySetEvent(TypedDict):
    level: int
    charging: NotRequired[Optional[bool]]
    lowBattery: NotRequired[Optional[bool]]


class LightState(BaseStateLight, LightSetEvent): ...


class LightStateWithoutLastEvent(BaseStateWithoutLastEvent, LightSetEvent): ...


class MotionState(BaseStateMotion, MotionSetEvent): ...


class MotionStateWithoutLastEvent(BaseStateWithoutLastEvent, MotionSetEvent): ...


class AudioState(BaseStateAudio, AudioSetEvent): ...


class AudioStateWithoutLastEvent(BaseStateWithoutLastEvent, AudioSetEvent): ...


class DoorbellState(BaseStateDoorbell, DoorbellSetEvent): ...


class DoorbellStateWithoutLastEvent(BaseStateWithoutLastEvent, DoorbellSetEvent): ...


class SirenState(BaseStateSiren, SirenSetEvent): ...


class SirenStateWithoutLastEvent(BaseStateWithoutLastEvent, SirenSetEvent): ...


class ObjectState(BaseStateObject, ObjectSetEvent): ...


class ObjectStateWithoutLastEvent(BaseStateWithoutLastEvent, ObjectSetEvent): ...


class BatteryState(BaseStateBattery, BatterySetEvent): ...


class BatteryStateWithoutLastEvent(BaseStateWithoutLastEvent, BatterySetEvent): ...


class FrameState(MotionState):
    frameData: "FrameData"
    metadata: "FrameMetadata"


T = TypeVar(
    "T",
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
)


class StateValues(Protocol):
    light: LightState
    motion: MotionState
    audio: AudioState
    object: ObjectState
    doorbell: DoorbellState
    siren: SirenState
    battery: BatteryState


class SetValues(Protocol):
    light: LightSetEvent
    motion: MotionSetEvent
    audio: AudioSetEvent
    object: ObjectSetEvent
    doorbell: DoorbellSetEvent
    siren: SirenSetEvent
    battery: BatterySetEvent


CameraStateCallbacks = dict[str, Callable[[T], None]]

StateValue = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

SetValue = Union[
    LightSetEvent,
    MotionSetEvent,
    AudioSetEvent,
    DoorbellSetEvent,
    SirenSetEvent,
    BatterySetEvent,
    ObjectSetEvent,
]

StateNames = Literal["light", "motion", "audio", "doorbell", "siren", "battery", "object"]

OnChangeCallback = Callable[[T, T], None]


class PrebufferState(TypedDict):
    url: Optional[str]
    duration: Optional[int]


Container = Literal["mpegts", "mp4"]

AudioCodec = Literal["PCMU", "PCMA", "MPEG4-GENERIC", "opus", "G722", "MPA", "PCM", "FLAC"]

VideoCodec = Literal["H264", "H265", "VP8", "VP9", "AV1", "JPEG", "RAW"]

AudioFFmpegCodec = Literal[
    "pcm_mulaw", "pcm_alaw", "aac", "libopus", "g722", "mp3", "pcm_s16be", "pcm_s16le", "flac"
]

VideoFFmpegCodec = Literal["h264", "hevc", "vp8", "vp9", "av1", "mjpeg", "rawvideo"]


class AudioCodecProperties(TypedDict):
    sampleRate: int
    channels: int
    payloadType: int


class VideoCodecProperties(TypedDict):
    clockRate: int
    payloadType: int


class AudioStreamInfo(TypedDict):
    codec: AudioCodec
    ffmpegCodec: AudioFFmpegCodec
    properties: AudioCodecProperties
    direction: Literal["sendonly", "recvonly"]


class VideoStreamInfo(TypedDict):
    codec: VideoCodec
    ffmpegCodec: VideoFFmpegCodec
    properties: VideoCodecProperties
    direction: Literal["sendonly"]


class ProbeStream(TypedDict):
    sdp: str
    audio: list[AudioStreamInfo]
    video: VideoStreamInfo


Interfaces = Literal["camera", "ptz", "prebuffer", "audioDetector", "motionDetector", "objectDetector"]


class CameraDelegate(metaclass=ABCMeta):
    @abstractmethod
    async def snapshot(self) -> Optional[bytes]: ...


CameraDelegateMethodNames = Literal["reboot", "snapshot"]


class CameraPrebufferDelegate(metaclass=ABCMeta):
    @abstractmethod
    async def getPrebufferingState(
        self, source_name: str, container: Container
    ) -> Optional[PrebufferState]: ...


CameraPrebufferDelegateMethodNames = Literal["getPrebufferingState"]


class CameraPTZDelegate(metaclass=ABCMeta):
    @abstractmethod
    async def moveAbsolute(self, pan: float, tilt: float, zoom: float) -> None: ...

    @abstractmethod
    async def moveRelative(self, pan: float, tilt: float, zoom: float) -> None: ...

    @abstractmethod
    async def moveContinuous(self, pan: float, tilt: float, zoom: float) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...


CameraPTZDelegateMethodNames = Literal["moveAbsolute", "moveRelative", "moveContinuous", "stop"]


class CameraSource(Protocol):
    # from CameraInput
    id: str  # _id
    name: str
    roles: list["CameraRoles"]
    urls: StreamUrls
    # end

    async def get_prebuffering_state(self, container: Container) -> Optional[PrebufferState]: ...
    async def probe_stream(self) -> Optional[ProbeStream]: ...


ImageInputFormat = Literal["yuv", "rgb", "rgba", "gray"]
ImageOutputFormat = Literal["rgb", "rgba", "gray"]


class ImageFormat(TypedDict):
    to: ImageOutputFormat


class ImageCrop(TypedDict):
    top: int
    left: int
    width: int
    height: int


class ImageResize(TypedDict):
    width: NotRequired[int]
    height: NotRequired[int]


class ImageOptions(TypedDict):
    format: NotRequired[ImageFormat]
    crop: NotRequired[ImageCrop]
    resize: NotRequired[ImageResize]


class IceServer(TypedDict):
    urls: list[str]
    username: NotRequired[str]
    credential: NotRequired[str]


DecoderFormat = Literal["yuv", "rgb"]


class ImageMetadata(TypedDict):
    width: int
    height: int


class AudioMetadata(TypedDict):
    mimeType: Literal["audio/mpeg", "audio/wav", "audio/ogg"]


class FrameMetadata(TypedDict):
    format: DecoderFormat
    frameSize: float
    width: int
    height: int
    origWidth: int
    origHeight: int


class FrameData(TypedDict):
    frameId: str
    timestamp: int


class ImageInformation(TypedDict):
    width: int
    height: int
    channels: Literal[1, 3, 4]
    format: ImageInputFormat


class FrameBuffer(TypedDict):
    image: bytes
    info: ImageInformation


class FrameImage(TypedDict):
    image: Image.Image
    info: ImageInformation


class VideoFrame(Protocol):
    frame_data: FrameData
    metadata: FrameMetadata
    input_width: int
    input_height: int
    input_format: DecoderFormat

    async def save(self, path: str, options: Optional[ImageOptions] = {}) -> None: ...
    async def to_buffer(self, options: Optional[ImageOptions] = {}) -> FrameBuffer: ...
    async def to_image(self, options: Optional[ImageOptions] = {}) -> FrameImage: ...


class MotionFrame(VideoFrame):
    motion: MotionState


SV = TypeVar("SV", bound=StateValue)


class CameraStateChangedObject(Generic[SV], dict[str, SV]):
    old_state: SV
    new_state: SV


class CameraPropertyObservableObject(TypedDict):
    property: str
    old_state: Any
    new_state: Any


@runtime_checkable
class CameraDevice(Protocol):
    id: str
    plugin_id: str
    native_id: Optional[str]
    connected: bool
    disabled: bool
    name: str
    type: CameraType
    info: CameraInformation
    sources: list[CameraSource]
    activity_zones: list[DetectionZone]
    activity_settings: CameraActivitySettings
    frameworker_settings: CameraFrameWorkerSettings
    is_cloud: bool
    has_light: bool
    has_siren: bool
    has_binary_sensor: bool
    has_battery: bool
    has_motion_detector: bool
    has_audio_detector: bool
    has_object_detector: bool
    has_ptz: bool
    has_prebuffer: bool

    on_connected: Observable[bool]
    on_light_switched: Observable[LightState]
    on_motion_detected: Observable[MotionState]
    on_audio_detected: Observable[AudioState]
    on_object_detected: Observable[ObjectState]
    on_doorbell_pressed: Observable[DoorbellState]
    on_siren_detected: Observable[SirenState]
    on_battery_changed: Observable[BatteryState]

    stream_source: CameraSource
    snapshot_source: Optional[CameraSource]
    high_resolution_source: Optional[CameraSource]
    mid_resolution_source: Optional[CameraSource]
    low_resolution_source: Optional[CameraSource]

    ptz: CameraPTZDelegate

    @overload
    def set_delegate(self, name: Literal["cameraDelegate"], delegate: CameraDelegate) -> None: ...
    @overload
    def set_delegate(self, name: Literal["prebufferDelegate"], delegate: CameraPrebufferDelegate) -> None: ...
    @overload
    def set_delegate(self, name: Literal["ptzDelegate"], delegate: CameraPTZDelegate) -> None: ...

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def snapshot(self, force_new: Optional[bool] = None) -> Optional[bytes]: ...
    async def get_frames(self, prebuffer_duration: int = 0) -> AsyncGenerator[VideoFrame, None]: ...
    async def get_motion_frames(self) -> AsyncGenerator[MotionFrame, None]: ...

    async def get_value(
        self, state_name: str
    ) -> Union[
        LightState,
        MotionState,
        AudioState,
        ObjectState,
        DoorbellState,
        SirenState,
        BatteryState,
    ]: ...

    async def add_camera_source(self, source: "CameraConfigInputSettings") -> None: ...
    async def update_camera_source(
        self, source_id: str, source: "CameraConfigInputSettingsPartial"
    ) -> None: ...
    async def remove_camera_source(self, source_id: str) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["light"],
        event_data: LightSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["motion"],
        event_data: MotionSetEvent,
        frame: Optional[VideoFrame] = None,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["audio"],
        event_data: AudioSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["object"],
        event_data: ObjectSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["doorbell"],
        event_data: DoorbellSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["siren"],
        event_data: SirenSetEvent,
    ) -> None: ...
    @overload
    async def update_state(
        self,
        state_name: Literal["battery"],
        event_data: BatterySetEvent,
    ) -> None: ...
    async def update_state(
        self, state_name: str, event_data: Any, frame: Optional[VideoFrame] = None
    ) -> None: ...

    @overload
    def on_state_change(
        self, state_name: Literal["light"]
    ) -> Observable[CameraStateChangedObject[LightState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["motion"]
    ) -> Observable[CameraStateChangedObject[MotionState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["audio"]
    ) -> Observable[CameraStateChangedObject[AudioState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["doorbell"]
    ) -> Observable[CameraStateChangedObject[DoorbellState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["siren"]
    ) -> Observable[CameraStateChangedObject[SirenState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["battery"]
    ) -> Observable[CameraStateChangedObject[BatteryState]]: ...
    @overload
    def on_state_change(
        self, state_name: Literal["object"]
    ) -> Observable[CameraStateChangedObject[ObjectState]]: ...
    def on_state_change(  # type: ignore
        self, state_name: StateNames
    ) -> Observable[CameraStateChangedObject[StateValue]]: ...

    def on_property_change(
        self, property: Union[CameraPublicProperties, list[CameraPublicProperties]]
    ) -> Observable[CameraPropertyObservableObject]: ...

    def remove_all_listeners(self) -> None: ...


# camera create config
class BaseCameraConfig(TypedDict):
    name: str
    nativeId: NotRequired[str]
    isCloud: NotRequired[bool]
    hasLight: NotRequired[bool]
    hasSiren: NotRequired[bool]
    hasBinarySensor: NotRequired[bool]
    hasBattery: NotRequired[bool]
    disabled: NotRequired[bool]
    info: NotRequired[CameraInformation]


class CameraConfigInputSettingsPartial(TypedDict, total=False):
    # _id: str
    name: str
    roles: list[CameraRoles]
    urls: list[str]


class CameraConfigInputSettings(TypedDict):
    name: str
    roles: list[CameraRoles]
    urls: list[str]


class CameraConfig(BaseCameraConfig):
    sources: list[CameraConfigInputSettings]


# CoreManager
class FfmpegArgs(TypedDict):
    hwaccel: str
    hwaccelArgs: list[str]
    hwaccelFilter: str
    threads: str


class DBSystem(TypedDict):
    serverAddresses: list[str]


SystemUpdateCallback = Union[
    Callable[[DBSystem], None],
    Callable[[DBSystem], Coroutine[None, None, None]],
]

# CoreManagerEventType = Literal["systemUpdated"]


@runtime_checkable
class CoreManager(Protocol):
    async def get_ffmpeg_path(self) -> str: ...
    async def get_hwaccel_info(self) -> FfmpegArgs: ...
    async def get_ice_servers(self) -> list[IceServer]: ...
    async def get_server_addresses(self) -> list[str]: ...

    # def on(self, event: Literal["systemUpdated"], listener: SystemUpdateCallback) -> "CoreManager": ...

    # def once(self, event: Literal["systemUpdated"], listener: SystemUpdateCallback) -> "CoreManager": ...

    # def remove_listener(
    #     self, event: Literal["systemUpdated"], listener: SystemUpdateCallback
    # ) -> "DeviceManager": ...

    # def remove_all_listeners(self, event: Optional[CoreManagerEventType] = None) -> "CoreManager": ...


# DeviceManager
CameraSelectedCallback = Union[
    Callable[[CameraDevice, CameraExtension], None],
    Callable[[CameraDevice, CameraExtension], Coroutine[None, None, None]],
]
CameraDeselectedCallback = Union[
    Callable[[str, CameraExtension], None],
    Callable[[str, CameraExtension], Coroutine[None, None, None]],
]

DeviceManagerEventType = Literal[
    "cameraSelected",
    "cameraDeselected",
]


@runtime_checkable
class DeviceManager(Protocol):
    async def get_camera_by_id(self, id: str) -> Optional[CameraDevice]: ...
    async def get_camera_by_name(self, name: str) -> Optional[CameraDevice]: ...
    async def create_camera(self, camera_config: CameraConfig) -> CameraDevice: ...
    async def remove_camera_by_id(self, id: str) -> None: ...
    async def remove_camera_by_name(self, name: str) -> None: ...

    @overload
    def on(self, event: Literal["cameraSelected"], listener: CameraSelectedCallback) -> "DeviceManager": ...
    @overload
    def on(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...

    @overload
    def once(self, event: Literal["cameraSelected"], listener: CameraSelectedCallback) -> "DeviceManager": ...
    @overload
    def once(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...

    @overload
    def remove_listener(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def remove_listener(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...

    def remove_all_listeners(self, event: Optional[DeviceManagerEventType] = None) -> "DeviceManager": ...


# camera storage
P = TypeVar("P")
CS = TypeVar("CS", default=dict[str, Any])


@runtime_checkable
class CameraStorage(Protocol, Generic[CS]):
    values: CS
    schema: JsonSchemaForm

    async def initializeStorage(self) -> None: ...
    @overload
    def getValue(self, path: str) -> Union[Awaitable[P], P, None]: ...
    @overload
    def getValue(self, path: str, default_value: P) -> Union[Awaitable[P], P]: ...
    def getValue(self, path: str, default_value: Optional[P] = None) -> Union[Awaitable[P], P, None]: ...
    async def setValue(self, path: str, new_value: Any) -> None: ...
    def hasValue(self, path: str) -> bool: ...
    async def getConfig(self) -> SchemaConfig: ...
    async def setConfig(self, new_config: CS) -> None: ...
    @overload
    async def addSchema(self, schema_or_path: JsonSchemaForm) -> None: ...
    @overload
    async def addSchema(self, schema_or_path: str, schema: JsonSchema) -> None: ...
    async def addSchema(
        self,
        schema_or_path: Union[JsonSchemaForm, str],
        schema: Optional[JsonSchema] = None,
    ) -> None: ...
    def removeSchema(self, path: str) -> None: ...
    async def changeSchema(self, path: str, new_schema: dict[str, Any]) -> None: ...
    def getSchema(self, path: str) -> Optional[JsonSchema]: ...
    def hasSchema(self, path: str) -> bool: ...


SC = TypeVar("SC", default=CameraStorage[dict[str, Any]], covariant=True)


# StorageController
@runtime_checkable
class StorageController(Protocol[SC]):
    def create_camera_storage(
        self,
        instance: Any,
        camera_id: str,
        schema: Optional[JsonSchemaForm] = None,
    ) -> SC: ...
    def get_camera_storage(self, camera_id: str) -> Optional[SC]: ...
    def remove_camera_storage(self, camera_id: str) -> None: ...


# config service
@runtime_checkable
class ConfigService(Protocol):
    def get(
        self,
        key: str,
        default: Optional[Any] = None,
        validate: Optional[Callable[[Any], bool]] = None,
        refresh: bool = False,
        write_if_not_valid: bool = False,
    ) -> Any: ...

    def has(self, key: str, refresh: bool = False) -> bool: ...
    def ensure_exists(self, key: str, default: Optional[Any] = None, write: bool = False) -> None: ...
    def set(self, key: str, value: Any, write: bool = False) -> None: ...
    def insert(self, key: str, value: Any, index: Optional[int] = None, write: bool = False) -> None: ...
    def push(self, key: str, *values: Any, write: bool = False) -> None: ...
    def delete(self, key: str, write: bool = False) -> None: ...
    def all(self, refresh: bool = False) -> dict[str, Any]: ...
    def replace(self, new_config: dict[str, Any], write: bool = False) -> None: ...
    def update_value(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        target_key: str,
        new_value: Any,
        write: bool = False,
    ) -> None: ...
    def replace_or_add_item(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        new_item: Any,
        write: bool = False,
    ) -> None: ...


# Plugin API
APIEventType = Literal["finishLaunching", "shutdown"]

PA = TypeVar("PA", bound=CameraStorage[Any], default=CameraStorage[Any])


@runtime_checkable
class PluginAPI(Protocol[PA]):
    storage_path: str
    config_file: str
    config_service: ConfigService
    storage_controller: StorageController[PA]
    core_manager: CoreManager
    device_manager: DeviceManager

    def on(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def once(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def off(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def remove_listener(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def remove_all_listeners(self, event: Optional[APIEventType] = None) -> "PluginAPI": ...


# logger
@runtime_checkable
class LoggerService(Protocol):
    def log(self, *args: Any) -> None: ...
    def error(self, *args: Any) -> None: ...
    def warn(self, *args: Any) -> None: ...
    def attention(self, *args: Any) -> None: ...
    def debug(self, *args: Any) -> None: ...
    def trace(self, *args: Any) -> None: ...


# plugin
PluginConfig = dict[str, Any]
JSONValue = Union[str, int, float, bool, dict[str, Any], list[Any]]


class ToastMessage(TypedDict):
    type: Literal["info", "success", "warning", "error"]
    message: str


class FormSubmitSchema(TypedDict):
    config: JsonSchemaObjectWithButtons


class FormSubmitResponse(TypedDict):
    toast: NotRequired[ToastMessage]
    schema: NotRequired[FormSubmitSchema]


class MotionDetectionPluginResponse(TypedDict):
    filePath: str


class ObjectDetectionPluginResponse(TypedDict):
    detections: list[Detection]


class AudioDetectionPluginResponse(TypedDict):
    detected: bool


class BasePlugin(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, logger: LoggerService, api_instance: PluginAPI) -> None: ...
    @abstractmethod
    async def onFormSubmit(self, action_id: str, payload: Any) -> Union[FormSubmitResponse, None]: ...
    @abstractmethod
    def configure_cameras(self, cameras: list[CameraDevice]) -> None: ...


class MotionDetectionPlugin(BasePlugin):
    @abstractmethod
    def interfaceSchema(self) -> Optional[RootSchema]: ...
    @abstractmethod
    async def detectMotion(
        self, video_path: str, config: dict[str, Any]
    ) -> MotionDetectionPluginResponse: ...


class ObjectDetectionPlugin(BasePlugin):
    @abstractmethod
    def interfaceSchema(self) -> Optional[RootSchema]: ...
    @abstractmethod
    async def detectObjects(
        self, image_path: str, metadata: ImageMetadata, config: dict[str, Any]
    ) -> ObjectDetectionPluginResponse: ...


class AudioDetectionPlugin(BasePlugin):
    @abstractmethod
    def interfaceSchema(self) -> Optional[RootSchema]: ...
    @abstractmethod
    async def detectAudio(
        self, audio_path: str, metadata: AudioMetadata, config: dict[str, Any]
    ) -> AudioDetectionPluginResponse: ...
