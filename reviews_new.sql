-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema examprep
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema examprep
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `examprep` DEFAULT CHARACTER SET utf8 ;
USE `examprep` ;

-- -----------------------------------------------------
-- Table `examprep`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examprep`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `alias` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `pw_hash` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examprep`.`authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examprep`.`authors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examprep`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examprep`.`books` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `author_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_books_authors_idx` (`author_id` ASC),
  CONSTRAINT `fk_books_authors`
    FOREIGN KEY (`author_id`)
    REFERENCES `examprep`.`authors` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `examprep`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `examprep`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` INT(11) UNSIGNED NULL,
  `message` VARCHAR(255) NULL,
  `book_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reviews_books1_idx` (`book_id` ASC),
  INDEX `fk_reviews_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_reviews_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `examprep`.`books` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reviews_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `examprep`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
