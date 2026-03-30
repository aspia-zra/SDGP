-- Active: 1739273350592@@127.0.0.1@3306@secondverparagonapartment
-- MySQL dump 10.13  Distrib 9.3.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: secondverparagonapartment
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Apartment`
--

DROP TABLE IF EXISTS `Apartment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Apartment` (
  `apartmentID` int NOT NULL AUTO_INCREMENT,
  `locationID` int NOT NULL,
  `apartmentNumber` varchar(20) NOT NULL,
  `Type` varchar(50) DEFAULT NULL,
  `monthlyRent` decimal(10,2) NOT NULL,
  `Status` enum('available','occupied','maintenance') DEFAULT 'available',
  PRIMARY KEY (`apartmentID`),
  KEY `idx_apartment_location` (`locationID`),
  CONSTRAINT `apartment_ibfk_1` FOREIGN KEY (`locationID`) REFERENCES `Location` (`locationID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Apartment`
--

LOCK TABLES `Apartment` WRITE;
/*!40000 ALTER TABLE `Apartment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Apartment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Complaint`
--

DROP TABLE IF EXISTS `Complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Complaint` (
  `complaintID` int NOT NULL AUTO_INCREMENT,
  `tenantID` int NOT NULL,
  `apartmentID` int NOT NULL,
  `Description` text NOT NULL,
  `reportDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `Severity` enum('1','2','3','4','5') NOT NULL DEFAULT '1',
  `Status` enum('open','closed') DEFAULT 'open',
  `Resolution` text,
  PRIMARY KEY (`complaintID`),
  KEY `idx_complaint_tenant` (`tenantID`),
  KEY `idx_complaint_apartment` (`apartmentID`),
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`tenantID`) REFERENCES `Tenant` (`tenantID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `complaint_ibfk_2` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Complaint`
--

LOCK TABLES `Complaint` WRITE;
/*!40000 ALTER TABLE `Complaint` DISABLE KEYS */;
/*!40000 ALTER TABLE `Complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Invoice`
--

DROP TABLE IF EXISTS `Invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Invoice` (
  `invoiceID` int NOT NULL AUTO_INCREMENT,
  `leaseID` int NOT NULL,
  `Amount` decimal(10,2) NOT NULL,
  `dueDate` date NOT NULL,
  `Created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `Status` enum('paid','pending','overdue') DEFAULT 'pending',
  `Description` text,
  PRIMARY KEY (`invoiceID`),
  KEY `idx_invoice_lease` (`leaseID`),
  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`leaseID`) REFERENCES `LeaseAgreement` (`leaseID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Invoice`
--

LOCK TABLES `Invoice` WRITE;
/*!40000 ALTER TABLE `Invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `Invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LeaseAgreement`
--

DROP TABLE IF EXISTS `LeaseAgreement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LeaseAgreement` (
  `leaseID` int NOT NULL AUTO_INCREMENT,
  `tenantID` int NOT NULL,
  `apartmentID` int NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `depositAmount` decimal(10,2) DEFAULT NULL,
  `monthlyRent` decimal(10,2) NOT NULL,
  `Status` enum('active','ended','renewal') DEFAULT 'active',
  PRIMARY KEY (`leaseID`),
  KEY `idx_lease_tenant` (`tenantID`),
  KEY `idx_lease_apartment` (`apartmentID`),
  CONSTRAINT `leaseagreement_ibfk_1` FOREIGN KEY (`tenantID`) REFERENCES `Tenant` (`tenantID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `leaseagreement_ibfk_2` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LeaseAgreement`
--

LOCK TABLES `LeaseAgreement` WRITE;
/*!40000 ALTER TABLE `LeaseAgreement` DISABLE KEYS */;
/*!40000 ALTER TABLE `LeaseAgreement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Location`
--

DROP TABLE IF EXISTS `Location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Location` (
  `locationID` int NOT NULL AUTO_INCREMENT,
  `City` varchar(100) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`locationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Location`
--

LOCK TABLES `Location` WRITE;
/*!40000 ALTER TABLE `Location` DISABLE KEYS */;
/*!40000 ALTER TABLE `Location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MaintenanceLog`
--

DROP TABLE IF EXISTS `MaintenanceLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MaintenanceLog` (
  `logID` int NOT NULL AUTO_INCREMENT,
  `apartmentID` int NOT NULL,
  `userID` int DEFAULT NULL,
  `maintenanceDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `timeTaken` int DEFAULT NULL,
  `Cost` decimal(10,2) DEFAULT NULL,
  `Notes` text,
  PRIMARY KEY (`logID`),
  KEY `idx_maintenance_apartment` (`apartmentID`),
  KEY `idx_maintenance_worker` (`userID`),
  CONSTRAINT `maintenancelog_ibfk_1` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `maintenancelog_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `UserTbl` (`userID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MaintenanceLog`
--

LOCK TABLES `MaintenanceLog` WRITE;
/*!40000 ALTER TABLE `MaintenanceLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `MaintenanceLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ReportLog`
--

DROP TABLE IF EXISTS `ReportLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ReportLog` (
  `reportID` int NOT NULL AUTO_INCREMENT,
  `userID` int DEFAULT NULL,
  `reportType` varchar(255) NOT NULL,
  `Period` date NOT NULL,
  `Generated_At` datetime DEFAULT CURRENT_TIMESTAMP,
  `Data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`reportID`),
  KEY `reportlog_ibfk_1` (`userID`),
  CONSTRAINT `reportlog_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `UserTbl` (`userID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ReportLog`
--

LOCK TABLES `ReportLog` WRITE;
/*!40000 ALTER TABLE `ReportLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `ReportLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tenant`
--

DROP TABLE IF EXISTS `Tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tenant` (
  `tenantID` int NOT NULL AUTO_INCREMENT,
  `fullName` varchar(150) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `national_Insurance` varchar(45) DEFAULT NULL,
  `Email` varchar(150) DEFAULT NULL,
  `Created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `Status` enum('active','inactive') DEFAULT 'active',
  PRIMARY KEY (`tenantID`),
  UNIQUE KEY `email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tenant`
--

LOCK TABLES `Tenant` WRITE;
/*!40000 ALTER TABLE `Tenant` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tenant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserTbl`
--

DROP TABLE IF EXISTS `UserTbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UserTbl` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `fullName` varchar(150) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Email` varchar(150) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Role` enum('admin','manager','maintenance','frontdesk') NOT NULL,
  `locationID` int DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `email` (`Email`),
  KEY `idx_user_location` (`locationID`),
  CONSTRAINT `usertbl_ibfk_1` FOREIGN KEY (`locationID`) REFERENCES `Location` (`locationID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserTbl`
--

LOCK TABLES `UserTbl` WRITE;
/*!40000 ALTER TABLE `UserTbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `UserTbl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-16 14:04:05
