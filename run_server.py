import sys
import os
import json
import tempfile
import subprocess

IS_FROZEN = getattr(sys, 'frozen', False)
from mcpo import app as mcpo_typer_app

def clone_repo_if_needed():
    """Clone the MCP git repo if it doesn't exist and return the path."""
    repo_url = "https://github.com/nsourlos/MCP_git_repo_to_single_file/"
    current_dir = os.getcwd()
    repo_dir = os.path.join(current_dir, "MCP_git_repo_to_single_file")
    
    if not os.path.exists(repo_dir):
        print(f"Cloning {repo_url} to {repo_dir}...")
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
    else:
        print(f"Repository already exists at {repo_dir}")
    
    return repo_dir

def main():
    """
    Reads the config file, constructs the command, and crucially, expands
    the PATH to ensure subprocesses can find system tools like 'git'.
    """

    # When the app is packaged, we must manually add standard system paths
    # to the environment. This allows the 'uvx' subprocess to find 'git' and 'python3'.
    # This does not check if they exist, it only provides the search paths.
    if IS_FROZEN:
        original_path = os.environ.get('PATH', '')
        # print(f"original_path: {original_path}")
        # Standard locations for macOS (Intel & Apple Silicon), Linux, and Windows.
        additional_paths = [
            '/opt/homebrew/bin', '/usr/local/bin', '/usr/bin', '/bin',
            os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'Git', 'bin')
        ]
        # print(f"additional_paths: {additional_paths}")
        os.environ['PATH'] = os.pathsep.join(additional_paths + [original_path])
        # print(f"os.environ['PATH']: {os.environ['PATH']}")

    # Clone the repository if needed
    repo_dir = clone_repo_if_needed()
    print(f"repo_dir: {repo_dir} \n")
    
    # Create the config content with the cloned repo directory
    config_content = {
        "mcpServers": {
            "git-files-server": {
                "command": "uv",
                "args": ["--directory", repo_dir, "run", "server.py"],
                "env": {}
            }
        }
    }

    # 'w+' opens for writing, 'delete=False' is crucial for subprocesses on Windows
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json", encoding="utf-8") as temp_config_file:
        # Write the JSON content to the file
        json.dump(config_content, temp_config_file)
        # Ensure data is written to disk before mcpo tries to read it
        temp_config_file.flush()
        
        # Get the path of the temporary file
        config_file_path = temp_config_file.name
        print(f"Generated temporary config file at: {config_file_path}")
        print(f"Config content: {json.dumps(config_content, indent=2)} \n")
    
    try:
        # Call mcpo_main() directly instead of subprocess
        sys.argv = ['mcpo', '--config', config_file_path]
        
        print(f"Calling mcpo_main() with sys.argv: {sys.argv} \n")
        
        # Call mcpo_main directly
        mcpo_typer_app()
        
    finally:
        print(f"Finally block \n")

if __name__ == '__main__':
    main()