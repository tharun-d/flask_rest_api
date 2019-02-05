#3. Using Database folder
create database FlaskRestApi;

#users table
create table users(id int primary key AUTO_INCREMENT,
				   username varchar(20),
				   loginpassword varchar(20));
                   
insert into users (username, loginpassword) values('bob','asdf');

select * from users;

drop table users;

#items table
create table items(itemname varchar(20),
					price float);
                    
insert into items values('apple',20);

update items set price = 10 where itemname='apple';

select * from items;

drop table items;
