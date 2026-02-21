# MP3 Server

A self-hosted music server with a dark-themed web UI. Stream and manage your MP3 collection from any browser, organized by genre categories, with a persistent audio player — all backed by NFS and running on Kubernetes.

![Python](https://img.shields.io/badge/Python-3.9-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey) ![Docker](https://img.shields.io/badge/Docker-ARM-informational) ![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326CE5)

---

## Features

- **Dark UI** — card grid layout with sidebar category navigation
- **Genre categories** — organized by subfolder (e.g. `/mp3-files/blues/`, `/mp3-files/rock/`)
- **Bottom audio player** — persistent prev/play/next controls, scrubber, time display, and volume
- **Upload modal** — upload tracks directly from the browser into any category
- **NFS-backed storage** — music lives on the NFS share, survives pod restarts
- **Kubernetes-native** — single-replica deployment with PV/PVC and NodePort service

---

## UI Overview

```
┌─────────────────────────────────────────────────────────┐
│  Categories      │  MP3 Server                          │
│                  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐        │
│  All Tracks      │  │ ♫  │ │ ♫  │ │ ♫  │ │ ♫  │        │
│  Blues           │  └────┘ └────┘ └────┘ └────┘        │
│  Metal           │                                      │
│  Rock            │                                      │
│                  │                                      │
│  + Upload Track  │                                      │
├─────────────────────────────────────────────────────────┤
│  |◀  ▶  ▶|   ━━━━━━━━━━━○──────  Track Name  0:42/3:21 │
└─────────────────────────────────────────────────────────┘
```

---

## Running Locally

```bash
pip install flask
mkdir -p /tmp/mp3-files/blues /tmp/mp3-files/rock
UPLOAD_FOLDER=/tmp/mp3-files python app.py
# Open http://localhost:8080
```

---

## Docker

```bash
# Build (ARM)
docker build -t mhefner1983/mp3-server:arm .

# Push
docker push mhefner1983/mp3-server:arm

# Run locally with a volume
docker run -p 8080:8080 -v /tmp/mp3-files:/mp3-files mhefner1983/mp3-server:arm
```

---

## Kubernetes

Manifests are in `k8s/` and managed with Kustomize.

```bash
# Apply everything
kubectl apply -k k8s/

# Or just the deployment
kubectl apply -f k8s/deployment.yaml

# Force a rollout to pull the latest image
kubectl rollout restart deployment/mp3-server
kubectl rollout status deployment/mp3-server
```

| Resource | Detail |
|---|---|
| NFS server | `10.0.0.14` — update in `k8s/pv.yaml` if it changes |
| NFS path | `/mnt/storage/mp3s` |
| Storage | 1Gi PV/PVC, `ReadWriteMany`, `Retain` policy |
| Service | NodePort `30082` |
| Image | `mhefner1983/mp3-server:arm` |

---

## Project Structure

```
mp3-server/
├── app.py               # Flask app — routing, file scanning, uploads
├── Dockerfile
├── templates/
│   └── index.html       # Dark UI — sidebar, card grid, audio player
└── k8s/
    ├── kustomization.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── pv.yaml
    ├── pvc.yaml
    └── application.yaml  # Argo CD Application resource
```
