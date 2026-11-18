# Milestones

## 1) The Juice Engine
- [ ] **Build Local GPU & System Specs Reader**
    - **GPU Metrics:** Model name, total/free VRAM, utilization %, and temperature
    - **System Metrics:** Total/available RAM, CPU core count, and disk space
    - **Resilience:** Include graceful CPU-only fallback when no GPU is detected
- [ ] **Real-Time Live GPU Telemetry & Websocket API**
    - **Redis Pub/Sub:** Publish hardware telemetry payloads every 1–2s to `channel:hardware:telemetry`
    - **WebSocket Endpoint:** Expose `/ws/telemetry` to stream live metrics to connected clients
- [ ] **VRAM Compatibility Calculator**
    - **Workload Modes:** Support Inference, QLoRA/LoRA Fine-Tuning, and From-Scratch Training
    - **Inputs:** Parameter count, precision (`fp16` / `4-bit`), and batch size
    - **Status Output:** Classify hardware fit as `Ready`, `Tight`, or `Too Heavy`
- [ ] **Hardware Upgrade & Cloud GPU Advisor**
    - **Trigger:** Activate when local VRAM is insufficient (`Tight` or `Too Heavy`)
    - **Local Recommendation:** Suggest minimum viable local GPU VRAM tier (`12GB` / `16GB` / `24GB`)
    - **Cloud Recommendation:** Suggest the best cost-to-performance cloud GPU rental option

## 2) Frontend & UI Shell
- [ ] **Frontend Scaffolding & Navigation**
    - **Tech Stack:** Set up React + Vite + Tailwind CSS
    - **Layout & Navigation:** Build main application shell with tabs for `Hardware`, `Datasets`, `Models`, `Studio`, and `Playground`
- [ ] **Live Hardware Dashboard & Compatibility Widget**
    - **WebSocket Integration:** Connect frontend client to `/ws/telemetry` for real-time updates
    - **Live Telemetry Gauges:** Render dynamic VRAM usage and GPU temperature gauges
    - **Interactive Compatibility Checker:** Build UI widget to test model configurations against live hardware specs

## 3) Dataset Management & Ingestion
- [ ] **Local Dataset Upload & Metadata Ingestion**
    - **File Storage:** Save uploaded local files into `storage/datasets/`
    - **Database Persistence:** Record dataset metadata in SQLite
    - **Inspection Response:** Return inferred schema alongside a 20-row data preview
- [ ] **Unified External Dataset Search & Download**
    - **Search Endpoint:** Query Hugging Face Hub and Kaggle search APIs through a single unified endpoint
    - **Format Conversion & Storage:** Download selected datasets and convert/save them locally in `Parquet` or `JSONL` format
- [ ] **Automated Dataset Profiling & Analytics (Polars)**
    - **Structural Metrics:** Compute row/column counts, column data types, null percentages, and duplicate row counts
    - **Content & Target Stats:** Calculate text length statistics and target class balance distribution
- [ ] **Deterministic Health Diagnostics & 1-Click Fix Engine**
    - **Rule-Based Evaluation:** Analyze the Polars health report against deterministic quality thresholds
    - **Actionable Output:** Emit plain-English warnings paired with 1-click fix IDs (e.g., missing values, duplicates, severe class imbalance)
- [ ] **Non-Destructive Data Cleaning & Snapshot Pipeline (Polars)**
    - **Cleaning Operations:** Support dropping duplicates, dropping/filling nulls, balancing target classes, and formatting prompt/response pairs
    - **Versioning & Storage:** Preserve raw files and save transformed datasets as immutable cleaned snapshots
- [ ] **Configurable Dataset Splitting (`Train / Val / Test`)**
    - **Ratio Partitioning:** Split cleaned datasets using user-configured ratios (e.g., `80/10/10`)
    - **File Output:** Export separate `train`, `val`, and `test` files into `storage/datasets/`
- [ ] **Datasets Explorer & Cleaning Dashboard UI**
    - **Search & Discovery:** Build unified search bar for local and external datasets
    - **Visual Analytics:** Render dataset overview cards and interactive class distribution charts
    - **Interactive Remediation:** Add 1-click cleaning toolbar wired to backend fix IDs

## 4) Model Discovery & Hub Integration
- [ ] **Curated Model Catalog & Live Hugging Face Search**
    - **Curated Presets:** Provide beginner-friendly model presets tagged by plain-English use cases
    - **Live Hub Search:** Integrate real-time search against the Hugging Face Hub API
    - **Metadata Extraction:** Automatically parse and extract model parameter counts for compatibility checks
- [ ] **Hardware Feasibility Scoring & Weight Downloader**
    - **Juice Calculator Integration:** Run catalog and search models against local GPU specs to tag compatibility
    - **Local Model Caching:** Download selected model weights directly into `storage/models/`
- [ ] **Models Hub & Compatibility UI**
    - **Discovery & Status:** Display plain-English purpose filters alongside green/yellow/red Juice fit badges
    - **Advisor & Progress:** Render upgrade/cloud rental recommendations and live weight download progress bars

## 5) No-Code Model Builder & Training Studio
- [ ] **Visual Architecture Builder & Template Wizard**
    - **No-Code Block Assembly:** Build a visual wizard and block editor for assembling Tabular MLPs and simple neural networks from starter templates
    - **Zero-Code Execution:** Compile visual configurations directly into runnable models without requiring users to write PyTorch code
- [ ] **Pre-Training Footprint & Resource Estimator**
    - **Exact Architecture Profiling:** Calculate exact parameter count and projected checkpoint disk size for custom visual models
    - **Hardware Gatekeeper:** Compute minimum VRAM and system RAM needed to load and run the model before training starts
- [ ] **Training Job Worker & Lifecycle State Machine**
    - **Queue Consumer:** Implement `worker/main.py` listening on `queue:training` via `redis-py`
    - **State Persistence:** Track and update run status transitions in SQLite (`QUEUED` → `RUNNING` → `COMPLETED` / `FAILED`)
- [ ] **Graceful Step-Loop Control & Live Metrics Streaming**
    - **Interrupt Polling:** Poll `run:{id}:control` inside the training step loop to handle `Pause` and `Stop` signals
    - **Checkpoint & Exit:** Save model checkpoints to `storage/checkpoints/` and exit cleanly upon interruption
    - **Live Step Telemetry:** Publish real-time training step metrics to Redis Pub/Sub
- [ ] **From-Scratch PyTorch Training & Validation Engine**
    - **Core Execution Loop:** Build clean PyTorch training and validation loops for custom scratch models
    - **Checkpoint Persistence & Recovery:** Implement periodic checkpoint saving and full resume-from-checkpoint state restoration
- [ ] **Single-GPU LLM Fine-Tuning Pipeline (`Unsloth`)**
    - **Adapter Training:** Integrate `FastLanguageModel` for memory-efficient LoRA/QLoRA fine-tuning on cleaned datasets
    - **State Recovery:** Support pause/resume adapter checkpointing throughout training runs
- [ ] **Smart Hyperparameter Auto-Tuner & Optuna Sweep Engine**
    - **Heuristic Auto-Configuration:** Automatically compute safe batch size, gradient accumulation steps, learning rate, and epochs from available VRAM and dataset size
    - **Automated HPO Sweeps:** Support optional `Optuna` hyperparameter trial runs for deeper optimization
- [ ] **Training Exception Interceptor & 1-Click Auto-Remediation**
    - **Failure Detection:** Catch `torch.cuda.OutOfMemoryError`, `NaN` loss divergence, and tensor shape/schema mismatches during execution
    - **Actionable Diagnostics:** Translate runtime tracebacks into plain-English explanations paired with 1-click fix suggestions
- [ ] **Training Studio UI & Error Doctor Controls**
    - **Guided Configuration & Queueing:** Build plain-English hyperparameter sliders and a multi-run job queue builder
    - **Live Run Management & Alerts:** Add `Pause` / `Resume` / `Stop` controls alongside interactive Error Doctor alert banners
- [ ] **Live Training Metrics Stream & Recharts Visualization**
    - **WebSocket Metric Relay:** Stream real-time training step metrics over WebSockets from Redis Pub/Sub to the frontend
    - **Multi-Metric Charts:** Render live `Loss`, `Accuracy`, `Precision`, `Recall`, and `F1` curves using Recharts
- [ ] **Real-Time Overfitting & Convergence Coach**
    - **Rolling Gap Analysis:** Continuously evaluate rolling train vs. validation loss divergence during active runs
    - **Actionable Coaching Banners:** Display plain-English diagnostic banners (e.g., overfitting, underfitting, plateauing) with concrete next-step recommendations

## 6) Evaluation, Export & Playground
- [ ] **Multi-Run Comparison & Post-Training Test Evaluation**
    - **Side-by-Side Run Comparator:** Compare hyperparameters, loss curves, and final metrics across multiple queued runs
    - **Test-Set Report Card:** Automatically generate a post-training evaluation card highlighting overall accuracy and worst-predicted failure examples
- [ ] **Interactive Inference Playground**
    - **Universal Model Loader:** Load any downloaded, fine-tuned, or scratch-built model directly inside the web UI
    - **Chat & Batch Testing:** Provide an interactive interface for live LLM chat sessions and custom tabular/classification test predictions

## 7) Cloud GPU Marketplace & Offloading
- [ ] **Live Cloud GPU Pricing & Availability Aggregator**
    - **Provider API Integration:** Fetch live GPU instance availability and hourly pricing using user-supplied API keys (`BYO API key`)
    - **Real-Time Rental UI:** Display live cloud GPU rental options, specs, and hourly rates directly inside the interface
- [ ] **Hybrid Local-to-Cloud Training Burst & Metric Sync**
    - **Hybrid Workflow:** Keep data preparation and cleaning local while offloading heavy training jobs to rented cloud GPU instances
    - **Remote Telemetry & Artifact Sync:** Stream live step metrics back to the local dashboard and sync final checkpoints upon completion

## 8) Containerization & Deployment
- [ ] **Multi-Service Docker & GPU Orchestration**
    - **Container Images:** Create Dockerfiles for `frontend`, `backend`, and `worker` (built on `unsloth/unsloth:core`)
    - **Docker Compose & GPU Passthrough:** Configure `docker-compose.yml` with `redis:alpine`, NVIDIA GPU device reservation, `shm_size: '8gb'` (for PyTorch DataLoaders), and a shared `./storage:/storage` volume.