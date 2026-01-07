CREATE OR REPLACE FUNCTION GetTranscription(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    dictation_id BIGINT,
    doctor_id BIGINT,
    raw_text TEXT,
    model_name TEXT,
    confidence NUMERIC,
    word_count INT,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.dictation_id, t.doctor_id, t.raw_text,
           t.model_name, t.confidence, t.word_count, t.created_at
    FROM transcriptions t
    WHERE p_id IS NULL OR t.id = p_id;
END;
$$ LANGUAGE plpgsql;