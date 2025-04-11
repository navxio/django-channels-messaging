### Requirements:
- `python 3.11`
- `uv`
- (Optional)[Taskfile](https://taskfile.dev)

### How to setup:
Create a virtual env with uv venv .venv --python=3.11


You can run all the commands in parallel using 

task -p "dev:frontend" "dev:backend" "start:client-website"

and it will launch:
- the backend running on port 8000
- the frontend running on port 5173
- the client website served via index.html on port 3000
