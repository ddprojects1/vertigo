--liquibase formatted sql
--changeset liquibase:1 labels:create_sequence splitStatements:true endDelimiter:;

 DROP SEQUENCE IF EXISTS public.secrets_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.secrets_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 10000
    CACHE 1;


DROP SEQUENCE IF EXISTS public.user_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.user_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 1000
    CACHE 1;

