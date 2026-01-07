CREATE OR REPLACE FUNCTION SaveSNOMEDAnnotation(
    p_id BIGINT,
    p_dictation_id BIGINT,
    p_doctor_id BIGINT,
    p_transcription_id BIGINT,
    p_snomed_concept_id BIGINT,
    p_term TEXT,
    p_category TEXT,
    p_start_char INT,
    p_end_char INT,
    p_confidence NUMERIC,
    p_model_used TEXT,
    p_extra JSONB
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO snomed_annotations (
        dictation_id, doctor_id, transcription_id, snomed_concept_id,
        term, category, start_char, end_char, confidence, model_used, extra
    )
    VALUES (
        p_dictation_id, p_doctor_id, p_transcription_id, p_snomed_concept_id,
        p_term, p_category, p_start_char, p_end_char, p_confidence, p_model_used, p_extra
    )
    ON CONFLICT (id) DO UPDATE SET
        term = EXCLUDED.term,
        category = EXCLUDED.category,
        confidence = EXCLUDED.confidence,
        model_used = EXCLUDED.model_used,
        extra = EXCLUDED.extra
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;