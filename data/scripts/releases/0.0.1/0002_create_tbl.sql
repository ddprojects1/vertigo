--liquibase formatted sql
--changeset liquibase:0002 labels:create_tables splitStatements:true endDelimiter:;

-- Table: public.tbl_secrets

CREATE TABLE IF NOT EXISTS public.tbl_secrets
(
    secret_id integer NOT NULL DEFAULT nextval('secrets_id_seq'::regclass),
    secret character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT tbl_secrets_pkey PRIMARY KEY (secret_id)
);

-- Table: public.tbl_users

CREATE TABLE IF NOT EXISTS public.tbl_users
(
    user_id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    user_name character varying(255) COLLATE pg_catalog."default",
    secret_id integer,
    first_name character varying(255) COLLATE pg_catalog."default",
    last_name character varying(255) COLLATE pg_catalog."default",
    address character varying(1000) COLLATE pg_catalog."default",
    city character varying(255) COLLATE pg_catalog."default",
    country character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT tbl_users_pkey PRIMARY KEY (user_id),
    CONSTRAINT fk_secret FOREIGN KEY (secret_id)
        REFERENCES public.tbl_secrets (secret_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
   