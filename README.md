# Aha! REST API

API for interacting with Aha! product management platform.

**Version:** 1.0.3

## Overview

This OpenAPI specification defines the REST API for the Aha! product management platform. The API provides comprehensive access to features, ideas, releases, epics, and other product management resources.

## Base URL

```
https://{subdomain}.aha.io/api/v1
```

## Authentication

The API supports the following authentication methods:

- **OAuth2**: oauth2 authentication (OAuth 2.0)
- **BearerAuth**: http authentication (bearer scheme)

## API Statistics

| Feature | Count |
|---------|-------|
| References | 66 |
| External Documents | 0 |
| Schemas | 66 |
| Parameters | 41 |
| Links | 0 |
| Path Items | 72 |
| Webhooks | 0 |
| Operations | 113 |
| Tags | 18 |

## API Tags

### Competitors

Competitive analysis and competitor tracking

### Users

User management and authentication

### Features

Product features and functionality management

### Releases

Release planning and management

### Comments

Comments and discussions on various resources

### Epics

Epic management and feature grouping

### Requirements

Requirements and specification management

### Ideas

Idea management and innovation tracking

### Initiatives

Strategic initiatives and high-level planning

### Goals

Goal setting and OKR management

### Strategic Models

Strategic planning and modeling

### Release Phases

Release phase and milestone management

### Todos

Task and todo management

### Products

Product catalog and configuration

### Me

Current user profile and settings

### Idea Organizations

Idea organization and categorization

## Resource Overview

The API is organized around the following main resources:

- **Competitors**: Competitive analysis and competitor tracking
- **Users**: User management and authentication
- **Features**: Product features and functionality management
- **Releases**: Release planning and management
- **Comments**: Comments and discussions on various resources
- **Epics**: Epic management and feature grouping
- **Requirements**: Requirements and specification management
- **Ideas**: Idea management and innovation tracking
- **Initiatives**: Strategic initiatives and high-level planning
- **Goals**: Goal setting and OKR management
- **Strategic Models**: Strategic planning and modeling
- **Release Phases**: Release phase and milestone management
- **Todos**: Task and todo management
- **Products**: Product catalog and configuration
- **Me**: Current user profile and settings
- **Idea Organizations**: Idea organization and categorization


## Development

### Validation

```bash
make lint
```

### Generate README

```bash
make readme
```

### View API Statistics

```bash
make stats
```

### Build HTML Documentation

```bash
make build-docs
```

## File Structure

```
api/
├── openapi.yaml          # Main OpenAPI specification
├── paths/               # API path definitions
│   ├── comments.yaml
│   ├── competitors.yaml
│   ├── features/
│   ├── ideas/
│   ├── releases/
│   └── ...
└── schemas/             # Data model schemas
    ├── comments.yaml
    ├── competitors.yaml
    ├── features/
    ├── ideas/
    ├── releases/
    └── ...
```

## Key Features

- **Comprehensive API Coverage**: {stats.get('operations', {}).get('total', 99)} operations across {stats.get('tags', {}).get('total', 18)} resource categories
- **Modular Design**: Separate files for paths and schemas for better organization
- **Flexible Authentication**: Supports both OAuth 2.0 and Bearer token authentication
- **Consistent Error Handling**: Standardized 4XX error responses across all operations
- **Rich Documentation**: Detailed descriptions, examples, and parameter documentation

## Documentation

- **OpenAPI Specification**: `api/openapi.yaml`
- **Interactive Documentation**: Available via `make build-docs`
- **Live Documentation**: [GitHub Pages](https://cedricziel.github.io/aha-spec/)
- **API Statistics**: Available via `make stats`

---

*This README was automatically generated from the OpenAPI specification using Redocly CLI stats.*
