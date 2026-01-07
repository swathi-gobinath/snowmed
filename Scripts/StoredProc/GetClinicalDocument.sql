CREATE OR REPLACE FUNCTION GetClinicalDocument(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    dictation_id BIGINT,
    hospital_id BIGINT,
    department_id BIGINT,
    doctor_id BIGINT,
    patient_id BIGINT,
    encounter_id BIGINT,
    document_type TEXT,
    version INT,
    status TEXT,
    final_text TEXT,
    fhir_resource_type TEXT,
    fhir_json JSONB,
    doctor_signature TEXT,
    signed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.dictation_id, c.hospital_id, c.department_id,
           c.doctor_id, c.patient_id, c.encounter_id,
           c.document_type, c.version, c.status, c.final_text,
           c.fhir_resource_type, c.fhir_json,
           c.doctor_signature, c.signed_at,
           c.created_at, c.updated_at
    FROM clinical_documents c
    WHERE p_id IS NULL OR c.id = p_id;
END;
$$ LANGUAGE plpgsql;