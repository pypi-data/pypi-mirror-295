from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


# @lc-entity
# @lc-identifier :Annotation
# @lc-name Annotation
# @lc-description Base class for all annotations.
@dataclass(kw_only=True)
class Annotation:
    # @lc-property
    # @lc-name name
    name: str
    # @lc-property
    # @lc-name value
    value: str | None
    # @lc-property
    # @lc-name line
    line_number: int


# @lc-entity
# @lc-identifier :SourceFileAnotations
# @lc-name SourceFileAnotations
# @lc-description Represent a single resource file.
@dataclass(kw_only=True)
class SourceFileAnnotations:
    # @lc-property
    # @lc-name relativeFilePath
    # @lc-description Relative path to the file.
    relative_file_path: str
    # @lc-property
    # @lc-name annotations
    # @lc-description Annotations found in given file.
    annotations: list[Annotation] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.annotations:
            self.annotations = deepcopy(self.annotations)

    def to_json(self) -> dict[str, Any]:
        return {
            "relativeFilePath": self.relative_file_path,
            "annotations": [annotation.__dict__ for annotation in self.annotations],
        }


# @lc-entity
# @lc-identifier :Property
# @lc-name Property
# @lc-description Represent a property of an entity.
@dataclass(kw_only=True)
class Property:
    # @lc-property
    # @lc-name name
    name: str | None
    # @lc-property
    # @lc-name value
    description: str | None


# @lc-entity
# @lc-identifier :EntityInstance
# @lc-name EntityInstance
# @lc-description Represent an instance of an entity.
@dataclass(kw_only=True)
class EntityInstance:
    # @lc-property
    # @lc-name from_file
    from_file: str
    # @lc-property
    # @lc-name identifier
    identifier: str
    # @lc-property
    # @lc-name description
    description: str | None
    # @lc-property
    # @lc-name properties
    properties: list[Property] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.properties:
            self.properties = deepcopy(self.properties)

    def to_json(self) -> dict[str, Any]:
        return {
            "from_file": self.from_file,
            "identifier": self.identifier,
            "description": self.description,
            "properties": [prop.__dict__ for prop in self.properties],
        }


# @lc-entity
# @lc-identifier :Entity
# @lc-name Entity
# @lc-description Represent an entity.
@dataclass(kw_only=True)
class Entity:
    # @lc-property
    # @lc-name name
    name: str | None
    # @lc-property
    # @lc-name instances
    instances: list[EntityInstance] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.instances:
            self.instances = deepcopy(self.instances)

    def to_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "instances": [instance.to_json() for instance in self.instances],
        }
