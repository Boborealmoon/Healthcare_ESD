-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: smuclinic
--
CREATE DATABASE IF NOT EXISTS orders DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE orders;

-- --------------------------------------------------------

--
-- Table structure for table orders
--

DROP TABLE IF EXISTS orders;
CREATE TABLE IF NOT EXISTS orders (
  OrderID INT  NOT NULL,
  ProductID INT NOT NULL,
  ProductName VARCHAR(50) NOT NULL,
  ProductQty INT NOT NULL,
  UnitsOrdered INT NOT NULL,
  OrderDate DATE NOT NULL,
  SupplierID INT NOT NULL,
  SupplierContactEmail VARCHAR(100),
  CONSTRAINT orders_pk PRIMARY KEY (OrderID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table orders
--

INSERT INTO Orders (OrderID, ProductID, ProductName, ProductQty, UnitsOrdered, OrderDate, SupplierID, SupplierContactEmail) VALUES 

(1, 701, 'Aspirin', 50, 300, '2023-10-15', 81, 'shizer@gmail.com'),
(2, 702, 'Amoxicillin', 40, 200, '2023-11-20', 82, 'jackson&jackson@gmail.com');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;