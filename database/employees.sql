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
-- Database: employees
--
CREATE DATABASE IF NOT EXISTS employees DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE employees;

-- --------------------------------------------------------

--
-- Table structure for table employees
--

DROP TABLE IF EXISTS employees;
CREATE TABLE IF NOT EXISTS employees (
  EmployeeID CHAR(2) NOT NULL,
  EmployeeName VARCHAR(50) NOT NULL,
  Email VarChar(50) NOT NULL,
  PRIMARY KEY (EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table employees
--

INSERT INTO employees (EmployeeID, EmployeeName, Email) VALUES 

(21,'Bruce Wayne', 'brucewayne@gmail.com');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;