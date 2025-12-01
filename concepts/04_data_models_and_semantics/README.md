# 04 - Data Models and Semantics

> Data models and semantics define what information means in your digital twin system—ensuring everyone and every system speaks the same language.

## What?

### Non-Technical Explanation

Imagine trying to communicate with someone who speaks a different language. Even if you both see the same thing, you might describe it differently. Data models are like a shared dictionary that ensures everyone describes things the same way.

When a sensor says "temperature is 25," the data model tells us: Is that Celsius or Fahrenheit? Is it the air temperature or the machine temperature? When was it measured? A good data model answers all these questions so there's no confusion.

### Technical Definition

**Data Models and Semantics** in digital twins refers to the formal structures that define:

- **Schema**: The structure of data (fields, types, relationships)
- **Ontology**: The concepts and categories in the domain
- **Semantics**: The meaning and interpretation of data
- **Relationships**: How different data elements connect
- **Constraints**: Rules that data must follow

Common standards include DTDL (Digital Twins Definition Language), OWL (Web Ontology Language), and industry-specific models like CFIHOS for oil & gas or Brick for buildings.

## Why?

Data models and semantics are critical for several reasons:

**Interoperability**: Different systems can exchange data because they share common definitions. A sensor from vendor A can feed data to a platform from vendor B.

**Consistency**: Everyone interprets data the same way. "Temperature" always means the same thing across the organization.

**Validation**: Data can be automatically checked against the model. Invalid data is caught before it corrupts the twin.

**Discovery**: Users can find and understand data without reading documentation. The model itself describes what's available.

**Evolution**: Models can be versioned and extended as needs change, while maintaining backward compatibility.

**Scenario Examples**:
- A building uses the Brick schema so that any analytics application can understand its HVAC data structure
- A manufacturer defines a product model that tracks components through assembly, testing, and shipping
- An energy company uses CIM (Common Information Model) so grid data can be shared across utilities

## Where?

### Industries

**Manufacturing**: Product models, process models, equipment models (ISA-95, OPC-UA)
**Buildings**: Space models, equipment models (Brick, Haystack, RealEstateCore)
**Energy**: Grid models, asset models (CIM, IEC 61850)
**Healthcare**: Patient models, device models (HL7 FHIR)
**Smart Cities**: Infrastructure models, service models (FIWARE, NGSI-LD)

### Systems

- Digital twin platforms (Azure Digital Twins, AWS IoT TwinMaker)
- Building management systems
- Manufacturing execution systems
- Enterprise asset management
- Data lakes and warehouses

### Platforms

- **Azure Digital Twins**: Uses DTDL (Digital Twins Definition Language)
- **AWS IoT TwinMaker**: Uses component types and entity definitions
- **Open Standards**: RDF, OWL, JSON-LD for semantic web
- **Industry Standards**: Brick, Haystack, CIM, ISA-95

## Who?

### Roles That Work with Data Models

**Data Architects**: Design overall data model structure and governance
**Domain Experts**: Define business concepts and relationships
**Data Engineers**: Implement models in databases and pipelines
**Integration Specialists**: Map between different models and systems
**Analysts**: Use models to query and understand data

### Non-IT vs IT Perspectives

**Non-IT Professionals** care about:
- Does the model capture our business concepts correctly?
- Can I find the data I need?
- Do reports show the right information?
- Can we add new types of equipment or processes?

**IT Professionals** care about:
- What schema format should we use?
- How do we version and migrate models?
- How do we validate incoming data?
- How do we map between different standards?

## How?

### High-Level Process

1. **Domain Analysis**: Understand the business domain and concepts
2. **Model Design**: Define entities, properties, and relationships
3. **Standard Selection**: Choose appropriate standards and formats
4. **Implementation**: Create schemas in the chosen format
5. **Validation Rules**: Define constraints and validation logic
6. **Documentation**: Document the model for users
7. **Governance**: Establish processes for model changes

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA MODEL LAYER                                │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    ONTOLOGY / SCHEMA                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │    │
│  │  │  Asset   │  │ Process  │  │  Space   │  │  Event   │    │    │
│  │  │  Types   │  │  Types   │  │  Types   │  │  Types   │    │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │    │
│  │       │             │             │             │           │    │
│  │       └─────────────┴──────┬──────┴─────────────┘           │    │
│  │                            │                                 │    │
│  │                    ┌───────▼───────┐                        │    │
│  │                    │ Relationships │                        │    │
│  │                    └───────────────┘                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│  │   Validation    │  │    Mapping      │  │   Versioning    │      │
│  │     Rules       │  │    Functions    │  │    Control      │      │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA INSTANCES                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │ Pump-01 │  │ Line-A  │  │ Room-1  │  │ Alert-X │                │
│  │ (Asset) │  │(Process)│  │ (Space) │  │ (Event) │                │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘                │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Terms

| Term | Definition |
|------|------------|
| **Schema** | Formal definition of data structure (fields, types) |
| **Ontology** | Formal representation of concepts and relationships in a domain |
| **Semantics** | The meaning of data elements |
| **DTDL** | Digital Twins Definition Language (Microsoft) |
| **RDF** | Resource Description Framework for semantic data |
| **Property** | An attribute of an entity (e.g., temperature, status) |
| **Relationship** | A connection between entities (e.g., "contains", "feeds") |
| **Telemetry** | Time-series data from sensors |
| **Component** | A reusable part of a model |

## Relations to Other Concepts

- **01 - Digital Twin Fundamentals**: Data models define twin structure
- **03 - IoT and Sensor Data**: Sensor data must conform to model schemas
- **05 - Simulation Models**: Physics models use data model properties
- **08 - AI and Analytics**: ML models depend on consistent data semantics
- **12 - Governance**: Data models are key governance artifacts

## Programs in This Folder

### main_04_data_models_and_semantics.py

**Description**: Demonstrates data model definition, validation, and usage with a simple twin model including assets, properties, and relationships.

**Command**:
```bash
python code/main_04_data_models_and_semantics.py
```

**Expected Output**:
- Definition of a twin data model
- Creation of model instances
- Validation of data against the model
- Querying relationships between entities

### Notebooks

| Notebook | Description |
|----------|-------------|
| `intro_04_data_models_and_semantics.ipynb` | Introduction to data modeling concepts |
| `examples_04_data_models_and_semantics.ipynb` | Practical examples of model definition |
| `exercises_04_data_models_and_semantics.ipynb` | Hands-on exercises for building models |

### HTML Demo

Open `html_demo/index.html` in a browser to see an animated visualization of data models, showing how schemas define structure and semantics provide meaning.
