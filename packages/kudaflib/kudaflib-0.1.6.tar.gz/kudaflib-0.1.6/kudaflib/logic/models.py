# Metadata models adapted from https://github.com/statisticsnorway/microdata-tools/blob/master/microdata_tools/validation/model/metadata.py
# Under MIT License
# Copyright (c) 2023 Statistics Norway

from enum import Enum
from typing import Optional, Union, List, Dict, Any 

from pydantic import BaseModel, conlist, Extra


class TemporalityType(str, Enum):
    FIXED = "FIXED"
    STATUS = "STATUS"
    ACCUMULATED = "ACCUMULATED"
    EVENT = "EVENT"


class DataType(str, Enum):
    STRING = "STRING"
    LONG = "LONG"
    DATE = "DATE"
    DOUBLE = "DOUBLE"
    BOOL = "BOOL"


class SensitivityLevel(str, Enum):
    PUBLIC = "PUBLIC"
    NONPUBLIC = "NONPUBLIC"


class LanguageCode(str, Enum):
    no = "no"
    nb = "nb"
    nn = "nn"
    en = "en"


class UnitTypeGlobal(str, Enum):
    PERSON = "PERSON"
    ORGANISASJON = "ORGANISASJON"
    KOMMUNE = "KOMMUNE"
    FYLKE = "FYLKE"
    FYLKESKOMMUNE = "FYLKESKOMMUNE"


class MultiLingualString(BaseModel):
    languageCode: LanguageCode
    value: str


class DataRevision(BaseModel, extra=Extra.forbid):
    description: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]
    temporalEndOfSeries: bool


class KeyType(BaseModel):
    name: str
    label: str
    description: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]


class CodeListItem(BaseModel, extra=Extra.forbid):
    code: str
    categoryTitle: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]
    validFrom: Optional[Union[str, None]]
    validUntil: Optional[Union[str, None]]


class SentinelItem(BaseModel, extra=Extra.forbid):
    code: str
    categoryTitle: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]


class ValidPeriod(BaseModel, extra=Extra.forbid):
    start: Optional[Union[str, None]]
    start: Optional[Union[str, None]]


class ValueDomain(BaseModel, extra=Extra.forbid):
    description: Optional[Union[
        str, conlist(MultiLingualString, min_items=1)
    ]]
    measurementType: Optional[str]
    measurementUnitDescription: Optional[Union[
        str, conlist(MultiLingualString, min_items=1)
    ]    ]
    uriDefinition: Optional[List[Union[str, None]]]
    codeList: Optional[conlist(CodeListItem, min_items=1)]
    sentinelAndMissingValues: Optional[List[SentinelItem]]


class UnitTypeShort(BaseModel, extra=Extra.ignore):
    shortName: str
    name: conlist(MultiLingualString, min_items=1)
    description: conlist(MultiLingualString, min_items=1)


class UnitTypeMetadata(BaseModel, extra=Extra.ignore):
    shortName: str
    name: conlist(MultiLingualString, min_items=1)
    description: conlist(MultiLingualString, min_items=1)
    dataType: Optional[DataType]
    valueDomain: Optional[ValueDomain]
    validPeriod: Optional[ValidPeriod]
    unitType: UnitTypeShort


class RepresentedVariable(BaseModel, extra=Extra.ignore):
    description: conlist(MultiLingualString, min_items=1)
    validPeriod: Optional[ValidPeriod]
    valueDomain: Optional[ValueDomain]


class InstanceVariable(BaseModel):
    name: str
    label: Optional[str]
    variableRole: Optional[str]
    dataType: Optional[DataType]
    format: Optional[str]
    keyType: Optional[KeyType]
    uriDefinition: Optional[List[Union[str, None]]]
    representedVariables: conlist(RepresentedVariable, min_items=1) 


class VariableMetadata(BaseModel, extra=Extra.ignore):
    name: str
    temporalityType: TemporalityType
    dataRetrievalUrl: Optional[str]  
    sensitivityLevel: SensitivityLevel
    populationDescription: Optional[conlist(Union[
        str, MultiLingualString
    ], min_items=1)]
    spatialCoverageDescription: Optional[conlist(Union[
        str, MultiLingualString
    ], min_items=1)]
    subjectFields: Optional[conlist(Union[
        str, conlist(MultiLingualString, min_items=1)
    ], min_items=1)]
    updatedAt: Optional[str]  
    dataRevision: Optional[DataRevision] 
    identifierVariables: conlist(InstanceVariable, min_items=1)
    measureVariables: conlist(InstanceVariable, min_items=1)
    attributeVariables: Optional[List[Dict[str, Any]]]


##################################################################
# INPUT YAML DATA: KUDAF METADATA DESCRIPTION (from CONFIG.YAML) #
##################################################################

class UnitTypeMetadataInput(BaseModel, extra=Extra.ignore):
    shortName: str
    name: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]
    description: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]
    dataType: Optional[DataType]
    format: Optional[str]
    valueDomain: Optional[ValueDomain]
    validPeriod: Optional[ValidPeriod]


class IdentifierVariableInput(BaseModel, extra=Extra.forbid):
    unitType: Union[UnitTypeGlobal, UnitTypeMetadataInput]  # If not a UnitTypeGlobal, then it must have been previously defined as IdentifierVariable


class MeasureVariableInput(BaseModel, extra=Extra.ignore):
    unitType: Optional[Union[UnitTypeGlobal, UnitTypeMetadataInput]]  # If not a UnitTypeGlobal, then it must have been previously defined as IdentifierVariable
    label: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]  # 20231107 DD changed from 'name' to avoid confusion
    description: Union[
        str, conlist(MultiLingualString, min_items=1)
    ]
    dataType: Optional[DataType]
    uriDefinition: Optional[List[Union[str, None]]]
    format: Optional[str]
    valueDomain: Optional[ValueDomain]
    validPeriod: Optional[ValidPeriod]


class VariableMetadataInput(VariableMetadata):
    identifierVariables: conlist(IdentifierVariableInput, min_items=1) 
    measureVariables: conlist(MeasureVariableInput, min_items=1) 
