--liquibase formatted sql
--changeset liquibase:0004 labels: Instock Sequence and Tables splitStatements:true endDelimiter:;


CREATE SEQUENCE IF NOT EXISTS public.stock_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 1000000
    CACHE 1;



CREATE TABLE IF NOT EXISTS public.tbl_instock
(
    stock_id integer NOT NULL DEFAULT nextval('stock_id_seq'),
    user_id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    user_name character varying(255) COLLATE pg_catalog."default",
    device_name character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT tbl_instock_pkey PRIMARY KEY (stock_id),
    CONSTRAINT fk_user_id FOREIGN KEY (user_id)
        REFERENCES public.tbl_users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);