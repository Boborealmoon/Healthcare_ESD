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
CREATE DATABASE IF NOT EXISTS claims DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE claims;

-- --------------------------------------------------------

--
-- Table structure for table claims
--

DROP TABLE IF EXISTS claims;
CREATE TABLE IF NOT EXISTS claims (
  ClaimID CHAR(3) NOT NULL,
  StatusOfClaims VARCHAR(50) NOT NULL,
  AppointmentID INT NOT NULL,
  CONSTRAINT calendars_pk PRIMARY KEY (ClaimID),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table claims
--

INSERT INTO claims (ClaimID, StatusOfClaims, AppointmentID) VALUES 

(901,'Approved',1);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;