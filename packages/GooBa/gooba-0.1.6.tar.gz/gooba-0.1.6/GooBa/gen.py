import os

def create_project_structure(project_name):
    directories = [
        f"{project_name}/",
        f"{project_name}/output/"
    ]

    files = {
        f"{project_name}/main.py": '''from GooBa import Document, CreateElement

# Create a new document
doc = Document()

text = CreateElement("h1")
text.text = "This is a Heading"

p = CreateElement("p")
p.text = "This is a paragraph."

doc.body(text, p)
doc.title("Page Title")

doc.build()
''',

        f"{project_name}/server.py": '''import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "output"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        requested_path = self.directory + self.path
        if not os.path.exists(requested_path) or os.path.isdir(requested_path):
            self.path = "/index.html"
        return super().do_GET()

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
''',

        f"{project_name}/run.py": '''import time
import subprocess
import os
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import http.server
import socketserver

PORT = 8000
DIRECTORY = "output"

class ServerManager:
    def __init__(self):
        self.process = None

    def start_server(self):
        if self.process:
            self.stop_server()
        self.process = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_server(self):
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process.terminate()
            self.process.wait()
            self.process = None

    def restart_server(self):
        print("File changed. Restarting server... Server run on Port 8000")
        subprocess.run(['python', 'main.py'])
        self.stop_server()
        self.start_server()

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, server_manager):
        self.server_manager = server_manager

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File {event.src_path} has changed!")
            self.server_manager.restart_server()

def run_server():
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)

        def do_GET(self):
            requested_path = self.directory + self.path
            if not os.path.exists(requested_path) or os.path.isdir(requested_path):
                self.path = "/index.html"
            return super().do_GET()

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    server_manager = ServerManager()
    server_manager.start_server()

    observer = Observer()
    event_handler = ChangeHandler(server_manager)
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
'''
    }

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create files with default content
    for file_path, content in files.items():
        with open(file_path, 'w') as file:
            file.write(content)

    print(f"Project {project_name} generated successfully!")

def main():
    project_name = input("Enter the project name: ")
    create_project_structure(project_name)

if __name__ == "__main__":
    main()