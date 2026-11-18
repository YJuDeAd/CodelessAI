# CodelessAI - Automated AI Training Platform

**An open-source, Dockerized visual AI Studio that enables non-coding users to import and clean datasets, check hardware compatibility, train models from scratch, or fine-tune existing open-weight models—using their local GPU, rented cloud GPUs, or both in hybrid mode—without writing code.**


## Why CodelessAI?

Training and fine-tuning AI models usually requires wrestling with Python environments, CUDA out-of-memory crashes, command-line scripts, and complex cloud setups. **CodelessAI** turns that workflow into a guided, visual experience:

* **Built for Non-Coders:** Plain-English controls, automated dataset cleaning suggestions, and live coaching banners that warn you when a model is overfitting or underfitting.
* **Hardware-Aware ("The Juice Engine"):** Automatically scans your local GPU/RAM and tells you whether you have enough compute to run, fine-tune, or train a model—or recommends the exact hardware upgrade or cheapest cloud GPU to rent.
* **Flexible Compute:** Train on your **local GPU**, burst to **rented cloud GPUs**, or combine both in **Hybrid Mode**.


## Core Features

### 1. Hardware & Compute ("The Juice Engine")
* **Auto Hardware Scanner:** Real-time detection of GPU model, VRAM usage, utilization, temperature, system RAM, and disk space.
* **"Do I Have the Juice?" Checker:** Instant `Ready` / `Tight` / `Too Heavy` compatibility badges for inference, QLoRA fine-tuning, and from-scratch training.
* **Upgrade & Rental Advisor:** Suggests minimum local GPU upgrades or bang-for-your-buck cloud GPU rentals when local VRAM falls short.
* **Compute Modes:** Switch seamlessly between **Local GPU**, **Rented Cloud GPU** (RunPod / Vast.ai), and **Hybrid Mode** (clean/prep locally, burst training to cloud).

### 2. Unified Data Hub & No-Code Cleaning Studio
* **Multi-Source Marketplace:** Search datasets across Hugging Face and Kaggle in one bar and import in a single click alongside local uploads (`CSV`, `JSONL`, `Parquet`).
* **Dataset Health Dashboard:** Instant overview of row counts, missing values, duplicates, and class balance distributions.
* **Point-and-Click Cleaning & Smart Advisor:** Automated plain-English recommendations with 1-click fixes (drop duplicates, handle nulls, balance classes, split Train/Val/Test sets).

### 3. Model Marketplace & Scratch Builder
* **Purpose-First Model Hub:** Browse open-weight models organized by real-world use cases, each stamped with a live hardware compatibility badge.
* **No-Code Scratch Builder:** Assemble custom tabular or neural network models visually without writing PyTorch code.
* **Inference Footprint Estimator:** Calculates the exact VRAM, RAM, and disk space needed to load and run your custom model before training starts.

### 4. Guided Training Studio, Queue & Error Doctor
* **Plain-English Hyperparameters + Queue:** Sliders with simple explanations, smart auto-recommendations (plus Optuna hyperparameter sweeps), and a multi-run experiment queue.
* **Pause & Resume Checkpointing:** Safely pause long training runs anytime and resume later without losing progress.
* **Plain-English Error Doctor:** Translates cryptic crashes (`CUDA Out of Memory`, `NaN` loss, shape mismatches) into clear explanations and 1-click fixes.

### 5. Live Analytics, Coaching & Playground
* **Live Overfit / Underfit Coach:** Real-time Loss, Accuracy, Precision, Recall, and F1 charts paired with automated plain-English guidance.
* **Run Comparison & Evaluation:** Compare queued runs side-by-side and inspect easy-to-read evaluation report cards.
* **In-App Playground:** Chat with or test any downloaded, fine-tuned, or scratch-built model directly inside the browser.


## Tech Stack:

|        **Layer**        |                       **Technology**                        |                                            **Role in Project**                                             |
| :---------------------: | :---------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------: |
| Packaging & Deployment  | **Docker + Docker Compose** (with NVIDIA Container Toolkit) |                 Packages the web app, API, worker, and broker with local GPU passthrough.                  |
|       Frontend UI       |           React (Vite) + Tailwind CSS + Recharts            |          Fast local SPA dashboard for live training charts, GPU telemetry, and no-code controls.           |
|       Backend API       |                Python + FastAPI + WebSockets                |                      REST endpoints and real-time WebSocket streaming to the browser.                      |
| Queue, State & Pub/Sub  |                     Redis (`redis-py`)                      |       Handles the multi-run job queue, instant Pause/Stop flags, and live training metric streaming.       |
|        Database         |                           SQLite                            |           Lightweight persistent storage for dataset metadata, run history, and model registry.            |
|   Hardware Telemetry    |            `nvidia-ml-py` (`pynvml`) + `psutil`             |                     Reads exact GPU VRAM, utilization, temperature, and system specs.                      |
|     Data Processing     |              Polars + Hugging Face `datasets`               |         Fast dataset loading, statistical profiling, and point-and-click cleaning transformations.         |
| ML & Fine-Tuning Engine |                 PyTorch + Unsloth + Optuna                  | Custom training loops, memory-efficient single-GPU fine-tuning, and automated hyperparameter optimization. |