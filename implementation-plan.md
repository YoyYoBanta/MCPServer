# Implementation Plan: Google Workspace MCP Server

This document outlines the technical implementation plan for building a generic, reusable Model Context Protocol (MCP) server that acts as a secure bridge between AI agents and Google Workspace, as defined in `context.md`.

## User Review Required

> [!IMPORTANT]
> **Technology Stack Selection**: We need to decide between TypeScript (using `@modelcontextprotocol/sdk`) and Python (using the `mcp` SDK). TypeScript is very common for MCP servers and has excellent support for Google APIs via `googleapis`. Which language do you prefer for this project?
> 
> **Authentication Flow**: Google OAuth 2.0 requires setting up a Google Cloud Console project, configuring an OAuth consent screen, and generating desktop/web credentials. Do you already have a GCP project and `credentials.json` ready, or will that need to be part of the initial setup?

## Open Questions

> [!WARNING]
> 1. **Token Storage**: How should we manage user authentication tokens locally across restarts? Using a local `.token.json` file is standard for local tools, but we must ensure it's securely excluded from version control.
> 2. **Transport Layer**: Do you prefer `stdio` or `SSE` for the MCP transport layer? `stdio` is simplest for local execution (agent runs the server as a subprocess), while `SSE` is better if the server runs independently as a background service.

## Proposed Changes

---

### Project Setup and Configuration

This phase involves initializing the project, setting up the development environment, and configuring dependencies. (Assuming TypeScript for now, pending your feedback).

#### [NEW] [package.json](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/package.json)
Initialize the Node.js project and add necessary dependencies:
- `@modelcontextprotocol/sdk`
- `googleapis`
- `dotenv`
- Typescript build tools (`typescript`, `@types/node`, `tsup`).

#### [NEW] [.env.example](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/.env.example)
Template for environment variables:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`

#### [NEW] [tsconfig.json](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/tsconfig.json)
TypeScript configuration for building the project.

---

### Authentication Module

#### [NEW] [src/auth.ts](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/src/auth.ts)
Handles the Google OAuth 2.0 flow. 
- Implements functions to generate the auth URL, exchange the authorization code for access/refresh tokens, and automatically refresh expired tokens.
- Defines required scopes: 
  - `https://www.googleapis.com/auth/documents`
  - `https://www.googleapis.com/auth/drive`
  - `https://www.googleapis.com/auth/gmail.compose`
- Handles reading/writing the local token cache (e.g., `.token.json`).

---

### Google Workspace Services

#### [NEW] [src/services/docs.ts](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/src/services/docs.ts)
Service layer for interacting with Google Drive and Docs.
- Implements `createDocument(title: string, content: string)`: Creates a new document via Drive API and appends content using Docs API.

#### [NEW] [src/services/gmail.ts](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/src/services/gmail.ts)
Service layer for interacting with Gmail.
- Implements `draftEmail(to: string[], subject: string, body: string)`: Constructs a raw MIME message and calls `gmail.users.drafts.create`.

---

### MCP Server Implementation

#### [NEW] [src/index.ts](file:///c:/Users/Manu%20S%20Nair/OneDrive/mcpserver/src/index.ts)
Main entry point for the MCP server.
- Initializes the MCP server instance.
- Registers the `create_doc` tool, defining its input schema (markdown/text content) and wiring it to `src/services/docs.ts`.
- Registers the `draft_email` tool, defining its input schema (recipients, subject, body) and wiring it to `src/services/gmail.ts`.
- Starts the server using the chosen transport (defaulting to `stdio`).

## Verification Plan

### Automated Tests
- Basic unit tests for the authentication utility (mocking Google API responses) and the tool schema definitions.

### Manual Verification
- Run the compiled server locally.
- Use the MCP Inspector (`npx @modelcontextprotocol/inspector`) to connect to the server via `stdio`.
- **Test 1**: Invoke `create_doc` with sample markdown and verify the document appears in the authenticated user's Google Drive.
- **Test 2**: Invoke `draft_email` with sample details and verify the draft appears in the authenticated user's Gmail Outbox.
