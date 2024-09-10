import http.server
import os
import socketserver
import subprocess
import threading

import typer

app = typer.Typer()


# Command to create a Tailwind project
@app.command()
def create(app_name: str):
    """Create a Tailwind CSS project with public directories for images and fonts."""

    # Define project directories
    src_path = os.path.join(app_name, "src")
    dist_path = os.path.join(app_name, "dist")
    public_images_path = os.path.join(app_name, "public", "images")
    public_fonts_path = os.path.join(app_name, "public", "fonts")

    # Create directories
    os.makedirs(src_path, exist_ok=True)
    os.makedirs(dist_path, exist_ok=True)
    os.makedirs(public_images_path, exist_ok=True)
    os.makedirs(public_fonts_path, exist_ok=True)

    # Create index.html in src with link to output.css
    with open(f"{app_name}/src/index.html", "w") as f:
        f.write(
            """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tailwind App</title>
  <link href="../dist/output.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
  <h1 class="text-3xl font-bold underline text-center mt-10">Hello, Tailwind CSS!</h1>
</body>
</html>
        """
        )

    # Create Tailwind config file in the root
    with open(f"{app_name}/tailwind.config.js", "w") as f:
        f.write(
            f"""
/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: ['./src/**/*{{html,js}}'],
  theme: {{
    extend: {{ }},
  }},
  plugins: [],
}}
        """
        )

    # Create input.css in src
    with open(f"{app_name}/src/input.css", "w") as f:
        f.write(
            """
@tailwind base;
@tailwind components;
@tailwind utilities;
        """
        )

    typer.echo(f"Tailwind CSS project '{app_name}' created successfully!")


# Serve the project using Python's HTTP server
def serve_project():
    """Serve the project using Python's HTTP server from the current directory."""
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        typer.echo(f"Serving at http://localhost:8000")
        httpd.serve_forever()


# Run Tailwind CLI in watch mode
def watch_tailwind():
    """Watch for file changes and rebuild Tailwind CSS automatically."""
    try:
        subprocess.run(
            ["tailwindcss", "-i", "src/input.css", "-o", "dist/output.css", "--watch"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error during Tailwind build: {e}")


# Command to start development server and build Tailwind CSS
@app.command()
def dev():
    """Start a development server and watch for CSS changes."""

    # Run the HTTP server and Tailwind watch in parallel
    try:
        # Start the server in a separate thread
        server_thread = threading.Thread(target=serve_project)
        server_thread.start()

        # Run Tailwind watch mode in the main thread
        watch_tailwind()

    except KeyboardInterrupt:
        typer.echo("Stopping development server...")


if __name__ == "__main__":
    app()
