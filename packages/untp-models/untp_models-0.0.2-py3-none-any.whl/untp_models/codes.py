from enum import Enum


class AssessorLevelCode(str, Enum):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#assessorLevelCode
    Self = "Self"
    Commercial = "Commercial"
    Buyer = "Buyer"
    Membership = "Membership"
    Unspecified = "Unspecified"
    ThirdParty = "3rdParty"


class AssessmentLevelCode(str, Enum):
    #https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#assessmentlevelcode
    GovtApproval = "GovtApproval"
    GlobalMLA = "GlobalMLA"
    Accredited = "Accredited"
    Verified = "Verified"
    Validated = "Validated"
    Unspecified = "Unspecified"


class AttestationType(str, Enum):
    # https://uncefact.github.io/spec-untp/docs/specification/ConformityCredential/#attestationtype
    Certification = "Certification"
    Declaration = "Declaration"
    Inspection = "Inspection"
    Testing = "Testing"
    Verification = "Verification"
    Validation = "Validation"
    Calibration = "Calibration"


class HashMethod(str, Enum):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#hashmethodcode
    SHA256 = "SHA-256"
    SHA1 = "SHA-1"


class EncryptionMethod(str, Enum):
    NONE = "None"
    AES = "AES"


class ConformityTopicCode(str, Enum):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#conformityTopicCode
    Environment_Energy = "Environment.Energy"
    Environment_Emissions = "Environment.Emissions"
    Environment_Water = "Environment.Water"
    Environment_Waste = "Environment.Waste"
    Environment_Deforestation = "Environment.Deforestation"
    Environment_Biodiversity = "Environment.Biodiversity"
    Cirularity_Content = "Circularity.Content"
    Cirularity_Design = "Circularity.Design"
    Social_Labour = "Social.Labour"
    Social_Rights = "Social.Rights"
    Social_Safety = "Social.Safety"
    Social_Community = "Social.Community"
    Governance_Ethics = "Governance.Ethics"
    Governance_Compliance = "Governance.Compliance"
    Governance_Transparency = "Governance.Transparency"
