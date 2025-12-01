"""
Data Models and Semantics - Main Demonstration

This script demonstrates data model definition, validation, and usage
with a simple twin model including assets, properties, and relationships.

Usage:
    python main_04_data_models_and_semantics.py

Example:
    python main_04_data_models_and_semantics.py
"""

import sys
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


class PropertyType(Enum):
    """Supported property types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"


@dataclass
class PropertyDefinition:
    """Definition of a property in the model."""
    name: str
    property_type: PropertyType
    unit: Optional[str] = None
    description: str = ""
    required: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    def validate(self, value: Any) -> tuple[bool, str]:
        """Validate a value against this property definition."""
        if value is None:
            if self.required:
                return False, f"Property '{self.name}' is required"
            return True, ""
        
        type_map = {
            PropertyType.STRING: str,
            PropertyType.INTEGER: int,
            PropertyType.FLOAT: (int, float),
            PropertyType.BOOLEAN: bool,
            PropertyType.DATETIME: datetime,
        }
        
        expected_type = type_map[self.property_type]
        if not isinstance(value, expected_type):
            return False, f"Property '{self.name}' must be {self.property_type.value}"
        
        if self.property_type in (PropertyType.INTEGER, PropertyType.FLOAT):
            if self.min_value is not None and value < self.min_value:
                return False, f"Property '{self.name}' must be >= {self.min_value}"
            if self.max_value is not None and value > self.max_value:
                return False, f"Property '{self.name}' must be <= {self.max_value}"
        
        return True, ""


@dataclass
class RelationshipDefinition:
    """Definition of a relationship in the model."""
    name: str
    target_type: str
    description: str = ""
    min_count: int = 0
    max_count: Optional[int] = None


@dataclass
class EntityType:
    """Definition of an entity type in the model."""
    type_id: str
    display_name: str
    description: str = ""
    properties: List[PropertyDefinition] = field(default_factory=list)
    relationships: List[RelationshipDefinition] = field(default_factory=list)
    
    def add_property(self, prop: PropertyDefinition) -> None:
        self.properties.append(prop)
    
    def add_relationship(self, rel: RelationshipDefinition) -> None:
        self.relationships.append(rel)
    
    def validate_instance(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate data against this entity type."""
        errors = []
        
        for prop in self.properties:
            value = data.get(prop.name)
            valid, error = prop.validate(value)
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors


@dataclass
class TwinModel:
    """Complete twin data model."""
    model_id: str
    version: str
    description: str = ""
    entity_types: Dict[str, EntityType] = field(default_factory=dict)
    
    def add_entity_type(self, entity_type: EntityType) -> None:
        self.entity_types[entity_type.type_id] = entity_type
    
    def get_entity_type(self, type_id: str) -> Optional[EntityType]:
        return self.entity_types.get(type_id)
    
    def validate_instance(self, type_id: str, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        entity_type = self.get_entity_type(type_id)
        if not entity_type:
            return False, [f"Unknown entity type: {type_id}"]
        return entity_type.validate_instance(data)


@dataclass
class TwinInstance:
    """Instance of a twin based on a model."""
    instance_id: str
    type_id: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    
    def set_property(self, name: str, value: Any) -> None:
        self.properties[name] = value
    
    def add_relationship(self, rel_name: str, target_id: str) -> None:
        if rel_name not in self.relationships:
            self.relationships[rel_name] = []
        self.relationships[rel_name].append(target_id)


class TwinGraph:
    """Graph of twin instances with relationships."""
    
    def __init__(self, model: TwinModel):
        self.model = model
        self.instances: Dict[str, TwinInstance] = {}
    
    def create_instance(self, instance_id: str, type_id: str, 
                       properties: Dict[str, Any]) -> tuple[Optional[TwinInstance], List[str]]:
        """Create a new twin instance."""
        valid, errors = self.model.validate_instance(type_id, properties)
        if not valid:
            return None, errors
        
        instance = TwinInstance(
            instance_id=instance_id,
            type_id=type_id,
            properties=properties
        )
        self.instances[instance_id] = instance
        return instance, []
    
    def add_relationship(self, source_id: str, rel_name: str, target_id: str) -> bool:
        """Add a relationship between instances."""
        if source_id not in self.instances or target_id not in self.instances:
            return False
        
        self.instances[source_id].add_relationship(rel_name, target_id)
        return True
    
    def query_by_type(self, type_id: str) -> List[TwinInstance]:
        """Query instances by type."""
        return [i for i in self.instances.values() if i.type_id == type_id]
    
    def query_related(self, instance_id: str, rel_name: str) -> List[TwinInstance]:
        """Query related instances."""
        instance = self.instances.get(instance_id)
        if not instance:
            return []
        
        related_ids = instance.relationships.get(rel_name, [])
        return [self.instances[rid] for rid in related_ids if rid in self.instances]


def create_manufacturing_model() -> TwinModel:
    """Create a sample manufacturing data model."""
    
    model = TwinModel(
        model_id="manufacturing-model",
        version="1.0.0",
        description="Data model for manufacturing digital twins"
    )
    
    machine_type = EntityType(
        type_id="Machine",
        display_name="Machine",
        description="A manufacturing machine"
    )
    machine_type.add_property(PropertyDefinition(
        name="name", property_type=PropertyType.STRING, required=True
    ))
    machine_type.add_property(PropertyDefinition(
        name="status", property_type=PropertyType.STRING, required=True
    ))
    machine_type.add_property(PropertyDefinition(
        name="temperature", property_type=PropertyType.FLOAT, unit="celsius",
        min_value=-50, max_value=200
    ))
    machine_type.add_property(PropertyDefinition(
        name="speed", property_type=PropertyType.FLOAT, unit="rpm",
        min_value=0, max_value=10000
    ))
    machine_type.add_relationship(RelationshipDefinition(
        name="locatedIn", target_type="Zone"
    ))
    machine_type.add_relationship(RelationshipDefinition(
        name="feedsTo", target_type="Machine"
    ))
    model.add_entity_type(machine_type)
    
    zone_type = EntityType(
        type_id="Zone",
        display_name="Production Zone",
        description="A zone in the factory"
    )
    zone_type.add_property(PropertyDefinition(
        name="name", property_type=PropertyType.STRING, required=True
    ))
    zone_type.add_property(PropertyDefinition(
        name="area", property_type=PropertyType.FLOAT, unit="sqm"
    ))
    zone_type.add_relationship(RelationshipDefinition(
        name="contains", target_type="Machine"
    ))
    model.add_entity_type(zone_type)
    
    sensor_type = EntityType(
        type_id="Sensor",
        display_name="Sensor",
        description="A sensor attached to equipment"
    )
    sensor_type.add_property(PropertyDefinition(
        name="sensorId", property_type=PropertyType.STRING, required=True
    ))
    sensor_type.add_property(PropertyDefinition(
        name="sensorType", property_type=PropertyType.STRING, required=True
    ))
    sensor_type.add_property(PropertyDefinition(
        name="value", property_type=PropertyType.FLOAT
    ))
    sensor_type.add_relationship(RelationshipDefinition(
        name="attachedTo", target_type="Machine"
    ))
    model.add_entity_type(sensor_type)
    
    return model


def run_demonstration() -> None:
    """Run the data models demonstration."""
    
    print_section("Data Models and Semantics Demo")
    print("This demo shows how data models define structure and meaning.\n")
    
    model = create_manufacturing_model()
    
    print("Created Data Model:")
    print(f"  Model ID: {model.model_id}")
    print(f"  Version: {model.version}")
    print(f"  Entity Types: {list(model.entity_types.keys())}")
    
    print_section("Entity Type Definitions")
    
    for type_id, entity_type in model.entity_types.items():
        print(f"\n{entity_type.display_name} ({type_id}):")
        print(f"  Description: {entity_type.description}")
        print("  Properties:")
        for prop in entity_type.properties:
            req = " (required)" if prop.required else ""
            unit = f" [{prop.unit}]" if prop.unit else ""
            print(f"    - {prop.name}: {prop.property_type.value}{unit}{req}")
        print("  Relationships:")
        for rel in entity_type.relationships:
            print(f"    - {rel.name} -> {rel.target_type}")
    
    print_section("Creating Twin Instances")
    
    graph = TwinGraph(model)
    
    zone, errors = graph.create_instance("zone-1", "Zone", {
        "name": "Assembly Area",
        "area": 500.0
    })
    print(f"Created Zone: {zone.instance_id}" if zone else f"Error: {errors}")
    
    machine1, errors = graph.create_instance("machine-1", "Machine", {
        "name": "CNC Mill 1",
        "status": "running",
        "temperature": 45.0,
        "speed": 3000.0
    })
    print(f"Created Machine: {machine1.instance_id}" if machine1 else f"Error: {errors}")
    
    machine2, errors = graph.create_instance("machine-2", "Machine", {
        "name": "Assembly Robot",
        "status": "idle",
        "temperature": 30.0
    })
    print(f"Created Machine: {machine2.instance_id}" if machine2 else f"Error: {errors}")
    
    sensor, errors = graph.create_instance("sensor-1", "Sensor", {
        "sensorId": "TEMP-001",
        "sensorType": "temperature",
        "value": 45.0
    })
    print(f"Created Sensor: {sensor.instance_id}" if sensor else f"Error: {errors}")
    
    print_section("Validation Examples")
    
    print("\nValid data:")
    valid, errors = model.validate_instance("Machine", {
        "name": "Test Machine",
        "status": "running",
        "temperature": 50.0
    })
    print(f"  Result: {'Valid' if valid else 'Invalid'}")
    
    print("\nInvalid data (missing required field):")
    valid, errors = model.validate_instance("Machine", {
        "temperature": 50.0
    })
    print(f"  Result: {'Valid' if valid else 'Invalid'}")
    print(f"  Errors: {errors}")
    
    print("\nInvalid data (out of range):")
    valid, errors = model.validate_instance("Machine", {
        "name": "Test",
        "status": "running",
        "temperature": 500.0
    })
    print(f"  Result: {'Valid' if valid else 'Invalid'}")
    print(f"  Errors: {errors}")
    
    print_section("Creating Relationships")
    
    graph.add_relationship("machine-1", "locatedIn", "zone-1")
    graph.add_relationship("machine-2", "locatedIn", "zone-1")
    graph.add_relationship("machine-1", "feedsTo", "machine-2")
    graph.add_relationship("sensor-1", "attachedTo", "machine-1")
    graph.add_relationship("zone-1", "contains", "machine-1")
    graph.add_relationship("zone-1", "contains", "machine-2")
    
    print("Relationships created:")
    print("  machine-1 locatedIn zone-1")
    print("  machine-2 locatedIn zone-1")
    print("  machine-1 feedsTo machine-2")
    print("  sensor-1 attachedTo machine-1")
    
    print_section("Querying the Twin Graph")
    
    machines = graph.query_by_type("Machine")
    print(f"\nAll Machines ({len(machines)}):")
    for m in machines:
        print(f"  - {m.properties['name']} ({m.instance_id})")
    
    zone_machines = graph.query_related("zone-1", "contains")
    print(f"\nMachines in Zone-1 ({len(zone_machines)}):")
    for m in zone_machines:
        print(f"  - {m.properties['name']}")
    
    downstream = graph.query_related("machine-1", "feedsTo")
    print(f"\nDownstream from Machine-1:")
    for m in downstream:
        print(f"  - {m.properties['name']}")
    
    print_section("Key Takeaways")
    print("""
1. Data models define the structure of twin data (entities, properties)
2. Semantics provide meaning (units, descriptions, constraints)
3. Validation ensures data quality and consistency
4. Relationships connect entities into a knowledge graph
5. Queries enable discovery and navigation of twin data
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
