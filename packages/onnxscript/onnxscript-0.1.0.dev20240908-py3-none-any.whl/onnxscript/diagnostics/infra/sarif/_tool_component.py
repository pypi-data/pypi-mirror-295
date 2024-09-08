# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import Any, List, Literal, Optional

from onnxscript.diagnostics.infra.sarif import (
    _artifact_location,
    _multiformat_message_string,
    _property_bag,
    _reporting_descriptor,
    _tool_component_reference,
    _translation_metadata,
)


@dataclasses.dataclass
class ToolComponent:
    """A component, such as a plug-in or the driver, of the analysis tool that was run."""

    name: str = dataclasses.field(metadata={"schema_property_name": "name"})
    associated_component: Optional[_tool_component_reference.ToolComponentReference] = (
        dataclasses.field(
            default=None, metadata={"schema_property_name": "associatedComponent"}
        )
    )
    contents: List[Literal["localizedData", "nonLocalizedData"]] = dataclasses.field(
        default_factory=lambda: ["localizedData", "nonLocalizedData"],
        metadata={"schema_property_name": "contents"},
    )
    dotted_quad_file_version: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "dottedQuadFileVersion"}
    )
    download_uri: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "downloadUri"}
    )
    full_description: Optional[_multiformat_message_string.MultiformatMessageString] = (
        dataclasses.field(default=None, metadata={"schema_property_name": "fullDescription"})
    )
    full_name: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "fullName"}
    )
    global_message_strings: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "globalMessageStrings"}
    )
    guid: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "guid"}
    )
    information_uri: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "informationUri"}
    )
    is_comprehensive: Optional[bool] = dataclasses.field(
        default=None, metadata={"schema_property_name": "isComprehensive"}
    )
    language: str = dataclasses.field(
        default="en-US", metadata={"schema_property_name": "language"}
    )
    localized_data_semantic_version: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "localizedDataSemanticVersion"}
    )
    locations: Optional[List[_artifact_location.ArtifactLocation]] = dataclasses.field(
        default=None, metadata={"schema_property_name": "locations"}
    )
    minimum_required_localized_data_semantic_version: Optional[str] = dataclasses.field(
        default=None,
        metadata={"schema_property_name": "minimumRequiredLocalizedDataSemanticVersion"},
    )
    notifications: Optional[List[_reporting_descriptor.ReportingDescriptor]] = (
        dataclasses.field(default=None, metadata={"schema_property_name": "notifications"})
    )
    organization: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "organization"}
    )
    product: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "product"}
    )
    product_suite: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "productSuite"}
    )
    properties: Optional[_property_bag.PropertyBag] = dataclasses.field(
        default=None, metadata={"schema_property_name": "properties"}
    )
    release_date_utc: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "releaseDateUtc"}
    )
    rules: Optional[List[_reporting_descriptor.ReportingDescriptor]] = dataclasses.field(
        default=None, metadata={"schema_property_name": "rules"}
    )
    semantic_version: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "semanticVersion"}
    )
    short_description: Optional[_multiformat_message_string.MultiformatMessageString] = (
        dataclasses.field(default=None, metadata={"schema_property_name": "shortDescription"})
    )
    supported_taxonomies: Optional[List[_tool_component_reference.ToolComponentReference]] = (
        dataclasses.field(
            default=None, metadata={"schema_property_name": "supportedTaxonomies"}
        )
    )
    taxa: Optional[List[_reporting_descriptor.ReportingDescriptor]] = dataclasses.field(
        default=None, metadata={"schema_property_name": "taxa"}
    )
    translation_metadata: Optional[_translation_metadata.TranslationMetadata] = (
        dataclasses.field(
            default=None, metadata={"schema_property_name": "translationMetadata"}
        )
    )
    version: Optional[str] = dataclasses.field(
        default=None, metadata={"schema_property_name": "version"}
    )


# flake8: noqa
