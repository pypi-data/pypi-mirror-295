import pydantic
from pathlib import Path
from typing import Union, List, Dict, Tuple, Any, TypeVar 

from kudaflib.logic.models import (
    VariableMetadataInput,
    VariableMetadata,
    InstanceVariable,
    UnitTypeMetadataInput,
    UnitTypeMetadata,
    UnitTypeGlobal,
    UnitTypeShort,
    KeyType,
    ValueDomain,
    RepresentedVariable,
    MultiLingualString,
)
from kudaflib.logic.utils import (
    write_json,
    load_yaml,
    replace_enums,
    convert_to_multilingual_dict,
    convert_list_to_multilingual,
    unittype_to_multilingual,
    value_domain_to_multilingual,
)
from kudaflib.logic.exceptions import (
    ValidationError,
    UnregisteredUnitTypeError,
    ParseMetadataError,
)
from kudaflib.logic import (
    temporal_attributes,
    unit_type_variables,
)


ModelType = TypeVar("ModelType")


class MetadataProcess:

    def generate(
        self, 
        config_yaml_path: Path,
        output_metadata_dir: Union[Path, None] = None,
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Generates Kudaf JSON Metadata files (for both Variables and Unit Types) from a YAML configuration file
        """
        variables = []
        unit_types = []

        config_dict = load_yaml(config_yaml_path)

        #### PROCESS YAML VARIABLES SECTION ####
        for _var in config_dict.get('variables'):
            # Validate Input Variable Metadata
            _in_varmodel = self.validate_metadata_model(Model=VariableMetadataInput, metadata_json=_var)

            # Add the Instance (Identifier, Measure, Attribute) Variables
            _ds_units, _inst_vars = self.insert_instance_variables(metadata_input=_in_varmodel)
            _var.update(_inst_vars)
            _descript_vars = self.convert_descriptions_to_multilingual(metadata_input=_in_varmodel, default_lang='no')
            _var.update(_descript_vars)     

            # Validate completed Output Variable Metadata model
            _metmodel = self.validate_metadata_model(Model=VariableMetadata, metadata_json=_var)

            variables.append(_metmodel.dict(exclude_unset=True))

            # Working list of UnitTypes so far
            ut_names = [_u.get('shortName') for _u in unit_types]
            # Add to UnitTypes if new
            unit_types += [_unit for _unit in _ds_units if _unit.get('shortName') not in ut_names]

        #### WRITE OUT METADATA FILES ####
        out_dir = str(output_metadata_dir) if output_metadata_dir else "./"

        write_json(
            filepath=Path(out_dir) / "variables_metadata.json", 
            content=variables
        )
        if unit_types:
            write_json(
                filepath=Path(out_dir) / "unit_types_metadata.json", 
                content=unit_types
            )

        return variables
    
    def create_unittype_metadata(self, unittype_model_input: UnitTypeMetadataInput) -> Dict[str, Any]:
        """
        Creates the Unit Type metadata from the body input, for a given Catalog.
        """
        _utdict = unittype_model_input.dict(exclude_unset=True)
        # Add a keyType field, as above
        _utdict.update({
            "unitType": UnitTypeShort(**{
                "shortName": unittype_model_input.shortName,
                "name": unittype_model_input.name,
                "description": unittype_model_input.description,
            }),
        })

        _utmodel = self.validate_metadata_model(Model=UnitTypeMetadata, metadata_json=_utdict)             
        
        return _utmodel.dict(exclude_unset=True)
        
    def insert_instance_variables(self, metadata_input: VariableMetadataInput) -> Tuple[List, Dict]:
        """
        Create instance variable metadata for Identifier, Measure and Attibute Variables
        Create metadata for Datasource-specific Unit Types, if any
        """
        # Identifier Variables: 
        # Could come from pre-defined Global Unit Types or from provided Datasource-specific Unit Types
        ivars = []
        ds_units = []
        for _iv in metadata_input.identifierVariables:
            _utype = _iv.unitType
            if not isinstance(_utype, UnitTypeMetadataInput) and \
                hasattr(_utype, 'value') and \
                _utype.value in UnitTypeGlobal._member_names_ and \
                _utype in unit_type_variables.GLOBAL_UNIT_TYPES:
                _ivmodel = self.convert_unit_type_to_identifier(unit_type_variables.get(_utype))
                ivars.append(replace_enums(input_dict=_ivmodel.dict(exclude_unset=True)))
            elif isinstance(_utype, UnitTypeMetadataInput):
                # This is a datasource-specific UnitType
                # First create an Identifier Variable out of it (an InstanceVariable)
                if isinstance(_iv.unitType.name, str):
                    # Extract if string before converting to dicts
                    _label = _iv.unitType.name
                if isinstance(_iv.unitType.name, list):
                    # Pick first item in the list, typically the default language
                    _name = _iv.unitType.name[0]
                    if isinstance(_name, dict):
                        _label = _name.get('value', "")
                    elif isinstance(_name, str):
                        _label = _name
                    elif isinstance(_name, MultiLingualString):
                        _label = _name.value
                    else:
                        _label = "N/A"
                else:
                    _label = "N/A"

                _utype = unittype_to_multilingual(utype=_utype, default_lang="no")
                _ivdict = {
                    "name": _utype.shortName,
                    "label": _label,
                    "dataType": _iv.unitType.dataType,
                    "variableRole": "Identifier",
                    "keyType": KeyType(**{
                        "name": _utype.shortName,
                        "label": _label,
                        "description": _utype.description,
                    }),
                    "representedVariables": [
                        RepresentedVariable(**{
                            "description": _utype.description,
                            "valueDomain": _utype.valueDomain,
                        })
                    ]
                }

                _ivmodel = self.validate_metadata_model(Model=InstanceVariable, metadata_json=_ivdict)             
                ivars.append(replace_enums(input_dict=_ivmodel.dict(exclude_unset=True)))   

                # Now create the metadata for this new UnitType
                _utype_metadata = self.create_unittype_metadata(unittype_model_input=_utype)
                ds_units.append(_utype_metadata)
            else:
                error = f"Unregistered Unit Type: {_utype}"
                print(error)
                raise UnregisteredUnitTypeError(error)
            
        # Measure Variables 
        mvars = []
        for _mv in metadata_input.measureVariables:
            insert_measure = {}
            _mvdict = _mv.dict(exclude_unset=True)
            _utype = _mvdict.get("unitType", "")

            insert_measure["name"] = metadata_input.name
            insert_measure["label"] = _mvdict["label"]
            insert_measure["description"] = _mvdict["description"] if isinstance(_mvdict["description"], list) else [
                            convert_to_multilingual_dict(input_str=_mvdict["description"], default_lang="no")
                        ]
            insert_measure["variableRole"] = "Measure"

            if _utype:
                if not isinstance(_utype, UnitTypeMetadataInput) and \
                    hasattr(_utype, 'value') and \
                    _utype.value in UnitTypeGlobal._member_names_ and \
                    _utype in unit_type_variables.GLOBAL_UNIT_TYPES:
                    utmodel = UnitTypeMetadataInput(**unit_type_variables.get(_utype))
                elif isinstance(_utype, dict):
                    utmodel = UnitTypeMetadataInput(**_utype)
                    utmodel = unittype_to_multilingual(utype=utmodel, default_lang="no")
                    # Now create the metadata for this new UnitType
                    _mutype_metadata = self.create_unittype_metadata(unittype_model_input=utmodel)
                    ds_units.append(_mutype_metadata)
                elif type(_utype) not in [str, UnitTypeMetadataInput]:
                    print(f"UNIT TYPE: {_utype} NOT FOUND")
                    raise UnregisteredUnitTypeError
                
                insert_measure.update({
                    "keyType": KeyType(**{
                        "name": utmodel.shortName,
                        "label":utmodel.name[0].get('value', "") if isinstance(utmodel.name[0], dict) else utmodel.name[0].value,
                        "description": utmodel.description if isinstance(utmodel.description, list) else [
                            convert_to_multilingual_dict(input_str=utmodel.description, default_lang="no")
                        ],
                    }),
                    "representedVariables": [
                        RepresentedVariable(**{
                            "description": _mvdict["description"] if isinstance(_mvdict["description"], list) else [
                            convert_to_multilingual_dict(input_str=_mvdict["description"], default_lang="no")
                        ],
                            "valueDomain": utmodel.valueDomain,
                        })
                    ]
                })
            else:
                insert_measure.update({
                    "representedVariables": [
                        RepresentedVariable(**{
                            "description": _mvdict["description"] if isinstance(_mvdict["description"], list) else [
                                convert_to_multilingual_dict(input_str=_mvdict["description"], default_lang="no")
                            ],
                            "valueDomain": value_domain_to_multilingual(
                                val_dom=_mvdict.get('valueDomain') if _mvdict.get('valueDomain') else ValueDomain(**{
                                        "uriDefinition": None,
                                        "description": "N/A",
                                        "measurementUnitDescription": "N/A"
                                }), 
                                default_lang="no"
                            ),
                        })
                    ]
                })

            _mvmodel = self.validate_metadata_model(Model=InstanceVariable, metadata_json=insert_measure)         
            mvars.append(replace_enums(input_dict=_mvmodel.dict(exclude_unset=True)))

        # Attribute Variables
        attrvars = [
            temporal_attributes.generate_start_time_attribute(metadata_input.temporalityType),
            temporal_attributes.generate_stop_time_attribute(metadata_input.temporalityType),
        ] # + metadata_input.get("attributeVariables", [])

        instance_vars = {
            "identifierVariables": ivars,
            "measureVariables": mvars,
            "attributeVariables": attrvars,
        }

        return ds_units, instance_vars
  
    def convert_unit_type_to_identifier(self, utype: Dict) -> InstanceVariable:
        try:
            utmodel = UnitTypeMetadata(**utype)
            ivmodel = InstanceVariable(**{
                "name": utmodel.shortName,
                "label": utmodel.name[0].value,
                "dataType": utmodel.dataType,
                "variableRole": "Identifier",
                "keyType": KeyType(**{
                    "name": utmodel.unitType.shortName,
                    "label": utmodel.unitType.name[0].value,
                    "description": utmodel.unitType.description,
                }),
                "representedVariables": [
                    RepresentedVariable(**{
                        "description": utmodel.description,
                        "valueDomain": utmodel.valueDomain,
                    })
                ]
            })
        except pydantic.ValidationError as e:
            error_messages = [
                self._format_pydantic_error(error) for error in e.errors()
            ]
            print(f"Metadata file validation errors: {error_messages}")
            raise ValidationError("metadata file", errors=error_messages)
        except Exception as e:
            print(e)
            raise e 
        return ivmodel
    
    def convert_descriptions_to_multilingual(
        self, 
        metadata_input: VariableMetadataInput, 
        default_lang: str = "no"
    ) -> Dict[str, Any]:
        multi_dict = {}
        multilingual_fields = ["populationDescription", "spatialCoverageDescription", "subjectFields"]
        nested_list_fields = ["subjectFields"]
        # Convert string fields to Norwegian multilungual strings if needed
        for field in multilingual_fields:
            field_contents = getattr(metadata_input, field)
            if isinstance(field_contents, list):
                if field in nested_list_fields:
                    multi_dict[field] = convert_list_to_multilingual(
                        input_list=field_contents, 
                        default_lang=default_lang,
                        nested_list=True)
                else:
                    multi_dict[field] = convert_list_to_multilingual(input_list=field_contents, default_lang=default_lang)

        return multi_dict
     
    def validate_metadata_model(self, Model: ModelType, metadata_json: Dict) -> ModelType:
        try:
            model_obj = Model(**metadata_json)  
        except pydantic.ValidationError as e:
            error_messages = [
                self._format_pydantic_error(error) for error in e.errors()
            ]
            print(f"Metadata file validation errors: {error_messages}")
            raise ValidationError("metadata file", errors=error_messages)
        except Exception as e:
            print(e)
            raise e
        
        return model_obj
  
    @staticmethod
    def _format_pydantic_error(error: Dict) -> str:
        location = "->".join(
            loc for loc in error["loc"] if loc != "__root__" and not isinstance(loc, int)
        )
        return f'{location}: {error["msg"]}'   
                    

metadata_process = MetadataProcess()
