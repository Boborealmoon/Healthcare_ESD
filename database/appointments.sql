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
CREATE DATABASE IF NOT EXISTS smuclinic DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE smuclinic;

-- --------------------------------------------------------

--
-- Table structure for table orders
--

DROP TABLE IF EXISTS appointments;
CREATE TABLE IF NOT EXISTS appointments (
  AppointmentID INT NOT NULL,
  AppointmentDate DATE NOT NULL,
  TimeslotID INT NOT NULL,
  EmployeeID CHAR(2) NOT NULL,
  PatientID CHAR(3) NOT NULL,
  PatientName VARCHAR(50) NOT NULL,
  Claimed BOOLEAN NOT NULL,
  CONSTRAINT appointments_pk PRIMARY KEY (AppointmentID),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table orders
--

INSERT INTO appointments (AppointmentID, AppointmentDate, TimeslotID, EmployeeID, PatientID, PatientName, Claimed) VALUES 

(1, '2024-03-16', 2, 21, 100, 'John Doe', TRUE),
(2, '2024-03-29', 3, 21, 100, 'John Doe', FALSE);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;