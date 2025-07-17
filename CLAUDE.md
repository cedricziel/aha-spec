# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OpenAPI specification for the Aha! REST API, a product management platform. The specification is structured as a modular OpenAPI 3.0.3 document with separate files for paths and schemas.

## Architecture

The OpenAPI specification is organized into several key areas:

### Main Structure
- `api/openapi.yaml` - Main OpenAPI specification file that references other components
- `api/paths/` - Directory containing path definitions organized by resource type
- `api/schemas/` - Directory containing schema definitions organized by resource type

### Resource Organization
The API covers these main resources:
- **Users** - User management and authentication
- **Features** - Core product features with extensive relationship management
- **Ideas** - Product ideas from various sources (portal users, categories, scores)
- **Initiatives** - Strategic initiatives linked to products
- **Products** - Product catalog and management
- **Epics** - Epic management and feature relationships
- **Comments** - Comments system for all major resources
- **Competitors** - Competitive analysis data

### Path Structure
Paths are organized hierarchically:
- Resource collections (e.g., `/features`, `/products`)
- Resource-specific endpoints (e.g., `/features/{id}`)
- Nested relationships (e.g., `/products/{product_id}/features`)
- Custom actions (e.g., `/features/{id}/convert_to_epic`)

### Schema Organization
Schemas are split by resource type with common patterns:
- `{Resource}CreateRequest` - Request schemas for creation
- `{Resource}` - Base resource schema
- `{Resource}Response` - Response wrapper schemas
- `{Resource}ListResponse` - List response schemas

## Common Development Tasks

Since this is a specification-only repository, there are no build, test, or lint commands. Development work involves:

1. **Modifying API paths**: Edit files in `api/paths/` directory
2. **Updating schemas**: Edit files in `api/schemas/` directory  
3. **Adding new resources**: Create new path and schema files following existing patterns
4. **Validating OpenAPI spec**: Use OpenAPI validation tools on `api/openapi.yaml`

## File Organization Patterns

- Path files use descriptive names indicating the HTTP method and resource (e.g., `create.yaml`, `list.yaml`, `get.yaml`)
- Schema files are grouped by resource type in subdirectories
- All external references use relative paths with explicit anchor references
- The main OpenAPI file serves as the central registry for all paths and schemas

## API Design Patterns

- RESTful resource design with standard HTTP methods
- Nested resource relationships for hierarchical data
- Consistent request/response schema naming
- OAuth2 and Bearer token authentication support
- Multi-tenant architecture with subdomain-based routing