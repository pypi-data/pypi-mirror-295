class DataDict:
    def __init__(self, data: dict=None) -> None:
        if data is None:
            data = {}
        self.__import__(data)
    def __iter__(self):
        return iter(self.__export__().items())
    def __import__(self, data: dict={}):
        for k,v in data.items():
            setattr(self, k,v)
    def __export__(self):
        export_dict = {}
        for key in self.__dict__:
            export_dict[key] = getattr(self, key)
        return export_dict
    def __repr__(self) -> str:
        data = self.__export__()
        out_list = []
        for k,v in data.items():
            add_quotes = isinstance(v, str)
            if add_quotes:
                out_list.append(f"{k}: '{v}'")
            else:
                out_list.append(f"{k}: {v}")
        return "(" + ", ".join(out_list) + ")"

#region VoIP
#region VoIP trunks
# region VoIP SIP
class SIPVoIPSubscriptionInfo(DataDict):
    event: str
    notifyServer: str
    notifyServerPort: int
class SIPVoIPEventSubscibeLine(DataDict):
    eventSubscribeEvent: str
    eventSubscribeAuthUserName: str
    eventSubscribeAuthPassword: str
class SIPVoIPInfo(DataDict):
    registrarServer: str
    registrarServerPort: int
    userAgentDomain: str
    userAgentPort: int    
    subscriptionInfo: list[SIPVoIPSubscriptionInfo]
class SIPVoIPTrunkLine(DataDict):
    name: str
    groupId: str
    enable: str
    status: str
    statusInfo: str
    directoryNumber: str
    uri: str
    event_subscribe_lines: SIPVoIPEventSubscibeLine
class SIPVoIPTrunk(DataDict):
    name: str
    signalingProtocol: str
    enable: str
    trunk_lines: SIPVoIPTrunkLine
    directoryNumber: str
    uri: str
    sip: SIPVoIPInfo
#endregion VoIP SIP

class H323VoIPTrunk(DataDict):
    #TODO: Get info about this, i don't have FTTH so idk
    pass
#endregion VoIP trunks

class VoIPConnection(DataDict):
    Name: str
    Enable: str
    Protocol: str
    Encapsulation: str
    InterfaceId: str
    Interface: str
    PhysInterface: str

#endregion VoIP

#region WANStatus
class WANStatus(DataDict):
    LinkType: str
    LinkState: str
    MACAddress: str
    Protocol: str
    ConnectionState: str
    LastConnectionError: str
    IPAddress: str
    RemoteGateway: str
    DNSServers: str
    IPv6Address: str
#region DSL
class DSLLinkDetails(DataDict):
    CurrentProfile: str
    DataPath: str
    DownstreamAttenuation: int
    DownstreamCurrRate: int
    DownstreamMaxRate: int
    DownstreamNoiseMargin: int
    DownstreamPower: int
    FirmwareVersion: str
    InterleaveDepth: int
    LastChange: int
    LastChangeTime: int
    LinkStatus: str
    ModulationHint: str
    ModulationType: str
    StandardUsed: str
    StandardsSupported: str
    UPBOKLE: int
    UpstreamAttenuation: int
    UpstreamCurrRate: int
    UpstreamMaxRate: int
    UpstreamNoiseMargin: int
    UpstreamPower: int
class DSLErrors(DataDict):
    ReceiveBlocks: int
    TransmitBlocks: int
    CellDelin: int
    LinkRetrain: int
    InitErrors: int
    InitTimeouts: int
    LossOfFraming: int
    ErroredSecs: int
    SeverelyErroredSecs: int
    FECErrors: int
    ATUCFECErrors: int
    HECErrors: int
    ATUCHECErrors: int
    CRCErrors: int
    ATUCCRCErrors: int
#endregion DSL
#region PPP
class PPPInfo(DataDict):
    Username: str
    ConnectionStatus: str
    LastConnectionError: str
    MaxMRUSize: int
    PPPoESessionID: int
    PPPoEACName: str
    PPPoEServiceName: str
    RemoteIPAddress: str
    LocalIPAddress: str
    LastChangeTime: int
    LastChange: int
    DNSServers: str
    TransportType: str
    LCPEcho: int
    LCPEchoRetry: int
    IPCPEnable: bool
    IPv6CPEnable: bool
    IPv6CPLocalInterfaceIdentifier: str
    IPv6CPRemoteInterfaceIdentifier: str
    ConnectionTrigger: str
    IdleDisconnectTime: int
#endregion PPP
#endregion WANStatus

#region Managment

class User(DataDict):
    name: str
    enable: bool
    type: str
    groups: list[str]
class LEDStatus(DataDict):
    name: str
    color: str
    state: str
class LANIPAddress(DataDict):
    Address: str
    Netmask: str
    DHCPEnabled: bool
    DHCPMinAddress: str
    DHCPMaxAddress: str
class IPv6Status(DataDict):
    Enable: bool
    IPv4UserRequested: bool
    IPv6Address: str

#endregion Managment

#region WiFi
class WifiAdapterDevice(DataDict):
    RadioStatus: str
    LastChangeTime: int
    LastChange: int
    MaxBitRate: int
    SupportedFrequencyBands: str
    OperatingFrequencyBand: str
    SupportedStandards: str
    OperatingStandards: str
    PossibleChannels: str
    ChannelsInUse: str
    Channel: int
    AutoChannelSupported: bool
    AutoChannelEnable: bool
    AutoChannelRefreshPeriod: int
    AutoChannelSelecting: bool
    ActiveAntennaCtrl: int
    OperatingChannelBandwidth: str
    ExtensionChannel: str
    GuardInterval: str
    MCS: int
    TransmitPowerSupported: str
    TransmitPower: int
    IEEE80211hSupported: bool
    IEEE80211hEnabled: bool
    RegulatoryDomain: str
class WifiNetworkSecurity(DataDict):
    ModesSupported: str
    ModeEnabled: str
    WEPKey: str
    PreSharedKey: str
    KeyPassPhrase: str
    RekeyingInterval: int
    RadiusServerIPAddr: str
    RadiusServerPort: int
    RadiusSecret: str
    RadiusDefaultSessionTimeout: int
    RadiusOwnIPAddress: str
    RadiusNASIdentifier: str
    RadiusCalledStationId: str
    RadiusChargeableUserId: bool
class WifiNetworkWPSInfo(DataDict):
    Enable: bool
    ConfigMethodsSupported: str
    ConfigMethodsEnabled: str
    SelfPIN: str
    Configured: bool
    PairingInProgress: bool
class WifiNetworkInfo(DataDict):
    VAPStatus: str
    LastChangeTime: int
    LastChange: int
    BSSID: str
    SSID: str
    SSIDAdvertisementEnabled: bool
    RetryLimit: int
    WMMCapability: bool
    UAPSDCapability: bool
    WMMEnable: bool
    UAPSDEnable: bool
    MaxStations: int
    APBridgeDisable: bool
    BridgeInterface: str
    AssociatedDeviceNumberOfEntries: int
    Security: WifiNetworkSecurity
    WPS: WifiNetworkWPSInfo
    MACFiltering: dict
    HotSpot2: dict
class WifiBytes(DataDict):
    RxBytes: int
    TxBytes: int
class WifiOpenMode(DataDict):
    Enable: bool
    Status: str
    SSID: str
#endregion WiFi

#region IPTV
class IPTVChannel(DataDict):
    ChannelStatus: bool
    ChannelType: str
    ChannelNumber: str
    ChannelFlags: str
#endregion IPTV

#region DHCP
class DHCPStaticLease(DataDict):
    IPAddress: str
    MACAddress: str
    LeasePath: str
#endregion DHCP

#region Firewall
class ForwardedPort(DataDict):
    Id: str
    Origin: str
    Description: str
    Status: str
    SourceInterface: str
    Protocol: str
    ExternalPort: str
    InternalPort: str
    SourcePrefix: str
    DestinationIPAddress: str
    DestinationMACAddress: str # This is unused, if it actually worked then you could do wake on wan without any other router or server (i have a wol proxy, receives from the router and just sends the same thing in the local network)
    LeaseDuration: int
    Time: str
    HairpinNAT: bool
    SymmetricSNAT: bool
    Enable: bool
#endregion Firewall