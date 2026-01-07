CREATE OR REPLACE FUNCTION GetSNOMEDAnnotation(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    dictation_id BIGINT,
    doctor_id BIGINT,
    transcription_id BIGINT,
    snomed_concept_id BIGINT,
    term TEXT,
    category TEXT,
    start_char INT,
    end_char INT,
    confidence NUMERIC,
    model_used TEXT,
    extra JSONB,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT s.id, s.dictation_id, s.doctor_id, s.transcription_id,
           s.snomed_concept_id, s.term, s.category,
           s.start_char, s.end_char, s.confidence, s.model_used,
           s.extra, s.created_at
    FROM snomed_annotations s
    WHERE p_id IS NULL OR s.id = p_id;
END;
$$ LANGUAGE plpgsql;