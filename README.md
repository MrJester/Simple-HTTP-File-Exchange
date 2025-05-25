# file_browser

Simple HTTP file browser and uploader. Mostly used for easily exchanging files during engagements.

## Features

*   Serves files from a specified directory.
*   Allows file uploads to the specified directory.
*   Configurable port and upload folder via command-line arguments.
*   Supports SSL/TLS encryption (HTTPS) if certificates are provided.
*   Path validation for the upload folder to ensure it's an absolute path and exists.
*   Refined SSL context for improved security.

## Configuration

### Environment Variables

*   **`FLASK_SECRET_KEY`**: This environment variable is used to set the Flask `secret_key`. The secret key is crucial for session security (e.g., for flash messages). It is highly recommended to set this to a strong, unique random string in a production environment to prevent session hijacking. If not set, a default, less secure key will be used with a warning.

## Installation and Usage

1.  Clone the repository or download `filebrowser.py`.
2.  (Optional) Install dependencies if any are added in the future (currently uses standard Python libraries and Flask).
3.  Run the script:
    ```bash
    python filebrowser.py -f /path/to/your/folder -p 8080
    ```
    *   Use `-f` or `--folder` to specify the directory to serve.
    *   Use `-p` or `--port` to specify the port.
    *   Use `--ssl` to enable SSL, and `--fullchain` / `--privkey` to specify certificate paths.

    Example with SSL:
    ```bash
    python filebrowser.py -f /srv/uploads --ssl --fullchain /etc/letsencrypt/live/yourdomain.com/fullchain.pem --privkey /etc/letsencrypt/live/yourdomain.com/privkey.pem
    ```
4.  Access the file browser via `http://localhost:PORT` or `https://localhost:PORT` if SSL is enabled.

### Setting `FLASK_SECRET_KEY`

**Linux/macOS (bash):**
```bash
export FLASK_SECRET_KEY='your_very_strong_random_secret_key_here'
python filebrowser.py
```

**Windows (Command Prompt):**
```cmd
set FLASK_SECRET_KEY=your_very_strong_random_secret_key_here
python filebrowser.py
```

**Windows (PowerShell):**
```powershell
$env:FLASK_SECRET_KEY="your_very_strong_random_secret_key_here"
python filebrowser.py
```
It's best to set this in your shell's profile (e.g., `.bashrc`, `.zshrc`) or your deployment environment's configuration.

# TODO

1.) <s>Add Arguments</s>

2.) <s>Change port with switch</s>

3.) Authentication
