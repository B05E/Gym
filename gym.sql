 create database gym_manage;
 use gym_manage;

  create table login(
    username varchar(20),
    pwd varchar(20),
    primary key(username,pwd)
);

create table memeber(
    mem_id varchar(20),
    name varchar(30),
    dob varchar(20),
    age varchar(20),
    package varchar(10),
    mobno bigint
    check(mobno between 100000000 and 9999999999),
    pay_id varchar(10),
    trainer_id varchar(20),
    primary key(mem_id,pay_id,trainer_id,package),
    foreign key(pay_id) references payment(pay_id),
    foreign key(trainer_id) references trainer(trainer_id)
);

create table gym(
    gym_id varchar(20) primary key,
    gym_name varchar(30) unique,
    address varchar(150),
    type varchar(20) 
);

create table payment(
    pay_id varchar(20),
    amount varchar(20),
    gym_id varchar(20),
    primary key(pay_id,gym_id),
    foreign key(gym_id) references gym(gym_id)
);

create table trainer(
    trainer_id varchar(20),
    name varchar(20),
    time varchar(10),
    mobno varchar(10),
    pay_id varchar(20),
    primary key(trainer_id,pay_id),
    foreign key(pay_id) references payment(pay_id)
);
