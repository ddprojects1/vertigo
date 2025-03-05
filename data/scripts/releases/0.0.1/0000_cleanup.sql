--liquibase formatted sql
--changeset liquibase:0000 labels:db clean up  splitStatements:true endDelimiter:;


DROP TABLE tbl_users;
DROP TABLE tbl_secrets;

DROP SEQUENCE public.secrets_id_seq;
DROP SEQUENCE public.user_id_seq ;