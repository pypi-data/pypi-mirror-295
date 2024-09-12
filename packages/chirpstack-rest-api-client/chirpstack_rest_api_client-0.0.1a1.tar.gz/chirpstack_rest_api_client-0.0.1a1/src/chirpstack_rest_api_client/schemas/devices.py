from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, UUID4


class CommonDeviceClassEnum(str, Enum):
    class_a = "CLASS_A"
    class_b = "CLASS_B"
    class_c = "CLASS_C"


class DeviceStatus(BaseModel):
    batteryLevel: float  # Device battery level as a percentage. -1 when the battery level is not available.
    externalPowerSource: bool  # Device is connected to an external power source.
    margin: int  # The device margin status -32..32: The demodulation SNR ration in dB


class DeviceListItem(BaseModel):
    createdAt: datetime  # Created at timestamp.
    description: str  # Description.
    devEui: str  # DevEUI (EUI64).
    deviceProfileId: UUID4  # Device-profile ID (UUID).
    deviceProfileName: str  # Device-profile name.
    deviceStatus: Optional[DeviceStatus]
    lastSeenAt: Optional[datetime]  # Last seen at timestamp.
    name: str  # Name.
    updatedAt: datetime  # Last update timestamp.


class ListDevicesResponse(BaseModel):
    result: List[DeviceListItem] = []
    totalCount: int


class Device(BaseModel):
    applicationId: UUID4  # Application ID (UUID).
    description: Optional[str] = None # Description.
    devEui: str  # DevEUI (EUI64).
    deviceProfileId: UUID4  # Device-profile ID (UUID).
    isDisabled: bool = False  # Device is disabled.
    joinEui: Optional[str] = None  # JoinEUI (optional, EUI64).
    # This field will be automatically set / updated on OTAA. However, in some
    # cases it must be pre-configured. For example to allow OTAA using a Relay.
    # In this case the Relay needs to know the JoinEUI + DevEUI combinations
    # of the devices for which it needs to forward uplinks.
    name: str  # Name.
    skipFcntCheck: bool = (
        True  # Skip frame-counter checks (this is insecure, but could be helpful for debugging).
    )
    tags: Optional[dict[str, str]] = {}
    variables: Optional[dict[str, str]] = {}


class CreateDeviceRequest(BaseModel):
    device: Device


class GetDeviceResponse(BaseModel):
    classEnabled: CommonDeviceClassEnum = (
        CommonDeviceClassEnum.class_a
    )  # default: CLASS_A
    createdAt: datetime  # Created at timestamp.
    device: Device
    deviceStatus: Optional[DeviceStatus]
    lastSeenAt: Optional[datetime]  # Last seen at timestamp.
    updatedAt: datetime


class DeviceActivation(BaseModel):
    aFCntDown: int = 0  # Downlink application frame-counter.
    appSKey: str  # Application session key (HEX encoded).
    devAddr: str  # Device address (HEX encoded).
    devEui: Optional[str] = None  # Device EUI (EUI64).
    fCntUp: int = 0  # Uplink frame-counter.
    fNwkSIntKey: str  # Forwarding network session integrity key (HEX encoded).
    nFCntDown: int = 0  # Downlink network frame-counter.
    nwkSEncKey: str  # Network session encryption key (HEX encoded).
    # Note: For ABP in LoRaWAN 1.0.x, use this, the serving and the forwarding
    # network session integrity key fields with the LoRaWAN 1.0.x 'NwkSKey`!
    sNwkSIntKey: str  # Serving network session integrity key (HEX encoded)

class DeviceActivationRequest(BaseModel):
    deviceActivation: DeviceActivation

class CommonKeyEnvelope(BaseModel):
    aesKey: bytes  # AES key (when the kek_label is set, this value must first be decrypted).
    kekLabel: str  # KEK label.


class CommonJoinServerContext(BaseModel):
    appSKey: CommonKeyEnvelope
    sessionKeyId: str  # Session-key ID.


class GetDeviceActivationResponse(BaseModel):
    deviceActivation: DeviceActivation
    joinServerContext: Optional[CommonJoinServerContext]
