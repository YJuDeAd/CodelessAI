# Technical Architecture Plan — CodelessAI

## 1. Service Communication & Data Flow

```text
┌───────────────────┐  REST (/api/*) & WS (/ws/*)   ┌───────────────────┐
│  Frontend (Vite)  │ <---------------------------> │ Backend (FastAPI) │
└───────────────────┘                               └─────────┬─────────┘
                                                              │
                                         ┌────────────────────┼────────────────────┐
                                         ▼                    ▼                    ▼
                                ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
                                │ SQLite (State)  │  │  Redis (Broker) │  │ Storage Volume  │
                                └─────────────────┘  └────────┬────────┘  └────────┬────────┘
                                                              │                    │
                                                     LPUSH/BRPOP & Pub/Sub    Read/Write
                                                              │                    │
                                                              ▼                    ▼
                                                     ┌──────────────────────────────────────┐
                                                     │   Worker (PyTorch / Unsloth / Polars)│
                                                     └──────────────────────────────────────┘

```

* **Synchronous / Fast Operations (Backend -> SQLite):** Hardware detection, Juice VRAM math, dataset previewing, Polars profiling/cleaning, and model catalog queries run directly in FastAPI or short background tasks.
* **Asynchronous Heavy Jobs (Backend -> Redis -> Worker):** Training runs and Optuna hyperparameter sweeps are pushed to `queue:training`, picked up by the GPU worker via `BRPOP`, and streamed back over Redis Pub/Sub -> FastAPI WebSockets.


## 2. SQLite Database Schema (`codeless.sqlite`)

### `datasets`

| Column | Type | Description |
| --- | --- | --- |
| `id` | `TEXT PRIMARY KEY` | UUID string |
| `name` | `TEXT NOT NULL` | Display name |
| `source` | `TEXT NOT NULL` | `local`, `huggingface`, or `kaggle` |
| `file_path` | `TEXT NOT NULL` | Relative path inside `storage/datasets/` |
| `parent_id` | `TEXT NULL` | Original dataset ID if this row is a cleaned snapshot |
| `row_count` | `INTEGER` | Total rows |
| `columns_json` | `TEXT` | JSON map of `{col_name: dtype}` |
| `health_report_json` | `TEXT` | Polars profiler stats & advisor fix IDs |
| `splits_json` | `TEXT NULL` | JSON paths for `{train, val, test}` files |
| `created_at` | `DATETIME` | UTC timestamp |

### `models`

| Column | Type | Description |
| --- | --- | --- |
| `id` | `TEXT PRIMARY KEY` | UUID string |
| `name` | `TEXT NOT NULL` | Model name (e.g., `Llama-3.2-3B-Instruct` or custom name) |
| `origin` | `TEXT NOT NULL` | `huggingface`, `scratch`, or `fine_tuned` |
| `task_type` | `TEXT NOT NULL` | `chat`, `classification`, `summarization`, `tabular` |
| `base_model_id` | `TEXT NULL` | Hugging Face repo ID or parent model UUID |
| `param_count` | `INTEGER` | Total parameter count |
| `architecture_json` | `TEXT NULL` | Layer config JSON (for scratch-built models) |
| `local_path` | `TEXT NULL` | Path inside `storage/models/` once downloaded/saved |
| `created_at` | `DATETIME` | UTC timestamp |

### `runs`

| Column | Type | Description |
| --- | --- | --- |
| `id` | `TEXT PRIMARY KEY` | UUID string |
| `model_id` | `TEXT NOT NULL` | Foreign key -> `models.id` |
| `dataset_id` | `TEXT NOT NULL` | Foreign key -> `datasets.id` |
| `mode` | `TEXT NOT NULL` | `fine_tune` or `scratch` |
| `compute_target` | `TEXT NOT NULL` | `local` or `cloud` |
| `status` | `TEXT NOT NULL` | `QUEUED`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED` |
| `hyperparams_json` | `TEXT NOT NULL` | Batch size, LR, epochs, LoRA rank, precision, etc. |
| `metrics_summary_json` | `TEXT NULL` | Final train/val loss, accuracy, F1, and test report |
| `error_diagnosis_json` | `TEXT NULL` | Error Doctor plain-English message + 1-click fix patch |
| `checkpoint_path` | `TEXT NULL` | Path inside `storage/checkpoints/{run_id}/` |
| `created_at` | `DATETIME` | UTC timestamp |


## 3. Redis Key & Pub/Sub Contracts

| Key / Channel | Redis Type | Producer -> Consumer | Payload / Value Format |
| --- | --- | --- | --- |
| `queue:training` | `List` | Backend (`LPUSH`) -> Worker (`BRPOP`) | `run_id` (UUID string) |
| `run:{id}:control` | `String` | Backend (`SET`) -> Worker (`GET`) | `"RUN"`, `"PAUSE"`, or `"STOP"` |
| `worker:heartbeat` | `String` (TTL 10s) | Worker (`SETEX`) -> Backend (`GET`) | JSON `{"status": "idle" | "busy", "run_id": "..."}` |
| `channel:hardware:telemetry` | `Pub/Sub` | Telemetry Loop -> Backend WS | `{"gpu_name": "...", "vram_used_mb": 2100, "vram_total_mb": 4096, "util_pct": 12, "temp_c": 48, "ram_used_gb": 8.4}` |
| `channel:run:{id}:metrics` | `Pub/Sub` | Worker -> Backend WS | `{"step": 50, "epoch": 1, "train_loss": 0.42, "val_loss": 0.45, "accuracy": 0.86, "coach": {"state": "healthy", "message": "..."}}` |


## 4. Core API & WebSocket Endpoints

* **Hardware & Juice Engine**
* `GET /api/hardware/specs` — Static CPU, RAM, disk, and GPU capabilities
* `POST /api/hardware/juice-check` — Body: `{param_count, mode, precision, batch_size}` -> Returns `Ready | Tight | Too Heavy` + upgrade/cloud advice
* `WS /ws/telemetry` — Live hardware telemetry stream

* **Datasets**
* `POST /api/datasets/upload` — Multipart upload (`CSV`, `JSONL`, `Parquet`)
* `GET /api/datasets/search?q=...&source=all` — Unified Hugging Face + Kaggle search
* `POST /api/datasets/import` — Import external dataset into local storage
* `POST /api/datasets/{id}/clean` — Apply Polars fix IDs (`drop_nulls`, `drop_duplicates`, `balance_classes`)
* `POST /api/datasets/{id}/split` — Split into `train / val / test`

* **Models**
* `GET /api/models/hub?task=...&q=...` — Curated + Hugging Face models stamped with Juice badges
* `POST /api/models/{id}/download` — Download weights to `storage/models/`
* `POST /api/models/scratch` — Save visual scratch architecture & return footprint estimate

* **Training & Playground**
* `POST /api/runs` — Enqueue one or more training runs
* `POST /api/runs/{id}/control` — Body: `{"action": "PAUSE" | "RESUME" | "STOP"}`
* `WS /ws/runs/{id}` — Live step metrics + Overfit/Underfit coach stream
* `POST /api/playground/infer` — Run inference/chat against any local model

## 5. Local Storage Conventions

```text
storage/
├── datasets/
│   ├── raw_{dataset_id}.parquet
│   └── clean_{dataset_id}_v1.parquet
├── checkpoints/
│   └── {run_id}/
│       └── step_{n}/
└── models/
    └── {model_id}/

```