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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Apartment`
--

LOCK TABLES `Apartment` WRITE;
/*!40000 ALTER TABLE `Apartment` DISABLE KEYS */;
INSERT INTO `Apartment` VALUES (1,1,'A101','Studio',900.00,'occupied'),(2,1,'A102','1 Bedroom',1100.00,'occupied'),(3,2,'B201','2 Bedroom',1500.00,'occupied'),(4,3,'C301','Studio',850.00,'occupied'),(5,4,'D401','1 Bedroom',1000.00,'available'),(6,2,'B202','2 Bedroom',1550.00,'occupied');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Complaint`
--

LOCK TABLES `Complaint` WRITE;
/*!40000 ALTER TABLE `Complaint` DISABLE KEYS */;
INSERT INTO `Complaint` VALUES (1,1,1,'Heating not working','2025-12-10 10:00:00','3','closed','Boiler repaired'),(2,2,2,'Water leak in bathroom','2026-01-12 09:30:00','4','closed','Pipe replaced'),(3,3,3,'Broken window','2026-02-05 14:20:00','2','open',NULL),(4,4,4,'Noise from neighbours','2026-03-02 19:10:00','1','open',NULL),(5,5,6,'Kitchen extractor fan broken','2026-01-22 11:00:00','2','closed','Fan replaced');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Invoice`
--

LOCK TABLES `Invoice` WRITE;
/*!40000 ALTER TABLE `Invoice` DISABLE KEYS */;
INSERT INTO `Invoice` VALUES (14,1,900.00,'2025-12-01','2025-11-25 00:00:00','paid','Monthly rent'),(15,1,900.00,'2026-01-01','2025-12-26 00:00:00','overdue','Monthly rent'),(16,1,900.00,'2026-02-01','2026-01-25 00:00:00','overdue','Monthly rent'),(17,1,900.00,'2026-03-01','2026-02-25 00:00:00','pending','Monthly rent'),(18,2,1100.00,'2026-01-01','2025-12-20 00:00:00','paid','Monthly rent'),(19,2,1100.00,'2026-02-01','2026-01-20 00:00:00','paid','Monthly rent'),(20,2,1100.00,'2026-03-01','2026-02-20 00:00:00','pending','Monthly rent'),(21,3,1500.00,'2026-02-01','2026-01-20 00:00:00','paid','Monthly rent'),(22,3,1500.00,'2026-03-01','2026-02-20 00:00:00','pending','Monthly rent'),(23,4,850.00,'2025-12-01','2025-11-20 00:00:00','paid','Monthly rent'),(24,4,850.00,'2026-01-01','2025-12-20 00:00:00','paid','Monthly rent'),(25,4,850.00,'2026-02-01','2026-01-20 00:00:00','paid','Monthly rent'),(26,5,1550.00,'2026-03-01','2026-02-15 00:00:00','pending','Monthly rent');
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
  `Status` enum('active','ended','renewal') DEFAULT 'active',
  PRIMARY KEY (`leaseID`),
  KEY `idx_lease_tenant` (`tenantID`),
  KEY `idx_lease_apartment` (`apartmentID`),
  CONSTRAINT `leaseagreement_ibfk_1` FOREIGN KEY (`tenantID`) REFERENCES `Tenant` (`tenantID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `leaseagreement_ibfk_2` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LeaseAgreement`
--

LOCK TABLES `LeaseAgreement` WRITE;
/*!40000 ALTER TABLE `LeaseAgreement` DISABLE KEYS */;
INSERT INTO `LeaseAgreement` VALUES (1,1,1,'2025-11-01','2026-10-31',900.00,'active'),(2,2,2,'2025-12-01','2026-11-30',1100.00,'active'),(3,3,3,'2026-01-01','2026-12-31',1500.00,'active'),(4,4,4,'2025-11-15','2026-11-14',850.00,'active'),(5,5,6,'2026-02-01','2027-01-31',1550.00,'active');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Location`
--

LOCK TABLES `Location` WRITE;
/*!40000 ALTER TABLE `Location` DISABLE KEYS */;
INSERT INTO `Location` VALUES (1,'Bristol','1 memory lane','0117*******'),(2,'Bristol','12 Park Street, Bristol','01179234561'),(3,'London','44 Camden Road, London','02071234567'),(4,'Manchester','8 Oxford Road, Manchester','01614567891'),(5,'Cardiff','21 Queen Street, Cardiff','02920345678');
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
  `userID` int NOT NULL,
  `maintenanceDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `timeTaken` int DEFAULT NULL,
  `Cost` decimal(10,2) DEFAULT NULL,
  `Notes` text,
  PRIMARY KEY (`logID`),
  KEY `idx_maintenance_apartment` (`apartmentID`),
  KEY `fk_maintenancelog_userID` (`userID`),
  CONSTRAINT `fk_maintenancelog_userID` FOREIGN KEY (`userID`) REFERENCES `UserTbl` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `maintenancelog_ibfk_1` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MaintenanceLog`
--

LOCK TABLES `MaintenanceLog` WRITE;
/*!40000 ALTER TABLE `MaintenanceLog` DISABLE KEYS */;
INSERT INTO `MaintenanceLog` VALUES (1,1,5,'2025-12-11 11:00:00',120,150.00,'Boiler repair'),(2,2,5,'2026-01-13 10:30:00',90,120.00,'Pipe replacement'),(3,3,7,'2026-02-06 13:00:00',60,80.00,'Temporary window fix'),(4,6,7,'2026-01-23 12:00:00',45,60.00,'Extractor fan replaced');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ReportLog`
--

LOCK TABLES `ReportLog` WRITE;
/*!40000 ALTER TABLE `ReportLog` DISABLE KEYS */;
INSERT INTO `ReportLog` VALUES (1,1,'Monthly Financial','2025-12-01','2025-12-31 18:00:00','December rent report'),(2,1,'Monthly Financial','2026-01-01','2026-01-31 18:00:00','January rent report'),(3,1,'Monthly Financial','2026-02-01','2026-02-28 18:00:00','February rent report'),(4,1,'Monthly Financial','2026-03-01','2026-03-10 18:00:00','March rent report');
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
  `userID` int DEFAULT NULL,
  `national_Insurance` varchar(45) DEFAULT NULL,
  `Email` varchar(150) DEFAULT NULL,
  `Status` enum('active','inactive') DEFAULT 'active',
  PRIMARY KEY (`tenantID`),
  UNIQUE KEY `email` (`Email`),
  KEY `fk_tenant_user` (`userID`),
  CONSTRAINT `fk_tenant_user` FOREIGN KEY (`userID`) REFERENCES `UserTbl` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tenant`
--

LOCK TABLES `Tenant` WRITE;
/*!40000 ALTER TABLE `Tenant` DISABLE KEYS */;
INSERT INTO `Tenant` VALUES (1,2,'Rho','rho@test.com','active'),(2,8,'AB123456C','john.smith@email.com','active'),(3,9,'CD654321A','emma.jones@email.com','active'),(4,10,'EF998877B','michael.lee@email.com','active'),(5,11,'GH776655D','sara.white@email.com','active'),(6,12,'JK554433E','daniel.green@email.com','active');
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
  `Role` enum('tenant','admin','manager','maintenance','frontdesk') NOT NULL,
  `locationID` int DEFAULT NULL,
  `Created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `email` (`Email`),
  KEY `idx_user_location` (`locationID`),
  CONSTRAINT `usertbl_ibfk_1` FOREIGN KEY (`locationID`) REFERENCES `Location` (`locationID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserTbl`
--

LOCK TABLES `UserTbl` WRITE;
/*!40000 ALTER TABLE `UserTbl` DISABLE KEYS */;
INSERT INTO `UserTbl` VALUES (1,'Imaan Mohamed','07389868843','imaan@pams.com','$2b$12$V911MVhGicKRL9PRTDbyyO.pIynN2Tza6JWXQA9thYizVOUaTGfFy','admin',1,NULL),(2,'Rho','07123456789','rho@test.com','$2b$12$clm66bD1lpfOH2f2LntJpeaTTxleBpzDdZ1c9LHGJgc/D3neRX5A2','admin',1,NULL),(3,'Helen Carter','07111111111','helen.admin@paragon.com','pass123','admin',1,NULL),(4,'Mark Davies','07222222222','mark.manager@paragon.com','pass123','manager',2,NULL),(5,'Samir Khan','07333333333','samir.maint@paragon.com','pass123','maintenance',1,NULL),(6,'Lucy Brown','07444444444','lucy.frontdesk@paragon.com','pass123','frontdesk',3,NULL),(7,'Tom Wilson','07555555555','tom.maint@paragon.com','pass123','maintenance',4,NULL),(8,'John Smith','07666666666','john.smith@email.com','pass123','tenant',NULL,NULL),(9,'Emma Jones','07777777777','emma.jones@email.com','pass123','tenant',NULL,NULL),(10,'Michael Lee','07888888888','michael.lee@email.com','pass123','tenant',NULL,NULL),(11,'Sara White','07999999999','sara.white@email.com','pass123','tenant',NULL,NULL),(12,'Daniel Green','071111111111','daniel.green@email.com','pass123','tenant',NULL,NULL);
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

-- Dump completed on 2026-03-12 13:11:14
