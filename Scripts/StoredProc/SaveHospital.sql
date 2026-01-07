-- SaveHospital.sql
-- Performs a merge (insert or update) for hospitals and returns the id of the affected row

CREATE OR REPLACE FUNCTION SaveHospital(
    p_id bigint,
    p_name text,
    p_code text,
    p_address text,
    p_city text,
    p_state text,
    p_pincode text,
    p_abha_facility_id text,
    p_is_active boolean
) RETURNS bigint AS $$
DECLARE
    result_id bigint;
BEGIN
    IF p_id IS NULL THEN
        -- Insert new hospital
        INSERT INTO hospitals (name, code, address, city, state, pincode, abha_facility_id, is_active)
        VALUES (p_name, p_code, p_address, p_city, p_state, p_pincode, p_abha_facility_id, p_is_active)
        RETURNING id INTO result_id;
    ELSE
        -- Try to update; if not found, insert with given id
        UPDATE hospitals
        SET name = COALESCE(p_name, name),
            code = COALESCE(p_code, code),
            address = COALESCE(p_address, address),
            city = COALESCE(p_city, city),
            state = COALESCE(p_state, state),
            pincode = COALESCE(p_pincode, pincode),
            abha_facility_id = COALESCE(p_abha_facility_id, abha_facility_id),
            is_active = COALESCE(p_is_active, is_active)
        WHERE id = p_id;

        IF FOUND THEN
            result_id := p_id;
        ELSE
            INSERT INTO hospitals (id, name, code, address, city, state, pincode, abha_facility_id, is_active)
            VALUES (p_id, p_name, p_code, p_address, p_city, p_state, p_pincode, p_abha_facility_id, p_is_active)
            RETURNING id INTO result_id;
        END IF;
    END IF;

    RETURN result_id;
END;
$$ LANGUAGE plpgsql;