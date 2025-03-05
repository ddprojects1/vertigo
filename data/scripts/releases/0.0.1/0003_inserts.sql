--liquibase formatted sql
--changeset liquibase:0003 labels:insert data splitStatements:true endDelimiter:;

-- create secrets for admin user 
INSERT INTO public.tbl_secrets(secret)
	VALUES (crypt('password',gen_salt('md5')));


INSERT INTO public.tbl_users(
	user_name, secret_id, first_name, last_name, address, city, country)
	VALUES ('admin',1,'admin','admin','usa','usa','usa');
