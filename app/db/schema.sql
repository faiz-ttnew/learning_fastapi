CREATE DATABASE IF NOT EXISTS `fastapi_learning`
    CHARACTER SET utf8mb4;

USE `fastapi_learning`;

CREATE TABLE IF NOT EXISTS `employees` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `age` INT NOT NULL,
    `department` VARCHAR(100) NOT NULL,
    `salary` DECIMAL(12, 2) NOT NULL,
    `city` VARCHAR(100) NOT NULL,
    `pincode` VARCHAR(6) NOT NULL,
    `skills` JSON NOT NULL,
    `joining_date` DATE NOT NULL,

    PRIMARY KEY (`id`),
    CONSTRAINT `uk_employees_email` UNIQUE (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;