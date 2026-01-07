CREATE OR REPLACE FUNCTION SaveTranscription(
    p_id BIGINT,
    p_dictation_id BIGINT,
    p_doctor_id BIGINT,
    p_raw_text TEXT,
    p_model_name TEXT,
    p_confidence NUMERIC,
    p_word_count INT
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO transcriptions (
        dictation_id, doctor_id, raw_text, model_name, confidence, word_count
    )
    VALUES (
        p_dictation_id, p_doctor_id, p_raw_text, p_model_name, p_confidence, p_word_count
    )
    ON CONFLICT (id) DO UPDATE SET
        raw_text = EXCLUDED.raw_text,
        model_name = EXCLUDED.model_name,
        confidence = EXCLUDED.confidence,
        word_count = EXCLUDED.word_count
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;