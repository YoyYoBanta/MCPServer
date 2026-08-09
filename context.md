# Context: Google Workspace MCP Server

## Overview
This project involves building a generic, reusable Model Context Protocol (MCP) server designed to act as a secure bridge between any AI agent and Google Workspace. By exposing standard tools, this server will empower any compliant AI agent (such as, but not limited to, a Mobile Store Feedback Orchestrator) to automate interactions with Google Docs and Gmail on behalf of the user, without being tied to specific agent implementations.

## Core Objectives

1.  **Google Docs Integration**
    *   **Tool**: `create_doc`
    *   **Functionality**: Accepts markdown or raw text, authenticates via Google Drive/Docs API, and generates a formatted Google Document.
    *   **Output**: Returns the URL of the newly created document to the AI agent.

2.  **Gmail Integration**
    *   **Tool**: `draft_email`
    *   **Functionality**: Accepts a recipient list, a subject line, and HTML/text body content, authenticates via the Gmail API, and securely places a drafted email in the user's outbox.
    *   **Constraint**: Emails must only be drafted, not automatically sent.

3.  **MCP Compliance**
    *   **Protocol**: Implements the standard Model Context Protocol (via `stdio` or `SSE`).
    *   **Goal**: Ensure any compliant AI agent can discover and invoke the provided tools.

## Technical Requirements

*   **Authentication**: Secure handling of Google OAuth 2.0. Required scopes:
    *   `https://www.googleapis.com/auth/documents`
    *   `https://www.googleapis.com/auth/drive`
    *   `https://www.googleapis.com/auth/gmail.compose`
*   **Framework Options**: 
    *   TypeScript: `@modelcontextprotocol/sdk`
    *   Python: `mcp` SDK
*   **Security Posture**: The server must act strictly as a pass-through layer. It must **never** permanently store sensitive data passed by the AI agent.

## Expected Outcomes
Upon successful deployment, any compliant AI agent can connect to this MCP server over `stdio` or `SSE` and pass arbitrary content to generate Google Docs or draft emails. For example, an Orchestrator script could pass an AI-generated Weekly Pulse JSON, and the generic server will successfully generate the Google Doc report and draft a notification email within the user's Google account, demonstrating its capability to handle varied agent workloads.
