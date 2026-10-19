CREATE TABLE IF NOT EXISTS interventions (
    id SERIAL PRIMARY KEY,
    client TEXT NOT NULL,
    ville TEXT NOT NULL,
    type TEXT NOT NULL,
    priorite TEXT NOT NULL
        CHECK (priorite IN ('normale', 'élevée', 'urgente')),
    duree INTEGER NOT NULL CHECK (duree >= 0),
    probleme TEXT NOT NULL,
    action TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
