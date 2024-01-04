BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "VetCalendar_todo" (
	"id"	integer NOT NULL,
	"title"	varchar(120) NOT NULL,
	"description"	text NOT NULL,
	"completed"	bool NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "VetCalendar_calendar" (
	"id"	integer NOT NULL,
	"user_initials"	varchar(4) NOT NULL,
	"shift"	varchar(20) NOT NULL,
	"start"	datetime NOT NULL,
	"end"	datetime NOT NULL,
	"month"	varchar(20) NOT NULL,
	"year"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "VetCalendar_shift" (
	"id"	integer NOT NULL,
	"shift"	varchar(20) NOT NULL,
	"start_time"	time NOT NULL,
	"end_time"	time NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "VetCalendar_shifttype" (
	"id"	integer NOT NULL,
	"name"	varchar(20) NOT NULL,
	"color"	varchar(20) NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "VetCalendar_scheduleshift" (
	"id"	integer NOT NULL,
	"date"	date NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"shift_id"	bigint NOT NULL,
	"shift_type_id"	bigint NOT NULL,
	"user_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "login_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("shift_id") REFERENCES "VetCalendar_shift"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("shift_type_id") REFERENCES "VetCalendar_shifttype"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "VetCalendar_todo" VALUES (1,'First Item','Test of the Django Rest framework module',0);
INSERT INTO "auth_user_user_permissions" VALUES (1,2,1);
INSERT INTO "auth_user_user_permissions" VALUES (2,2,2);
INSERT INTO "auth_user_user_permissions" VALUES (3,2,3);
INSERT INTO "auth_user_user_permissions" VALUES (4,2,4);
INSERT INTO "auth_user_user_permissions" VALUES (5,2,5);
INSERT INTO "auth_user_user_permissions" VALUES (6,2,6);
INSERT INTO "auth_user_user_permissions" VALUES (7,2,7);
INSERT INTO "auth_user_user_permissions" VALUES (8,2,8);
INSERT INTO "auth_user_user_permissions" VALUES (9,2,9);
INSERT INTO "auth_user_user_permissions" VALUES (10,2,10);
INSERT INTO "auth_user_user_permissions" VALUES (11,2,11);
INSERT INTO "auth_user_user_permissions" VALUES (12,2,12);
INSERT INTO "auth_user_user_permissions" VALUES (13,2,13);
INSERT INTO "auth_user_user_permissions" VALUES (14,2,14);
INSERT INTO "auth_user_user_permissions" VALUES (15,2,15);
INSERT INTO "auth_user_user_permissions" VALUES (16,2,16);
INSERT INTO "auth_user_user_permissions" VALUES (17,2,17);
INSERT INTO "auth_user_user_permissions" VALUES (18,2,18);
INSERT INTO "auth_user_user_permissions" VALUES (19,2,19);
INSERT INTO "auth_user_user_permissions" VALUES (20,2,20);
INSERT INTO "auth_user_user_permissions" VALUES (21,2,21);
INSERT INTO "auth_user_user_permissions" VALUES (22,2,22);
INSERT INTO "auth_user_user_permissions" VALUES (23,2,23);
INSERT INTO "auth_user_user_permissions" VALUES (24,2,24);
INSERT INTO "auth_user_user_permissions" VALUES (25,2,25);
INSERT INTO "auth_user_user_permissions" VALUES (26,2,26);
INSERT INTO "auth_user_user_permissions" VALUES (27,2,27);
INSERT INTO "auth_user_user_permissions" VALUES (28,2,28);
INSERT INTO "auth_user_user_permissions" VALUES (29,2,29);
INSERT INTO "auth_user_user_permissions" VALUES (30,2,30);
INSERT INTO "auth_user_user_permissions" VALUES (31,2,31);
INSERT INTO "auth_user_user_permissions" VALUES (32,2,32);
INSERT INTO "auth_user_user_permissions" VALUES (33,2,33);
INSERT INTO "auth_user_user_permissions" VALUES (34,2,34);
INSERT INTO "auth_user_user_permissions" VALUES (35,2,35);
INSERT INTO "auth_user_user_permissions" VALUES (36,2,36);
INSERT INTO "auth_user_user_permissions" VALUES (37,2,37);
INSERT INTO "auth_user_user_permissions" VALUES (38,2,38);
INSERT INTO "auth_user_user_permissions" VALUES (39,2,39);
INSERT INTO "auth_user_user_permissions" VALUES (40,2,40);
INSERT INTO "auth_user_user_permissions" VALUES (41,2,41);
INSERT INTO "auth_user_user_permissions" VALUES (42,2,42);
INSERT INTO "auth_user_user_permissions" VALUES (43,2,43);
INSERT INTO "auth_user_user_permissions" VALUES (44,2,44);
INSERT INTO "auth_user_user_permissions" VALUES (45,2,45);
INSERT INTO "auth_user_user_permissions" VALUES (46,2,46);
INSERT INTO "auth_user_user_permissions" VALUES (47,2,47);
INSERT INTO "auth_user_user_permissions" VALUES (48,2,48);
INSERT INTO "auth_user_user_permissions" VALUES (49,2,49);
INSERT INTO "auth_user_user_permissions" VALUES (50,2,50);
INSERT INTO "auth_user_user_permissions" VALUES (51,2,51);
INSERT INTO "auth_user_user_permissions" VALUES (52,2,52);
INSERT INTO "auth_user_user_permissions" VALUES (53,2,53);
INSERT INTO "auth_user_user_permissions" VALUES (54,2,54);
INSERT INTO "auth_user_user_permissions" VALUES (55,2,55);
INSERT INTO "auth_user_user_permissions" VALUES (56,2,56);
INSERT INTO "auth_user_user_permissions" VALUES (57,2,57);
INSERT INTO "auth_user_user_permissions" VALUES (58,2,58);
INSERT INTO "auth_user_user_permissions" VALUES (59,2,59);
INSERT INTO "auth_user_user_permissions" VALUES (60,2,60);
INSERT INTO "auth_user_user_permissions" VALUES (61,2,61);
INSERT INTO "auth_user_user_permissions" VALUES (62,2,62);
INSERT INTO "auth_user_user_permissions" VALUES (63,2,63);
INSERT INTO "auth_user_user_permissions" VALUES (64,2,64);
INSERT INTO "auth_user_user_permissions" VALUES (65,2,65);
INSERT INTO "auth_user_user_permissions" VALUES (66,2,66);
INSERT INTO "auth_user_user_permissions" VALUES (67,2,67);
INSERT INTO "auth_user_user_permissions" VALUES (68,2,68);
INSERT INTO "auth_user_user_permissions" VALUES (69,2,69);
INSERT INTO "auth_user_user_permissions" VALUES (70,2,70);
INSERT INTO "auth_user_user_permissions" VALUES (71,2,71);
INSERT INTO "auth_user_user_permissions" VALUES (72,2,72);
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_todo','Can add todo');
INSERT INTO "auth_permission" VALUES (26,7,'change_todo','Can change todo');
INSERT INTO "auth_permission" VALUES (27,7,'delete_todo','Can delete todo');
INSERT INTO "auth_permission" VALUES (28,7,'view_todo','Can view todo');
INSERT INTO "auth_permission" VALUES (29,8,'add_calendar','Can add calendar');
INSERT INTO "auth_permission" VALUES (30,8,'change_calendar','Can change calendar');
INSERT INTO "auth_permission" VALUES (31,8,'delete_calendar','Can delete calendar');
INSERT INTO "auth_permission" VALUES (32,8,'view_calendar','Can view calendar');
INSERT INTO "auth_permission" VALUES (33,9,'add_userinitials','Can add user initials');
INSERT INTO "auth_permission" VALUES (34,9,'change_userinitials','Can change user initials');
INSERT INTO "auth_permission" VALUES (35,9,'delete_userinitials','Can delete user initials');
INSERT INTO "auth_permission" VALUES (36,9,'view_userinitials','Can view user initials');
INSERT INTO "auth_permission" VALUES (37,10,'add_shift','Can add shift');
INSERT INTO "auth_permission" VALUES (38,10,'change_shift','Can change shift');
INSERT INTO "auth_permission" VALUES (39,10,'delete_shift','Can delete shift');
INSERT INTO "auth_permission" VALUES (40,10,'view_shift','Can view shift');
INSERT INTO "auth_permission" VALUES (41,11,'add_shifttype','Can add shift type');
INSERT INTO "auth_permission" VALUES (42,11,'change_shifttype','Can change shift type');
INSERT INTO "auth_permission" VALUES (43,11,'delete_shifttype','Can delete shift type');
INSERT INTO "auth_permission" VALUES (44,11,'view_shifttype','Can view shift type');
INSERT INTO "auth_permission" VALUES (45,12,'add_scheduleshift','Can add schedule shift');
INSERT INTO "auth_permission" VALUES (46,12,'change_scheduleshift','Can change schedule shift');
INSERT INTO "auth_permission" VALUES (47,12,'delete_scheduleshift','Can delete schedule shift');
INSERT INTO "auth_permission" VALUES (48,12,'view_scheduleshift','Can view schedule shift');
INSERT INTO "auth_permission" VALUES (49,13,'add_citystate','Can add city state');
INSERT INTO "auth_permission" VALUES (50,13,'change_citystate','Can change city state');
INSERT INTO "auth_permission" VALUES (51,13,'delete_citystate','Can delete city state');
INSERT INTO "auth_permission" VALUES (52,13,'view_citystate','Can view city state');
INSERT INTO "auth_permission" VALUES (53,14,'add_zipcode','Can add zipcode');
INSERT INTO "auth_permission" VALUES (54,14,'change_zipcode','Can change zipcode');
INSERT INTO "auth_permission" VALUES (55,14,'delete_zipcode','Can delete zipcode');
INSERT INTO "auth_permission" VALUES (56,14,'view_zipcode','Can view zipcode');
INSERT INTO "auth_permission" VALUES (57,15,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (58,15,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (59,15,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (60,15,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (61,16,'add_user_type','Can add user_ type');
INSERT INTO "auth_permission" VALUES (62,16,'change_user_type','Can change user_ type');
INSERT INTO "auth_permission" VALUES (63,16,'delete_user_type','Can delete user_ type');
INSERT INTO "auth_permission" VALUES (64,16,'view_user_type','Can view user_ type');
INSERT INTO "auth_permission" VALUES (65,17,'add_address','Can add address');
INSERT INTO "auth_permission" VALUES (66,17,'change_address','Can change address');
INSERT INTO "auth_permission" VALUES (67,17,'delete_address','Can delete address');
INSERT INTO "auth_permission" VALUES (68,17,'view_address','Can view address');
INSERT INTO "auth_permission" VALUES (69,18,'add_user_level','Can add user_ level');
INSERT INTO "auth_permission" VALUES (70,18,'change_user_level','Can change user_ level');
INSERT INTO "auth_permission" VALUES (71,18,'delete_user_level','Can delete user_ level');
INSERT INTO "auth_permission" VALUES (72,18,'view_user_level','Can view user_ level');
INSERT INTO "auth_permission" VALUES (73,19,'add_user_info','Can add user_ info');
INSERT INTO "auth_permission" VALUES (74,19,'change_user_info','Can change user_ info');
INSERT INTO "auth_permission" VALUES (75,19,'delete_user_info','Can delete user_ info');
INSERT INTO "auth_permission" VALUES (76,19,'view_user_info','Can view user_ info');
INSERT INTO "auth_permission" VALUES (77,20,'add_accesslevel','Can add access level');
INSERT INTO "auth_permission" VALUES (78,20,'change_accesslevel','Can change access level');
INSERT INTO "auth_permission" VALUES (79,20,'delete_accesslevel','Can delete access level');
INSERT INTO "auth_permission" VALUES (80,20,'view_accesslevel','Can view access level');
INSERT INTO "auth_permission" VALUES (81,21,'add_occupation','Can add occupation');
INSERT INTO "auth_permission" VALUES (82,21,'change_occupation','Can change occupation');
INSERT INTO "auth_permission" VALUES (83,21,'delete_occupation','Can delete occupation');
INSERT INTO "auth_permission" VALUES (84,21,'view_occupation','Can view occupation');
INSERT INTO "auth_permission" VALUES (85,22,'add_phone','Can add phone');
INSERT INTO "auth_permission" VALUES (86,22,'change_phone','Can change phone');
INSERT INTO "auth_permission" VALUES (87,22,'delete_phone','Can delete phone');
INSERT INTO "auth_permission" VALUES (88,22,'view_phone','Can view phone');
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$600000$MgwxDYIXXSW8b4RUsDduOX$oOiXlwb4YHnmzbhDsHV+yQafDc83oqXqjSsTkPpz6PU=','2023-11-07 00:12:23',1,'SuperBear','','calisurfr22@yahoo.com',1,1,'2023-05-04 21:41:58','');
INSERT INTO "auth_user" VALUES (2,'pbkdf2_sha256$600000$xdN0qDDtu43FhiHOCPwZ0l$ZByn33ZDvE1NLOLTGWIRglPZuNSyOctcd8Eijf0rHR4=',NULL,0,'JMeyer','Meyer','jgmeyer82@gmail.com',0,1,'2023-11-07 00:14:23','Jesse');
INSERT INTO "VetCalendar_calendar" VALUES (1032,'AC','','2023-06-01 14:00:00','2023-06-02 02:00:00','06',2023,'2023-09-27 15:50:36.629908','2023-09-27 15:50:36.629908');
INSERT INTO "VetCalendar_calendar" VALUES (1033,'AC','','2023-06-02 14:00:00','2023-06-03 02:00:00','06',2023,'2023-09-27 15:50:36.636232','2023-09-27 15:50:36.636232');
INSERT INTO "VetCalendar_calendar" VALUES (1034,'AC','','2023-06-03 14:00:00','2023-06-04 02:00:00','06',2023,'2023-09-27 15:50:36.641091','2023-09-27 15:50:36.641091');
INSERT INTO "VetCalendar_calendar" VALUES (1035,'JE','','2023-06-01 17:00:00','2023-06-02 05:00:00','06',2023,'2023-09-27 15:50:36.647850','2023-09-27 15:50:36.647850');
INSERT INTO "VetCalendar_calendar" VALUES (1036,'JE','','2023-06-02 17:00:00','2023-06-03 05:00:00','06',2023,'2023-09-27 15:50:36.653277','2023-09-27 15:50:36.653277');
INSERT INTO "VetCalendar_calendar" VALUES (1037,'NW','','2023-06-03 17:00:00','2023-06-04 05:00:00','06',2023,'2023-09-27 15:50:36.657143','2023-09-27 15:50:36.657143');
INSERT INTO "VetCalendar_calendar" VALUES (1038,'MC','','2023-06-01 21:00:00','2023-06-02 09:00:00','06',2023,'2023-09-27 15:50:36.665480','2023-09-27 15:50:36.665480');
INSERT INTO "VetCalendar_calendar" VALUES (1039,'DH','','2023-06-02 21:00:00','2023-06-03 09:00:00','06',2023,'2023-09-27 15:50:36.669996','2023-09-27 15:50:36.669996');
INSERT INTO "VetCalendar_calendar" VALUES (1040,'DH','','2023-06-03 21:00:00','2023-06-04 09:00:00','06',2023,'2023-09-27 15:50:36.675473','2023-09-27 15:50:36.675473');
INSERT INTO "VetCalendar_calendar" VALUES (1041,'NB','','2023-06-02 01:00:00','2023-06-02 13:00:00','06',2023,'2023-09-27 15:50:36.681970','2023-09-27 15:50:36.681970');
INSERT INTO "VetCalendar_calendar" VALUES (1042,'SM','','2023-06-03 01:00:00','2023-06-03 13:00:00','06',2023,'2023-09-27 15:50:36.687130','2023-09-27 15:50:36.687130');
INSERT INTO "VetCalendar_calendar" VALUES (1043,'SM','','2023-06-04 01:00:00','2023-06-04 13:00:00','06',2023,'2023-09-27 15:50:36.693577','2023-09-27 15:50:36.693577');
INSERT INTO "VetCalendar_calendar" VALUES (1044,'TR','','2023-06-04 14:00:00','2023-06-05 02:00:00','06',2023,'2023-09-27 15:50:36.699250','2023-09-27 15:50:36.699250');
INSERT INTO "VetCalendar_calendar" VALUES (1045,'ST','','2023-06-05 14:00:00','2023-06-06 02:00:00','06',2023,'2023-09-27 15:50:36.706202','2023-09-27 15:50:36.706202');
INSERT INTO "VetCalendar_calendar" VALUES (1046,'ST','','2023-06-06 14:00:00','2023-06-07 02:00:00','06',2023,'2023-09-27 15:50:36.713134','2023-09-27 15:50:36.713134');
INSERT INTO "VetCalendar_calendar" VALUES (1047,'MA','','2023-06-07 14:00:00','2023-06-08 02:00:00','06',2023,'2023-09-27 15:50:36.719154','2023-09-27 15:50:36.719154');
INSERT INTO "VetCalendar_calendar" VALUES (1048,'NW','','2023-06-08 14:00:00','2023-06-09 02:00:00','06',2023,'2023-09-27 15:50:36.724186','2023-09-27 15:50:36.724186');
INSERT INTO "VetCalendar_calendar" VALUES (1049,'AC','','2023-06-09 14:00:00','2023-06-10 02:00:00','06',2023,'2023-09-27 15:50:36.731957','2023-09-27 15:50:36.731957');
INSERT INTO "VetCalendar_calendar" VALUES (1050,'AC','','2023-06-10 14:00:00','2023-06-11 02:00:00','06',2023,'2023-09-27 15:50:36.735969','2023-09-27 15:50:36.735969');
INSERT INTO "VetCalendar_calendar" VALUES (1051,'NW','','2023-06-04 17:00:00','2023-06-05 05:00:00','06',2023,'2023-09-27 15:50:36.743179','2023-09-27 15:50:36.743179');
INSERT INTO "VetCalendar_calendar" VALUES (1052,'TR','','2023-06-05 17:00:00','2023-06-06 05:00:00','06',2023,'2023-09-27 15:50:36.749397','2023-09-27 15:50:36.749397');
INSERT INTO "VetCalendar_calendar" VALUES (1053,'TR','','2023-06-06 17:00:00','2023-06-07 05:00:00','06',2023,'2023-09-27 15:50:36.755711','2023-09-27 15:50:36.755711');
INSERT INTO "VetCalendar_calendar" VALUES (1054,'JS','','2023-06-07 17:00:00','2023-06-08 05:00:00','06',2023,'2023-09-27 15:50:36.760918','2023-09-27 15:50:36.760918');
INSERT INTO "VetCalendar_calendar" VALUES (1055,'BC','','2023-06-08 17:00:00','2023-06-09 05:00:00','06',2023,'2023-09-27 15:50:36.766475','2023-09-27 15:50:36.766475');
INSERT INTO "VetCalendar_calendar" VALUES (1056,'TR','','2023-06-09 17:00:00','2023-06-10 05:00:00','06',2023,'2023-09-27 15:50:36.772374','2023-09-27 15:50:36.772374');
INSERT INTO "VetCalendar_calendar" VALUES (1057,'MA','','2023-06-10 17:00:00','2023-06-11 05:00:00','06',2023,'2023-09-27 15:50:36.777292','2023-09-27 15:50:36.777292');
INSERT INTO "VetCalendar_calendar" VALUES (1058,'DH','','2023-06-04 21:00:00','2023-06-05 09:00:00','06',2023,'2023-09-27 15:50:36.783418','2023-09-27 15:50:36.783418');
INSERT INTO "VetCalendar_calendar" VALUES (1059,'MW','','2023-06-05 21:00:00','2023-06-06 09:00:00','06',2023,'2023-09-27 15:50:36.788971','2023-09-27 15:50:36.788971');
INSERT INTO "VetCalendar_calendar" VALUES (1060,'MW','','2023-06-06 21:00:00','2023-06-07 09:00:00','06',2023,'2023-09-27 15:50:36.795447','2023-09-27 15:50:36.795447');
INSERT INTO "VetCalendar_calendar" VALUES (1061,'MW','','2023-06-07 21:00:00','2023-06-08 09:00:00','06',2023,'2023-09-27 15:50:36.800006','2023-09-27 15:50:36.800006');
INSERT INTO "VetCalendar_calendar" VALUES (1062,'CC','','2023-06-08 21:00:00','2023-06-09 09:00:00','06',2023,'2023-09-27 15:50:36.805760','2023-09-27 15:50:36.805760');
INSERT INTO "VetCalendar_calendar" VALUES (1063,'CC','','2023-06-09 21:00:00','2023-06-10 09:00:00','06',2023,'2023-09-27 15:50:36.811812','2023-09-27 15:50:36.811812');
INSERT INTO "VetCalendar_calendar" VALUES (1064,'NW','','2023-06-10 21:00:00','2023-06-11 09:00:00','06',2023,'2023-09-27 15:50:36.817494','2023-09-27 15:50:36.817494');
INSERT INTO "VetCalendar_calendar" VALUES (1065,'SM','','2023-06-05 01:00:00','2023-06-05 13:00:00','06',2023,'2023-09-27 15:50:36.823112','2023-09-27 15:50:36.823112');
INSERT INTO "VetCalendar_calendar" VALUES (1066,'NB','','2023-06-06 01:00:00','2023-06-06 13:00:00','06',2023,'2023-09-27 15:50:36.826269','2023-09-27 15:50:36.826269');
INSERT INTO "VetCalendar_calendar" VALUES (1067,'NB','','2023-06-07 01:00:00','2023-06-07 13:00:00','06',2023,'2023-09-27 15:50:36.834642','2023-09-27 15:50:36.834642');
INSERT INTO "VetCalendar_calendar" VALUES (1068,'NB','','2023-06-08 01:00:00','2023-06-08 13:00:00','06',2023,'2023-09-27 15:50:36.839015','2023-09-27 15:50:36.839015');
INSERT INTO "VetCalendar_calendar" VALUES (1069,'SM','','2023-06-09 01:00:00','2023-06-09 13:00:00','06',2023,'2023-09-27 15:50:36.845478','2023-09-27 15:50:36.845478');
INSERT INTO "VetCalendar_calendar" VALUES (1070,'JE','','2023-06-10 01:00:00','2023-06-10 13:00:00','06',2023,'2023-09-27 15:50:36.851401','2023-09-27 15:50:36.851401');
INSERT INTO "VetCalendar_calendar" VALUES (1071,'JE','','2023-06-11 01:00:00','2023-06-11 13:00:00','06',2023,'2023-09-27 15:50:36.857503','2023-09-27 15:50:36.857503');
INSERT INTO "VetCalendar_calendar" VALUES (1072,'DH','','2023-06-11 14:00:00','2023-06-12 02:00:00','06',2023,'2023-09-27 15:50:36.863654','2023-09-27 15:50:36.863654');
INSERT INTO "VetCalendar_calendar" VALUES (1073,'DH','','2023-06-12 14:00:00','2023-06-13 02:00:00','06',2023,'2023-09-27 15:50:36.871002','2023-09-27 15:50:36.871002');
INSERT INTO "VetCalendar_calendar" VALUES (1074,'TR','','2023-06-13 14:00:00','2023-06-14 02:00:00','06',2023,'2023-09-27 15:50:36.876724','2023-09-27 15:50:36.876724');
INSERT INTO "VetCalendar_calendar" VALUES (1075,'AC','','2023-06-14 14:00:00','2023-06-15 02:00:00','06',2023,'2023-09-27 15:50:36.882557','2023-09-27 15:50:36.882557');
INSERT INTO "VetCalendar_calendar" VALUES (1076,'AC','','2023-06-15 14:00:00','2023-06-16 02:00:00','06',2023,'2023-09-27 15:50:36.888574','2023-09-27 15:50:36.888574');
INSERT INTO "VetCalendar_calendar" VALUES (1077,'AC','','2023-06-16 14:00:00','2023-06-17 02:00:00','06',2023,'2023-09-27 15:50:36.893323','2023-09-27 15:50:36.893323');
INSERT INTO "VetCalendar_calendar" VALUES (1078,'SM','','2023-06-17 14:00:00','2023-06-18 02:00:00','06',2023,'2023-09-27 15:50:36.899830','2023-09-27 15:50:36.899830');
INSERT INTO "VetCalendar_calendar" VALUES (1079,'MA','','2023-06-11 17:00:00','2023-06-12 05:00:00','06',2023,'2023-09-27 15:50:36.905763','2023-09-27 15:50:36.905763');
INSERT INTO "VetCalendar_calendar" VALUES (1080,'MA','','2023-06-12 17:00:00','2023-06-13 05:00:00','06',2023,'2023-09-27 15:50:36.911284','2023-09-27 15:50:36.911284');
INSERT INTO "VetCalendar_calendar" VALUES (1081,'CC','','2023-06-13 17:00:00','2023-06-14 05:00:00','06',2023,'2023-09-27 15:50:36.919436','2023-09-27 15:50:36.919436');
INSERT INTO "VetCalendar_calendar" VALUES (1082,'TR','','2023-06-14 17:00:00','2023-06-15 05:00:00','06',2023,'2023-09-27 15:50:36.924882','2023-09-27 15:50:36.924882');
INSERT INTO "VetCalendar_calendar" VALUES (1083,'JK','','2023-06-15 17:00:00','2023-06-16 05:00:00','06',2023,'2023-09-27 15:50:36.935938','2023-09-27 15:50:36.935938');
INSERT INTO "VetCalendar_calendar" VALUES (1084,'JE','','2023-06-16 17:00:00','2023-06-17 05:00:00','06',2023,'2023-09-27 15:50:36.938341','2023-09-27 15:50:36.938341');
INSERT INTO "VetCalendar_calendar" VALUES (1085,'JE','','2023-06-17 17:00:00','2023-06-18 05:00:00','06',2023,'2023-09-27 15:50:36.949497','2023-09-27 15:50:36.949497');
INSERT INTO "VetCalendar_calendar" VALUES (1086,'NW','','2023-06-11 21:00:00','2023-06-12 09:00:00','06',2023,'2023-09-27 15:50:36.955643','2023-09-27 15:50:36.955643');
INSERT INTO "VetCalendar_calendar" VALUES (1087,'NW','','2023-06-12 21:00:00','2023-06-13 09:00:00','06',2023,'2023-09-27 15:50:36.961795','2023-09-27 15:50:36.961795');
INSERT INTO "VetCalendar_calendar" VALUES (1088,'SM','','2023-06-13 21:00:00','2023-06-14 09:00:00','06',2023,'2023-09-27 15:50:36.969154','2023-09-27 15:50:36.969154');
INSERT INTO "VetCalendar_calendar" VALUES (1089,'MC','','2023-06-14 21:00:00','2023-06-15 09:00:00','06',2023,'2023-09-27 15:50:36.974890','2023-09-27 15:50:36.974890');
INSERT INTO "VetCalendar_calendar" VALUES (1090,'MW','','2023-06-15 21:00:00','2023-06-16 09:00:00','06',2023,'2023-09-27 15:50:36.981296','2023-09-27 15:50:36.981296');
INSERT INTO "VetCalendar_calendar" VALUES (1091,'UCC','','2023-06-16 21:00:00','2023-06-17 09:00:00','06',2023,'2023-09-27 15:50:36.987216','2023-09-27 15:50:36.987216');
INSERT INTO "VetCalendar_calendar" VALUES (1092,'CC','','2023-06-17 21:00:00','2023-06-18 09:00:00','06',2023,'2023-09-27 15:50:36.993506','2023-09-27 15:50:36.993506');
INSERT INTO "VetCalendar_calendar" VALUES (1093,'JE','','2023-06-12 01:00:00','2023-06-12 13:00:00','06',2023,'2023-09-27 15:50:36.998608','2023-09-27 15:50:36.998608');
INSERT INTO "VetCalendar_calendar" VALUES (1094,'NB','','2023-06-13 01:00:00','2023-06-13 13:00:00','06',2023,'2023-09-27 15:50:37.005395','2023-09-27 15:50:37.005395');
INSERT INTO "VetCalendar_calendar" VALUES (1095,'NB','','2023-06-14 01:00:00','2023-06-14 13:00:00','06',2023,'2023-09-27 15:50:37.010201','2023-09-27 15:50:37.010201');
INSERT INTO "VetCalendar_calendar" VALUES (1096,'NB','','2023-06-15 01:00:00','2023-06-15 13:00:00','06',2023,'2023-09-27 15:50:37.016166','2023-09-27 15:50:37.016166');
INSERT INTO "VetCalendar_calendar" VALUES (1097,'DH','','2023-06-16 01:00:00','2023-06-16 13:00:00','06',2023,'2023-09-27 15:50:37.021357','2023-09-27 15:50:37.021357');
INSERT INTO "VetCalendar_calendar" VALUES (1098,'DH','','2023-06-17 01:00:00','2023-06-17 13:00:00','06',2023,'2023-09-27 15:50:37.027982','2023-09-27 15:50:37.027982');
INSERT INTO "VetCalendar_calendar" VALUES (1099,'TR','','2023-06-18 01:00:00','2023-06-18 13:00:00','06',2023,'2023-09-27 15:50:37.034328','2023-09-27 15:50:37.034328');
INSERT INTO "VetCalendar_calendar" VALUES (1100,'SM','','2023-06-18 14:00:00','2023-06-19 02:00:00','06',2023,'2023-09-27 15:50:37.038929','2023-09-27 15:50:37.038929');
INSERT INTO "VetCalendar_calendar" VALUES (1101,'SM','','2023-06-19 14:00:00','2023-06-20 02:00:00','06',2023,'2023-09-27 15:50:37.045436','2023-09-27 15:50:37.045436');
INSERT INTO "VetCalendar_calendar" VALUES (1102,'MA','','2023-06-20 14:00:00','2023-06-21 02:00:00','06',2023,'2023-09-27 15:50:37.051711','2023-09-27 15:50:37.051711');
INSERT INTO "VetCalendar_calendar" VALUES (1103,'MA','','2023-06-21 14:00:00','2023-06-22 02:00:00','06',2023,'2023-09-27 15:50:37.057391','2023-09-27 15:50:37.057391');
INSERT INTO "VetCalendar_calendar" VALUES (1104,'AC','','2023-06-22 14:00:00','2023-06-23 02:00:00','06',2023,'2023-09-27 15:50:37.061668','2023-09-27 15:50:37.063152');
INSERT INTO "VetCalendar_calendar" VALUES (1105,'AC','','2023-06-23 14:00:00','2023-06-24 02:00:00','06',2023,'2023-09-27 15:50:37.068901','2023-09-27 15:50:37.068901');
INSERT INTO "VetCalendar_calendar" VALUES (1106,'AC','','2023-06-24 14:00:00','2023-06-25 02:00:00','06',2023,'2023-09-27 15:50:37.073454','2023-09-27 15:50:37.073454');
INSERT INTO "VetCalendar_calendar" VALUES (1107,'JE','','2023-06-18 17:00:00','2023-06-19 05:00:00','06',2023,'2023-09-27 15:50:37.078821','2023-09-27 15:50:37.078821');
INSERT INTO "VetCalendar_calendar" VALUES (1108,'JC','','2023-06-19 17:00:00','2023-06-20 05:00:00','06',2023,'2023-09-27 15:50:37.086089','2023-09-27 15:50:37.086089');
INSERT INTO "VetCalendar_calendar" VALUES (1109,'ST','','2023-06-20 17:00:00','2023-06-21 05:00:00','06',2023,'2023-09-27 15:50:37.090196','2023-09-27 15:50:37.090196');
INSERT INTO "VetCalendar_calendar" VALUES (1110,'JK','','2023-06-21 17:00:00','2023-06-22 05:00:00','06',2023,'2023-09-27 15:50:37.095227','2023-09-27 15:50:37.096481');
INSERT INTO "VetCalendar_calendar" VALUES (1111,'JK','','2023-06-22 17:00:00','2023-06-23 05:00:00','06',2023,'2023-09-27 15:50:37.101894','2023-09-27 15:50:37.101894');
INSERT INTO "VetCalendar_calendar" VALUES (1112,'CC','','2023-06-23 17:00:00','2023-06-24 05:00:00','06',2023,'2023-09-27 15:50:37.106429','2023-09-27 15:50:37.106429');
INSERT INTO "VetCalendar_calendar" VALUES (1113,'CC','','2023-06-24 17:00:00','2023-06-25 05:00:00','06',2023,'2023-09-27 15:50:37.110780','2023-09-27 15:50:37.110780');
INSERT INTO "VetCalendar_calendar" VALUES (1114,'CC','','2023-06-18 21:00:00','2023-06-19 09:00:00','06',2023,'2023-09-27 15:50:37.118608','2023-09-27 15:50:37.118608');
INSERT INTO "VetCalendar_calendar" VALUES (1115,'SB','','2023-06-19 21:00:00','2023-06-20 09:00:00','06',2023,'2023-09-27 15:50:37.124583','2023-09-27 15:50:37.124583');
INSERT INTO "VetCalendar_calendar" VALUES (1116,'DH','','2023-06-20 21:00:00','2023-06-21 09:00:00','06',2023,'2023-09-27 15:50:37.130280','2023-09-27 15:50:37.130280');
INSERT INTO "VetCalendar_calendar" VALUES (1117,'DH','','2023-06-21 21:00:00','2023-06-22 09:00:00','06',2023,'2023-09-27 15:50:37.136583','2023-09-27 15:50:37.136583');
INSERT INTO "VetCalendar_calendar" VALUES (1118,'JE','','2023-06-22 21:00:00','2023-06-23 09:00:00','06',2023,'2023-09-27 15:50:37.141455','2023-09-27 15:50:37.141455');
INSERT INTO "VetCalendar_calendar" VALUES (1119,'JE','','2023-06-23 21:00:00','2023-06-24 09:00:00','06',2023,'2023-09-27 15:50:37.148553','2023-09-27 15:50:37.148553');
INSERT INTO "VetCalendar_calendar" VALUES (1120,'MA','','2023-06-24 21:00:00','2023-06-25 09:00:00','06',2023,'2023-09-27 15:50:37.153580','2023-09-27 15:50:37.153580');
INSERT INTO "VetCalendar_calendar" VALUES (1121,'TR','','2023-06-19 01:00:00','2023-06-19 13:00:00','06',2023,'2023-09-27 15:50:37.155851','2023-09-27 15:50:37.155851');
INSERT INTO "VetCalendar_calendar" VALUES (1122,'TR','','2023-06-20 01:00:00','2023-06-20 13:00:00','06',2023,'2023-09-27 15:50:37.166222','2023-09-27 15:50:37.166222');
INSERT INTO "VetCalendar_calendar" VALUES (1123,'NW','','2023-06-21 01:00:00','2023-06-21 13:00:00','06',2023,'2023-09-27 15:50:37.171882','2023-09-27 15:50:37.171882');
INSERT INTO "VetCalendar_calendar" VALUES (1124,'NW','','2023-06-22 01:00:00','2023-06-22 13:00:00','06',2023,'2023-09-27 15:50:37.178480','2023-09-27 15:50:37.178480');
INSERT INTO "VetCalendar_calendar" VALUES (1125,'ST','','2023-06-23 01:00:00','2023-06-23 13:00:00','06',2023,'2023-09-27 15:50:37.184100','2023-09-27 15:50:37.184100');
INSERT INTO "VetCalendar_calendar" VALUES (1126,'NB','','2023-06-24 01:00:00','2023-06-24 13:00:00','06',2023,'2023-09-27 15:50:37.190109','2023-09-27 15:50:37.190109');
INSERT INTO "VetCalendar_calendar" VALUES (1127,'NB','','2023-06-25 01:00:00','2023-06-25 13:00:00','06',2023,'2023-09-27 15:50:37.196712','2023-09-27 15:50:37.196712');
INSERT INTO "VetCalendar_calendar" VALUES (1128,'DH','','2023-06-25 14:00:00','2023-06-26 02:00:00','06',2023,'2023-09-27 15:50:37.203499','2023-09-27 15:50:37.203499');
INSERT INTO "VetCalendar_calendar" VALUES (1129,'ST','','2023-06-26 14:00:00','2023-06-27 02:00:00','06',2023,'2023-09-27 15:50:37.208901','2023-09-27 15:50:37.208901');
INSERT INTO "VetCalendar_calendar" VALUES (1130,'ST','','2023-06-27 14:00:00','2023-06-28 02:00:00','06',2023,'2023-09-27 15:50:37.215617','2023-09-27 15:50:37.215617');
INSERT INTO "VetCalendar_calendar" VALUES (1131,'AC','','2023-06-28 14:00:00','2023-06-29 02:00:00','06',2023,'2023-09-27 15:50:37.221519','2023-09-27 15:50:37.221519');
INSERT INTO "VetCalendar_calendar" VALUES (1132,'AC','','2023-06-29 14:00:00','2023-06-30 02:00:00','06',2023,'2023-09-27 15:50:37.226926','2023-09-27 15:50:37.226926');
INSERT INTO "VetCalendar_calendar" VALUES (1133,'SM','','2023-06-30 14:00:00','2023-07-01 02:00:00','06',2023,'2023-09-27 15:50:37.233458','2023-09-27 15:50:37.233458');
INSERT INTO "VetCalendar_calendar" VALUES (1134,'CC','','2023-06-25 17:00:00','2023-06-26 05:00:00','06',2023,'2023-09-27 15:50:37.238467','2023-09-27 15:50:37.238467');
INSERT INTO "VetCalendar_calendar" VALUES (1135,'DH','','2023-06-26 17:00:00','2023-06-27 05:00:00','06',2023,'2023-09-27 15:50:37.249784','2023-09-27 15:50:37.249784');
INSERT INTO "VetCalendar_calendar" VALUES (1136,'DH','','2023-06-27 17:00:00','2023-06-28 05:00:00','06',2023,'2023-09-27 15:50:37.256993','2023-09-27 15:50:37.256993');
INSERT INTO "VetCalendar_calendar" VALUES (1137,'JK','','2023-06-28 17:00:00','2023-06-29 05:00:00','06',2023,'2023-09-27 15:50:37.263447','2023-09-27 15:50:37.263447');
INSERT INTO "VetCalendar_calendar" VALUES (1138,'JE','','2023-06-29 17:00:00','2023-06-30 05:00:00','06',2023,'2023-09-27 15:50:37.268459','2023-09-27 15:50:37.268459');
INSERT INTO "VetCalendar_calendar" VALUES (1139,'JE','','2023-06-30 17:00:00','2023-07-01 05:00:00','06',2023,'2023-09-27 15:50:37.275559','2023-09-27 15:50:37.275559');
INSERT INTO "VetCalendar_calendar" VALUES (1140,'MA','','2023-06-25 21:00:00','2023-06-26 09:00:00','06',2023,'2023-09-27 15:50:37.281753','2023-09-27 15:50:37.281753');
INSERT INTO "VetCalendar_calendar" VALUES (1141,'MA','','2023-06-26 21:00:00','2023-06-27 09:00:00','06',2023,'2023-09-27 15:50:37.287565','2023-09-27 15:50:37.287565');
INSERT INTO "VetCalendar_calendar" VALUES (1142,'NW','','2023-06-27 21:00:00','2023-06-28 09:00:00','06',2023,'2023-09-27 15:50:37.293490','2023-09-27 15:50:37.293490');
INSERT INTO "VetCalendar_calendar" VALUES (1143,'CC','','2023-06-28 21:00:00','2023-06-29 09:00:00','06',2023,'2023-09-27 15:50:37.299803','2023-09-27 15:50:37.299803');
INSERT INTO "VetCalendar_calendar" VALUES (1144,'CC','','2023-06-29 21:00:00','2023-06-30 09:00:00','06',2023,'2023-09-27 15:50:37.304316','2023-09-27 15:50:37.304316');
INSERT INTO "VetCalendar_calendar" VALUES (1145,'MA','','2023-06-30 21:00:00','2023-07-01 09:00:00','06',2023,'2023-09-27 15:50:37.309747','2023-09-27 15:50:37.309747');
INSERT INTO "VetCalendar_calendar" VALUES (1146,'NB','','2023-06-26 01:00:00','2023-06-26 13:00:00','06',2023,'2023-09-27 15:50:37.316228','2023-09-27 15:50:37.316228');
INSERT INTO "VetCalendar_calendar" VALUES (1147,'TR','','2023-06-27 01:00:00','2023-06-27 13:00:00','06',2023,'2023-09-27 15:50:37.321419','2023-09-27 15:50:37.321419');
INSERT INTO "VetCalendar_calendar" VALUES (1148,'TR','','2023-06-28 01:00:00','2023-06-28 13:00:00','06',2023,'2023-09-27 15:50:37.326388','2023-09-27 15:50:37.326388');
INSERT INTO "VetCalendar_calendar" VALUES (1149,'TR','','2023-06-29 01:00:00','2023-06-29 13:00:00','06',2023,'2023-09-27 15:50:37.332369','2023-09-27 15:50:37.332369');
INSERT INTO "VetCalendar_calendar" VALUES (1150,'NB','','2023-06-30 01:00:00','2023-06-30 13:00:00','06',2023,'2023-09-27 15:50:37.337566','2023-09-27 15:50:37.337566');
INSERT INTO "VetCalendar_calendar" VALUES (1151,'NB','','2023-07-01 01:00:00','2023-07-01 13:00:00','06',2023,'2023-09-27 15:50:37.341476','2023-09-27 15:50:37.342883');
INSERT INTO "VetCalendar_calendar" VALUES (1270,'TR','','2023-07-30 14:00:00','2023-07-31 02:00:00','07',2023,'2023-09-27 23:09:46.321661','2023-09-27 23:09:46.321661');
INSERT INTO "VetCalendar_calendar" VALUES (1271,'ST','','2023-07-31 14:00:00','2023-08-01 02:00:00','07',2023,'2023-09-27 23:09:46.326725','2023-09-27 23:09:46.326725');
INSERT INTO "VetCalendar_calendar" VALUES (1272,'SM','','2023-07-01 14:00:00','2023-07-02 02:00:00','07',2023,'2023-09-27 23:09:46.331726','2023-09-27 23:09:46.331726');
INSERT INTO "VetCalendar_calendar" VALUES (1273,'DH','','2023-07-30 17:00:00','2023-07-31 05:00:00','07',2023,'2023-09-27 23:09:46.335690','2023-09-27 23:09:46.335690');
INSERT INTO "VetCalendar_calendar" VALUES (1274,'TR','','2023-07-31 17:00:00','2023-08-01 05:00:00','07',2023,'2023-09-27 23:09:46.340740','2023-09-27 23:09:46.340740');
INSERT INTO "VetCalendar_calendar" VALUES (1275,'JE','','2023-07-01 17:00:00','2023-07-02 05:00:00','07',2023,'2023-09-27 23:09:46.346348','2023-09-27 23:09:46.346348');
INSERT INTO "VetCalendar_calendar" VALUES (1276,'MA','','2023-07-30 21:00:00','2023-07-31 09:00:00','07',2023,'2023-09-27 23:09:46.351154','2023-09-27 23:09:46.351154');
INSERT INTO "VetCalendar_calendar" VALUES (1277,'MA','','2023-07-31 21:00:00','2023-08-01 09:00:00','07',2023,'2023-09-27 23:09:46.355608','2023-09-27 23:09:46.355608');
INSERT INTO "VetCalendar_calendar" VALUES (1278,'MA','','2023-07-01 21:00:00','2023-07-02 09:00:00','07',2023,'2023-09-27 23:09:46.360608','2023-09-27 23:09:46.360608');
INSERT INTO "VetCalendar_calendar" VALUES (1279,'NB','','2023-07-31 01:00:00','2023-07-31 13:00:00','07',2023,'2023-09-27 23:09:46.364979','2023-09-27 23:09:46.364979');
INSERT INTO "VetCalendar_calendar" VALUES (1280,'CC','','2023-08-01 01:00:00','2023-08-01 13:00:00','07',2023,'2023-09-27 23:09:46.369484','2023-09-27 23:09:46.369484');
INSERT INTO "VetCalendar_calendar" VALUES (1281,'NB','','2023-07-02 01:00:00','2023-07-02 13:00:00','07',2023,'2023-09-27 23:09:46.372994','2023-09-27 23:09:46.372994');
INSERT INTO "VetCalendar_calendar" VALUES (1282,'SM','','2023-07-02 14:00:00','2023-07-03 02:00:00','07',2023,'2023-09-27 23:09:46.380702','2023-09-27 23:09:46.380702');
INSERT INTO "VetCalendar_calendar" VALUES (1283,'NW','','2023-07-03 14:00:00','2023-07-04 02:00:00','07',2023,'2023-09-27 23:09:46.384721','2023-09-27 23:09:46.384721');
INSERT INTO "VetCalendar_calendar" VALUES (1284,'NW','','2023-07-04 14:00:00','2023-07-05 02:00:00','07',2023,'2023-09-27 23:09:46.389105','2023-09-27 23:09:46.389105');
INSERT INTO "VetCalendar_calendar" VALUES (1285,'ST','','2023-07-05 14:00:00','2023-07-06 02:00:00','07',2023,'2023-09-27 23:09:46.393722','2023-09-27 23:09:46.393722');
INSERT INTO "VetCalendar_calendar" VALUES (1286,'AC','','2023-07-06 14:00:00','2023-07-07 02:00:00','07',2023,'2023-09-27 23:09:46.399177','2023-09-27 23:09:46.399177');
INSERT INTO "VetCalendar_calendar" VALUES (1287,'AC','','2023-07-07 14:00:00','2023-07-08 02:00:00','07',2023,'2023-09-27 23:09:46.403708','2023-09-27 23:09:46.403708');
INSERT INTO "VetCalendar_calendar" VALUES (1288,'AC','','2023-07-08 14:00:00','2023-07-09 02:00:00','07',2023,'2023-09-27 23:09:46.408123','2023-09-27 23:09:46.408123');
INSERT INTO "VetCalendar_calendar" VALUES (1289,'DH','','2023-07-02 17:00:00','2023-07-03 05:00:00','07',2023,'2023-09-27 23:09:46.412987','2023-09-27 23:09:46.412987');
INSERT INTO "VetCalendar_calendar" VALUES (1290,'TR','','2023-07-03 17:00:00','2023-07-04 05:00:00','07',2023,'2023-09-27 23:09:46.417489','2023-09-27 23:09:46.417489');
INSERT INTO "VetCalendar_calendar" VALUES (1291,'MA','','2023-07-04 17:00:00','2023-07-05 05:00:00','07',2023,'2023-09-27 23:09:46.421413','2023-09-27 23:09:46.421413');
INSERT INTO "VetCalendar_calendar" VALUES (1292,'MA','','2023-07-05 17:00:00','2023-07-06 05:00:00','07',2023,'2023-09-27 23:09:46.426536','2023-09-27 23:09:46.426536');
INSERT INTO "VetCalendar_calendar" VALUES (1293,'TR','','2023-07-06 17:00:00','2023-07-07 05:00:00','07',2023,'2023-09-27 23:09:46.430958','2023-09-27 23:09:46.430958');
INSERT INTO "VetCalendar_calendar" VALUES (1294,'NW','','2023-07-07 17:00:00','2023-07-08 05:00:00','07',2023,'2023-09-27 23:09:46.436301','2023-09-27 23:09:46.436301');
INSERT INTO "VetCalendar_calendar" VALUES (1295,'NW','','2023-07-08 17:00:00','2023-07-09 05:00:00','07',2023,'2023-09-27 23:09:46.440142','2023-09-27 23:09:46.440142');
INSERT INTO "VetCalendar_calendar" VALUES (1296,'CC','','2023-07-02 21:00:00','2023-07-03 09:00:00','07',2023,'2023-09-27 23:09:46.445312','2023-09-27 23:09:46.445312');
INSERT INTO "VetCalendar_calendar" VALUES (1297,'CC','','2023-07-03 21:00:00','2023-07-04 09:00:00','07',2023,'2023-09-27 23:09:46.449424','2023-09-27 23:09:46.449424');
INSERT INTO "VetCalendar_calendar" VALUES (1298,'CC','','2023-07-04 21:00:00','2023-07-05 09:00:00','07',2023,'2023-09-27 23:09:46.455468','2023-09-27 23:09:46.455468');
INSERT INTO "VetCalendar_calendar" VALUES (1299,'NW','','2023-07-05 21:00:00','2023-07-06 09:00:00','07',2023,'2023-09-27 23:09:46.459351','2023-09-27 23:09:46.459351');
INSERT INTO "VetCalendar_calendar" VALUES (1300,'NB','','2023-07-06 21:00:00','2023-07-07 09:00:00','07',2023,'2023-09-27 23:09:46.466050','2023-09-27 23:09:46.466050');
INSERT INTO "VetCalendar_calendar" VALUES (1301,'NB','','2023-07-07 21:00:00','2023-07-08 09:00:00','07',2023,'2023-09-27 23:09:46.471054','2023-09-27 23:09:46.471054');
INSERT INTO "VetCalendar_calendar" VALUES (1302,'CC','','2023-07-08 21:00:00','2023-07-09 09:00:00','07',2023,'2023-09-27 23:09:46.475053','2023-09-27 23:09:46.476054');
INSERT INTO "VetCalendar_calendar" VALUES (1303,'NB','','2023-07-03 01:00:00','2023-07-03 13:00:00','07',2023,'2023-09-27 23:09:46.481055','2023-09-27 23:09:46.481055');
INSERT INTO "VetCalendar_calendar" VALUES (1304,'DH','','2023-07-04 01:00:00','2023-07-04 13:00:00','07',2023,'2023-09-27 23:09:46.486570','2023-09-27 23:09:46.486570');
INSERT INTO "VetCalendar_calendar" VALUES (1305,'DH','','2023-07-05 01:00:00','2023-07-05 13:00:00','07',2023,'2023-09-27 23:09:46.491081','2023-09-27 23:09:46.491081');
INSERT INTO "VetCalendar_calendar" VALUES (1306,'SM','','2023-07-06 01:00:00','2023-07-06 13:00:00','07',2023,'2023-09-27 23:09:46.497366','2023-09-27 23:09:46.497366');
INSERT INTO "VetCalendar_calendar" VALUES (1307,'SM','','2023-07-07 01:00:00','2023-07-07 13:00:00','07',2023,'2023-09-27 23:09:46.502380','2023-09-27 23:09:46.502380');
INSERT INTO "VetCalendar_calendar" VALUES (1308,'JE','','2023-07-08 01:00:00','2023-07-08 13:00:00','07',2023,'2023-09-27 23:09:46.507379','2023-09-27 23:09:46.507379');
INSERT INTO "VetCalendar_calendar" VALUES (1309,'JE','','2023-07-09 01:00:00','2023-07-09 13:00:00','07',2023,'2023-09-27 23:09:46.512001','2023-09-27 23:09:46.512001');
INSERT INTO "VetCalendar_calendar" VALUES (1310,'TR','','2023-07-09 14:00:00','2023-07-10 02:00:00','07',2023,'2023-09-27 23:09:46.516426','2023-09-27 23:09:46.516426');
INSERT INTO "VetCalendar_calendar" VALUES (1311,'TR','','2023-07-10 14:00:00','2023-07-11 02:00:00','07',2023,'2023-09-27 23:09:46.521820','2023-09-27 23:09:46.521820');
INSERT INTO "VetCalendar_calendar" VALUES (1312,'TR','','2023-07-11 14:00:00','2023-07-12 02:00:00','07',2023,'2023-09-27 23:09:46.526165','2023-09-27 23:09:46.526165');
INSERT INTO "VetCalendar_calendar" VALUES (1313,'AC','','2023-07-12 14:00:00','2023-07-13 02:00:00','07',2023,'2023-09-27 23:09:46.531375','2023-09-27 23:09:46.531375');
INSERT INTO "VetCalendar_calendar" VALUES (1314,'AC','','2023-07-13 14:00:00','2023-07-14 02:00:00','07',2023,'2023-09-27 23:09:46.535526','2023-09-27 23:09:46.535526');
INSERT INTO "VetCalendar_calendar" VALUES (1315,'AC','','2023-07-14 14:00:00','2023-07-15 02:00:00','07',2023,'2023-09-27 23:09:46.539753','2023-09-27 23:09:46.539753');
INSERT INTO "VetCalendar_calendar" VALUES (1316,'DH','','2023-07-15 14:00:00','2023-07-16 02:00:00','07',2023,'2023-09-27 23:09:46.544815','2023-09-27 23:09:46.544815');
INSERT INTO "VetCalendar_calendar" VALUES (1317,'NW','','2023-07-09 17:00:00','2023-07-10 05:00:00','07',2023,'2023-09-27 23:09:46.549655','2023-09-27 23:09:46.549655');
INSERT INTO "VetCalendar_calendar" VALUES (1318,'SM','','2023-07-10 17:00:00','2023-07-11 05:00:00','07',2023,'2023-09-27 23:09:46.553707','2023-09-27 23:09:46.553707');
INSERT INTO "VetCalendar_calendar" VALUES (1319,'NB','','2023-07-11 17:00:00','2023-07-12 05:00:00','07',2023,'2023-09-27 23:09:46.557978','2023-09-27 23:09:46.557978');
INSERT INTO "VetCalendar_calendar" VALUES (1320,'NB','','2023-07-12 17:00:00','2023-07-13 05:00:00','07',2023,'2023-09-27 23:09:46.561978','2023-09-27 23:09:46.561978');
INSERT INTO "VetCalendar_calendar" VALUES (1321,'NB','','2023-07-13 17:00:00','2023-07-14 05:00:00','07',2023,'2023-09-27 23:09:46.566379','2023-09-27 23:09:46.566379');
INSERT INTO "VetCalendar_calendar" VALUES (1322,'CC','','2023-07-14 17:00:00','2023-07-15 05:00:00','07',2023,'2023-09-27 23:09:46.570883','2023-09-27 23:09:46.570883');
INSERT INTO "VetCalendar_calendar" VALUES (1323,'SM','','2023-07-15 17:00:00','2023-07-16 05:00:00','07',2023,'2023-09-27 23:09:46.575891','2023-09-27 23:09:46.575891');
INSERT INTO "VetCalendar_calendar" VALUES (1324,'CC','','2023-07-09 21:00:00','2023-07-10 09:00:00','07',2023,'2023-09-27 23:09:46.579395','2023-09-27 23:09:46.579395');
INSERT INTO "VetCalendar_calendar" VALUES (1325,'CC','','2023-07-10 21:00:00','2023-07-11 09:00:00','07',2023,'2023-09-27 23:09:46.583906','2023-09-27 23:09:46.585229');
INSERT INTO "VetCalendar_calendar" VALUES (1326,'SM','','2023-07-11 21:00:00','2023-07-12 09:00:00','07',2023,'2023-09-27 23:09:46.588739','2023-09-27 23:09:46.589737');
INSERT INTO "VetCalendar_calendar" VALUES (1327,'MW','','2023-07-12 21:00:00','2023-07-13 09:00:00','07',2023,'2023-09-27 23:09:46.593186','2023-09-27 23:09:46.593186');
INSERT INTO "VetCalendar_calendar" VALUES (1328,'MW','','2023-07-13 21:00:00','2023-07-14 09:00:00','07',2023,'2023-09-27 23:09:46.597442','2023-09-27 23:09:46.597442');
INSERT INTO "VetCalendar_calendar" VALUES (1329,'JE','','2023-07-10 01:00:00','2023-07-10 13:00:00','07',2023,'2023-09-27 23:09:46.602015','2023-09-27 23:09:46.602015');
INSERT INTO "VetCalendar_calendar" VALUES (1330,'DH','','2023-07-11 01:00:00','2023-07-11 13:00:00','07',2023,'2023-09-27 23:09:46.605205','2023-09-27 23:09:46.605205');
INSERT INTO "VetCalendar_calendar" VALUES (1331,'DH','','2023-07-12 01:00:00','2023-07-12 13:00:00','07',2023,'2023-09-27 23:09:46.609218','2023-09-27 23:09:46.609218');
INSERT INTO "VetCalendar_calendar" VALUES (1332,'NW','','2023-07-13 01:00:00','2023-07-13 13:00:00','07',2023,'2023-09-27 23:09:46.614172','2023-09-27 23:09:46.614172');
INSERT INTO "VetCalendar_calendar" VALUES (1333,'NW','','2023-07-14 01:00:00','2023-07-14 13:00:00','07',2023,'2023-09-27 23:09:46.618228','2023-09-27 23:09:46.618228');
INSERT INTO "VetCalendar_calendar" VALUES (1334,'MA','','2023-07-15 01:00:00','2023-07-15 13:00:00','07',2023,'2023-09-27 23:09:46.622257','2023-09-27 23:09:46.622257');
INSERT INTO "VetCalendar_calendar" VALUES (1335,'MA','','2023-07-16 01:00:00','2023-07-16 13:00:00','07',2023,'2023-09-27 23:09:46.626328','2023-09-27 23:09:46.626328');
INSERT INTO "VetCalendar_calendar" VALUES (1336,'DH','','2023-07-16 14:00:00','2023-07-17 02:00:00','07',2023,'2023-09-27 23:09:46.629667','2023-09-27 23:09:46.629667');
INSERT INTO "VetCalendar_calendar" VALUES (1337,'DH','','2023-07-17 14:00:00','2023-07-18 02:00:00','07',2023,'2023-09-27 23:09:46.633186','2023-09-27 23:09:46.633186');
INSERT INTO "VetCalendar_calendar" VALUES (1338,'ST','','2023-07-18 14:00:00','2023-07-19 02:00:00','07',2023,'2023-09-27 23:09:46.637271','2023-09-27 23:09:46.637271');
INSERT INTO "VetCalendar_calendar" VALUES (1339,'ST','','2023-07-19 14:00:00','2023-07-20 02:00:00','07',2023,'2023-09-27 23:09:46.640680','2023-09-27 23:09:46.640680');
INSERT INTO "VetCalendar_calendar" VALUES (1340,'AC','','2023-07-20 14:00:00','2023-07-21 02:00:00','07',2023,'2023-09-27 23:09:46.644242','2023-09-27 23:09:46.644242');
INSERT INTO "VetCalendar_calendar" VALUES (1341,'AC','','2023-07-21 14:00:00','2023-07-22 02:00:00','07',2023,'2023-09-27 23:09:46.649367','2023-09-27 23:09:46.649367');
INSERT INTO "VetCalendar_calendar" VALUES (1342,'AC','','2023-07-22 14:00:00','2023-07-23 02:00:00','07',2023,'2023-09-27 23:09:46.651987','2023-09-27 23:09:46.651987');
INSERT INTO "VetCalendar_calendar" VALUES (1343,'SM','','2023-07-16 17:00:00','2023-07-17 05:00:00','07',2023,'2023-09-27 23:09:46.656332','2023-09-27 23:09:46.656332');
INSERT INTO "VetCalendar_calendar" VALUES (1344,'SB','','2023-07-17 17:00:00','2023-07-18 05:00:00','07',2023,'2023-09-27 23:09:46.659835','2023-09-27 23:09:46.659835');
INSERT INTO "VetCalendar_calendar" VALUES (1345,'NW','','2023-07-18 17:00:00','2023-07-19 05:00:00','07',2023,'2023-09-27 23:09:46.663030','2023-09-27 23:09:46.663030');
INSERT INTO "VetCalendar_calendar" VALUES (1346,'SM','','2023-07-19 17:00:00','2023-07-20 05:00:00','07',2023,'2023-09-27 23:09:46.667030','2023-09-27 23:09:46.667030');
INSERT INTO "VetCalendar_calendar" VALUES (1347,'MA','','2023-07-20 17:00:00','2023-07-21 05:00:00','07',2023,'2023-09-27 23:09:46.671074','2023-09-27 23:09:46.671074');
INSERT INTO "VetCalendar_calendar" VALUES (1348,'MA','','2023-07-21 17:00:00','2023-07-22 05:00:00','07',2023,'2023-09-27 23:09:46.674801','2023-09-27 23:09:46.674801');
INSERT INTO "VetCalendar_calendar" VALUES (1349,'MA','','2023-07-22 17:00:00','2023-07-23 05:00:00','07',2023,'2023-09-27 23:09:46.678251','2023-09-27 23:09:46.678251');
INSERT INTO "VetCalendar_calendar" VALUES (1350,'MW','','2023-07-17 21:00:00','2023-07-18 09:00:00','07',2023,'2023-09-27 23:09:46.682017','2023-09-27 23:09:46.682017');
INSERT INTO "VetCalendar_calendar" VALUES (1351,'','','2023-07-18 21:00:00','2023-07-19 09:00:00','07',2023,'2023-09-27 23:09:46.686086','2023-09-27 23:09:46.686086');
INSERT INTO "VetCalendar_calendar" VALUES (1352,'NW','','2023-07-19 21:00:00','2023-07-20 09:00:00','07',2023,'2023-09-27 23:09:46.689780','2023-09-27 23:09:46.689780');
INSERT INTO "VetCalendar_calendar" VALUES (1353,'NW','','2023-07-20 21:00:00','2023-07-21 09:00:00','07',2023,'2023-09-27 23:09:46.693720','2023-09-27 23:09:46.693720');
INSERT INTO "VetCalendar_calendar" VALUES (1354,'NW','','2023-07-22 21:00:00','2023-07-23 09:00:00','07',2023,'2023-09-27 23:09:46.697720','2023-09-27 23:09:46.697720');
INSERT INTO "VetCalendar_calendar" VALUES (1355,'NB','','2023-07-17 01:00:00','2023-07-17 13:00:00','07',2023,'2023-09-27 23:09:46.701026','2023-09-27 23:09:46.701026');
INSERT INTO "VetCalendar_calendar" VALUES (1356,'NB','','2023-07-18 01:00:00','2023-07-18 13:00:00','07',2023,'2023-09-27 23:09:46.706043','2023-09-27 23:09:46.706043');
INSERT INTO "VetCalendar_calendar" VALUES (1357,'TR','','2023-07-19 01:00:00','2023-07-19 13:00:00','07',2023,'2023-09-27 23:09:46.710535','2023-09-27 23:09:46.710535');
INSERT INTO "VetCalendar_calendar" VALUES (1358,'TR','','2023-07-20 01:00:00','2023-07-20 13:00:00','07',2023,'2023-09-27 23:09:46.714682','2023-09-27 23:09:46.714682');
INSERT INTO "VetCalendar_calendar" VALUES (1359,'TR','','2023-07-21 01:00:00','2023-07-21 13:00:00','07',2023,'2023-09-27 23:09:46.718254','2023-09-27 23:09:46.718254');
INSERT INTO "VetCalendar_calendar" VALUES (1360,'JE','','2023-07-22 01:00:00','2023-07-22 13:00:00','07',2023,'2023-09-27 23:09:46.722838','2023-09-27 23:09:46.722838');
INSERT INTO "VetCalendar_calendar" VALUES (1361,'JE','','2023-07-23 01:00:00','2023-07-23 13:00:00','07',2023,'2023-09-27 23:09:46.726961','2023-09-27 23:09:46.726961');
INSERT INTO "VetCalendar_calendar" VALUES (1362,'ST','','2023-07-23 14:00:00','2023-07-24 02:00:00','07',2023,'2023-09-27 23:09:46.730779','2023-09-27 23:09:46.730779');
INSERT INTO "VetCalendar_calendar" VALUES (1363,'ST','','2023-07-24 14:00:00','2023-07-25 02:00:00','07',2023,'2023-09-27 23:09:46.735307','2023-09-27 23:09:46.735307');
INSERT INTO "VetCalendar_calendar" VALUES (1364,'ST','','2023-07-25 14:00:00','2023-07-26 02:00:00','07',2023,'2023-09-27 23:09:46.739494','2023-09-27 23:09:46.739494');
INSERT INTO "VetCalendar_calendar" VALUES (1365,'DH','','2023-07-26 14:00:00','2023-07-27 02:00:00','07',2023,'2023-09-27 23:09:46.743493','2023-09-27 23:09:46.743493');
INSERT INTO "VetCalendar_calendar" VALUES (1366,'AC','','2023-07-27 14:00:00','2023-07-28 02:00:00','07',2023,'2023-09-27 23:09:46.747672','2023-09-27 23:09:46.748672');
INSERT INTO "VetCalendar_calendar" VALUES (1367,'AC','','2023-07-28 14:00:00','2023-07-29 02:00:00','07',2023,'2023-09-27 23:09:46.752183','2023-09-27 23:09:46.752183');
INSERT INTO "VetCalendar_calendar" VALUES (1368,'AC','','2023-07-29 14:00:00','2023-07-30 02:00:00','07',2023,'2023-09-27 23:09:46.756431','2023-09-27 23:09:46.756431');
INSERT INTO "VetCalendar_calendar" VALUES (1369,'JK','','2023-07-23 17:00:00','2023-07-24 05:00:00','07',2023,'2023-09-27 23:09:46.759477','2023-09-27 23:09:46.759477');
INSERT INTO "VetCalendar_calendar" VALUES (1370,'SB','','2023-07-24 17:00:00','2023-07-25 05:00:00','07',2023,'2023-09-27 23:09:46.764897','2023-09-27 23:09:46.764897');
INSERT INTO "VetCalendar_calendar" VALUES (1371,'MA','','2023-07-25 17:00:00','2023-07-26 05:00:00','07',2023,'2023-09-27 23:09:46.769172','2023-09-27 23:09:46.769172');
INSERT INTO "VetCalendar_calendar" VALUES (1372,'JK','','2023-07-26 17:00:00','2023-07-27 05:00:00','07',2023,'2023-09-27 23:09:46.773695','2023-09-27 23:09:46.773695');
INSERT INTO "VetCalendar_calendar" VALUES (1373,'JK','','2023-07-27 17:00:00','2023-07-28 05:00:00','07',2023,'2023-09-27 23:09:46.777229','2023-09-27 23:09:46.777229');
INSERT INTO "VetCalendar_calendar" VALUES (1374,'DH','','2023-07-28 17:00:00','2023-07-29 05:00:00','07',2023,'2023-09-27 23:09:46.781744','2023-09-27 23:09:46.781744');
INSERT INTO "VetCalendar_calendar" VALUES (1375,'DH','','2023-07-29 17:00:00','2023-07-30 05:00:00','07',2023,'2023-09-27 23:09:46.785777','2023-09-27 23:09:46.785777');
INSERT INTO "VetCalendar_calendar" VALUES (1376,'NW','','2023-07-23 21:00:00','2023-07-24 09:00:00','07',2023,'2023-09-27 23:09:46.790700','2023-09-27 23:09:46.790700');
INSERT INTO "VetCalendar_calendar" VALUES (1377,'NW','','2023-07-24 21:00:00','2023-07-25 09:00:00','07',2023,'2023-09-27 23:09:46.794948','2023-09-27 23:09:46.794948');
INSERT INTO "VetCalendar_calendar" VALUES (1378,'MW','','2023-07-25 21:00:00','2023-07-26 09:00:00','07',2023,'2023-09-27 23:09:46.799947','2023-09-27 23:09:46.799947');
INSERT INTO "VetCalendar_calendar" VALUES (1379,'MW','','2023-07-26 21:00:00','2023-07-27 09:00:00','07',2023,'2023-09-27 23:09:46.803638','2023-09-27 23:09:46.803638');
INSERT INTO "VetCalendar_calendar" VALUES (1380,'TR','','2023-07-28 21:00:00','2023-07-29 09:00:00','07',2023,'2023-09-27 23:09:46.807550','2023-09-27 23:09:46.807550');
INSERT INTO "VetCalendar_calendar" VALUES (1381,'JE','','2023-07-24 01:00:00','2023-07-24 13:00:00','07',2023,'2023-09-27 23:09:46.812045','2023-09-27 23:09:46.812045');
INSERT INTO "VetCalendar_calendar" VALUES (1382,'TR','','2023-07-25 01:00:00','2023-07-25 13:00:00','07',2023,'2023-09-27 23:09:46.816138','2023-09-27 23:09:46.816138');
INSERT INTO "VetCalendar_calendar" VALUES (1383,'TR','','2023-07-26 01:00:00','2023-07-26 13:00:00','07',2023,'2023-09-27 23:09:46.820829','2023-09-27 23:09:46.820829');
INSERT INTO "VetCalendar_calendar" VALUES (1384,'MA','','2023-07-27 01:00:00','2023-07-27 13:00:00','07',2023,'2023-09-27 23:09:46.824236','2023-09-27 23:09:46.824236');
INSERT INTO "VetCalendar_calendar" VALUES (1385,'MA','','2023-07-28 01:00:00','2023-07-28 13:00:00','07',2023,'2023-09-27 23:09:46.828759','2023-09-27 23:09:46.828759');
INSERT INTO "VetCalendar_calendar" VALUES (1386,'NB','','2023-07-29 01:00:00','2023-07-29 13:00:00','07',2023,'2023-09-27 23:09:46.832335','2023-09-27 23:09:46.832335');
INSERT INTO "VetCalendar_calendar" VALUES (1387,'NB','','2023-07-30 01:00:00','2023-07-30 13:00:00','07',2023,'2023-09-27 23:09:46.835340','2023-09-27 23:09:46.835340');
INSERT INTO "VetCalendar_calendar" VALUES (2723,'JK','','2023-10-01 14:00:00','2023-10-02 02:00:00','10',2023,'2023-11-01 16:32:49.412598','2023-11-01 16:32:49.412598');
INSERT INTO "VetCalendar_calendar" VALUES (2724,'DH','','2023-10-02 14:00:00','2023-10-03 02:00:00','10',2023,'2023-11-01 16:32:49.417147','2023-11-01 16:32:49.417147');
INSERT INTO "VetCalendar_calendar" VALUES (2725,'DH','','2023-10-03 14:00:00','2023-10-04 02:00:00','10',2023,'2023-11-01 16:32:49.420997','2023-11-01 16:32:49.420997');
INSERT INTO "VetCalendar_calendar" VALUES (2726,'AC','','2023-10-04 14:00:00','2023-10-05 02:00:00','10',2023,'2023-11-01 16:32:49.425044','2023-11-01 16:32:49.425044');
INSERT INTO "VetCalendar_calendar" VALUES (2727,'AC','','2023-10-05 14:00:00','2023-10-06 02:00:00','10',2023,'2023-11-01 16:32:49.428112','2023-11-01 16:32:49.428112');
INSERT INTO "VetCalendar_calendar" VALUES (2728,'AC','','2023-10-06 14:00:00','2023-10-07 02:00:00','10',2023,'2023-11-01 16:32:49.432585','2023-11-01 16:32:49.432585');
INSERT INTO "VetCalendar_calendar" VALUES (2729,'NW','','2023-10-07 14:00:00','2023-10-08 02:00:00','10',2023,'2023-11-01 16:32:49.440859','2023-11-01 16:32:49.440859');
INSERT INTO "VetCalendar_calendar" VALUES (2730,'MA','','2023-10-01 17:00:00','2023-10-02 05:00:00','10',2023,'2023-11-01 16:32:49.444464','2023-11-01 16:32:49.444464');
INSERT INTO "VetCalendar_calendar" VALUES (2731,'MW','','2023-10-03 17:00:00','2023-10-04 05:00:00','10',2023,'2023-11-01 16:32:49.448901','2023-11-01 16:32:49.448901');
INSERT INTO "VetCalendar_calendar" VALUES (2732,'MA','','2023-10-04 17:00:00','2023-10-05 05:00:00','10',2023,'2023-11-01 16:32:49.452643','2023-11-01 16:32:49.452643');
INSERT INTO "VetCalendar_calendar" VALUES (2733,'MC','','2023-10-05 17:00:00','2023-10-06 05:00:00','10',2023,'2023-11-01 16:32:49.456499','2023-11-01 16:32:49.456499');
INSERT INTO "VetCalendar_calendar" VALUES (2734,'NW','','2023-10-02 01:00:00','2023-10-02 13:00:00','10',2023,'2023-11-01 16:32:49.460495','2023-11-01 16:32:49.460495');
INSERT INTO "VetCalendar_calendar" VALUES (2735,'NW','','2023-10-03 01:00:00','2023-10-03 13:00:00','10',2023,'2023-11-01 16:32:49.463492','2023-11-01 16:32:49.463492');
INSERT INTO "VetCalendar_calendar" VALUES (2736,'ST','','2023-10-04 01:00:00','2023-10-04 13:00:00','10',2023,'2023-11-01 16:32:49.468577','2023-11-01 16:32:49.468577');
INSERT INTO "VetCalendar_calendar" VALUES (2737,'TR','','2023-10-05 01:00:00','2023-10-05 13:00:00','10',2023,'2023-11-01 16:32:49.472698','2023-11-01 16:32:49.472698');
INSERT INTO "VetCalendar_calendar" VALUES (2738,'TR','','2023-10-06 01:00:00','2023-10-06 13:00:00','10',2023,'2023-11-01 16:32:49.475792','2023-11-01 16:32:49.475792');
INSERT INTO "VetCalendar_calendar" VALUES (2739,'NB','','2023-10-07 01:00:00','2023-10-07 13:00:00','10',2023,'2023-11-01 16:32:49.480181','2023-11-01 16:32:49.480181');
INSERT INTO "VetCalendar_calendar" VALUES (2740,'NB','','2023-10-08 01:00:00','2023-10-08 13:00:00','10',2023,'2023-11-01 16:32:49.484372','2023-11-01 16:32:49.484372');
INSERT INTO "VetCalendar_calendar" VALUES (2741,'NW','','2023-10-08 14:00:00','2023-10-09 02:00:00','10',2023,'2023-11-01 16:32:49.489023','2023-11-01 16:32:49.489023');
INSERT INTO "VetCalendar_calendar" VALUES (2742,'ST','','2023-10-09 14:00:00','2023-10-10 02:00:00','10',2023,'2023-11-01 16:32:49.493033','2023-11-01 16:32:49.493033');
INSERT INTO "VetCalendar_calendar" VALUES (2743,'MA','','2023-10-10 14:00:00','2023-10-11 02:00:00','10',2023,'2023-11-01 16:32:49.497102','2023-11-01 16:32:49.497102');
INSERT INTO "VetCalendar_calendar" VALUES (2744,'ST','','2023-10-11 14:00:00','2023-10-12 02:00:00','10',2023,'2023-11-01 16:32:49.501677','2023-11-01 16:32:49.501677');
INSERT INTO "VetCalendar_calendar" VALUES (2745,'ST','','2023-10-12 14:00:00','2023-10-13 02:00:00','10',2023,'2023-11-01 16:32:49.505706','2023-11-01 16:32:49.505706');
INSERT INTO "VetCalendar_calendar" VALUES (2746,'AC','','2023-10-13 14:00:00','2023-10-14 02:00:00','10',2023,'2023-11-01 16:32:49.509876','2023-11-01 16:32:49.509876');
INSERT INTO "VetCalendar_calendar" VALUES (2747,'AC','','2023-10-14 14:00:00','2023-10-15 02:00:00','10',2023,'2023-11-01 16:32:49.513067','2023-11-01 16:32:49.513067');
INSERT INTO "VetCalendar_calendar" VALUES (2748,'DH','','2023-10-08 17:00:00','2023-10-09 05:00:00','10',2023,'2023-11-01 16:32:49.518041','2023-11-01 16:32:49.518041');
INSERT INTO "VetCalendar_calendar" VALUES (2749,'MC','','2023-10-09 17:00:00','2023-10-10 05:00:00','10',2023,'2023-11-01 16:32:49.521550','2023-11-01 16:32:49.521550');
INSERT INTO "VetCalendar_calendar" VALUES (2750,'NW','','2023-10-10 17:00:00','2023-10-11 05:00:00','10',2023,'2023-11-01 16:32:49.525991','2023-11-01 16:32:49.525991');
INSERT INTO "VetCalendar_calendar" VALUES (2751,'JK','','2023-10-11 17:00:00','2023-10-12 05:00:00','10',2023,'2023-11-01 16:32:49.530209','2023-11-01 16:32:49.530209');
INSERT INTO "VetCalendar_calendar" VALUES (2752,'JK','','2023-10-12 17:00:00','2023-10-13 05:00:00','10',2023,'2023-11-01 16:32:49.534005','2023-11-01 16:32:49.534005');
INSERT INTO "VetCalendar_calendar" VALUES (2753,'MA','','2023-10-13 17:00:00','2023-10-14 05:00:00','10',2023,'2023-11-01 16:32:49.538740','2023-11-01 16:32:49.538740');
INSERT INTO "VetCalendar_calendar" VALUES (2754,'MA','','2023-10-14 17:00:00','2023-10-15 05:00:00','10',2023,'2023-11-01 16:32:49.542334','2023-11-01 16:32:49.542334');
INSERT INTO "VetCalendar_calendar" VALUES (2755,'NB','','2023-10-09 01:00:00','2023-10-09 13:00:00','10',2023,'2023-11-01 16:32:49.546835','2023-11-01 16:32:49.546835');
INSERT INTO "VetCalendar_calendar" VALUES (2756,'TR','','2023-10-10 01:00:00','2023-10-10 13:00:00','10',2023,'2023-11-01 16:32:49.551438','2023-11-01 16:32:49.551438');
INSERT INTO "VetCalendar_calendar" VALUES (2757,'TR','','2023-10-11 01:00:00','2023-10-11 13:00:00','10',2023,'2023-11-01 16:32:49.556116','2023-11-01 16:32:49.556116');
INSERT INTO "VetCalendar_calendar" VALUES (2758,'DH','','2023-10-12 01:00:00','2023-10-12 13:00:00','10',2023,'2023-11-01 16:32:49.560135','2023-11-01 16:32:49.560135');
INSERT INTO "VetCalendar_calendar" VALUES (2759,'DH','','2023-10-13 01:00:00','2023-10-13 13:00:00','10',2023,'2023-11-01 16:32:49.563215','2023-11-01 16:32:49.563215');
INSERT INTO "VetCalendar_calendar" VALUES (2760,'NB','','2023-10-14 01:00:00','2023-10-14 13:00:00','10',2023,'2023-11-01 16:32:49.567644','2023-11-01 16:32:49.567644');
INSERT INTO "VetCalendar_calendar" VALUES (2761,'NB','','2023-10-15 01:00:00','2023-10-15 13:00:00','10',2023,'2023-11-01 16:32:49.571721','2023-11-01 16:32:49.571721');
INSERT INTO "VetCalendar_calendar" VALUES (2762,'NW','','2023-10-15 14:00:00','2023-10-16 02:00:00','10',2023,'2023-11-01 16:32:49.576726','2023-11-01 16:32:49.576726');
INSERT INTO "VetCalendar_calendar" VALUES (2763,'NW','','2023-10-16 14:00:00','2023-10-17 02:00:00','10',2023,'2023-11-01 16:32:49.580447','2023-11-01 16:32:49.580447');
INSERT INTO "VetCalendar_calendar" VALUES (2764,'DH','','2023-10-17 14:00:00','2023-10-18 02:00:00','10',2023,'2023-11-01 16:32:49.585242','2023-11-01 16:32:49.585242');
INSERT INTO "VetCalendar_calendar" VALUES (2765,'AC','','2023-10-18 14:00:00','2023-10-19 02:00:00','10',2023,'2023-11-01 16:32:49.589204','2023-11-01 16:32:49.589204');
INSERT INTO "VetCalendar_calendar" VALUES (2766,'AC','','2023-10-19 14:00:00','2023-10-20 02:00:00','10',2023,'2023-11-01 16:32:49.593305','2023-11-01 16:32:49.593305');
INSERT INTO "VetCalendar_calendar" VALUES (2767,'AC','','2023-10-20 14:00:00','2023-10-21 02:00:00','10',2023,'2023-11-01 16:32:49.597785','2023-11-01 16:32:49.597785');
INSERT INTO "VetCalendar_calendar" VALUES (2768,'DH','','2023-10-21 14:00:00','2023-10-22 02:00:00','10',2023,'2023-11-01 16:32:49.601094','2023-11-01 16:32:49.601094');
INSERT INTO "VetCalendar_calendar" VALUES (2769,'MA','','2023-10-15 17:00:00','2023-10-16 05:00:00','10',2023,'2023-11-01 16:32:49.605270','2023-11-01 16:32:49.605270');
INSERT INTO "VetCalendar_calendar" VALUES (2770,'JK','','2023-10-16 17:00:00','2023-10-17 05:00:00','10',2023,'2023-11-01 16:32:49.608740','2023-11-01 16:32:49.608740');
INSERT INTO "VetCalendar_calendar" VALUES (2771,'MW','','2023-10-17 17:00:00','2023-10-18 05:00:00','10',2023,'2023-11-01 16:32:49.611945','2023-11-01 16:32:49.611945');
INSERT INTO "VetCalendar_calendar" VALUES (2772,'DH','','2023-10-18 17:00:00','2023-10-19 05:00:00','10',2023,'2023-11-01 16:32:49.616038','2023-11-01 16:32:49.616038');
INSERT INTO "VetCalendar_calendar" VALUES (2773,'NW','','2023-10-19 17:00:00','2023-10-20 05:00:00','10',2023,'2023-11-01 16:32:49.619038','2023-11-01 16:32:49.619038');
INSERT INTO "VetCalendar_calendar" VALUES (2774,'NB','','2023-10-20 17:00:00','2023-10-21 05:00:00','10',2023,'2023-11-01 16:32:49.623110','2023-11-01 16:32:49.623110');
INSERT INTO "VetCalendar_calendar" VALUES (2775,'NW','','2023-10-21 17:00:00','2023-10-22 05:00:00','10',2023,'2023-11-01 16:32:49.626526','2023-11-01 16:32:49.626526');
INSERT INTO "VetCalendar_calendar" VALUES (2776,'TR','','2023-10-16 01:00:00','2023-10-16 13:00:00','10',2023,'2023-11-01 16:32:49.630526','2023-11-01 16:32:49.630526');
INSERT INTO "VetCalendar_calendar" VALUES (2777,'TR','','2023-10-17 01:00:00','2023-10-17 13:00:00','10',2023,'2023-11-01 16:32:49.634296','2023-11-01 16:32:49.634296');
INSERT INTO "VetCalendar_calendar" VALUES (2778,'TR','','2023-10-18 01:00:00','2023-10-18 13:00:00','10',2023,'2023-11-01 16:32:49.638740','2023-11-01 16:32:49.638740');
INSERT INTO "VetCalendar_calendar" VALUES (2779,'ST','','2023-10-19 01:00:00','2023-10-19 13:00:00','10',2023,'2023-11-01 16:32:49.642208','2023-11-01 16:32:49.642208');
INSERT INTO "VetCalendar_calendar" VALUES (2780,'ST','','2023-10-20 01:00:00','2023-10-20 13:00:00','10',2023,'2023-11-01 16:32:49.646021','2023-11-01 16:32:49.646021');
INSERT INTO "VetCalendar_calendar" VALUES (2781,'MA','','2023-10-21 01:00:00','2023-10-21 13:00:00','10',2023,'2023-11-01 16:32:49.649019','2023-11-01 16:32:49.649019');
INSERT INTO "VetCalendar_calendar" VALUES (2782,'MA','','2023-10-22 01:00:00','2023-10-22 13:00:00','10',2023,'2023-11-01 16:32:49.653113','2023-11-01 16:32:49.653113');
INSERT INTO "VetCalendar_calendar" VALUES (2783,'DH','','2023-10-22 14:00:00','2023-10-23 02:00:00','10',2023,'2023-11-01 16:32:49.656233','2023-11-01 16:32:49.656233');
INSERT INTO "VetCalendar_calendar" VALUES (2784,'ST','','2023-10-23 14:00:00','2023-10-24 02:00:00','10',2023,'2023-11-01 16:32:49.659371','2023-11-01 16:32:49.659371');
INSERT INTO "VetCalendar_calendar" VALUES (2785,'ST','','2023-10-24 14:00:00','2023-10-25 02:00:00','10',2023,'2023-11-01 16:32:49.663371','2023-11-01 16:32:49.663371');
INSERT INTO "VetCalendar_calendar" VALUES (2786,'ST','','2023-10-25 14:00:00','2023-10-26 02:00:00','10',2023,'2023-11-01 16:32:49.666767','2023-11-01 16:32:49.666767');
INSERT INTO "VetCalendar_calendar" VALUES (2787,'AC','','2023-10-26 14:00:00','2023-10-27 02:00:00','10',2023,'2023-11-01 16:32:49.670676','2023-11-01 16:32:49.670676');
INSERT INTO "VetCalendar_calendar" VALUES (2788,'AC','','2023-10-27 14:00:00','2023-10-28 02:00:00','10',2023,'2023-11-01 16:32:49.673534','2023-11-01 16:32:49.673534');
INSERT INTO "VetCalendar_calendar" VALUES (2789,'AC','','2023-10-28 14:00:00','2023-10-29 02:00:00','10',2023,'2023-11-01 16:32:49.677369','2023-11-01 16:32:49.677369');
INSERT INTO "VetCalendar_calendar" VALUES (2790,'FA','','2023-10-22 17:00:00','2023-10-23 05:00:00','10',2023,'2023-11-01 16:32:49.681809','2023-11-01 16:32:49.681809');
INSERT INTO "VetCalendar_calendar" VALUES (2791,'','','2023-10-23 17:00:00','2023-10-24 05:00:00','10',2023,'2023-11-01 16:32:49.685260','2023-11-01 16:32:49.685260');
INSERT INTO "VetCalendar_calendar" VALUES (2792,'NB','','2023-10-24 17:00:00','2023-10-25 05:00:00','10',2023,'2023-11-01 16:32:49.689350','2023-11-01 16:32:49.689350');
INSERT INTO "VetCalendar_calendar" VALUES (2793,'','','2023-10-25 17:00:00','2023-10-26 05:00:00','10',2023,'2023-11-01 16:32:49.692584','2023-11-01 16:32:49.692584');
INSERT INTO "VetCalendar_calendar" VALUES (2794,'MW','','2023-10-26 17:00:00','2023-10-27 05:00:00','10',2023,'2023-11-01 16:32:49.696036','2023-11-01 16:32:49.696036');
INSERT INTO "VetCalendar_calendar" VALUES (2795,'MC','','2023-10-22 21:00:00','2023-10-23 09:00:00','10',2023,'2023-11-01 16:32:49.699034','2023-11-01 16:32:49.699034');
INSERT INTO "VetCalendar_calendar" VALUES (2796,'MA','','2023-10-23 01:00:00','2023-10-23 13:00:00','10',2023,'2023-11-01 16:32:49.703221','2023-11-01 16:32:49.703221');
INSERT INTO "VetCalendar_calendar" VALUES (2797,'NW','','2023-10-24 01:00:00','2023-10-24 13:00:00','10',2023,'2023-11-01 16:32:49.707045','2023-11-01 16:32:49.707045');
INSERT INTO "VetCalendar_calendar" VALUES (2798,'NW','','2023-10-25 01:00:00','2023-10-25 13:00:00','10',2023,'2023-11-01 16:32:49.710087','2023-11-01 16:32:49.710087');
INSERT INTO "VetCalendar_calendar" VALUES (2799,'MA','','2023-10-26 01:00:00','2023-10-26 13:00:00','10',2023,'2023-11-01 16:32:49.713524','2023-11-01 16:32:49.713524');
INSERT INTO "VetCalendar_calendar" VALUES (2800,'MA','','2023-10-27 01:00:00','2023-10-27 13:00:00','10',2023,'2023-11-01 16:32:49.717949','2023-11-01 16:32:49.717949');
INSERT INTO "VetCalendar_calendar" VALUES (2801,'DH','','2023-10-28 01:00:00','2023-10-28 13:00:00','10',2023,'2023-11-01 16:32:49.722000','2023-11-01 16:32:49.722000');
INSERT INTO "VetCalendar_calendar" VALUES (2802,'DH','','2023-10-29 01:00:00','2023-10-29 13:00:00','10',2023,'2023-11-01 16:32:49.726006','2023-11-01 16:32:49.726006');
INSERT INTO "VetCalendar_calendar" VALUES (2803,'TR','','2023-10-29 14:00:00','2023-10-30 02:00:00','10',2023,'2023-11-01 16:32:49.730181','2023-11-01 16:32:49.730181');
INSERT INTO "VetCalendar_calendar" VALUES (2804,'TR','','2023-10-30 14:00:00','2023-10-31 02:00:00','10',2023,'2023-11-01 16:32:49.733652','2023-11-01 16:32:49.733652');
INSERT INTO "VetCalendar_calendar" VALUES (2805,'TR','','2023-10-31 14:00:00','2023-11-01 02:00:00','10',2023,'2023-11-01 16:32:49.738381','2023-11-01 16:32:49.738381');
INSERT INTO "VetCalendar_calendar" VALUES (2806,'FA','','2023-10-29 17:00:00','2023-10-30 05:00:00','10',2023,'2023-11-01 16:32:49.743218','2023-11-01 16:32:49.743218');
INSERT INTO "VetCalendar_calendar" VALUES (2807,'MC','','2023-10-30 17:00:00','2023-10-31 05:00:00','10',2023,'2023-11-01 16:32:49.747898','2023-11-01 16:32:49.747898');
INSERT INTO "VetCalendar_calendar" VALUES (2808,'MA','','2023-10-31 17:00:00','2023-11-01 05:00:00','10',2023,'2023-11-01 16:32:49.751463','2023-11-01 16:32:49.751463');
INSERT INTO "VetCalendar_calendar" VALUES (2809,'DH','','2023-10-30 01:00:00','2023-10-30 13:00:00','10',2023,'2023-11-01 16:32:49.756468','2023-11-01 16:32:49.756468');
INSERT INTO "VetCalendar_calendar" VALUES (2810,'ST','','2023-10-31 01:00:00','2023-10-31 13:00:00','10',2023,'2023-11-01 16:32:49.761269','2023-11-01 16:32:49.761269');
INSERT INTO "VetCalendar_calendar" VALUES (2811,'ST','','2023-11-01 01:00:00','2023-11-01 13:00:00','10',2023,'2023-11-01 16:32:49.765133','2023-11-01 16:32:49.765133');
INSERT INTO "VetCalendar_calendar" VALUES (4169,'NW','','2023-11-01 14:00:00','2023-11-02 02:00:00','11',2023,'2023-11-18 19:05:57.202857','2023-11-18 19:05:57.202857');
INSERT INTO "VetCalendar_calendar" VALUES (4170,'NW','','2023-11-02 14:00:00','2023-11-03 02:00:00','11',2023,'2023-11-18 19:05:57.211999','2023-11-18 19:05:57.211999');
INSERT INTO "VetCalendar_calendar" VALUES (4171,'TR','','2023-11-03 14:00:00','2023-11-04 02:00:00','11',2023,'2023-11-18 19:05:57.219505','2023-11-18 19:05:57.220511');
INSERT INTO "VetCalendar_calendar" VALUES (4172,'TR','','2023-11-04 14:00:00','2023-11-05 02:00:00','11',2023,'2023-11-18 19:05:57.227087','2023-11-18 19:05:57.227087');
INSERT INTO "VetCalendar_calendar" VALUES (4173,'MA','','2023-11-01 17:00:00','2023-11-02 05:00:00','11',2023,'2023-11-18 19:05:57.235079','2023-11-18 19:05:57.235079');
INSERT INTO "VetCalendar_calendar" VALUES (4174,'JS','','2023-11-02 17:00:00','2023-11-03 05:00:00','11',2023,'2023-11-18 19:05:57.244276','2023-11-18 19:05:57.244276');
INSERT INTO "VetCalendar_calendar" VALUES (4175,'CV','','2023-11-03 17:00:00','2023-11-04 05:00:00','11',2023,'2023-11-18 19:05:57.254193','2023-11-18 19:05:57.254193');
INSERT INTO "VetCalendar_calendar" VALUES (4176,'CV','','2023-11-04 17:00:00','2023-11-05 05:00:00','11',2023,'2023-11-18 19:05:57.263150','2023-11-18 19:05:57.263150');
INSERT INTO "VetCalendar_calendar" VALUES (4177,'ST','','2023-11-02 01:00:00','2023-11-02 13:00:00','11',2023,'2023-11-18 19:05:57.270314','2023-11-18 19:05:57.270314');
INSERT INTO "VetCalendar_calendar" VALUES (4178,'DH','','2023-11-03 01:00:00','2023-11-03 13:00:00','11',2023,'2023-11-18 19:05:57.275852','2023-11-18 19:05:57.275852');
INSERT INTO "VetCalendar_calendar" VALUES (4179,'DH','','2023-11-04 01:00:00','2023-11-04 13:00:00','11',2023,'2023-11-18 19:05:57.283124','2023-11-18 19:05:57.283124');
INSERT INTO "VetCalendar_calendar" VALUES (4180,'MA','','2023-11-05 01:00:00','2023-11-05 14:00:00','11',2023,'2023-11-18 19:05:57.290735','2023-11-18 19:05:57.290735');
INSERT INTO "VetCalendar_calendar" VALUES (4181,'NW','','2023-11-05 15:00:00','2023-11-06 03:00:00','11',2023,'2023-11-18 19:05:57.297784','2023-11-18 19:05:57.297784');
INSERT INTO "VetCalendar_calendar" VALUES (4182,'ST','','2023-11-06 15:00:00','2023-11-07 03:00:00','11',2023,'2023-11-18 19:05:57.305676','2023-11-18 19:05:57.305676');
INSERT INTO "VetCalendar_calendar" VALUES (4183,'NW','','2023-11-07 15:00:00','2023-11-08 03:00:00','11',2023,'2023-11-18 19:05:57.312985','2023-11-18 19:05:57.312985');
INSERT INTO "VetCalendar_calendar" VALUES (4184,'NW','','2023-11-08 15:00:00','2023-11-09 03:00:00','11',2023,'2023-11-18 19:05:57.320305','2023-11-18 19:05:57.320305');
INSERT INTO "VetCalendar_calendar" VALUES (4185,'ST','','2023-11-09 15:00:00','2023-11-10 03:00:00','11',2023,'2023-11-18 19:05:57.327559','2023-11-18 19:05:57.327559');
INSERT INTO "VetCalendar_calendar" VALUES (4186,'MA','','2023-11-10 15:00:00','2023-11-11 03:00:00','11',2023,'2023-11-18 19:05:57.334306','2023-11-18 19:05:57.334306');
INSERT INTO "VetCalendar_calendar" VALUES (4187,'MA','','2023-11-11 15:00:00','2023-11-12 03:00:00','11',2023,'2023-11-18 19:05:57.342320','2023-11-18 19:05:57.342320');
INSERT INTO "VetCalendar_calendar" VALUES (4188,'CV','','2023-11-05 18:00:00','2023-11-06 06:00:00','11',2023,'2023-11-18 19:05:57.349603','2023-11-18 19:05:57.349603');
INSERT INTO "VetCalendar_calendar" VALUES (4189,'MC','','2023-11-06 18:00:00','2023-11-07 06:00:00','11',2023,'2023-11-18 19:05:57.356615','2023-11-18 19:05:57.356615');
INSERT INTO "VetCalendar_calendar" VALUES (4190,'ST','','2023-11-07 18:00:00','2023-11-08 06:00:00','11',2023,'2023-11-18 19:05:57.364148','2023-11-18 19:05:57.364148');
INSERT INTO "VetCalendar_calendar" VALUES (4191,'TR','','2023-11-08 18:00:00','2023-11-09 06:00:00','11',2023,'2023-11-18 19:05:57.373014','2023-11-18 19:05:57.373014');
INSERT INTO "VetCalendar_calendar" VALUES (4192,'ST','','2023-11-10 18:00:00','2023-11-11 06:00:00','11',2023,'2023-11-18 19:05:57.380756','2023-11-18 19:05:57.380756');
INSERT INTO "VetCalendar_calendar" VALUES (4193,'NB','','2023-11-11 18:00:00','2023-11-12 06:00:00','11',2023,'2023-11-18 19:05:57.386324','2023-11-18 19:05:57.386324');
INSERT INTO "VetCalendar_calendar" VALUES (4194,'MA','','2023-11-06 02:00:00','2023-11-06 14:00:00','11',2023,'2023-11-18 19:05:57.395330','2023-11-18 19:05:57.395330');
INSERT INTO "VetCalendar_calendar" VALUES (4195,'MA','','2023-11-07 02:00:00','2023-11-07 14:00:00','11',2023,'2023-11-18 19:05:57.404389','2023-11-18 19:05:57.404389');
INSERT INTO "VetCalendar_calendar" VALUES (4196,'DH','','2023-11-08 02:00:00','2023-11-08 14:00:00','11',2023,'2023-11-18 19:05:57.410924','2023-11-18 19:05:57.411923');
INSERT INTO "VetCalendar_calendar" VALUES (4197,'DH','','2023-11-09 02:00:00','2023-11-09 14:00:00','11',2023,'2023-11-18 19:05:57.419460','2023-11-18 19:05:57.419460');
INSERT INTO "VetCalendar_calendar" VALUES (4198,'DH','','2023-11-10 02:00:00','2023-11-10 14:00:00','11',2023,'2023-11-18 19:05:57.429451','2023-11-18 19:05:57.429451');
INSERT INTO "VetCalendar_calendar" VALUES (4199,'TR','','2023-11-11 02:00:00','2023-11-11 14:00:00','11',2023,'2023-11-18 19:05:57.437619','2023-11-18 19:05:57.437619');
INSERT INTO "VetCalendar_calendar" VALUES (4200,'TR','','2023-11-12 02:00:00','2023-11-12 14:00:00','11',2023,'2023-11-18 19:05:57.445139','2023-11-18 19:05:57.445139');
INSERT INTO "VetCalendar_calendar" VALUES (4201,'MA','','2023-11-12 15:00:00','2023-11-13 03:00:00','11',2023,'2023-11-18 19:05:57.454284','2023-11-18 19:05:57.454284');
INSERT INTO "VetCalendar_calendar" VALUES (4202,'ST','','2023-11-13 15:00:00','2023-11-14 03:00:00','11',2023,'2023-11-18 19:05:57.464059','2023-11-18 19:05:57.464059');
INSERT INTO "VetCalendar_calendar" VALUES (4203,'ST','','2023-11-14 15:00:00','2023-11-15 03:00:00','11',2023,'2023-11-18 19:05:57.472980','2023-11-18 19:05:57.472980');
INSERT INTO "VetCalendar_calendar" VALUES (4204,'MA','','2023-11-15 15:00:00','2023-11-16 03:00:00','11',2023,'2023-11-18 19:05:57.479287','2023-11-18 19:05:57.479287');
INSERT INTO "VetCalendar_calendar" VALUES (4205,'MA','','2023-11-16 15:00:00','2023-11-17 03:00:00','11',2023,'2023-11-18 19:05:57.487143','2023-11-18 19:05:57.487143');
INSERT INTO "VetCalendar_calendar" VALUES (4206,'AC','','2023-11-17 15:00:00','2023-11-18 03:00:00','11',2023,'2023-11-18 19:05:57.494476','2023-11-18 19:05:57.494476');
INSERT INTO "VetCalendar_calendar" VALUES (4207,'AC','','2023-11-18 15:00:00','2023-11-19 03:00:00','11',2023,'2023-11-18 19:05:57.501372','2023-11-18 19:05:57.501372');
INSERT INTO "VetCalendar_calendar" VALUES (4208,'NB','','2023-11-12 18:00:00','2023-11-13 06:00:00','11',2023,'2023-11-18 19:05:57.507072','2023-11-18 19:05:57.507072');
INSERT INTO "VetCalendar_calendar" VALUES (4209,'JK','','2023-11-15 18:00:00','2023-11-16 06:00:00','11',2023,'2023-11-18 19:05:57.514362','2023-11-18 19:05:57.514362');
INSERT INTO "VetCalendar_calendar" VALUES (4210,'JK','','2023-11-16 18:00:00','2023-11-17 06:00:00','11',2023,'2023-11-18 19:05:57.520186','2023-11-18 19:05:57.521184');
INSERT INTO "VetCalendar_calendar" VALUES (4211,'NW','','2023-11-17 18:00:00','2023-11-18 06:00:00','11',2023,'2023-11-18 19:05:57.527730','2023-11-18 19:05:57.527730');
INSERT INTO "VetCalendar_calendar" VALUES (4212,'NW','','2023-11-18 18:00:00','2023-11-19 06:00:00','11',2023,'2023-11-18 19:05:57.534405','2023-11-18 19:05:57.534405');
INSERT INTO "VetCalendar_calendar" VALUES (4213,'TR','','2023-11-13 02:00:00','2023-11-13 14:00:00','11',2023,'2023-11-18 19:05:57.542001','2023-11-18 19:05:57.542001');
INSERT INTO "VetCalendar_calendar" VALUES (4214,'DH','','2023-11-14 02:00:00','2023-11-14 14:00:00','11',2023,'2023-11-18 19:05:57.548037','2023-11-18 19:05:57.548037');
INSERT INTO "VetCalendar_calendar" VALUES (4215,'DH','','2023-11-15 02:00:00','2023-11-15 14:00:00','11',2023,'2023-11-18 19:05:57.555424','2023-11-18 19:05:57.555424');
INSERT INTO "VetCalendar_calendar" VALUES (4216,'TR','','2023-11-16 02:00:00','2023-11-16 14:00:00','11',2023,'2023-11-18 19:05:57.561593','2023-11-18 19:05:57.561593');
INSERT INTO "VetCalendar_calendar" VALUES (4217,'TR','','2023-11-17 02:00:00','2023-11-17 14:00:00','11',2023,'2023-11-18 19:05:57.568031','2023-11-18 19:05:57.568031');
INSERT INTO "VetCalendar_calendar" VALUES (4218,'NB','','2023-11-18 02:00:00','2023-11-18 14:00:00','11',2023,'2023-11-18 19:05:57.574482','2023-11-18 19:05:57.574482');
INSERT INTO "VetCalendar_calendar" VALUES (4219,'NB','','2023-11-19 02:00:00','2023-11-19 14:00:00','11',2023,'2023-11-18 19:05:57.581262','2023-11-18 19:05:57.581262');
INSERT INTO "VetCalendar_calendar" VALUES (4220,'DH','','2023-11-19 15:00:00','2023-11-20 03:00:00','11',2023,'2023-11-18 19:05:57.588154','2023-11-18 19:05:57.588154');
INSERT INTO "VetCalendar_calendar" VALUES (4221,'DH','','2023-11-20 15:00:00','2023-11-21 03:00:00','11',2023,'2023-11-18 19:05:57.594135','2023-11-18 19:05:57.594135');
INSERT INTO "VetCalendar_calendar" VALUES (4222,'DH','','2023-11-21 15:00:00','2023-11-22 03:00:00','11',2023,'2023-11-18 19:05:57.601117','2023-11-18 19:05:57.601117');
INSERT INTO "VetCalendar_calendar" VALUES (4223,'NW','','2023-11-22 15:00:00','2023-11-23 03:00:00','11',2023,'2023-11-18 19:05:57.607686','2023-11-18 19:05:57.607686');
INSERT INTO "VetCalendar_calendar" VALUES (4224,'AC','','2023-11-23 15:00:00','2023-11-24 03:00:00','11',2023,'2023-11-18 19:05:57.614224','2023-11-18 19:05:57.614224');
INSERT INTO "VetCalendar_calendar" VALUES (4225,'AC','','2023-11-24 15:00:00','2023-11-25 03:00:00','11',2023,'2023-11-18 19:05:57.620094','2023-11-18 19:05:57.620094');
INSERT INTO "VetCalendar_calendar" VALUES (4226,'AC','','2023-11-25 15:00:00','2023-11-26 03:00:00','11',2023,'2023-11-18 19:05:57.627012','2023-11-18 19:05:57.627012');
INSERT INTO "VetCalendar_calendar" VALUES (4227,'NW','','2023-11-19 18:00:00','2023-11-20 06:00:00','11',2023,'2023-11-18 19:05:57.635011','2023-11-18 19:05:57.635011');
INSERT INTO "VetCalendar_calendar" VALUES (4228,'JK','','2023-11-20 18:00:00','2023-11-21 06:00:00','11',2023,'2023-11-18 19:05:57.641681','2023-11-18 19:05:57.641681');
INSERT INTO "VetCalendar_calendar" VALUES (4229,'TR','','2023-11-21 18:00:00','2023-11-22 06:00:00','11',2023,'2023-11-18 19:05:57.648636','2023-11-18 19:05:57.648636');
INSERT INTO "VetCalendar_calendar" VALUES (4230,'JK','','2023-11-22 18:00:00','2023-11-23 06:00:00','11',2023,'2023-11-18 19:05:57.654368','2023-11-18 19:05:57.654368');
INSERT INTO "VetCalendar_calendar" VALUES (4231,'CV','','2023-11-23 18:00:00','2023-11-24 06:00:00','11',2023,'2023-11-18 19:05:57.661160','2023-11-18 19:05:57.661160');
INSERT INTO "VetCalendar_calendar" VALUES (4232,'CV','','2023-11-24 18:00:00','2023-11-25 06:00:00','11',2023,'2023-11-18 19:05:57.669549','2023-11-18 19:05:57.669549');
INSERT INTO "VetCalendar_calendar" VALUES (4233,'CV','','2023-11-25 18:00:00','2023-11-26 06:00:00','11',2023,'2023-11-18 19:05:57.675788','2023-11-18 19:05:57.675788');
INSERT INTO "VetCalendar_calendar" VALUES (4234,'JK','','2023-11-23 22:00:00','2023-11-24 10:00:00','11',2023,'2023-11-18 19:05:57.681362','2023-11-18 19:05:57.681362');
INSERT INTO "VetCalendar_calendar" VALUES (4235,'MA','','2023-11-20 02:00:00','2023-11-20 14:00:00','11',2023,'2023-11-18 19:05:57.688743','2023-11-18 19:05:57.688743');
INSERT INTO "VetCalendar_calendar" VALUES (4236,'MA','','2023-11-21 02:00:00','2023-11-21 14:00:00','11',2023,'2023-11-18 19:05:57.695512','2023-11-18 19:05:57.695512');
INSERT INTO "VetCalendar_calendar" VALUES (4237,'MA','','2023-11-22 02:00:00','2023-11-22 14:00:00','11',2023,'2023-11-18 19:05:57.702560','2023-11-18 19:05:57.702560');
INSERT INTO "VetCalendar_calendar" VALUES (4238,'TR','','2023-11-23 02:00:00','2023-11-23 14:00:00','11',2023,'2023-11-18 19:05:57.709600','2023-11-18 19:05:57.709600');
INSERT INTO "VetCalendar_calendar" VALUES (4239,'TR','','2023-11-24 02:00:00','2023-11-24 14:00:00','11',2023,'2023-11-18 19:05:57.716371','2023-11-18 19:05:57.716371');
INSERT INTO "VetCalendar_calendar" VALUES (4240,'TR','','2023-11-25 02:00:00','2023-11-25 14:00:00','11',2023,'2023-11-18 19:05:57.722920','2023-11-18 19:05:57.722920');
INSERT INTO "VetCalendar_calendar" VALUES (4241,'NW','','2023-11-26 02:00:00','2023-11-26 14:00:00','11',2023,'2023-11-18 19:05:57.729697','2023-11-18 19:05:57.729697');
INSERT INTO "VetCalendar_calendar" VALUES (4242,'DH','','2023-11-26 15:00:00','2023-11-27 03:00:00','11',2023,'2023-11-18 19:05:57.738071','2023-11-18 19:05:57.738071');
INSERT INTO "VetCalendar_calendar" VALUES (4243,'ST','','2023-11-27 15:00:00','2023-11-28 03:00:00','11',2023,'2023-11-18 19:05:57.744248','2023-11-18 19:05:57.744248');
INSERT INTO "VetCalendar_calendar" VALUES (4244,'TR','','2023-11-28 15:00:00','2023-11-29 03:00:00','11',2023,'2023-11-18 19:05:57.752044','2023-11-18 19:05:57.752044');
INSERT INTO "VetCalendar_calendar" VALUES (4245,'AC','','2023-11-29 15:00:00','2023-11-30 03:00:00','11',2023,'2023-11-18 19:05:57.758710','2023-11-18 19:05:57.758710');
INSERT INTO "VetCalendar_calendar" VALUES (4246,'AC','','2023-11-30 15:00:00','2023-12-01 03:00:00','11',2023,'2023-11-18 19:05:57.765589','2023-11-18 19:05:57.765589');
INSERT INTO "VetCalendar_calendar" VALUES (4247,'JK','','2023-11-26 18:00:00','2023-11-27 06:00:00','11',2023,'2023-11-18 19:05:57.772193','2023-11-18 19:05:57.772193');
INSERT INTO "VetCalendar_calendar" VALUES (4248,'DH','','2023-11-27 18:00:00','2023-11-28 06:00:00','11',2023,'2023-11-18 19:05:57.778366','2023-11-18 19:05:57.778366');
INSERT INTO "VetCalendar_calendar" VALUES (4249,'DH','','2023-11-28 18:00:00','2023-11-29 06:00:00','11',2023,'2023-11-18 19:05:57.784312','2023-11-18 19:05:57.784312');
INSERT INTO "VetCalendar_calendar" VALUES (4250,'TR','','2023-11-29 18:00:00','2023-11-30 06:00:00','11',2023,'2023-11-18 19:05:57.790940','2023-11-18 19:05:57.790940');
INSERT INTO "VetCalendar_calendar" VALUES (4251,'TR','','2023-11-30 18:00:00','2023-12-01 06:00:00','11',2023,'2023-11-18 19:05:57.798871','2023-11-18 19:05:57.798871');
INSERT INTO "VetCalendar_calendar" VALUES (4252,'','','2023-11-28 22:00:00','2023-11-29 10:00:00','11',2023,'2023-11-18 19:05:57.805631','2023-11-18 19:05:57.805631');
INSERT INTO "VetCalendar_calendar" VALUES (4253,'NW','','2023-11-27 02:00:00','2023-11-27 14:00:00','11',2023,'2023-11-18 19:05:57.812963','2023-11-18 19:05:57.812963');
INSERT INTO "VetCalendar_calendar" VALUES (4254,'NW','','2023-11-28 02:00:00','2023-11-28 14:00:00','11',2023,'2023-11-18 19:05:57.818793','2023-11-18 19:05:57.818793');
INSERT INTO "VetCalendar_calendar" VALUES (4255,'NB','','2023-11-29 02:00:00','2023-11-29 14:00:00','11',2023,'2023-11-18 19:05:57.826619','2023-11-18 19:05:57.826619');
INSERT INTO "VetCalendar_calendar" VALUES (4256,'NB','','2023-11-30 02:00:00','2023-11-30 14:00:00','11',2023,'2023-11-18 19:05:57.832881','2023-11-18 19:05:57.832881');
INSERT INTO "VetCalendar_calendar" VALUES (4257,'MA','','2023-12-01 02:00:00','2023-12-01 14:00:00','11',2023,'2023-11-18 19:05:57.839897','2023-11-18 19:05:57.839897');
INSERT INTO "VetCalendar_calendar" VALUES (4768,'MA','','2023-12-31 15:00:00','2024-01-01 03:00:00','12',2023,'2023-12-04 06:51:07.164819','2023-12-04 06:51:07.164819');
INSERT INTO "VetCalendar_calendar" VALUES (4769,'AC','','2023-12-01 15:00:00','2023-12-02 03:00:00','12',2023,'2023-12-04 06:51:07.169508','2023-12-04 06:51:07.169508');
INSERT INTO "VetCalendar_calendar" VALUES (4770,'NW','','2023-12-02 15:00:00','2023-12-03 03:00:00','12',2023,'2023-12-04 06:51:07.175950','2023-12-04 06:51:07.175950');
INSERT INTO "VetCalendar_calendar" VALUES (4771,'NW','','2023-12-31 18:00:00','2024-01-01 06:00:00','12',2023,'2023-12-04 06:51:07.181624','2023-12-04 06:51:07.181624');
INSERT INTO "VetCalendar_calendar" VALUES (4772,'DH','','2023-12-01 18:00:00','2023-12-02 06:00:00','12',2023,'2023-12-04 06:51:07.186934','2023-12-04 06:51:07.186934');
INSERT INTO "VetCalendar_calendar" VALUES (4773,'TB','','2023-12-02 18:00:00','2023-12-03 06:00:00','12',2023,'2023-12-04 06:51:07.199230','2023-12-04 06:51:07.199230');
INSERT INTO "VetCalendar_calendar" VALUES (4774,'TB','','2023-12-31 22:00:00','2024-01-01 10:00:00','12',2023,'2023-12-04 06:51:07.204407','2023-12-04 06:51:07.204407');
INSERT INTO "VetCalendar_calendar" VALUES (4775,'NB','','2024-01-01 02:00:00','2024-01-01 14:00:00','12',2023,'2023-12-04 06:51:07.209407','2023-12-04 06:51:07.209407');
INSERT INTO "VetCalendar_calendar" VALUES (4776,'MA','','2023-12-02 02:00:00','2023-12-02 14:00:00','12',2023,'2023-12-04 06:51:07.214203','2023-12-04 06:51:07.214203');
INSERT INTO "VetCalendar_calendar" VALUES (4777,'MA','','2023-12-03 02:00:00','2023-12-03 14:00:00','12',2023,'2023-12-04 06:51:07.218512','2023-12-04 06:51:07.218512');
INSERT INTO "VetCalendar_calendar" VALUES (4778,'NW','','2023-12-03 15:00:00','2023-12-04 03:00:00','12',2023,'2023-12-04 06:51:07.223182','2023-12-04 06:51:07.223182');
INSERT INTO "VetCalendar_calendar" VALUES (4779,'NW','','2023-12-04 15:00:00','2023-12-05 03:00:00','12',2023,'2023-12-04 06:51:07.228696','2023-12-04 06:51:07.228696');
INSERT INTO "VetCalendar_calendar" VALUES (4780,'DH','','2023-12-05 15:00:00','2023-12-06 03:00:00','12',2023,'2023-12-04 06:51:07.233322','2023-12-04 06:51:07.233322');
INSERT INTO "VetCalendar_calendar" VALUES (4781,'DH','','2023-12-06 15:00:00','2023-12-07 03:00:00','12',2023,'2023-12-04 06:51:07.237832','2023-12-04 06:51:07.237832');
INSERT INTO "VetCalendar_calendar" VALUES (4782,'AC','','2023-12-07 15:00:00','2023-12-08 03:00:00','12',2023,'2023-12-04 06:51:07.243246','2023-12-04 06:51:07.243246');
INSERT INTO "VetCalendar_calendar" VALUES (4783,'AC','','2023-12-08 15:00:00','2023-12-09 03:00:00','12',2023,'2023-12-04 06:51:07.249068','2023-12-04 06:51:07.249068');
INSERT INTO "VetCalendar_calendar" VALUES (4784,'AC','','2023-12-09 15:00:00','2023-12-10 03:00:00','12',2023,'2023-12-04 06:51:07.252715','2023-12-04 06:51:07.252715');
INSERT INTO "VetCalendar_calendar" VALUES (4785,'TB','','2023-12-03 18:00:00','2023-12-04 06:00:00','12',2023,'2023-12-04 06:51:07.257520','2023-12-04 06:51:07.257520');
INSERT INTO "VetCalendar_calendar" VALUES (4786,'TR','','2023-12-04 18:00:00','2023-12-05 06:00:00','12',2023,'2023-12-04 06:51:07.262639','2023-12-04 06:51:07.262639');
INSERT INTO "VetCalendar_calendar" VALUES (4787,'TR','','2023-12-05 18:00:00','2023-12-06 06:00:00','12',2023,'2023-12-04 06:51:07.267016','2023-12-04 06:51:07.267016');
INSERT INTO "VetCalendar_calendar" VALUES (4788,'NW','','2023-12-06 18:00:00','2023-12-07 06:00:00','12',2023,'2023-12-04 06:51:07.271471','2023-12-04 06:51:07.271471');
INSERT INTO "VetCalendar_calendar" VALUES (4789,'DH','','2023-12-07 18:00:00','2023-12-08 06:00:00','12',2023,'2023-12-04 06:51:07.275936','2023-12-04 06:51:07.275936');
INSERT INTO "VetCalendar_calendar" VALUES (4790,'TB','','2023-12-08 18:00:00','2023-12-09 06:00:00','12',2023,'2023-12-04 06:51:07.281433','2023-12-04 06:51:07.281433');
INSERT INTO "VetCalendar_calendar" VALUES (4791,'TB','','2023-12-09 18:00:00','2023-12-10 06:00:00','12',2023,'2023-12-04 06:51:07.285266','2023-12-04 06:51:07.285266');
INSERT INTO "VetCalendar_calendar" VALUES (4792,'NW','','2023-12-08 22:00:00','2023-12-09 10:00:00','12',2023,'2023-12-04 06:51:07.290666','2023-12-04 06:51:07.290666');
INSERT INTO "VetCalendar_calendar" VALUES (4793,'ST','','2023-12-04 02:00:00','2023-12-04 14:00:00','12',2023,'2023-12-04 06:51:07.295174','2023-12-04 06:51:07.295174');
INSERT INTO "VetCalendar_calendar" VALUES (4794,'ST','','2023-12-05 02:00:00','2023-12-05 14:00:00','12',2023,'2023-12-04 06:51:07.299026','2023-12-04 06:51:07.299026');
INSERT INTO "VetCalendar_calendar" VALUES (4795,'MA','','2023-12-06 02:00:00','2023-12-06 14:00:00','12',2023,'2023-12-04 06:51:07.303220','2023-12-04 06:51:07.303220');
INSERT INTO "VetCalendar_calendar" VALUES (4796,'MA','','2023-12-07 02:00:00','2023-12-07 14:00:00','12',2023,'2023-12-04 06:51:07.308594','2023-12-04 06:51:07.308594');
INSERT INTO "VetCalendar_calendar" VALUES (4797,'ST','','2023-12-08 02:00:00','2023-12-08 14:00:00','12',2023,'2023-12-04 06:51:07.312716','2023-12-04 06:51:07.312716');
INSERT INTO "VetCalendar_calendar" VALUES (4798,'TR','','2023-12-09 02:00:00','2023-12-09 14:00:00','12',2023,'2023-12-04 06:51:07.317185','2023-12-04 06:51:07.317185');
INSERT INTO "VetCalendar_calendar" VALUES (4799,'TR','','2023-12-10 02:00:00','2023-12-10 14:00:00','12',2023,'2023-12-04 06:51:07.322257','2023-12-04 06:51:07.322257');
INSERT INTO "VetCalendar_calendar" VALUES (4800,'DH','','2023-12-10 15:00:00','2023-12-11 03:00:00','12',2023,'2023-12-04 06:51:07.327602','2023-12-04 06:51:07.327602');
INSERT INTO "VetCalendar_calendar" VALUES (4801,'NW','','2023-12-11 15:00:00','2023-12-12 03:00:00','12',2023,'2023-12-04 06:51:07.332619','2023-12-04 06:51:07.332619');
INSERT INTO "VetCalendar_calendar" VALUES (4802,'ST','','2023-12-12 15:00:00','2023-12-13 03:00:00','12',2023,'2023-12-04 06:51:07.337326','2023-12-04 06:51:07.337326');
INSERT INTO "VetCalendar_calendar" VALUES (4803,'ST','','2023-12-13 15:00:00','2023-12-14 03:00:00','12',2023,'2023-12-04 06:51:07.342565','2023-12-04 06:51:07.342565');
INSERT INTO "VetCalendar_calendar" VALUES (4804,'AC','','2023-12-14 15:00:00','2023-12-15 03:00:00','12',2023,'2023-12-04 06:51:07.348127','2023-12-04 06:51:07.348127');
INSERT INTO "VetCalendar_calendar" VALUES (4805,'AC','','2023-12-15 15:00:00','2023-12-16 03:00:00','12',2023,'2023-12-04 06:51:07.358338','2023-12-04 06:51:07.358338');
INSERT INTO "VetCalendar_calendar" VALUES (4806,'AC','','2023-12-16 15:00:00','2023-12-17 03:00:00','12',2023,'2023-12-04 06:51:07.362534','2023-12-04 06:51:07.362534');
INSERT INTO "VetCalendar_calendar" VALUES (4807,'NB','','2023-12-10 18:00:00','2023-12-11 06:00:00','12',2023,'2023-12-04 06:51:07.367482','2023-12-04 06:51:07.367482');
INSERT INTO "VetCalendar_calendar" VALUES (4808,'JK','','2023-12-11 18:00:00','2023-12-12 06:00:00','12',2023,'2023-12-04 06:51:07.372295','2023-12-04 06:51:07.372295');
INSERT INTO "VetCalendar_calendar" VALUES (4809,'TR','','2023-12-12 18:00:00','2023-12-13 06:00:00','12',2023,'2023-12-04 06:51:07.376981','2023-12-04 06:51:07.376981');
INSERT INTO "VetCalendar_calendar" VALUES (4810,'NW','','2023-12-13 18:00:00','2023-12-14 06:00:00','12',2023,'2023-12-04 06:51:07.381715','2023-12-04 06:51:07.381715');
INSERT INTO "VetCalendar_calendar" VALUES (4811,'MC','','2023-12-14 18:00:00','2023-12-15 06:00:00','12',2023,'2023-12-04 06:51:07.386683','2023-12-04 06:51:07.386683');
INSERT INTO "VetCalendar_calendar" VALUES (4812,'TR','','2023-12-15 18:00:00','2023-12-16 06:00:00','12',2023,'2023-12-04 06:51:07.391482','2023-12-04 06:51:07.391482');
INSERT INTO "VetCalendar_calendar" VALUES (4813,'DH','','2023-12-16 18:00:00','2023-12-17 06:00:00','12',2023,'2023-12-04 06:51:07.395841','2023-12-04 06:51:07.395841');
INSERT INTO "VetCalendar_calendar" VALUES (4814,'TB','','2023-12-12 22:00:00','2023-12-13 10:00:00','12',2023,'2023-12-04 06:51:07.400895','2023-12-04 06:51:07.400895');
INSERT INTO "VetCalendar_calendar" VALUES (4815,'TB','','2023-12-13 22:00:00','2023-12-14 10:00:00','12',2023,'2023-12-04 06:51:07.406181','2023-12-04 06:51:07.406181');
INSERT INTO "VetCalendar_calendar" VALUES (4816,'TB','','2023-12-14 22:00:00','2023-12-15 10:00:00','12',2023,'2023-12-04 06:51:07.410687','2023-12-04 06:51:07.410687');
INSERT INTO "VetCalendar_calendar" VALUES (4817,'TR','','2023-12-11 02:00:00','2023-12-11 14:00:00','12',2023,'2023-12-04 06:51:07.415534','2023-12-04 06:51:07.415534');
INSERT INTO "VetCalendar_calendar" VALUES (4818,'DH','','2023-12-12 02:00:00','2023-12-12 14:00:00','12',2023,'2023-12-04 06:51:07.419681','2023-12-04 06:51:07.419681');
INSERT INTO "VetCalendar_calendar" VALUES (4819,'DH','','2023-12-13 02:00:00','2023-12-13 14:00:00','12',2023,'2023-12-04 06:51:07.424151','2023-12-04 06:51:07.424151');
INSERT INTO "VetCalendar_calendar" VALUES (4820,'MA','','2023-12-14 02:00:00','2023-12-14 14:00:00','12',2023,'2023-12-04 06:51:07.429058','2023-12-04 06:51:07.429058');
INSERT INTO "VetCalendar_calendar" VALUES (4821,'MA','','2023-12-15 02:00:00','2023-12-15 14:00:00','12',2023,'2023-12-04 06:51:07.433787','2023-12-04 06:51:07.433787');
INSERT INTO "VetCalendar_calendar" VALUES (4822,'NW','','2023-12-16 02:00:00','2023-12-16 14:00:00','12',2023,'2023-12-04 06:51:07.438286','2023-12-04 06:51:07.438286');
INSERT INTO "VetCalendar_calendar" VALUES (4823,'NW','','2023-12-17 02:00:00','2023-12-17 14:00:00','12',2023,'2023-12-04 06:51:07.443324','2023-12-04 06:51:07.443324');
INSERT INTO "VetCalendar_calendar" VALUES (4824,'TR','','2023-12-17 15:00:00','2023-12-18 03:00:00','12',2023,'2023-12-04 06:51:07.448605','2023-12-04 06:51:07.448605');
INSERT INTO "VetCalendar_calendar" VALUES (4825,'ST','','2023-12-18 15:00:00','2023-12-19 03:00:00','12',2023,'2023-12-04 06:51:07.452330','2023-12-04 06:51:07.452330');
INSERT INTO "VetCalendar_calendar" VALUES (4826,'ST','','2023-12-19 15:00:00','2023-12-20 03:00:00','12',2023,'2023-12-04 06:51:07.457675','2023-12-04 06:51:07.457675');
INSERT INTO "VetCalendar_calendar" VALUES (4827,'ST','','2023-12-20 15:00:00','2023-12-21 03:00:00','12',2023,'2023-12-04 06:51:07.461474','2023-12-04 06:51:07.461474');
INSERT INTO "VetCalendar_calendar" VALUES (4828,'AC','','2023-12-21 15:00:00','2023-12-22 03:00:00','12',2023,'2023-12-04 06:51:07.467020','2023-12-04 06:51:07.467020');
INSERT INTO "VetCalendar_calendar" VALUES (4829,'AC','','2023-12-22 15:00:00','2023-12-23 03:00:00','12',2023,'2023-12-04 06:51:07.470987','2023-12-04 06:51:07.470987');
INSERT INTO "VetCalendar_calendar" VALUES (4830,'AC','','2023-12-23 15:00:00','2023-12-24 03:00:00','12',2023,'2023-12-04 06:51:07.474836','2023-12-04 06:51:07.474836');
INSERT INTO "VetCalendar_calendar" VALUES (4831,'MC/NB','','2023-12-17 18:00:00','2023-12-18 06:00:00','12',2023,'2023-12-04 06:51:07.479843','2023-12-04 06:51:07.479843');
INSERT INTO "VetCalendar_calendar" VALUES (4832,'TR','','2023-12-18 18:00:00','2023-12-19 06:00:00','12',2023,'2023-12-04 06:51:07.483939','2023-12-04 06:51:07.483939');
INSERT INTO "VetCalendar_calendar" VALUES (4833,'TB','','2023-12-19 18:00:00','2023-12-20 06:00:00','12',2023,'2023-12-04 06:51:07.488695','2023-12-04 06:51:07.488695');
INSERT INTO "VetCalendar_calendar" VALUES (4834,'TB','','2023-12-20 18:00:00','2023-12-21 06:00:00','12',2023,'2023-12-04 06:51:07.492696','2023-12-04 06:51:07.492696');
INSERT INTO "VetCalendar_calendar" VALUES (4835,'MC 12-12','','2023-12-21 18:00:00','2023-12-22 06:00:00','12',2023,'2023-12-04 06:51:07.497077','2023-12-04 06:51:07.497077');
INSERT INTO "VetCalendar_calendar" VALUES (4836,'DH','','2023-12-22 18:00:00','2023-12-23 06:00:00','12',2023,'2023-12-04 06:51:07.501522','2023-12-04 06:51:07.501522');
INSERT INTO "VetCalendar_calendar" VALUES (4837,'JK','','2023-12-23 18:00:00','2023-12-24 06:00:00','12',2023,'2023-12-04 06:51:07.505836','2023-12-04 06:51:07.505836');
INSERT INTO "VetCalendar_calendar" VALUES (4838,'TR','','2023-12-19 22:00:00','2023-12-20 10:00:00','12',2023,'2023-12-04 06:51:07.510611','2023-12-04 06:51:07.510611');
INSERT INTO "VetCalendar_calendar" VALUES (4839,'MC','','2023-12-20 22:00:00','2023-12-21 10:00:00','12',2023,'2023-12-04 06:51:07.515216','2023-12-04 06:51:07.515216');
INSERT INTO "VetCalendar_calendar" VALUES (4840,'NW','','2023-12-18 02:00:00','2023-12-18 14:00:00','12',2023,'2023-12-04 06:51:07.519958','2023-12-04 06:51:07.519958');
INSERT INTO "VetCalendar_calendar" VALUES (4841,'MA','','2023-12-19 02:00:00','2023-12-19 14:00:00','12',2023,'2023-12-04 06:51:07.523480','2023-12-04 06:51:07.523480');
INSERT INTO "VetCalendar_calendar" VALUES (4842,'MA','','2023-12-20 02:00:00','2023-12-20 14:00:00','12',2023,'2023-12-04 06:51:07.528503','2023-12-04 06:51:07.528503');
INSERT INTO "VetCalendar_calendar" VALUES (4843,'NW','','2023-12-21 02:00:00','2023-12-21 14:00:00','12',2023,'2023-12-04 06:51:07.532591','2023-12-04 06:51:07.532591');
INSERT INTO "VetCalendar_calendar" VALUES (4844,'NW','','2023-12-22 02:00:00','2023-12-22 14:00:00','12',2023,'2023-12-04 06:51:07.537328','2023-12-04 06:51:07.537328');
INSERT INTO "VetCalendar_calendar" VALUES (4845,'TR','','2023-12-23 02:00:00','2023-12-23 14:00:00','12',2023,'2023-12-04 06:51:07.541771','2023-12-04 06:51:07.541771');
INSERT INTO "VetCalendar_calendar" VALUES (4846,'TR','','2023-12-24 02:00:00','2023-12-24 14:00:00','12',2023,'2023-12-04 06:51:07.545750','2023-12-04 06:51:07.546750');
INSERT INTO "VetCalendar_calendar" VALUES (4847,'MA','','2023-12-24 15:00:00','2023-12-25 03:00:00','12',2023,'2023-12-04 06:51:07.550748','2023-12-04 06:51:07.550748');
INSERT INTO "VetCalendar_calendar" VALUES (4848,'ST','','2023-12-25 15:00:00','2023-12-26 03:00:00','12',2023,'2023-12-04 06:51:07.555030','2023-12-04 06:51:07.555030');
INSERT INTO "VetCalendar_calendar" VALUES (4849,'MA','','2023-12-26 15:00:00','2023-12-27 03:00:00','12',2023,'2023-12-04 06:51:07.559285','2023-12-04 06:51:07.559285');
INSERT INTO "VetCalendar_calendar" VALUES (4850,'AC','','2023-12-27 15:00:00','2023-12-28 03:00:00','12',2023,'2023-12-04 06:51:07.564887','2023-12-04 06:51:07.564887');
INSERT INTO "VetCalendar_calendar" VALUES (4851,'AC','','2023-12-28 15:00:00','2023-12-29 03:00:00','12',2023,'2023-12-04 06:51:07.569635','2023-12-04 06:51:07.569635');
INSERT INTO "VetCalendar_calendar" VALUES (4852,'AC','','2023-12-29 15:00:00','2023-12-30 03:00:00','12',2023,'2023-12-04 06:51:07.573234','2023-12-04 06:51:07.573234');
INSERT INTO "VetCalendar_calendar" VALUES (4853,'NW','','2023-12-30 15:00:00','2023-12-31 03:00:00','12',2023,'2023-12-04 06:51:07.578062','2023-12-04 06:51:07.578062');
INSERT INTO "VetCalendar_calendar" VALUES (4854,'JK','','2023-12-24 18:00:00','2023-12-25 06:00:00','12',2023,'2023-12-04 06:51:07.583590','2023-12-04 06:51:07.583590');
INSERT INTO "VetCalendar_calendar" VALUES (4855,'TB','','2023-12-25 18:00:00','2023-12-26 06:00:00','12',2023,'2023-12-04 06:51:07.587579','2023-12-04 06:51:07.587579');
INSERT INTO "VetCalendar_calendar" VALUES (4856,'TB','','2023-12-26 18:00:00','2023-12-27 06:00:00','12',2023,'2023-12-04 06:51:07.592197','2023-12-04 06:51:07.592197');
INSERT INTO "VetCalendar_calendar" VALUES (4857,'MA','','2023-12-27 18:00:00','2023-12-28 06:00:00','12',2023,'2023-12-04 06:51:07.597029','2023-12-04 06:51:07.597029');
INSERT INTO "VetCalendar_calendar" VALUES (4858,'MC','','2023-12-28 18:00:00','2023-12-29 06:00:00','12',2023,'2023-12-04 06:51:07.601553','2023-12-04 06:51:07.601553');
INSERT INTO "VetCalendar_calendar" VALUES (4859,'JK','','2023-12-29 18:00:00','2023-12-30 06:00:00','12',2023,'2023-12-04 06:51:07.606246','2023-12-04 06:51:07.606246');
INSERT INTO "VetCalendar_calendar" VALUES (4860,'JK','','2023-12-30 18:00:00','2023-12-31 06:00:00','12',2023,'2023-12-04 06:51:07.610704','2023-12-04 06:51:07.610704');
INSERT INTO "VetCalendar_calendar" VALUES (4861,'','','2023-12-26 22:00:00','2023-12-27 10:00:00','12',2023,'2023-12-04 06:51:07.615601','2023-12-04 06:51:07.615601');
INSERT INTO "VetCalendar_calendar" VALUES (4862,'TB','','2023-12-30 22:00:00','2023-12-31 10:00:00','12',2023,'2023-12-04 06:51:07.619601','2023-12-04 06:51:07.619601');
INSERT INTO "VetCalendar_calendar" VALUES (4863,'DH','','2023-12-25 02:00:00','2023-12-25 14:00:00','12',2023,'2023-12-04 06:51:07.624429','2023-12-04 06:51:07.624429');
INSERT INTO "VetCalendar_calendar" VALUES (4864,'DH','','2023-12-26 02:00:00','2023-12-26 14:00:00','12',2023,'2023-12-04 06:51:07.628864','2023-12-04 06:51:07.628864');
INSERT INTO "VetCalendar_calendar" VALUES (4865,'TR','','2023-12-27 02:00:00','2023-12-27 14:00:00','12',2023,'2023-12-04 06:51:07.633045','2023-12-04 06:51:07.633045');
INSERT INTO "VetCalendar_calendar" VALUES (4866,'TR','','2023-12-28 02:00:00','2023-12-28 14:00:00','12',2023,'2023-12-04 06:51:07.637999','2023-12-04 06:51:07.637999');
INSERT INTO "VetCalendar_calendar" VALUES (4867,'TR','','2023-12-29 02:00:00','2023-12-29 14:00:00','12',2023,'2023-12-04 06:51:07.642132','2023-12-04 06:51:07.642132');
INSERT INTO "VetCalendar_calendar" VALUES (4868,'DH','','2023-12-30 02:00:00','2023-12-30 14:00:00','12',2023,'2023-12-04 06:51:07.645955','2023-12-04 06:51:07.645955');
INSERT INTO "VetCalendar_calendar" VALUES (4869,'NB','','2023-12-31 02:00:00','2023-12-31 14:00:00','12',2023,'2023-12-04 06:51:07.650737','2023-12-04 06:51:07.650737');
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "VetCalendar_scheduleshift_shift_id_cf8d9ca4" ON "VetCalendar_scheduleshift" (
	"shift_id"
);
CREATE INDEX IF NOT EXISTS "VetCalendar_scheduleshift_shift_type_id_3eae252c" ON "VetCalendar_scheduleshift" (
	"shift_type_id"
);
CREATE INDEX IF NOT EXISTS "VetCalendar_scheduleshift_user_id_ae770d0e" ON "VetCalendar_scheduleshift" (
	"user_id"
);
COMMIT;
