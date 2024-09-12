from typing import List, Optional
from pydantic import BaseModel, Field, AnyUrl
from .codes import EncryptionMethod, HashMethod


class IdentifierScheme(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#identifierscheme
    type: str = "IdentifierScheme"

    id: AnyUrl  # from vocabulary.uncefact.org/identifierSchemes
    name: str


class Entity(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#entity
    type: str = "Entity"

    id: AnyUrl
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None


class BinaryFile(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#binaryfile
    type: str = "BinaryFile"

    fileName: str
    fileType: str  # https://mimetype.io/all-types
    file: str  #Base64


class Link(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#link
    type: str = "Link"

    linkURL: AnyUrl
    linkName: str
    linkType: str  # drawn from a controlled vocabulary


class SecureLink(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#securelink
    type: str = "SecureLink"

    linkUrl: AnyUrl
    linkName: str
    linkType: str
    hashDigest: str
    hashMethod: HashMethod
    encryptionMethod: EncryptionMethod


class Measure(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#measure
    type: str = "Measure"

    value: float
    unit: str = Field(
        max_length="3")  # from https://vocabulary.uncefact.org/UnitMeasureCode


class Endorsement(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.3.10/artefacts/readme/render#endorsement
    type: str = "Endorsement"

    id: AnyUrl
    name: str
    trustmark: Optional[BinaryFile] = None
    issuingAuthority: Entity
    accreditationCertification: Optional[Link] = None
