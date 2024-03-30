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
CREATE DATABASE IF NOT EXISTS inventory DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE inventory;

-- --------------------------------------------------------

--
-- Table structure for table inventory
--

DROP TABLE IF EXISTS inventory;
CREATE TABLE IF NOT EXISTS inventory (
  ProductID INT,
  ProductName VARCHAR(50) NOT NULL,
  ProductQty INT NOT NULL,
  UnitOfMeasurement VARCHAR(20),
  UnitCost DECIMAL(10, 2),
  SupplierID INT,
  SupplierContactEmail VARCHAR(100),
  Threshold INT,
  UnitsToOrder INT,
  PRIMARY KEY (ProductID,SupplierID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table inventory
--

INSERT INTO inventory (ProductID, ProductName, ProductQty, UnitOfMeasurement, UnitCost, SupplierID, SupplierContactEmail, Threshold, UnitsToOrder) VALUES

(701, 'Aspirin', 0, 'Bottle', 5.99, 81, 'fooseejae@gmail.com', 100, 400),
(702, 'Amoxicillin', 300, 'Box', 24.50, 82, 'jackson&jackson@gmail.com', 50, 200),
(703, 'Lisinopril', 200, 'Each', 0.25, 82, 'jackson&jackson@gmail.com', 30, 200),
(704, 'Simvastatin', 400, 'Bottle', 12.75, 82, 'jackson&jackson@gmail.com', 80, 300),
(705, 'Metformin', 350, 'Box', 18.99, 82, 'jackson&jackson@gmail.com', 60, 200),
(706, 'Atorvastatin', 250, 'Each', 4.99, 81, 'shizer@gmail.com', 40, 200),
(707, 'Amlodipine', 150, 'Bottle', 15.75, 81, 'shizer@gmail.com', 20, 100),
(708, 'Ibuprofen', 600, 'Box', 8.99, 81, 'shizer@gmail.com', 120, 400),
(709, 'Omeprazole', 200, 'Each', 3.75, 83, 'Movartis@gmail.com', 30, 200),
(710, 'Losartan', 300, 'Bottle', 16.50, 83, 'Movartis@gmail.com', 70, 300);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;