async def create_schema(cursor):
    # datasets table queries
    await cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS datasets (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            file_path TEXT NOT NULL,
            parent_id TEXT NULL,
            row_count INTEGER,
            columns_json TEXT,
            health_report_json TEXT,
            splits_json TEXT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )

    # models table queries
    await cursor.execute (
        '''
        CREATE TABLE IF NOT EXISTS models (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            origin TEXT NOT NULL,
            task_type TEXT NOT NULL,
            base_model_id TEXT NULL,
            param_count INTEGER,
            architecture_json TEXT NULL,
            local_path TEXT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )

    # runs table queries
    await cursor.execute (
        '''
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            model_id TEXT NOT NULL,
            dataset_id TEXT NOT NULL,
            mode TEXT NOT NULL,
            compute_target TEXT NOT NULL,
            status TEXT NOT NULL,
            hyperparams_json TEXT NOT NULL,
            metrics_summary_json TEXT NULL,
            error_diagnosis_json TEXT NULL,
            checkpoint_path TEXT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
        )
        '''
    )

    await cursor.execute (
        '''
        CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
        '''
    )

    await cursor.execute (
        '''
        CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at DESC);
        '''
    )
    