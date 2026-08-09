# Deployment Plan: Railway Hosting

This document outlines the steps required to modify, prepare, and deploy the Google Workspace MCP Server to [Railway](https://railway.app/).

## User Review Required

> [!IMPORTANT]
> **Transport Layer Migration (CRITICAL)**: Our server currently uses `stdio` to communicate with AI agents locally. To host it remotely on Railway, we **must** switch the transport layer to Server-Sent Events (SSE) over HTTP using a web framework (like Starlette or FastAPI). Do you approve of migrating the codebase to use SSE?
> 
> **Token Storage Strategy**: Railway uses ephemeral storage by default. If we write `token.json` to the disk, it will be lost every time the server restarts or deploys, forcing you to re-authenticate constantly. We need to store the token in a Railway Persistent Volume, or switch to a database. The easiest approach is to mount a Railway Volume to store `token.json`. Does this approach work for you?
>
> **Authentication Flow**: Because Railway is a headless remote server, the Google OAuth "popup" window cannot run there. You will need to generate the `token.json` locally on your machine (which you just did!) and then upload that token to your Railway volume, or pass it via an environment variable. 

## Phase 1: Codebase Migration to SSE

To make the server accessible over the internet:
- [ ] **Dependencies**: Add `starlette` and `uvicorn` to `requirements.txt`.
- [ ] **SSE Implementation**: Update `src/main.py` to use `mcp.server.sse.sse_server`. We will expose a `/sse` endpoint for the connection and a `/messages` endpoint for the POST requests.
- [ ] **Dynamic Port Binding**: Bind the `uvicorn` server to the `PORT` environment variable (which Railway injects automatically).

## Phase 2: Railway Environment Setup

To ensure the server runs correctly in Railway's cloud environment:
- [ ] **Procfile / Start Command**: Railway uses Nixpacks to auto-detect Python, but we will define a clear start command (e.g., via a `Procfile`): `uvicorn src.main:app --host 0.0.0.0 --port $PORT`.
- [ ] **Configuration Updates**: Adjust the code so that if a persistent volume is mounted (e.g., at `/data`), the application reads/writes `token.json` from there.

## Phase 3: Comprehensive Documentation (README.md)

Deploying this requires specific manual steps in the Railway dashboard. The documentation must clearly explain:
1. How to create the Railway project linked to your GitHub repo.
2. How to securely set environment variables in Railway instead of relying on local files.
3. How to attach a Railway Volume for token persistence.
4. How to upload your locally generated `token.json` and `credentials.json` into the Railway volume (or inject them as base64-encoded environment variables).

## Phase 4: GitHub Push & Deployment Execution

- [ ] **Initialize Git**: Initialize a Git repository, commit the SSE-enabled codebase.
- [ ] **Push to Remote**: Push to a GitHub repository (Railway deploys directly from GitHub).
- [ ] **Deploy**: Follow the README instructions to connect Railway to the repository and trigger the build.

---

### Next Steps
If you approve this plan, I will immediately begin Phase 1: refactoring `src/main.py` to use an HTTP/SSE server instead of `stdio`!
