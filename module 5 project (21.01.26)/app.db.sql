BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "notes" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"content"	TEXT,
	"id_user"	INTEGER NOT NULL,
	"created_at"	TEXT,
	FOREIGN KEY("id_user") REFERENCES "users"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"login"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
INSERT INTO "notes" VALUES (1,'Конференция ИТ','Содержимое заметки',2,'03.02.2027');
INSERT INTO "notes" VALUES (2,'Список задач','Купить продукты, позвонить в банк',1,'07.02.2027');
INSERT INTO "notes" VALUES (3,'Отчёт за квартал','Подготовить отчёт для руководителя',3,'14.02.2027');
INSERT INTO "notes" VALUES (4,'Идеи для проекта','Добавить авторизацию и кэширование',2,'21.02.2027');
INSERT INTO "notes" VALUES (5,'Встреча с командой','Обсудить сроки и распределение задач',4,'28.02.2027');
INSERT INTO "users" VALUES (1,'admin');
INSERT INTO "users" VALUES (2,'user25');
INSERT INTO "users" VALUES (3,'ivanov');
INSERT INTO "users" VALUES (4,'petrova');
COMMIT;
