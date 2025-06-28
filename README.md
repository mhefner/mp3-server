# MP3 Server

A simple Flask-based MP3 server with upload support, backed by NFS and deployable via Kubernetes and Argo CD.

## Features

- List and serve `.mp3` files
- Upload new `.mp3` files directly from the web UI
- Uses NFS for persistent storage

## Build & Push

```bash
docker build -t mhefner1983/mp3-server:arm .
docker push mhefner1983/mp3-server:arm
