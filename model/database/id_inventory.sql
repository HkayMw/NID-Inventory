BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `batch` (
	`id`	INTEGER,
	`name`	TEXT NOT NULL,
	`storage`	INTEGER,
	`count`	INTEGER,
	`qr_text`	TEXT,
	`created_on`	TEXT NOT NULL,
	`updated_on`	TEXT,
	`created_by`	TEXT NOT NULL,
	`updated_by`	TEXT,
	PRIMARY KEY(`id` AUTOINCREMENT),
	CONSTRAINT `sorting_key_creator` FOREIGN KEY(`created_by`) REFERENCES `user`(`id_number`),
	CONSTRAINT `stored_in` FOREIGN KEY(`storage`) REFERENCES `storage_unit`(`id`),
	CONSTRAINT `sorting_key_modifier` FOREIGN KEY(`updated_by`) REFERENCES `user`(`id_number`)
);
CREATE TABLE IF NOT EXISTS `client_portal` (
	`signature`	TEXT,
	`uploaded_on`	TEXT NOT NULL,
	`uploaded_by`	TEXT,
	PRIMARY KEY(`signature`),
	CONSTRAINT `id_reference` FOREIGN KEY(`signature`) REFERENCES `id`(`signature`),
	CONSTRAINT `user_reference` FOREIGN KEY(`uploaded_by`) REFERENCES `user`(`id_number`)
);
CREATE TABLE IF NOT EXISTS `collection` (
	`id`	INT AUTOINCREMENT,
	`signature`	TEXT,
	`issued_out_on`	TEXT NOT NULL,
	`issued_out_by`	TEXT NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`issued_out_by`) REFERENCES `user`(`id_number`),
	FOREIGN KEY(`signature`) REFERENCES `id`(`signature`)
);
CREATE TABLE IF NOT EXISTS `contact` (
	`id_number`	TEXT,
	`phone_number`	TEXT NOT NULL,
	`created_on`	TEXT NOT NULL,
	`updated_on`	TEXT,
	`created_by`	TEXT NOT NULL,
	`updated_by`	TEXT,
	PRIMARY KEY(`id_number`),
	CONSTRAINT `contact_creator` FOREIGN KEY(`created_by`) REFERENCES `user`(`id_number`),
	CONSTRAINT `contact_modifier` FOREIGN KEY(`updated_by`) REFERENCES `user`(`id_number`)
);
CREATE TABLE IF NOT EXISTS `id` (
	`signature`	TEXT,
	`id_number`	TEXT,
	`firstname`	TEXT NOT NULL,
	`lastname`	TEXT NOT NULL,
	`othernames`	TEXT,
	`gender`	TEXT NOT NULL,
	`d_o_b`	TEXT NOT NULL,
	`status`	TEXT NOT NULL,
	`batch`	INTEGER,
	`notified_on`	TEXT,
	`created_on`	TEXT NOT NULL,
	`updated_on`	TEXT,
	`created_by`	TEXT NOT NULL,
	`updated_by`	TEXT,
	PRIMARY KEY(`signature`),
	CONSTRAINT `sorted_on` FOREIGN KEY(`batch`) REFERENCES `batch`(`id`),
	CONSTRAINT `id_record_creator` FOREIGN KEY(`created_by`) REFERENCES `user`(`id_number`),
	CONSTRAINT `id_record_modifier` FOREIGN KEY(`updated_by`) REFERENCES `user`(`id_number`)
);
CREATE TABLE IF NOT EXISTS `notification_api` (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`username`	TEXT NOT NULL,
	`api_key`	TEXT NOT NULL,
	PRIMARY KEY(`id` AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS `storage_unit` (
	`id`	INTEGER,
	`label`	TEXT NOT NULL,
	`created_on`	TEXT NOT NULL,
	`updated_on`	TEXT,
	`created_by`	TEXT NOT NULL,
	`updated_by`	TEXT,
	PRIMARY KEY(`id` AUTOINCREMENT),
	CONSTRAINT `storage_unit_creator` FOREIGN KEY(`created_by`) REFERENCES `user`(`id_number`),
	CONSTRAINT `storage_unit_modifier` FOREIGN KEY(`updated_by`) REFERENCES `user`(`id_number`)
);
CREATE TABLE IF NOT EXISTS `user` (
	`id_number`	TEXT NOT NULL,
	`firstname`	TEXT NOT NULL,
	`lastname`	TEXT NOT NULL,
	`othernames`	TEXT,
	`password_hash`	TEXT NOT NULL,
	`user_type`	TEXT NOT NULL,
	`created_on`	TEXT NOT NULL,
	`updated_on`	TEXT,
	`created_by`	TEXT,
	`updated_by`	TEXT,
	PRIMARY KEY(`id_number`),
	CONSTRAINT `account_creator` FOREIGN KEY(`created_by`) REFERENCES `user`(`id_number`),
	CONSTRAINT `account_modifier` FOREIGN KEY(`updated_by`) REFERENCES `user`(`id_number`)
);
CREATE INDEX IF NOT EXISTS `id_number` ON `id` (
	`id_number`
);
COMMIT;
