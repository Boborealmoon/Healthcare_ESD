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
CREATE DATABASE IF NOT EXISTS calendar DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE calendar;

-- --------------------------------------------------------

--
-- Table structure for table calendar
--

DROP TABLE IF EXISTS calendar;
CREATE TABLE IF NOT EXISTS calendar (
  TimeslotID INT NOT NULL,
  TimeBegin TIME NOT NULL,
  TimeEnd TIME NOT NULL,
  PRIMARY KEY (TimeslotID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table calendar
--

INSERT INTO calendar (TimeslotID, TimeBegin, TimeEnd) VALUES 

(1, '09:00:00', '09:30:00'),
(2, '09:30:00', '10:00:00'),
(3, '10:00:00', '10:30:00'),
(4, '10:30:00', '11:00:00'),
(5, '11:00:00', '11:30:00'),
(6, '11:30:00', '12:00:00'),
(7, '13:00:00', '13:30:00'),
(8, '13:30:00', '14:00:00'),
(9, '14:00:00', '14:30:00'),
(10, '14:30:00', '15:00:00'),
(11, '15:00:00', '15:30:00'),
(12, '15:30:00', '16:00:00'),
(13, '16:00:00', '16:30:00'),
(14, '16:30:00', '17:00:00');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;