create database rainbows owner rainbows;

\c rainbows
create extension pgcrypto;

\c rainbows rainbows

create table rainbows (
    clear_text_password text not null,
    primary key (clear_text_password)
);

create index md5_idx    on rainbows using hash (digest(clear_text_password,    'md5'));
create index sha1_idx   on rainbows using hash (digest(clear_text_password,   'sha1'));
create index sha224_idx on rainbows using hash (digest(clear_text_password, 'sha224'));
create index sha256_idx on rainbows using hash (digest(clear_text_password, 'sha256'));
create index sha384_idx on rainbows using hash (digest(clear_text_password, 'sha384'));
create index sha512_idx on rainbows using hash (digest(clear_text_password, 'sha512'));
