from typing import List, Optional
from pydantic import BaseModel, AnyUrl
from .codes import AssessorLevelCode, AssessmentLevelCode, AttestationType, ConformityTopicCode
from .base import Entity, Measure, BinaryFile, SecureLink, Endorsement, IdentifierScheme


class Standard(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#standard
    type: str = "Standard"

    id: AnyUrl
    name: str
    issuingParty: Entity
    issueDate: str  #iso8601 datetime string


class Regulation(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#regulation
    type: str = "Regulation"

    id: AnyUrl
    name: str
    jurisdictionCountry: str  #countryCode from https://vocabulary.uncefact.org/CountryId
    administeredBy: Entity
    effectiveDate: str  #iso8601 datetime string


class Metric(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#metric
    type: str = "Metric"

    metricName: str
    metricValue: Measure
    accuracy: float


class Criterion(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#criterion
    type: str = "Criterion"

    id: AnyUrl
    name: str
    thresholdValues: Metric


class Facility(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#facility
    type: str = "Facility"

    # this looks wrongs
    id: AnyUrl  # The globally unique ID of the entity as a resolvable URL according to ISO 18975.
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None
    IDverifiedByCAB: bool


class Product(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#product
    type: str = "Product"

    id: AnyUrl  # The globally unique ID of the entity as a resolvable URL according to ISO 18975.
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None
    IDverifiedByCAB: bool


class ConformityAssessment(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#conformityassessment
    type: str = "ConformityAssessment"

    id: AnyUrl
    referenceStandard: Optional[Standard] = None  #defines the specification
    referenceRegulation: Optional[Regulation] = None  #defines the regulation
    assessmentCriterion: Optional[Criterion] = None  #defines the criteria
    declaredValues: Optional[List[Metric]] = None
    compliance: Optional[bool] = False
    conformityTopic: ConformityTopicCode

    assessedProducts: Optional[List[Product]] = None
    assessedFacilities: Optional[List[Facility]] = None


class ConformityAssessmentScheme(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#conformityassessmentscheme
    type: str = "ConformityAssessmentScheme"

    id: str
    name: str
    issuingParty: Optional[Entity] = None
    issueDate: Optional[str] = None  #ISO8601 datetime string
    trustmark: Optional[BinaryFile] = None


class ConformityAttestation(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#ConformityAttestation
    type: str = "ConformityAttestation"
    id: str
    assessorLevel: Optional[AssessorLevelCode] = None
    assessmentLevel: AssessmentLevelCode
    attestationType: AttestationType
    attestationDescription: Optional[str] = None  #missing from context file
    issuedToParty: Entity
    authorisations: Optional[Endorsement] = None
    conformityCertificate: Optional[SecureLink] = None
    auditableEvidence: Optional[SecureLink] = None
    scope: ConformityAssessmentScheme
    assessments: List[ConformityAssessment] = None
