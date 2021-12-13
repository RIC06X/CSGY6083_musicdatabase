create table Artist(
   aid varchar(128) primary key ,
   name varchar(128)
);

create table Album(
  album_id varchar(128) primary key,
  name varchar(128),
  release_date date
);


create table Album_Artist_Map(
   album_id varchar(128),
   aid varchar(128),
    primary key (aid, album_id),
    foreign key (aid) references Artist(aid),
    foreign key (album_id) references Album(album_id)
);

create table Song(
  sid   varchar(128)    primary key,
  album_id varchar(128),
  name varchar(128) not null,
  duration_ms integer not null,
  release_date date not null,
  foreign key (album_id) references Album(album_id)
);

create table Song_Artist_Map(
    sid varchar(128),
    aid varchar(128),
    primary key (sid, aid),
    foreign key (aid) references Artist(aid),
    foreign key (sid) references Song(sid)
);

create table _User
(
   user_id     serial primary key,
   name    varchar(128) not null,
   email     varchar(128) not null
);

create table Company(
   company_id serial primary key ,
   name varchar(128)
);


create table Rating(
   cid serial primary key,
   sid varchar(128),
   rating integer not null,
   _time date
);


create table Playlist(
   pid serial primary key ,
   pname varchar(128),
   playtimes integer default 0,
   update_date timestamp not null
);

create table PlaylistStores(
   pid integer,
   sid varchar(128),
   primary key (pid,sid),
   foreign key (pid) references Playlist(pid),
   foreign key (sid) references Song(sid)
);


create table ArtistOwned(
   aid varchar(128) primary key,
   company_id integer,
   foreign key (aid) references Artist(aid),
   foreign key (company_id) references Company(company_id)
);


create table PlaylistCreated(
   pid integer primary key ,
   uid integer not null ,
   foreign key (pid) references Playlist(pid),
   foreign key (uid) references _User(user_id)
);

create table ArtistSubscribed(
   aid varchar(128) primary key ,
   uid integer,
   foreign key (aid) references Artist(aid),
   foreign key (uid) references _User(user_id)
);


create table ratingby(
   cid integer,
   uid integer,
   primary key (cid, uid),
   foreign key (cid) references Rating(cid),
   foreign key (uid) references _User(user_id) on delete cascade
);

