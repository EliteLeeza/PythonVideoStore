DROP DATABASE IF EXISTS video_store;
CREATE DATABASE video_store;

USE video_store;

CREATE TABLE customers(
	 custId 	int 			AUTO_INCREMENT
    ,fname		varchar(255) 	NOT NULL
    ,sname		varchar(255) 	NOT NULL
    ,address	varchar(255) 	NOT NULL
    ,phone		varchar(255) 	NOT NULL 	UNIQUE
    ,PRIMARY KEY(custId)
    );
    
CREATE TABLE videos(
	 videoId	int				AUTO_INCREMENT
    ,videoVer	int				NOT NULL	
    ,vname		varchar(255)	NOT NULL
    ,videoType	varchar(1)		NOT NULL
    ,dateAdded	date			NOT NULL
    ,PRIMARY KEY(videoId)
    );
    
CREATE TABLE hire(
	 custId		int				NOT NULL
    ,videoId	int				NOT NULL	
    ,videoVer   int				NOT NULL
    ,dateHired	date			NOT NULL
    ,dateReturn	date
    );


CREATE USER 'videoStoreUser'@'localhost' IDENTIFIED BY 'Qweasd1';

GRANT INSERT, UPDATE, DELETE, SELECT on video_store.* TO 'videoStoreUser'@'localhost' WITH GRANT OPTION;