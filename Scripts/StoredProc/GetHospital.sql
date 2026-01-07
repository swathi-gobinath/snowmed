-- GetHospital.sql
-- Returns hospital row for given id. If p_id is NULL or 0, returns all hospitals.

CREATE OR REPLACE FUNCTION GetHospital(p_id bigint) RETURNS SETOF hospitals AS $$
BEGIN
    IF p_id IS NULL OR p_id = 0 THEN
        RETURN QUERY SELECT * FROM hospitals;
    ELSE
        RETURN QUERY SELECT * FROM hospitals WHERE id = p_id;
    END IF;
END;
$$ LANGUAGE plpgsql;    