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
-- Table structure for table patients
--

DROP TABLE IF EXISTS patients;
CREATE TABLE IF NOT EXISTS patients (
  PatientID CHAR(3) NOT NULL,
  PatientName VarChar(50) NOT NULL,
  ContactNo CHAR(8) NOT NULL,
  Email VarChar(50) NOT NULL,
  NRIC CHAR(9) NOT NULL,
  PRIMARY KEY (PatientID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table patients
--

INSERT INTO patients (PatientID, PatientName, ContactNo, Email, NRIC) VALUES

(100, 'John Doe', '91234567', 'johndoe@gmail.com', 'S9812345W'),
(101, 'Jane Smith', '87654321', 'janesmith@outlook.com', 'T0753829R'),
(102, 'Alice Johnson', '93691470', 'alicejohnson@hotmail.com', 'T0203619F');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;