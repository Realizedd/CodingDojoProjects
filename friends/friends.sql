-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema exam
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema exam
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `exam` DEFAULT CHARACTER SET utf8 ;
USE `exam` ;

-- -----------------------------------------------------
-- Table `exam`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `exam`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `alias` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `pw_hash` VARCHAR(255) NULL,
  `date_of_birth` DATETIME NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `exam`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `exam`.`friends` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `owner_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_friends_users_idx` (`user_id` ASC),
  INDEX `fk_friends_users1_idx` (`owner_id` ASC),
  CONSTRAINT `fk_friends_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `exam`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_friends_users1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `exam`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
