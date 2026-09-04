-- =========================================================================
-- Chargeback Evidence AI - Complete Database Schema (Supabase / PostgreSQL)
-- Phase 1: Database Design (PDF Reference: Pages 12-13)
-- =========================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Merchants Table
CREATE TABLE IF NOT EXISTS merchants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(32) NOT NULL,
    gst_number VARCHAR(32),
    pan_number VARCHAR(32),
    business_type VARCHAR(64) DEFAULT 'E-Commerce / D2C',
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Merchant Vault Documents (KYC onboarding vault)
CREATE TABLE IF NOT EXISTS merchant_vault_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    doc_type VARCHAR(64) NOT NULL, -- GST, PAN, REGISTRATION, ADDRESS_PROOF
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    verification_status VARCHAR(32) DEFAULT 'VERIFIED', -- PENDING, VERIFIED, REJECTED
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Chargeback Cases Table
CREATE TABLE IF NOT EXISTS chargeback_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    order_id VARCHAR(128) NOT NULL,
    status VARCHAR(64) DEFAULT 'investigating', -- pending, investigating, verified, won, lost, reviewing
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(8) DEFAULT 'INR',
    dispute_reason VARCHAR(255) NOT NULL, -- e.g. "Product Not Received", "Fraudulent / Unauthorized", "Not as Described"
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(32),
    opened_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deadline_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP + INTERVAL '7 days'),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Documents Table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES chargeback_cases(id) ON DELETE CASCADE,
    doc_type VARCHAR(64) NOT NULL, -- invoice, receipt, delivery_proof, tracking_slip, chat_log, refund_statement
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    mime_type VARCHAR(64),
    ocr_text TEXT,
    ocr_confidence NUMERIC(5, 4) DEFAULT 0.0,
    page_count INTEGER DEFAULT 1,
    extraction_method VARCHAR(64) DEFAULT 'pymupdf_text_layer', -- pymupdf_text_layer, tesseract_fallback
    preprocessing JSONB DEFAULT '{"deskewed": true, "denoised": true, "binarized": true}'::jsonb,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Extracted Entities Table
CREATE TABLE IF NOT EXISTS extracted_entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    entity_type VARCHAR(64) NOT NULL, -- customer_name, order_id, address, date, amount, tracking_id
    raw_value TEXT NOT NULL,
    normalized_value JSONB NOT NULL DEFAULT '{}'::jsonb,
    confidence NUMERIC(5, 4) DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Evidence Scores Table
CREATE TABLE IF NOT EXISTS evidence_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES chargeback_cases(id) ON DELETE CASCADE,
    score NUMERIC(5, 2) NOT NULL, -- 0 to 100 Evidence Strength Score
    win_probability NUMERIC(5, 4) NOT NULL, -- 0.0 to 1.0
    model_version VARCHAR(64) DEFAULT 'xgb_v1.0.0',
    consistency_score NUMERIC(5, 4),
    completeness_score NUMERIC(5, 4),
    features JSONB DEFAULT '{}'::jsonb,
    breakdown JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Embeddings Table (pgvector 768-dim)
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES chargeback_cases(id) ON DELETE CASCADE,
    summary_text TEXT NOT NULL,
    vector vector(768),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Historical Cases Table (pgvector 768-dim)
CREATE TABLE IF NOT EXISTS historical_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(128) NOT NULL,
    dispute_reason VARCHAR(255) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(8) DEFAULT 'INR',
    outcome VARCHAR(16) NOT NULL, -- WIN, LOSE
    evidence_quality VARCHAR(32) DEFAULT 'High', -- High, Medium, Low
    summary TEXT NOT NULL,
    vector vector(768),
    features JSONB DEFAULT '{}'::jsonb,
    closed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================================
-- Performance Indexes
-- =========================================================================
CREATE INDEX IF NOT EXISTS idx_chargeback_cases_merchant_id ON chargeback_cases(merchant_id);
CREATE INDEX IF NOT EXISTS idx_documents_case_id ON documents(case_id);
CREATE INDEX IF NOT EXISTS idx_extracted_entities_document_id ON extracted_entities(document_id);
CREATE INDEX IF NOT EXISTS idx_evidence_scores_case_id ON evidence_scores(case_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_case_id ON embeddings(case_id);
CREATE INDEX IF NOT EXISTS idx_vault_docs_merchant_id ON merchant_vault_documents(merchant_id);

-- Cosine Distance IVFFlat Indexes for fast 768-dim vector retrieval
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings 
USING ivfflat (vector vector_cosine_ops) WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_historical_cases_vector ON historical_cases 
USING ivfflat (vector vector_cosine_ops) WITH (lists = 100);

-- =========================================================================
-- Row Level Security (RLS) Policies
-- =========================================================================
ALTER TABLE merchants ENABLE ROW LEVEL SECURITY;
ALTER TABLE merchant_vault_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chargeback_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE extracted_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE embeddings ENABLE ROW LEVEL SECURITY;

-- Allow merchants to access only their own rows
CREATE POLICY merchants_isolation_policy ON merchants
    FOR ALL
    USING (id = auth.uid());

CREATE POLICY vault_docs_isolation_policy ON merchant_vault_documents
    FOR ALL
    USING (merchant_id = auth.uid());

CREATE POLICY cases_isolation_policy ON chargeback_cases
    FOR ALL
    USING (merchant_id = auth.uid());

CREATE POLICY documents_isolation_policy ON documents
    FOR ALL
    USING (case_id IN (SELECT id FROM chargeback_cases WHERE merchant_id = auth.uid()));

CREATE POLICY entities_isolation_policy ON extracted_entities
    FOR ALL
    USING (document_id IN (
        SELECT d.id FROM documents d 
        JOIN chargeback_cases c ON d.case_id = c.id 
        WHERE c.merchant_id = auth.uid()
    ));

CREATE POLICY scores_isolation_policy ON evidence_scores
    FOR ALL
    USING (case_id IN (SELECT id FROM chargeback_cases WHERE merchant_id = auth.uid()));

CREATE POLICY embeddings_isolation_policy ON embeddings
    FOR ALL
    USING (case_id IN (SELECT id FROM chargeback_cases WHERE merchant_id = auth.uid()));
