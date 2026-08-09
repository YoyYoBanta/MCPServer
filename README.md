# Google Workspace MCP Server

This repository contains a Model Context Protocol (MCP) server that integrates with Google Workspace to automatically create Google Docs and draft emails in Gmail.

The server is built using Python, Starlette, and Server-Sent Events (SSE) to allow AI agents (such as custom Orchestrators or Claude Desktop) to connect remotely and execute tools securely.

## Prerequisites

- Python 3.10+
- A Google Cloud Platform (GCP) project with the following APIs enabled:
  - Google Docs API
  - Google Drive API
  - Gmail API
- An OAuth 2.0 Client ID (Desktop App) from the GCP Console, saved as `credentials.json`.

## Quick Start (Local Setup)

1. Clone this repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your settings.
4. Place your downloaded `credentials.json` in the root folder.
5. Generate the `token.json` locally by running:
   ```bash
   python generate_token.py
   ```
   *Follow the link provided in the console to log in to Google and authorize the application.*
6. Run the server locally:
   ```bash
   python src/main.py
   ```
   The server will start on `http://0.0.0.0:8000`. Your SSE endpoint will be available at `http://localhost:8000/sse`.

## Deploying to Railway

This server is configured to run effortlessly on [Railway](https://railway.app). 

Because Railway containers are ephemeral (their file systems reset on every deployment), you must securely provide your `token.json` so the server remains authenticated with Google.

### Deployment Steps:

1. **Push to GitHub**: Push this repository to your GitHub account.
2. **Create Railway Project**: Log into Railway, click "New Project", and deploy from your GitHub repo.
3. **Environment Variables**: Add the variables from your `.env` file into the Railway dashboard.
4. **Persistent Volume (Important)**:
   - Go to your Railway service settings.
   - Attach a new **Volume** to the service.
   - Mount the volume at a path like `/data`.
   - Update your Railway environment variable `TOKEN_PATH` to `/data/token.json`.
5. **Upload the Token**:
   - Railway doesn't easily allow direct file uploads to volumes. Instead, you can encode your `token.json` as a base64 string, store it in an environment variable, and update your startup command in Railway to decode it into the volume before starting the server.
   - Alternatively, you can use a database for token storage in the future.

## Tools Provided

- `create_doc(title: string, content: string)`: Creates a Google Doc and inserts the given markdown/text.
- `draft_email(to: string[], subject: string, body: string)`: Drafts an email securely in the authenticated user's outbox.
