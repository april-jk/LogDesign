# Check Event Id
EVENT_ID = [4624, 4625, 4662, 4768, 4769, 4776, 4672, 4720, 4726, 4728, 4729, 4732, 4733, 4756, 4757, 4719, 5137, 5141]

# EVTX Header
EVTX_HEADER = b"\x45\x6C\x66\x46\x69\x6C\x65\x00"

# String Check list
UCHECK = r"[%*+=\[\]\\/|;:\"<>?,&]"
HCHECK = r"[*\\/|:\"<>?&]"

# IPv4 regex
IPv4_PATTERN = re.compile(r"\A\d+\.\d+\.\d+\.\d+\Z", re.DOTALL)

# IPv6 regex
IPv6_PATTERN = re.compile(r"\A(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,5})?|([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,4})?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,3})?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,2})?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3}))?)?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::([0-9a-f]|[1-9a-f][0-9a-f]{1,3})?|(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){3}))))))\Z", re.DOTALL)

# LogonTracer folder path
FPATH = os.path.dirname(os.path.abspath(__file__))

# CategoryId
CATEGORY_IDs = {
    "%%8280": "Account_Logon",
    "%%8270": "Account_Management",
    "%%8276": "Detailed_Tracking",
    "%%8279": "DS_Access",
    "%%8273": "Logon/Logoff",
    "%%8274": "Object_Access",
    "%%8277": "Policy_Change",
    "%%8275": "Privilege_Use",
    "%%8272": "System"}

# Auditing Constants
AUDITING_CONSTANTS = {
    "{0cce9210-69ae-11d9-bed3-505054503030}": "SecurityStateChange",
    "{0cce9211-69ae-11d9-bed3-505054503030}": "SecuritySubsystemExtension",
    "{0cce9212-69ae-11d9-bed3-505054503030}": "Integrity",
    "{0cce9213-69ae-11d9-bed3-505054503030}": "IPSecDriverEvents",
    "{0cce9214-69ae-11d9-bed3-505054503030}": "Others",
    "{0cce9215-69ae-11d9-bed3-505054503030}": "Logon",
    "{0cce9216-69ae-11d9-bed3-505054503030}": "Logoff",
    "{0cce9217-69ae-11d9-bed3-505054503030}": "AccountLockout",
    "{0cce9218-69ae-11d9-bed3-505054503030}": "IPSecMainMode",
    "{0cce9219-69ae-11d9-bed3-505054503030}": "IPSecQuickMode",
    "{0cce921a-69ae-11d9-bed3-505054503030}": "IPSecUserMode",
    "{0cce921b-69ae-11d9-bed3-505054503030}": "SpecialLogon",
    "{0cce921c-69ae-11d9-bed3-505054503030}": "Others",
    "{0cce921d-69ae-11d9-bed3-505054503030}": "FileSystem",
    "{0cce921e-69ae-11d9-bed3-505054503030}": "Registry",
    "{0cce921f-69ae-11d9-bed3-505054503030}": "Kernel",
    "{0cce9220-69ae-11d9-bed3-505054503030}": "Sam",
    "{0cce9221-69ae-11d9-bed3-505054503030}": "CertificationServices",
    "{0cce9222-69ae-11d9-bed3-505054503030}": "ApplicationGenerated",
    "{0cce9223-69ae-11d9-bed3-505054503030}": "Handle",
    "{0cce9224-69ae-11d9-bed3-505054503030}": "Share",
    "{0cce9225-69ae-11d9-bed3-505054503030}": "FirewallPacketDrops",
    "{0cce9226-69ae-11d9-bed3-505054503030}": "FirewallConnection",
    "{0cce9227-69ae-11d9-bed3-505054503030}": "Other",
    "{0cce9228-69ae-11d9-bed3-505054503030}": "Sensitive",
    "{0cce9229-69ae-11d9-bed3-505054503030}": "NonSensitive",
    "{0cce922a-69ae-11d9-bed3-505054503030}": "Others",
    "{0cce922b-69ae-11d9-bed3-505054503030}": "ProcessCreation",
    "{0cce922c-69ae-11d9-bed3-505054503030}": "ProcessTermination",
    "{0cce922d-69ae-11d9-bed3-505054503030}": "DpapiActivity",
    "{0cce922e-69ae-11d9-bed3-505054503030}": "RpcCall",
    "{0cce922f-69ae-11d9-bed3-505054503030}": "AuditPolicy",
    "{0cce9230-69ae-11d9-bed3-505054503030}": "AuthenticationPolicy",
    "{0cce9231-69ae-11d9-bed3-505054503030}": "AuthorizationPolicy",
    "{0cce9232-69ae-11d9-bed3-505054503030}": "MpsscvRulePolicy",
    "{0cce9233-69ae-11d9-bed3-505054503030}": "WfpIPSecPolicy",
    "{0cce9234-69ae-11d9-bed3-505054503030}": "Others",
    "{0cce9235-69ae-11d9-bed3-505054503030}": "UserAccount",
    "{0cce9236-69ae-11d9-bed3-505054503030}": "ComputerAccount",
    "{0cce9237-69ae-11d9-bed3-505054503030}": "SecurityGroup",
    "{0cce9238-69ae-11d9-bed3-505054503030}": "DistributionGroup",
    "{0cce9239-69ae-11d9-bed3-505054503030}": "ApplicationGroup",
    "{0cce923a-69ae-11d9-bed3-505054503030}": "Others",
    "{0cce923b-69ae-11d9-bed3-505054503030}": "DSAccess",
    "{0cce923c-69ae-11d9-bed3-505054503030}": "AdAuditChanges",
    "{0cce923d-69ae-11d9-bed3-505054503030}": "Replication",
    "{0cce923e-69ae-11d9-bed3-505054503030}": "DetailedReplication",
    "{0cce923f-69ae-11d9-bed3-505054503030}": "CredentialValidation",
    "{0cce9240-69ae-11d9-bed3-505054503030}": "Kerberos",
    "{0cce9241-69ae-11d9-bed3-505054503030}": "Others",
    "{0cce9242-69ae-11d9-bed3-505054503030}": "KerbCredentialValidation",
    "{0cce9243-69ae-11d9-bed3-505054503030}": "NPS"}