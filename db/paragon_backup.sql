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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Apartment`
--

LOCK TABLES `Apartment` WRITE;
/*!40000 ALTER TABLE `Apartment` DISABLE KEYS */;
INSERT INTO `Apartment` VALUES (1,1,'A101','Studio',900.00,'occupied'),(2,1,'A102','1 Bedroom',1100.00,'occupied'),(3,2,'B201','2 Bedroom',1500.00,'occupied'),(4,3,'C301','Studio',850.00,'occupied'),(5,4,'D401','1 Bedroom',1000.00,'available'),(6,2,'B202','2 Bedroom',1550.00,'occupied'),(7,1,'A103','2 Bedroom',1300.00,'occupied'),(8,1,'A104','Studio',950.00,'available'),(9,2,'B203','1 Bedroom',1200.00,'maintenance'),(10,3,'C302','2 Bedroom',1600.00,'occupied');
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
  `InitialIssue` text NOT NULL,
  `FinalResolution` text,
  `Description` text NOT NULL,
  `reportDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `Severity` enum('1','2','3') NOT NULL DEFAULT '1',
  `Status` enum('open','closed') DEFAULT 'open',
  PRIMARY KEY (`complaintID`),
  KEY `idx_complaint_tenant` (`tenantID`),
  KEY `idx_complaint_apartment` (`apartmentID`),
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`tenantID`) REFERENCES `Tenant` (`tenantID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `complaint_ibfk_2` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Complaint`
--

LOCK TABLES `Complaint` WRITE;
/*!40000 ALTER TABLE `Complaint` DISABLE KEYS */;
INSERT INTO `Complaint` VALUES (1,1,1,'','Boiler repaired','Heating not working','2025-12-10 10:00:00','3','closed'),(2,2,2,'','Pipe replaced','Water leak in bathroom','2026-01-12 09:30:00','4','closed'),(3,3,3,'',NULL,'Broken window','2026-02-05 14:20:00','2','open'),(4,4,4,'',NULL,'Noise from neighbours','2026-03-02 19:10:00','1','open'),(5,5,6,'','Fan replaced','Kitchen extractor fan broken','2026-01-22 11:00:00','2','closed'),(6,2,2,'Mould in bathroom',NULL,'Mould spreading on ceiling','2026-03-26 14:35:33','3','open'),(7,3,3,'Broken heater',NULL,'No heating in winter','2026-03-26 14:35:33','5','open');
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Invoice`
--

LOCK TABLES `Invoice` WRITE;
/*!40000 ALTER TABLE `Invoice` DISABLE KEYS */;
INSERT INTO `Invoice` VALUES (14,1,900.00,'2025-12-01','2025-11-25 00:00:00','paid','Monthly rent'),(15,1,900.00,'2026-01-01','2025-12-26 00:00:00','paid','Monthly rent'),(16,1,900.00,'2026-02-01','2026-01-25 00:00:00','paid','Monthly rent'),(17,1,900.00,'2026-03-01','2026-02-25 00:00:00','pending','Monthly rent'),(18,2,1100.00,'2026-01-01','2025-12-20 00:00:00','paid','Monthly rent'),(19,2,1100.00,'2026-02-01','2026-01-20 00:00:00','paid','Monthly rent'),(20,2,1100.00,'2026-03-01','2026-02-20 00:00:00','pending','Monthly rent'),(21,3,1500.00,'2026-02-01','2026-01-20 00:00:00','paid','Monthly rent'),(22,3,1500.00,'2026-03-01','2026-02-20 00:00:00','paid','Monthly rent'),(23,4,850.00,'2025-12-01','2025-11-20 00:00:00','paid','Monthly rent'),(24,4,850.00,'2026-01-01','2025-12-20 00:00:00','paid','Monthly rent'),(25,4,850.00,'2026-02-01','2026-01-20 00:00:00','paid','Monthly rent'),(26,5,1550.00,'2026-03-01','2026-02-15 00:00:00','pending','Monthly rent'),(27,1,900.00,'2025-11-01','2025-10-25 00:00:00','paid','Monthly rent'),(28,1,900.00,'2025-10-01','2025-09-25 00:00:00','paid','Monthly rent'),(29,1,900.00,'2025-09-01','2025-08-25 00:00:00','paid','Monthly rent'),(30,1,900.00,'2025-08-01','2025-07-25 00:00:00','paid','Monthly rent'),(31,1,900.00,'2025-07-01','2025-06-25 00:00:00','paid','Monthly rent'),(32,2,1100.00,'2025-12-01','2025-11-20 00:00:00','paid','Monthly rent'),(33,2,1100.00,'2025-11-01','2025-10-20 00:00:00','paid','Monthly rent'),(34,2,1100.00,'2025-10-01','2025-09-20 00:00:00','paid','Monthly rent'),(35,2,1100.00,'2025-09-01','2025-08-20 00:00:00','paid','Monthly rent'),(36,3,1500.00,'2026-01-01','2025-12-20 00:00:00','paid','Monthly rent'),(37,3,1500.00,'2025-12-01','2025-11-20 00:00:00','paid','Monthly rent'),(38,3,1500.00,'2025-11-01','2025-10-20 00:00:00','paid','Monthly rent'),(39,4,850.00,'2025-11-01','2025-10-20 00:00:00','paid','Monthly rent'),(40,4,850.00,'2025-10-01','2025-09-20 00:00:00','paid','Monthly rent'),(41,4,850.00,'2025-09-01','2025-08-20 00:00:00','paid','Monthly rent'),(42,5,1550.00,'2026-02-01','2026-01-15 00:00:00','paid','Monthly rent'),(43,5,1550.00,'2026-01-01','2025-12-15 00:00:00','paid','Monthly rent'),(44,5,1550.00,'2025-12-01','2025-11-15 00:00:00','paid','Monthly rent'),(45,6,1300.00,'2026-03-01','2026-02-15 00:00:00','paid','Monthly rent'),(46,6,1300.00,'2026-02-01','2026-01-15 00:00:00','paid','Monthly rent'),(47,6,1300.00,'2026-01-01','2025-12-15 00:00:00','paid','Monthly rent'),(48,6,1300.00,'2025-12-01','2025-11-15 00:00:00','paid','Monthly rent'),(49,6,1300.00,'2025-11-01','2025-10-15 00:00:00','paid','Monthly rent'),(50,1,900.00,'2026-04-01','2026-03-26 14:35:33','overdue','Late rent'),(51,2,1100.00,'2026-04-01','2026-03-26 14:35:33','pending','Upcoming rent'),(52,3,1500.00,'2026-04-01','2026-03-26 14:35:33','paid','Monthly rent');
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LeaseAgreement`
--

LOCK TABLES `LeaseAgreement` WRITE;
/*!40000 ALTER TABLE `LeaseAgreement` DISABLE KEYS */;
INSERT INTO `LeaseAgreement` VALUES (1,1,1,'2025-11-01','2026-10-31',900.00,'active'),(2,2,2,'2025-12-01','2026-11-30',1100.00,'active'),(3,3,3,'2026-01-01','2026-12-31',1500.00,'active'),(4,4,4,'2025-11-15','2026-11-14',850.00,'active'),(5,5,6,'2026-02-01','2027-01-31',1550.00,'active'),(6,7,7,'2026-01-01','2026-12-31',1300.00,'active'),(7,6,3,'2026-03-01','2027-02-28',1500.00,'active'),(8,7,7,'2026-03-01','2027-02-28',1300.00,'active');
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
  `userID` int DEFAULT NULL,
  `maintenanceDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `Priority` enum('1','2','3') NOT NULL DEFAULT '2',
  `InitialIssue` text,
  `RepairDetails` text,
  `FinalResolution` text,
  `timeTaken` int DEFAULT NULL,
  `Cost` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`logID`),
  KEY `idx_maintenance_apartment` (`apartmentID`),
  KEY `fk_maintenancelog_userID` (`userID`),
  CONSTRAINT `fk_maintenancelog_userID` FOREIGN KEY (`userID`) REFERENCES `UserTbl` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `maintenancelog_ibfk_1` FOREIGN KEY (`apartmentID`) REFERENCES `Apartment` (`apartmentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MaintenanceLog`
--

LOCK TABLES `MaintenanceLog` WRITE;
/*!40000 ALTER TABLE `MaintenanceLog` DISABLE KEYS */;
INSERT INTO `MaintenanceLog` VALUES (1,1,5,'2025-12-11 11:00:00','2',NULL,NULL,NULL,120,150.00),(2,2,5,'2026-01-13 10:30:00','2',NULL,NULL,NULL,90,120.00),(3,3,7,'2026-02-06 13:00:00','2',NULL,NULL,NULL,60,80.00),(4,6,7,'2026-01-23 12:00:00','2',NULL,NULL,NULL,45,60.00),(5,1,5,'2025-11-15 14:30:00','2',NULL,NULL,NULL,60,95.00),(6,2,5,'2025-12-05 09:15:00','2',NULL,NULL,NULL,45,75.00),(7,3,7,'2026-01-20 11:45:00','2',NULL,NULL,NULL,120,200.00),(8,4,7,'2025-10-10 10:00:00','2',NULL,NULL,NULL,30,50.00),(9,6,5,'2025-11-30 13:20:00','2',NULL,NULL,NULL,90,135.00),(10,2,5,'2026-03-26 14:35:33','3','Severe leak','Pipe replaced','Leak fixed',120,200.00),(11,3,7,'2026-03-26 14:35:33','1','Routine check','Inspection done','No issues',30,40.00);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ReportLog`
--

LOCK TABLES `ReportLog` WRITE;
/*!40000 ALTER TABLE `ReportLog` DISABLE KEYS */;
INSERT INTO `ReportLog` VALUES (1,1,'Monthly Financial','2025-12-01','2025-12-31 18:00:00','December rent report'),(2,1,'Monthly Financial','2026-01-01','2026-01-31 18:00:00','January rent report'),(3,1,'Monthly Financial','2026-02-01','2026-02-28 18:00:00','February rent report'),(4,1,'Monthly Financial','2026-03-01','2026-03-10 18:00:00','March rent report'),(5,1,'Maintenance Summary','2026-03-01','2026-03-26 14:35:33','Monthly maintenance overview'),(6,1,'Occupancy Report','2026-03-01','2026-03-26 14:35:33','Apartment occupancy stats');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tenant`
--

LOCK TABLES `Tenant` WRITE;
/*!40000 ALTER TABLE `Tenant` DISABLE KEYS */;
INSERT INTO `Tenant` VALUES (1,2,'Rho','rho@test.com','active'),(2,8,'AB123456C','john.smith@email.com','active'),(3,9,'CD654321A','emma.jones@email.com','active'),(4,10,'EF998877B','michael.lee@email.com','active'),(5,11,'GH776655D','sara.white@email.com','active'),(6,12,'JK554433E','daniel.green@email.com','active'),(7,13,'LM112233E','david.johnson@email.com','active'),(12,2,'AA112233A','alice@email.com','active'),(13,8,'BB223344B','brian@email.com','active');
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
  `Role` enum('tenant','admin','manager','maintenance','frontdesk','finance') NOT NULL,
  `locationID` int DEFAULT NULL,
  `Created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `email` (`Email`),
  KEY `idx_user_location` (`locationID`),
  CONSTRAINT `usertbl_ibfk_1` FOREIGN KEY (`locationID`) REFERENCES `Location` (`locationID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserTbl`
--

LOCK TABLES `UserTbl` WRITE;
/*!40000 ALTER TABLE `UserTbl` DISABLE KEYS */;
INSERT INTO `UserTbl` VALUES (1,'Imaan Mohamed','07999999999','imaan@pams.com','$2b$12$V911MVhGicKRL9PRTDbyyO.pIynN2Tza6JWXQA9thYizVOUaTGfFy','admin',1,NULL),(2,'Rho','07123456789','rho@test.com','$2b$12$clm66bD1lpfOH2f2LntJpeaTTxleBpzDdZ1c9LHGJgc/D3neRX5A2','admin',1,NULL),(3,'Helen Carter','07111111111','helen.admin@paragon.com','pass123','maintenance',1,NULL),(4,'Mark Davies','07222222222','mark@pams.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','manager',2,NULL),(5,'Samir Khan','07333333333','samir.maint@paragon.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','finance',1,NULL),(6,'Lucy Brown','07444444444','lucy.frontdesk@paragon.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','frontdesk',3,NULL),(7,'Tom Wilson','07555555555','tom.maint@paragon.com','$2b$12$fWdlDZZB4TZF0J.8P35.ReHFMXmlCJ1fuQcKHFEmc3X2DPHBatttm','maintenance',4,NULL),(8,'John Smith','07666666666','john.smith@email.com','pass123','tenant',3,NULL),(9,'Emma Jones','07777777777','emma.jones@email.com','pass123','tenant',3,NULL),(10,'Michael Lee','07888888888','michael.lee@email.com','pass123','tenant',3,NULL),(11,'Sara White','07999999999','sara.white@email.com','pass123','tenant',3,NULL),(12,'Daniel Green','071111111111','daniel.green@email.com','pass123','tenant',3,NULL),(13,'David Johnson','07123456789','david.johnson@email.com','$2b$12$clm66bD1lpfOH2f2LntJpeaTTxleBpzDdZ1c9LHGJgc/D3neRX5A2','tenant',3,'2026-03-17 14:22:02'),(15,'test','098765','test@pams.com','$2b$12$gxFSXCblcdzIoqAvTGSWpO6jsXpimDXI9.hERcuLsHLI1QnAovUay','frontdesk',1,'2026-03-18 00:00:00'),(16,'test2','09876543','test.maint@pams.com','$2b$12$bn6yNp6rmqWN48y9.WbaGuCGaJboMjFwPvqA/n1vJ71.mxe9whyRu','maintenance',1,'2026-03-18 00:00:00'),(17,'drashti samgi','0987654321','drashti@pams.com','$2b$12$/FkOweyFwj1wzf8YrYxPz./G3ESBuSAxk/soDuWhz7vOPu4ZpTHPa','frontdesk',1,'2026-03-19 00:00:00'),(18,'tester','098765432','tester@pams.com','$2b$12$A4mipo7CP5aM2m5fYlZBCOWPNJT2ERHX2W6h6Cb8lDSN7WoWkD75m','manager',1,'2026-03-23 00:00:00'),(21,'Alice Cooper','07000000001','alice@email.com','$2b$12$dummyhash1','tenant',2,NULL),(22,'Brian Cox','07000000002','brian@email.com','$2b$12$dummyhash2','tenant',2,NULL),(23,'Charlie Black','07000000003','charlie.maint@paragon.com','$2b$12$dummyhash3','maintenance',2,NULL),(24,'Diana Prince','07000000004','diana.frontdesk@paragon.com','$2b$12$dummyhash4','frontdesk',3,NULL);
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

-- Dump completed on 2026-03-26 14:40:32