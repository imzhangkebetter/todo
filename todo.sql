create table zhuti
(
    id   int auto_increment
        primary key,
    name varchar(40) not null
);

create table xuanxiang
(
    id   int auto_increment
        primary key,
    name varchar(40)   not null,
    num  int default 0 not null,
    x_id int           null,
    constraint z_x_fk
        foreign key (x_id) references zhuti (id)
            on delete cascade
);