from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, UUID4


class CommonMacVersionEnum(str, Enum):
    lrw_100 = "LORAWAN_1_0_0"
    lrw_101 = "LORAWAN_1_0_1"
    lrw_102 = "LORAWAN_1_0_2"
    lrw_103 = "LORAWAN_1_0_3"
    lrw_104 = "LORAWAN_1_0_4"
    lrw_110 = "LORAWAN_1_1_0"


class CommonRegParamsRevisionEnum(str, Enum):
    a = "A"
    b = "B"
    rp_100 = "RP002_1_0_0"
    rp_101 = "RP002_1_0_1"
    rp_102 = "RP002_1_0_2"
    rp_103 = "RP002_1_0_3"
    rp_104 = "RP002_1_0_4"


class CommonRegionEnum(str, Enum):
    eu868 = "EU868"
    us915 = "US915"
    cn779 = "CN779"
    eu433 = "EU433"
    au915 = "AU915"
    cn470 = "CN470"
    as923 = "AS923"
    kr920 = "KR920"
    in865 = "IN865"
    ru864 = "RU864"
    ism2400 = "ISM2400"  # LoRaWAN 2.4 GHz
    as923_2 = "AS923_2"  # AS923 with -1.80 MHz frequency offset
    as923_3 = "AS923_3"  # AS923 with -6.60 MHz frequency offset
    as923_4 = "AS923_4"  # AS923 with -5.90 MHz frequency offset.


class CodecRuntimesEnum(str, Enum):
    none = "NONE"
    cayenne_lpp = "CAYENNE_LPP"
    js = "JS"  # JavaScript.


class CadPeriodicityEnum(str, Enum):
    sec_1 = "SEC_1"  # 1 second.
    ms_500 = "MS_500"  # 500 milliseconds
    ms_250 = "MS_250"  # 250 milliseconds
    ms_100 = "MS_100"  # 100 milliseconds
    ms_50 = "MS_50"  # 50 milliseconds
    ms_20 = "MS_20"  # 20 milliseconds


class SecondChAckOffsetEnum(str, Enum):
    khz_0 = "KHZ_0"  # 0 kHz.
    khz_200 = "KHZ_200"  # 200 kHz.
    khz_400 = "KHZ_400"  # 400 kHz.
    khz_800 = "KHZ_800"  # 800 kHz.
    khz_1600 = "KHZ_1600"  # 1600 kHz.
    khz_3200 = "KHZ_3200"  # 3200 kHz.


class RelayModeActivationEnum(str, Enum):
    disable_relay_mode = "DISABLE_RELAY_MODE"  # Disable the relay mode.
    enable_relay_mode = "ENABLE_RELAY_MODE"  # Enable the relay model.
    dynamic = "DYNAMIC"  # Dynamic.
    end_device_controlled = "END_DEVICE_CONTROLLED"  # End-device controlled.


class DeviceProfileListItem(BaseModel):
    createdAt: datetime  # Created at timestamp.
    id: UUID4  # Device-profile ID (UUID).
    macVersion: CommonMacVersionEnum = (
        CommonMacVersionEnum.lrw_103
    )  # default: LORAWAN_1_0_0
    name: str  # Name.
    regParamsRevision: CommonRegParamsRevisionEnum = (
        CommonRegParamsRevisionEnum.a
    )  # default: A
    region: CommonRegionEnum  # default: EU868
    supportsClassB: bool = False  # Supports Class-B.
    supportsClassC: bool = False  # Supports Class-C.
    supportsOtaa: bool = False  # Supports OTAA.
    updatedAt: datetime  # Last update timestamp.


class ListDeviceProfilesResponse(BaseModel):
    result: List[DeviceProfileListItem] = []
    totalCount: int


class DeviceProfile(BaseModel):
    abpRx1Delay: int = 15  # RX1 delay (for ABP).
    abpRx1DrOffset: int = 0  # RX1 DR offset (for ABP).
    abpRx2Dr: int = 3  # RX2 DR (for ABP).
    abpRx2Freq: int = 869525000  # RX2 frequency (for ABP, Hz).
    adrAlgorithmId: str = "default"  # ADR algorithm ID.
    allowRoaming: bool = (
        False  # Allow roaming. If set to true, it means that the device is allowed to use roaming.
    )
    autoDetectMeasurements: bool = True  # Auto-detect measurements.
    # If set to true, measurements will be automatically added based on the
    # keys of the decoded payload. In cases where the decoded payload contains
    # random keys in the data, you want to set this to false.
    classBPingSlotDr: int = 0  # Class-B ping-slot DR.
    classBPingSlotFreq: int = 0  # Class-B ping-slot freq (Hz).
    classBPingSlotNbK: int = (
        0  # Class-B ping-slots per beacon period. Valid options are: 0 - 7.
    )
    # The actual number of ping-slots per beacon period equals to 2^k.
    classBTimeout: int = 0  # Class-B timeout (seconds).
    # This is the maximum time ChirpStack will wait to receive an acknowledgement from the device (if requested).
    classCTimeout: int = 0  # Class-C timeout (seconds).
    # This is the maximum time ChirpStack will wait to receive an acknowledgement from the device (if requested).
    description: str = ""  # Description.
    deviceStatusReqInterval: int = 1  # Device-status request interval (times / day).
    # This defines the times per day that ChirpStack will request the device-status from the device.
    flushQueueOnActivate: bool = True  # Flush queue on device activation.
    id: Optional[UUID4] = None  # Device-profile ID (UUID). Note: on create this will be automatically generated.
    isRelay: bool = False  # Device is a Relay device.
    # Enable this in case the device is a Relay. A Relay device implements TS011
    # and is able to relay data from relay capable devices. See for more information the TS011 specification.
    isRelayEd: bool = False  # Device is a Relay end-device.
    # Enable this in case the device is an end-device that can operate under a
    # Relay. Please refer to the TS011 specification for more information.
    macVersion: CommonMacVersionEnum = (
        CommonMacVersionEnum.lrw_103
    )  # default: LORAWAN_1_0_0
    measurements: Optional[dict[str, str]] = {}
    name: str  # Name.
    payloadCodecRuntime: CodecRuntimesEnum = CodecRuntimesEnum.none # default: NONE
    payloadCodecScript: str = (
        "/**\n * Decode uplink function\n * \n * @param {object} input\n * @param {number[]} input.bytes Byte array containing the uplink payload, e.g. [255, 230, 255, 0]\n * @param {number} input.fPort Uplink fPort.\n * @param {Record<string, string>} input.variables Object containing the configured device variables.\n * \n * @returns {{data: object}} Object representing the decoded payload.\n */\nfunction decodeUplink(input) {\n  return {\n    data: {\n      // temp: 22.5\n    }\n  };\n}\n\n/**\n * Encode downlink function.\n * \n * @param {object} input\n * @param {object} input.data Object representing the payload that must be encoded.\n * @param {Record<string, string>} input.variables Object containing the configured device variables.\n * \n * @returns {{bytes: number[]}} Byte array containing the downlink payload.\n */\nfunction encodeDownlink(input) {\n  return {\n    // bytes: [225, 230, 255, 0]\n  };\n}\n"
    )
    # Payload codec script.
    regParamsRevision: CommonRegParamsRevisionEnum = CommonRegParamsRevisionEnum.a
    region: CommonRegionEnum = CommonRegionEnum.eu868  # default: EU868
    regionConfigId: str = ""  # Region configuration ID.
    # If set, devices will only use the associated region. If let blank, then
    # devices will use all regions matching the selected common-name. Note
    # that multiple region configurations can exist for the same common-name,
    # e.g. to provide an 8 channel and 16 channel configuration for the US915 band.
    relayCadPeriodicity: CadPeriodicityEnum = CadPeriodicityEnum.sec_1  # default: SEC_1
    relayDefaultChannelIndex: int = 0  # Relay default channel index.
    # Valid values are 0 and 1, please refer to the RP002 specification for the meaning of these values.
    relayEdActivationMode: RelayModeActivationEnum = RelayModeActivationEnum.disable_relay_mode  # default: DISABLE_RELAY_MODE

    relayEdBackOff: int = (
        0  # Relay end-device back-off (in case it does not receive WOR ACK frame).
    )
    # 0 = Always send a LoRaWAN uplink
    # 1..63 = Send a LoRaWAN uplink after X WOR frames without a WOR ACK
    relayEdRelayOnly: bool = False  # End-device only accept data through relay.
    # Only accept data for this device through a relay. This setting is useful
    # for testing as in case of a test-setup, the end-device is usually within range of the gateway.
    relayEdSmartEnableLevel: int = 0  # Relay end-device smart-enable level.
    relayEdUplinkLimitBucketSize: int = 0  # Relay end-device uplink limit bucket size.
    # This field indicates the multiplier to determine the bucket size according to the following formula:
    # BucketSize TOKEN = _reload_rate x _bucket_size Valid values (0 - 3):
    # 0 = 1
    # 1 = 2
    # 2 = 4
    # 3 = 12
    relayEdUplinkLimitReloadRate: int = 0  # Relay end-device uplink limit reload rate.

    # Valid values:
    # 0 - 62 = X tokens every hour
    # 63 = no limitation

    relayEnabled: bool = False  # Relay must be enabled.
    relayGlobalUplinkLimitBucketSize: int = 0  # Relay globak uplink limit bucket size.
    # This field indicates the multiplier to determine the bucket size
    # according to the following formula:
    # BucketSize TOKEN = _reload_rate x _bucket_size
    # Valid values (0 - 3):
    # 0 = 1
    # 1 = 2
    # 2 = 4
    # 3 = 12
    relayGlobalUplinkLimitReloadRate: int = (
        0  #     Relay global uplink limit reload rate.
    )

    # Valid values:

    #     0 - 126 = X tokens every hour
    #     127 = no limitation

    relayJoinReqLimitBucketSize: int = 0  # Relay join-request limit bucket size.
    # This field indicates the multiplier to determine the bucket size
    # according to the following formula:
    # BucketSize TOKEN = _reload_rate x _bucket_size

    # Valid values (0 - 3):
    # 0 = 1
    # 1 = 2
    # 2 = 4
    # 3 = 12
    relayJoinReqLimitReloadRate: int = 0  # Relay join-request limit reload rate.
    # Valid values:

    #     0 - 126 = X tokens every hour
    #     127 = no limitation

    relayNotifyLimitBucketSize: int = 0  # Relay notify limit bucket size.
    # This field indicates the multiplier to determine the bucket size
    # according to the following formula:
    # BucketSize TOKEN = _reload_rate x _bucket_size

    # Valid values (0 - 3):
    # 0 = 1
    # 1 = 2
    # 2 = 4
    # 3 = 12

    relayNotifyLimitReloadRate: int = 0  # Relay notify limit reload rate.

    # Valid values:

    #     0 - 126 = X tokens every hour
    #     127 = no limitation

    relayOverallLimitBucketSize: int = 0
    # Relay overall limit bucket size.

    # This field indicates the multiplier to determine the bucket size
    # according to the following formula:
    # BucketSize TOKEN = _reload_rate x _bucket_size

    # Valid values (0 - 3):
    # 0 = 1
    # 1 = 2
    # 2 = 4
    # 3 = 12

    relayOverallLimitReloadRate: int = 0

    # Relay overall limit reload rate.

    # Valid values:

    #     0 - 126 = X tokens every hour
    #     127 = no limitation

    relaySecondChannelAckOffset: SecondChAckOffsetEnum = (
        SecondChAckOffsetEnum.khz_0
    )  # default: KHZ_0

    relaySecondChannelDr: int = 0  # Relay second channel DR.
    relaySecondChannelFreq: int = 0  # Relay second channel frequency (Hz).
    rx1Delay: int = 0  # RX1 Delay.
    # This makes it possible to override the system RX1 Delay. Please note that
    # this values only has effect in case it is higher than the system value.
    # In other words, it can be used to increase the RX1 Delay but not to decrease
    # it.
    # Valid options are 1 - 15 (0 = always use system RX1 Delay).

    supportsClassB: bool = False  # Supports Class B.
    supportsClassC: bool = False  # Supports Class-C.
    supportsOtaa: bool = False  # Supports OTAA.
    tags: Optional[dict[str, str]] = {}
    tenantId: UUID4  # Tenant ID (UUID).
    uplinkInterval: int = 3600  # Uplink interval (seconds).
    # This defines the expected uplink interval which the device uses for
    # communication. If the uplink interval has expired and no uplink has
    # been received, the device is considered inactive.


class CreateDeviceProfileRequest(BaseModel):
    deviceProfile: DeviceProfile


class CreateDeviceProfileResponse(BaseModel):
    id: UUID4


class GetDeviceProfileResponse(BaseModel):
    createdAt: datetime
    deviceProfile: DeviceProfile
    updatedAt: datetime
