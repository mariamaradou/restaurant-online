-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- -----------------------------------------------------
-- Schema Restaurant
-- -----------------------------------------------------



-- -----------------------------------------------------
-- Table `project_db20_up1046879`.`Restaurant`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Restaurant` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Restaurant` (
  `idRestaurant` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45),
  `password` VARCHAR(45),
  PRIMARY KEY (`idRestaurant`),
  UNIQUE INDEX `password_UNIQUE` (`password` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Customer` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Customer` (
  `idCustomer` INT NOT NULL AUTO_INCREMENT,
  `last_name` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(60) NULL DEFAULT 'Not given',
  `phone` VARCHAR(45) NOT NULL,
 
  PRIMARY KEY (`idCustomer`),
  
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Table`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Table` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Table` (
  `idTable` INT NOT NULL AUTO_INCREMENT,
  `chairs_number` INT NULL,
  `status` VARCHAR(45) NOT NULL DEFAULT '0' COMMENT 'available(1) or not available(0)',
  `Description` VARCHAR(45) NOT NULL COMMENT 'Smoking or non smoking',
  `idRestaurant` INT NOT NULL,
  PRIMARY KEY (`idTable`),
  INDEX `fk_Table_Restaurant1_idx` (`idRestaurant` ASC) ,
  CONSTRAINT `fk_Table_Restaurant1`
    FOREIGN KEY (`idRestaurant`)
    REFERENCES `project_db20_up1046879`.`Restaurant` (`idRestaurant`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Delivery`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Delivery` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Delivery` (
  `idDelivery` INT NOT NULL AUTO_INCREMENT,
  `delivery_time` TIMESTAMP NOT NULL COMMENT 'time the order was made',
  `delivery_approximate_time` TIME NULL COMMENT 'time it takes to arrive',
  `delivery_status` VARCHAR(45) NOT NULL DEFAULT 'unknown' COMMENT 'sent or not sent',
  `idCustomer` INT NOT NULL,
  PRIMARY KEY (`idDelivery`),
  INDEX `fk_Delivery_Customer1_idx` (`idCustomer` ASC) ,
  CONSTRAINT `fk_Delivery_Customer1`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `project_db20_up1046879`.`Customer` (`idCustomer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Reservation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Reservation` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Reservation` (
  `idReservation` INT NOT NULL AUTO_INCREMENT,
  `people_amount` INT NOT NULL,
  `reserve_datetime` DATETIME NOT NULL,
  `idCustomer` INT NOT NULL,
  `idTable` INT NOT NULL,
  PRIMARY KEY (`idReservation`),
  INDEX `fk_Reservation_Customer1_idx` (`idCustomer` ASC) ,
  INDEX `fk_Reservation_Table1_idx` (`idTable` ASC) ,
  CONSTRAINT `fk_Reservation_Customer1`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `project_db20_up1046879`.`Customer` (`idCustomer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Reservation_Table1`
    FOREIGN KEY (`idTable`)
    REFERENCES `project_db20_up1046879`.`Table` (`idTable`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project_db20_up1046879`.`Payment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Payment` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Payment` (
  `idPayment` INT NOT NULL AUTO_INCREMENT,
  `total_amount` DECIMAL NOT NULL,
  `discount` DECIMAL NULL DEFAULT 0,
  `date` TIMESTAMP NOT NULL,
  `Pay_method` VARCHAR(45) NOT NULL DEFAULT 'Cash' COMMENT 'debit card, credit card, cash',
  `idOrder` INT NOT NULL ,
  PRIMARY KEY (`idPayment`),
  INDEX `fk_Payment_Order1_idx` (`idOrder` ASC),
  CONSTRAINT `fk_Payment_Order1`
    FOREIGN KEY (`idOrder`) 
    REFERENCES `project_db20_up1046879`.`Order`(`idOrder`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Order` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Order` (
  `idOrder` INT NOT NULL AUTO_INCREMENT,
  `order_type` VARCHAR(45) NOT NULL DEFAULT 'Sitting' COMMENT 'sitting or delivery',
  `idTable` INT,
  `order_date` DATETIME NULL,
  `idDelivery` INT,
  PRIMARY KEY (`idOrder`),
  INDEX `fk_Order_Table1_idx` (`idTable` ASC) ,
  INDEX `fk_Order_Delivery1_idx` (`idDelivery` ASC) ,
    CONSTRAINT `fk_Order_Table1`
    FOREIGN KEY (`idTable`)
    REFERENCES `project_db20_up1046879`.`Table` (`idTable`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Order_Delivery1`
    FOREIGN KEY (`idDelivery`)
    REFERENCES `project_db20_up1046879`.`Delivery` (`idDelivery`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Menu_item`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Menu_item` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Menu_item` (
  `idMenu_item` INT NOT NULL AUTO_INCREMENT,
  `item_name` VARCHAR(45) NOT NULL,
  `item_price` DECIMAL NOT NULL,
  PRIMARY KEY (`idMenu_item`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Order_item`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Order_item` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Order_item` (
  `idOrder_item` INT NOT NULL AUTO_INCREMENT,
  `availability` VARCHAR(5) NOT NULL COMMENT 'YES OR NO',
  `item_quantity` INT NOT NULL DEFAULT 1,
  `idOrder` INT NOT NULL,
  `idMenu_item` INT NOT NULL,
  INDEX `fk_Order_item_Order1_idx` (`idOrder` ASC) ,
  INDEX `fk_Order_item_Menu_item1_idx` (`idMenu_item` ASC) ,
  PRIMARY KEY (`idOrder_item`),
  CONSTRAINT `fk_Order_item_Order1`
    FOREIGN KEY (`idOrder`)
    REFERENCES `project_db20_up1046879`.`Order` (`idOrder`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Order_item_Menu_item1`
    FOREIGN KEY (`idMenu_item`)
    REFERENCES `project_db20_up1046879`.`Menu_item` (`idMenu_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Restaurant`.`Restaurant_Customer_Association`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project_db20_up1046879`.`Restaurant_Customer_Association` ;

CREATE TABLE IF NOT EXISTS `project_db20_up1046879`.`Restaurant_Customer_Association` (
  `idRestaurant` INT NOT NULL,
  `idCustomer` INT NOT NULL,
  PRIMARY KEY (`idRestaurant`, `idCustomer`),
  INDEX `fk_Restaurant_has_Customer_Customer1_idx` (`idCustomer` ASC) ,
  INDEX `fk_Restaurant_has_Customer_Restaurant1_idx` (`idRestaurant` ASC) ,
  CONSTRAINT `fk_Restaurant_has_Customer_Restaurant1`
    FOREIGN KEY (`idRestaurant`)
    REFERENCES `project_db20_up1046879`.`Restaurant` (`idRestaurant`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Restaurant_has_Customer_Customer1`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `project_db20_up1046879`.`Customer` (`idCustomer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
