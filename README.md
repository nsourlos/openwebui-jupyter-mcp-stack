# OpenWebUI Custom Setup

A Docker-based environment that integrates OpenWebUI with Jupyter Notebook and MCP (Model Context Protocol) server for enhanced AI-powered code execution and visualization capabilities. It allows someone without programming experience to generate animations similar to those of 3Blue1Brown.

## Overview

This project provides a complete containerized solution that combines:
- **OpenWebUI**: Web interface for AI interactions
- **Jupyter Notebook**: Code execution environment with Manim support for mathematical visualizations
- **MCP Server**: Model Context Protocol server for git repository file operations

## Features

- 🐳 **Docker Compose Setup**: Easy deployment with single command
- 📊 **Jupyter Integration**: Code execution with mathematical visualization support (Manim)
- 🔧 **MCP Server**: Git repository file operations via Model Context Protocol
- 🎯 **Multiple Model Support**: Compatible with Google Gemini, OpenAI, and local Ollama models
- 📦 **Standalone Executables**: Create portable executables for easy distribution

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git installed (for MCP functionality)

### Creating Standalone Executables

#### Optional - For Docker automation (needs pyinstaller installed):
```bash
pyinstaller --onefile --add-data "./*:." docker-wrap.py
```

### Installation

1. **Using Docker Compose** (Recommended):
   ```bash
   docker compose down
   docker compose build
   docker compose up -d
   ```

2. **Using the Standalone Executable**:
   - Run the `docker-wrap.exe` (from dist folder) while Docker Desktop is running
   - This will automatically execute the Docker Compose commands

### Access Points

After deployment, access the services at:

- **OpenWebUI**: http://localhost:3000
- **Jupyter Notebook**: http://localhost:8888 (Token: `123456`)
- **MCP Server**: http://localhost:8000

## Configuration

### OpenWebUI Setup

1. **Enable MCP External Tool**:
   - URL: `http://host.docker.internal:8000/git-files-server`
   - Set 'Function Calling' to 'Native' in Advanced Parameters

2. **Configure Code Execution**:
   - Jupyter URL: `http://host.docker.internal:8888`
   - Token: `123456`
   - [Documentation](https://docs.openwebui.com/tutorials/jupyter/)

### Model Endpoints

Configure your AI models with these URLs:

| Provider | URL |
|----------|-----|
| Google Gemini | `https://generativelanguage.googleapis.com/v1beta/openai` |
| OpenAI | `https://api.openai.com/v1` |
| Ollama (Local - needs to be installed) | `http://host.docker.internal:11434` |

## Services Architecture

### 🌐 OpenWebUI Service
- **Image**: `ghcr.io/open-webui/open-webui:latest`
- **Port**: 3000 → 8080
- **Purpose**: Main web interface for AI interactions

### 📓 Jupyter Service
- **Base**: `jupyter/minimal-notebook:latest`
- **Port**: 8888
- **Features**: 
  - Manim support for mathematical visualizations
  - Pre-installed packages: pandas, manim, manimlib, manimgl
  - System dependencies for Cairo and Pango rendering

### 🔧 MCP Server Service
- **Base**: `python:3.11-slim`
- **Port**: 8000
- **Purpose**: Git repository file operations via Model Context Protocol

## Example Usage

### Creating Visualizations with Manim

Use this prompt with Gemini 2.5 Pro (tested):

```
Using the available MCP tools, create a visualization of a red ball falling on a table. When it touches the table it turns green and the forces that act upon it are shown (weight and vertical force N of the table). Do not use any latex or additional packages/libraries. The code should be able to be executed as is. Return it in a python cell. Use explicit imports for every Manim class. The manim command needed to create the visualization should included in the python script (as if it was executed from the terminal). The python file needs to save itself first prior to calling the terminal resembling command. When executed the visualization should be saved directly. Also print the location when the file is saved after the manim command is executed. Use the code from https://github.com/3b1b/manim
```

Execute the generated code ('run code') and if errors, copy-paste these errors back to the model. At the end, when the final animation is created, it can be found inside the `jupyter_files` folder
## Development

### File Structure

```
openwebui-jupyter-mcp-stack/
├── docker-compose.yml      # Main orchestration file
├── Dockerfile.jupyter      # Jupyter container configuration
├── Dockerfile.mcp         # MCP server container configuration
├── run_server.py          # MCP server implementation
├── docker-wrap.py         # Docker automation script
├── docker-wrap.spec       # PyInstaller specification file
├── dist/                  # Distribution folder
│   └── docker-wrap.exe    # Standalone executable for Windows
├── LICENSE               # Project license file
└── README.md             # This file
```


## Data Persistence

The setup includes persistent volumes to maintain data across container restarts:
- **OpenWebUI data**: Stored in `open-webui` volume
- **Jupyter files**: Mapped to `./jupyter_files` directory

**Important**: When deleting containers, preserve the volumes in Docker Desktop to keep your settings and data.

## Troubleshooting

1. **Port Conflicts**: Ensure ports 3000, 8888, and 8000 are available
2. **Docker Issues**: Make sure Docker Desktop is running before executing commands
3. **MCP Connection**: Verify the MCP server URL in OpenWebUI settings
4. **Jupyter Access**: Use token `123456` if prompted for authentication

## Contributing

Feel free to submit issues and enhancement requests. When contributing:
1. Test changes with Docker Compose
2. Update documentation as needed
3. Ensure all services remain functional

## License

This project configuration is provided as-is for educational and development purposes.
