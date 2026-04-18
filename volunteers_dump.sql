-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: volunteers_db
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(20) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `organization_name` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (1,'ADMIN','+77000000001','',1),(2,'ORG','+77000000002','Добрый штаб',2),(3,'VOLUNTEER','+77000000003','',3),(4,'VOLUNTEER','','',4),(5,'VOLUNTEER','','',5);
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteeravailability`
--

DROP TABLE IF EXISTS `accounts_volunteeravailability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteeravailability` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `weekday` smallint unsigned NOT NULL,
  `time_of_day` varchar(16) NOT NULL,
  `volunteer_profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_volunteeravaila_volunteer_profile_id_wee_9eb6cdab_uniq` (`volunteer_profile_id`,`weekday`,`time_of_day`),
  CONSTRAINT `accounts_volunteerav_volunteer_profile_id_3627589d_fk_accounts_` FOREIGN KEY (`volunteer_profile_id`) REFERENCES `accounts_volunteerprofile` (`id`),
  CONSTRAINT `accounts_volunteeravailability_chk_1` CHECK ((`weekday` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=373 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteeravailability`
--

LOCK TABLES `accounts_volunteeravailability` WRITE;
/*!40000 ALTER TABLE `accounts_volunteeravailability` DISABLE KEYS */;
INSERT INTO `accounts_volunteeravailability` VALUES (353,1,'DAY',1),(354,1,'EVENING',1),(352,1,'MORNING',1),(356,2,'DAY',1),(357,2,'EVENING',1),(355,2,'MORNING',1),(359,3,'DAY',1),(360,3,'EVENING',1),(358,3,'MORNING',1),(362,4,'DAY',1),(363,4,'EVENING',1),(361,4,'MORNING',1),(365,5,'DAY',1),(366,5,'EVENING',1),(364,5,'MORNING',1),(368,6,'DAY',1),(369,6,'EVENING',1),(367,6,'MORNING',1),(371,7,'DAY',1),(372,7,'EVENING',1),(370,7,'MORNING',1);
/*!40000 ALTER TABLE `accounts_volunteeravailability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteerlanguage`
--

DROP TABLE IF EXISTS `accounts_volunteerlanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteerlanguage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` varchar(20) NOT NULL,
  `language_id` bigint NOT NULL,
  `volunteer_profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_volunteerlangua_volunteer_profile_id_lan_68bf3ec2_uniq` (`volunteer_profile_id`,`language_id`),
  KEY `accounts_volunteerla_language_id_63f12775_fk_core_lang` (`language_id`),
  CONSTRAINT `accounts_volunteerla_language_id_63f12775_fk_core_lang` FOREIGN KEY (`language_id`) REFERENCES `core_language` (`id`),
  CONSTRAINT `accounts_volunteerla_volunteer_profile_id_598a0c70_fk_accounts_` FOREIGN KEY (`volunteer_profile_id`) REFERENCES `accounts_volunteerprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerlanguage`
--

LOCK TABLES `accounts_volunteerlanguage` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerlanguage` DISABLE KEYS */;
INSERT INTO `accounts_volunteerlanguage` VALUES (4,'CONVERSATIONAL',3,2),(5,'CONVERSATIONAL',2,2),(6,'CONVERSATIONAL',1,2),(13,'CONVERSATIONAL',1,1),(14,'CONVERSATIONAL',2,1),(15,'CONVERSATIONAL',3,1);
/*!40000 ALTER TABLE `accounts_volunteerlanguage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteerprofile`
--

DROP TABLE IF EXISTS `accounts_volunteerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteerprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gender` varchar(24) NOT NULL,
  `birth_year` smallint unsigned DEFAULT NULL,
  `availability_start_date` date DEFAULT NULL,
  `availability_end_date` date DEFAULT NULL,
  `ready_for_night_shifts` tinyint(1) NOT NULL,
  `can_travel` tinyint(1) NOT NULL,
  `has_car` tinyint(1) NOT NULL,
  `physical_work_ok` tinyint(1) NOT NULL,
  `carry_heavy_ok` tinyint(1) NOT NULL,
  `restrictions_note` longtext NOT NULL,
  `avoid_night_shifts` tinyint(1) NOT NULL,
  `avoid_outdoor_winter_work` tinyint(1) NOT NULL,
  `avoid_large_crowds` tinyint(1) NOT NULL,
  `participation_goal` varchar(32) NOT NULL,
  `motivation_text` longtext NOT NULL,
  `completed_events_count` int unsigned NOT NULL,
  `volunteer_hours` int unsigned NOT NULL,
  `attendance_rate` decimal(5,2) NOT NULL,
  `coordinator_rating` decimal(3,2) NOT NULL,
  `response_speed_hours` int unsigned NOT NULL,
  `profile_completion_percent` smallint unsigned NOT NULL,
  `is_profile_completed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `city_id` bigint DEFAULT NULL,
  `district_id` bigint DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_volunteerprofile_city_id_38b48e5e_fk_core_city_id` (`city_id`),
  KEY `accounts_volunteerpr_district_id_af76c02e_fk_core_dist` (`district_id`),
  CONSTRAINT `accounts_volunteerpr_district_id_af76c02e_fk_core_dist` FOREIGN KEY (`district_id`) REFERENCES `core_district` (`id`),
  CONSTRAINT `accounts_volunteerprofile_city_id_38b48e5e_fk_core_city_id` FOREIGN KEY (`city_id`) REFERENCES `core_city` (`id`),
  CONSTRAINT `accounts_volunteerprofile_user_id_06845d71_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `accounts_volunteerprofile_chk_1` CHECK ((`birth_year` >= 0)),
  CONSTRAINT `accounts_volunteerprofile_chk_2` CHECK ((`completed_events_count` >= 0)),
  CONSTRAINT `accounts_volunteerprofile_chk_3` CHECK ((`volunteer_hours` >= 0)),
  CONSTRAINT `accounts_volunteerprofile_chk_4` CHECK ((`response_speed_hours` >= 0)),
  CONSTRAINT `accounts_volunteerprofile_chk_5` CHECK ((`profile_completion_percent` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile`
--

LOCK TABLES `accounts_volunteerprofile` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile` VALUES (1,'MALE',2000,'2026-04-13','2026-04-14',1,1,1,1,1,'x',0,0,0,'RESUME','x',2,6,66.67,5.00,0,100,1,'2026-04-13 06:38:56.938874','2026-04-18 17:01:41.160824',3,6,3),(2,'',2000,NULL,NULL,0,0,0,1,1,'',0,0,0,'','',1,8,100.00,3.00,0,37,0,'2026-04-15 15:08:23.409644','2026-04-15 15:09:35.044818',NULL,NULL,4),(3,'',NULL,NULL,NULL,0,0,0,1,1,'',0,0,0,'','',2,15,100.00,4.50,0,0,0,'2026-04-15 15:11:17.929288','2026-04-15 15:11:17.929308',NULL,NULL,5);
/*!40000 ALTER TABLE `accounts_volunteerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteerprofile_preferred_directions`
--

DROP TABLE IF EXISTS `accounts_volunteerprofile_preferred_directions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteerprofile_preferred_directions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `volunteerprofile_id` bigint NOT NULL,
  `volunteerdirection_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_volunteerprofil_volunteerprofile_id_volu_e5bdf1b2_uniq` (`volunteerprofile_id`,`volunteerdirection_id`),
  KEY `accounts_volunteerpr_volunteerdirection_i_a73ab7d3_fk_core_volu` (`volunteerdirection_id`),
  CONSTRAINT `accounts_volunteerpr_volunteerdirection_i_a73ab7d3_fk_core_volu` FOREIGN KEY (`volunteerdirection_id`) REFERENCES `core_volunteerdirection` (`id`),
  CONSTRAINT `accounts_volunteerpr_volunteerprofile_id_0753ef96_fk_accounts_` FOREIGN KEY (`volunteerprofile_id`) REFERENCES `accounts_volunteerprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile_preferred_directions`
--

LOCK TABLES `accounts_volunteerprofile_preferred_directions` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile_preferred_directions` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile_preferred_directions` VALUES (1,1,3);
/*!40000 ALTER TABLE `accounts_volunteerprofile_preferred_directions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteerprofile_preferred_task_types`
--

DROP TABLE IF EXISTS `accounts_volunteerprofile_preferred_task_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteerprofile_preferred_task_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `volunteerprofile_id` bigint NOT NULL,
  `tasktype_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_volunteerprofil_volunteerprofile_id_task_28817f2a_uniq` (`volunteerprofile_id`,`tasktype_id`),
  KEY `accounts_volunteerpr_tasktype_id_fa7d4814_fk_core_task` (`tasktype_id`),
  CONSTRAINT `accounts_volunteerpr_tasktype_id_fa7d4814_fk_core_task` FOREIGN KEY (`tasktype_id`) REFERENCES `core_tasktype` (`id`),
  CONSTRAINT `accounts_volunteerpr_volunteerprofile_id_daf8861b_fk_accounts_` FOREIGN KEY (`volunteerprofile_id`) REFERENCES `accounts_volunteerprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile_preferred_task_types`
--

LOCK TABLES `accounts_volunteerprofile_preferred_task_types` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile_preferred_task_types` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile_preferred_task_types` VALUES (1,1,5);
/*!40000 ALTER TABLE `accounts_volunteerprofile_preferred_task_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_volunteerskill`
--

DROP TABLE IF EXISTS `accounts_volunteerskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_volunteerskill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` varchar(20) NOT NULL,
  `skill_id` bigint NOT NULL,
  `volunteer_profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_volunteerskill_volunteer_profile_id_ski_21dbb13d_uniq` (`volunteer_profile_id`,`skill_id`),
  KEY `accounts_volunteerskill_skill_id_3361c0ad_fk_core_skill_id` (`skill_id`),
  CONSTRAINT `accounts_volunteersk_volunteer_profile_id_9486f227_fk_accounts_` FOREIGN KEY (`volunteer_profile_id`) REFERENCES `accounts_volunteerprofile` (`id`),
  CONSTRAINT `accounts_volunteerskill_skill_id_3361c0ad_fk_core_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `core_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerskill`
--

LOCK TABLES `accounts_volunteerskill` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerskill` DISABLE KEYS */;
INSERT INTO `accounts_volunteerskill` VALUES (2,'BEGINNER',3,2),(8,'BEGINNER',1,1),(9,'BEGINNER',3,1);
/*!40000 ALTER TABLE `accounts_volunteerskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applications_application`
--

DROP TABLE IF EXISTS `applications_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL,
  `motivation_text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `position_id` bigint NOT NULL,
  `volunteer_profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `applications_application_position_id_volunteer_pr_e0d658fd_uniq` (`position_id`,`volunteer_profile_id`),
  KEY `applications_applica_volunteer_profile_id_931a906d_fk_accounts_` (`volunteer_profile_id`),
  CONSTRAINT `applications_applica_position_id_05dbc68f_fk_events_ev` FOREIGN KEY (`position_id`) REFERENCES `events_eventposition` (`id`),
  CONSTRAINT `applications_applica_volunteer_profile_id_931a906d_fk_accounts_` FOREIGN KEY (`volunteer_profile_id`) REFERENCES `accounts_volunteerprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications_application`
--

LOCK TABLES `applications_application` WRITE;
/*!40000 ALTER TABLE `applications_application` DISABLE KEYS */;
INSERT INTO `applications_application` VALUES (2,'completed','','2026-04-15 14:53:39.178002',2,1),(3,'completed','','2026-04-15 15:10:03.487941',2,2),(4,'completed','','2026-04-15 15:11:43.010032',2,3),(5,'failed','','2026-04-15 17:44:57.444013',3,1),(8,'confirmed','','2026-04-18 16:31:47.535498',5,1),(9,'invited','','2026-04-18 16:31:54.341914',5,2);
/*!40000 ALTER TABLE `applications_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applications_assignment`
--

DROP TABLE IF EXISTS `applications_assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications_assignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `assigned_by_id` int DEFAULT NULL,
  `position_id` bigint NOT NULL,
  `volunteer_profile_id` bigint NOT NULL,
  `coordinator_rating` smallint unsigned DEFAULT NULL,
  `hours_worked` smallint unsigned NOT NULL,
  `coordinator_note` longtext NOT NULL DEFAULT (_utf8mb4''),
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `applications_assignment_position_id_volunteer_pr_9318d4ab_uniq` (`position_id`,`volunteer_profile_id`),
  KEY `applications_assignment_assigned_by_id_f81dd12c_fk_auth_user_id` (`assigned_by_id`),
  KEY `applications_assignm_volunteer_profile_id_0a51f2a5_fk_accounts_` (`volunteer_profile_id`),
  CONSTRAINT `applications_assignm_position_id_bc3058ca_fk_events_ev` FOREIGN KEY (`position_id`) REFERENCES `events_eventposition` (`id`),
  CONSTRAINT `applications_assignm_volunteer_profile_id_0a51f2a5_fk_accounts_` FOREIGN KEY (`volunteer_profile_id`) REFERENCES `accounts_volunteerprofile` (`id`),
  CONSTRAINT `applications_assignment_assigned_by_id_f81dd12c_fk_auth_user_id` FOREIGN KEY (`assigned_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `applications_assignment_chk_1` CHECK ((`coordinator_rating` >= 0)),
  CONSTRAINT `applications_assignment_chk_2` CHECK ((`hours_worked` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications_assignment`
--

LOCK TABLES `applications_assignment` WRITE;
/*!40000 ALTER TABLE `applications_assignment` DISABLE KEYS */;
INSERT INTO `applications_assignment` VALUES (2,'completed','2026-04-15 14:53:39.191195',2,2,1,5,3,'','2026-04-15 15:14:46.692350'),(3,'completed','2026-04-15 15:10:03.498106',2,2,2,3,8,'','2026-04-15 15:14:59.602627'),(4,'completed','2026-04-15 15:12:37.998313',2,2,3,4,10,'','2026-04-15 15:15:07.869899'),(5,'failed','2026-04-15 17:44:57.459651',2,3,1,5,123,'','2026-04-17 11:33:15.405393'),(8,'confirmed','2026-04-18 16:31:47.554821',2,5,1,NULL,0,'','2026-04-18 16:31:47.558759'),(9,'invited','2026-04-18 16:31:54.352850',2,5,2,NULL,0,'','2026-04-18 16:31:54.358153');
/*!40000 ALTER TABLE `applications_assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add city',7,'add_city'),(26,'Can change city',7,'change_city'),(27,'Can delete city',7,'delete_city'),(28,'Can view city',7,'view_city'),(29,'Can add language',8,'add_language'),(30,'Can change language',8,'change_language'),(31,'Can delete language',8,'delete_language'),(32,'Can view language',8,'view_language'),(33,'Can add skill category',9,'add_skillcategory'),(34,'Can change skill category',9,'change_skillcategory'),(35,'Can delete skill category',9,'delete_skillcategory'),(36,'Can view skill category',9,'view_skillcategory'),(37,'Can add task type',10,'add_tasktype'),(38,'Can change task type',10,'change_tasktype'),(39,'Can delete task type',10,'delete_tasktype'),(40,'Can view task type',10,'view_tasktype'),(41,'Can add volunteer direction',11,'add_volunteerdirection'),(42,'Can change volunteer direction',11,'change_volunteerdirection'),(43,'Can delete volunteer direction',11,'delete_volunteerdirection'),(44,'Can view volunteer direction',11,'view_volunteerdirection'),(45,'Can add skill',12,'add_skill'),(46,'Can change skill',12,'change_skill'),(47,'Can delete skill',12,'delete_skill'),(48,'Can view skill',12,'view_skill'),(49,'Can add district',13,'add_district'),(50,'Can change district',13,'change_district'),(51,'Can delete district',13,'delete_district'),(52,'Can view district',13,'view_district'),(53,'Can add profile',14,'add_profile'),(54,'Can change profile',14,'change_profile'),(55,'Can delete profile',14,'delete_profile'),(56,'Can view profile',14,'view_profile'),(57,'Can add volunteer profile',15,'add_volunteerprofile'),(58,'Can change volunteer profile',15,'change_volunteerprofile'),(59,'Can delete volunteer profile',15,'delete_volunteerprofile'),(60,'Can view volunteer profile',15,'view_volunteerprofile'),(61,'Can add volunteer language',16,'add_volunteerlanguage'),(62,'Can change volunteer language',16,'change_volunteerlanguage'),(63,'Can delete volunteer language',16,'delete_volunteerlanguage'),(64,'Can view volunteer language',16,'view_volunteerlanguage'),(65,'Can add volunteer availability',17,'add_volunteeravailability'),(66,'Can change volunteer availability',17,'change_volunteeravailability'),(67,'Can delete volunteer availability',17,'delete_volunteeravailability'),(68,'Can view volunteer availability',17,'view_volunteeravailability'),(69,'Can add volunteer skill',18,'add_volunteerskill'),(70,'Can change volunteer skill',18,'change_volunteerskill'),(71,'Can delete volunteer skill',18,'delete_volunteerskill'),(72,'Can view volunteer skill',18,'view_volunteerskill'),(73,'Can add event',19,'add_event'),(74,'Can change event',19,'change_event'),(75,'Can delete event',19,'delete_event'),(76,'Can view event',19,'view_event'),(77,'Can add event position',20,'add_eventposition'),(78,'Can change event position',20,'change_eventposition'),(79,'Can delete event position',20,'delete_eventposition'),(80,'Can view event position',20,'view_eventposition'),(81,'Can add event position availability requirement',21,'add_eventpositionavailabilityrequirement'),(82,'Can change event position availability requirement',21,'change_eventpositionavailabilityrequirement'),(83,'Can delete event position availability requirement',21,'delete_eventpositionavailabilityrequirement'),(84,'Can view event position availability requirement',21,'view_eventpositionavailabilityrequirement'),(85,'Can add event position language requirement',22,'add_eventpositionlanguagerequirement'),(86,'Can change event position language requirement',22,'change_eventpositionlanguagerequirement'),(87,'Can delete event position language requirement',22,'delete_eventpositionlanguagerequirement'),(88,'Can view event position language requirement',22,'view_eventpositionlanguagerequirement'),(89,'Can add event position optional skill',23,'add_eventpositionoptionalskill'),(90,'Can change event position optional skill',23,'change_eventpositionoptionalskill'),(91,'Can delete event position optional skill',23,'delete_eventpositionoptionalskill'),(92,'Can view event position optional skill',23,'view_eventpositionoptionalskill'),(93,'Can add event position required skill',24,'add_eventpositionrequiredskill'),(94,'Can change event position required skill',24,'change_eventpositionrequiredskill'),(95,'Can delete event position required skill',24,'delete_eventpositionrequiredskill'),(96,'Can view event position required skill',24,'view_eventpositionrequiredskill'),(97,'Can add application',25,'add_application'),(98,'Can change application',25,'change_application'),(99,'Can delete application',25,'delete_application'),(100,'Can view application',25,'view_application'),(101,'Can add assignment',26,'add_assignment'),(102,'Can change assignment',26,'change_assignment'),(103,'Can delete assignment',26,'delete_assignment'),(104,'Can view assignment',26,'view_assignment'),(105,'Can add notification',27,'add_notification'),(106,'Can change notification',27,'change_notification'),(107,'Can delete notification',27,'delete_notification'),(108,'Can view notification',27,'view_notification');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$HplSM2oPhGTOnR9v7DTDPk$7u0KqGzbMRTQgD9Nc8H9j87YmiL2XHxoMVnCVX/Bm50=','2026-04-18 17:00:18.368820',1,'admin','System','Admin','admin@example.com',1,1,'2026-04-13 06:38:55.860927'),(2,'pbkdf2_sha256$720000$kHSCuh6y98je8DoXD9of9V$6+PRlF9eUiesFLkoUBoeUUKY8Xh7D0zC9JklDt5o9zo=','2026-04-18 17:53:02.852347',0,'org_demo','Demo','Coordinator','org@example.com',0,1,'2026-04-13 06:38:56.242206'),(3,'pbkdf2_sha256$720000$WJaLIxPH4Jf1dIUeNDEw1l$aUmKc9BiDPhZrOSp6lW/gglSmFpsEyWy0lUeG82wU6Q=','2026-04-18 16:32:15.467580',0,'volunteer_demo','Demo','Volunteer','volunteer@example.com',0,1,'2026-04-13 06:38:56.587660'),(4,'pbkdf2_sha256$720000$r3QjaVpFWtQoHiklRZCfcw$RGSeL+t3y+MN1FUqlEIeX2dO6TOc1xtvKzo0wO1PlnU=','2026-04-16 05:47:38.895419',0,'vol2','Волонтер','Волонтерович','vol2@example.com',0,1,'2026-04-15 15:08:23.052801'),(5,'pbkdf2_sha256$720000$trOLAYIPxaPo31C3hUNeSb$J3RWs6Sp1q3m5OC/VMD80rSrTrw3f/XVCBf5KkrrsKA=','2026-04-15 15:11:17.940380',0,'vol3','','','',0,1,'2026-04-15 15:11:17.602034');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_city`
--

DROP TABLE IF EXISTS `core_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_city` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_city`
--

LOCK TABLES `core_city` WRITE;
/*!40000 ALTER TABLE `core_city` DISABLE KEYS */;
INSERT INTO `core_city` VALUES (3,'Булаево'),(1,'Петропавловск'),(2,'Сергеевка');
/*!40000 ALTER TABLE `core_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_district`
--

DROP TABLE IF EXISTS `core_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_district` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `city_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_district_city_id_name_7908f1f0_uniq` (`city_id`,`name`),
  CONSTRAINT `core_district_city_id_b6b3326c_fk_core_city_id` FOREIGN KEY (`city_id`) REFERENCES `core_city` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_district`
--

LOCK TABLES `core_district` WRITE;
/*!40000 ALTER TABLE `core_district` DISABLE KEYS */;
INSERT INTO `core_district` VALUES (1,'19-й микрорайон',1),(4,'Береке',1),(3,'Рабочий поселок',1),(2,'Центр',1),(5,'Центральный',2),(6,'Центральный',3);
/*!40000 ALTER TABLE `core_district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_language`
--

DROP TABLE IF EXISTS `core_language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_language` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `code` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_language`
--

LOCK TABLES `core_language` WRITE;
/*!40000 ALTER TABLE `core_language` DISABLE KEYS */;
INSERT INTO `core_language` VALUES (1,'Русский','RU'),(2,'Казахский','KZ'),(3,'Английский','EN');
/*!40000 ALTER TABLE `core_language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_skill`
--

DROP TABLE IF EXISTS `core_skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_skill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `core_skill_category_id_e2b959f5_fk_core_skillcategory_id` (`category_id`),
  CONSTRAINT `core_skill_category_id_e2b959f5_fk_core_skillcategory_id` FOREIGN KEY (`category_id`) REFERENCES `core_skillcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_skill`
--

LOCK TABLES `core_skill` WRITE;
/*!40000 ALTER TABLE `core_skill` DISABLE KEYS */;
INSERT INTO `core_skill` VALUES (1,'Работа с детьми',1),(2,'Работа с пожилыми',1),(3,'Психологическая поддержка',1),(4,'Логистика',2),(5,'Регистрация участников',2),(6,'Организация мероприятий',2),(7,'SMM / Фото / Видео',3),(8,'Переводы',4),(9,'Работа с документами / ПК',5),(10,'Первая помощь',6),(11,'Хирургия',3);
/*!40000 ALTER TABLE `core_skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_skillcategory`
--

DROP TABLE IF EXISTS `core_skillcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_skillcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `sort_order` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `core_skillcategory_chk_1` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_skillcategory`
--

LOCK TABLES `core_skillcategory` WRITE;
/*!40000 ALTER TABLE `core_skillcategory` DISABLE KEYS */;
INSERT INTO `core_skillcategory` VALUES (1,'Социальные',1),(2,'Операционные',2),(3,'Медиа',3),(4,'Языковые',4),(5,'Технические',5),(6,'Медицинские',6);
/*!40000 ALTER TABLE `core_skillcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_tasktype`
--

DROP TABLE IF EXISTS `core_tasktype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_tasktype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_tasktype`
--

LOCK TABLES `core_tasktype` WRITE;
/*!40000 ALTER TABLE `core_tasktype` DISABLE KEYS */;
INSERT INTO `core_tasktype` VALUES (5,'Логистика'),(4,'Медпост'),(2,'Организационная помощь'),(1,'Работа с людьми'),(3,'Техническая поддержка');
/*!40000 ALTER TABLE `core_tasktype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_volunteerdirection`
--

DROP TABLE IF EXISTS `core_volunteerdirection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_volunteerdirection` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_volunteerdirection`
--

LOCK TABLES `core_volunteerdirection` WRITE;
/*!40000 ALTER TABLE `core_volunteerdirection` DISABLE KEYS */;
INSERT INTO `core_volunteerdirection` VALUES (5,'Мероприятия'),(2,'Помощь детям'),(3,'Помощь пожилым'),(4,'ЧС'),(1,'Экология');
/*!40000 ALTER TABLE `core_volunteerdirection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-04-18 17:01:09.820960','11','Хирургия',1,'[{\"added\": {}}]',12,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (14,'accounts','profile'),(17,'accounts','volunteeravailability'),(16,'accounts','volunteerlanguage'),(15,'accounts','volunteerprofile'),(18,'accounts','volunteerskill'),(1,'admin','logentry'),(25,'applications','application'),(26,'applications','assignment'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'core','city'),(13,'core','district'),(8,'core','language'),(12,'core','skill'),(9,'core','skillcategory'),(10,'core','tasktype'),(11,'core','volunteerdirection'),(19,'events','event'),(20,'events','eventposition'),(21,'events','eventpositionavailabilityrequirement'),(22,'events','eventpositionlanguagerequirement'),(23,'events','eventpositionoptionalskill'),(24,'events','eventpositionrequiredskill'),(27,'notifications','notification'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'core','0001_initial','2026-04-13 06:38:47.218557'),(2,'contenttypes','0001_initial','2026-04-13 06:38:47.268577'),(3,'auth','0001_initial','2026-04-13 06:38:48.088675'),(4,'accounts','0001_initial','2026-04-13 06:38:49.688489'),(5,'admin','0001_initial','2026-04-13 06:38:49.902593'),(6,'admin','0002_logentry_remove_auto_add','2026-04-13 06:38:49.914748'),(7,'admin','0003_logentry_add_action_flag_choices','2026-04-13 06:38:49.928600'),(8,'events','0001_initial','2026-04-13 06:38:51.422361'),(9,'applications','0001_initial','2026-04-13 06:38:51.977370'),(10,'applications','0002_assignment_fields','2026-04-13 06:38:52.431627'),(11,'contenttypes','0002_remove_content_type_name','2026-04-13 06:38:52.583836'),(12,'auth','0002_alter_permission_name_max_length','2026-04-13 06:38:52.698307'),(13,'auth','0003_alter_user_email_max_length','2026-04-13 06:38:52.733722'),(14,'auth','0004_alter_user_username_opts','2026-04-13 06:38:52.746172'),(15,'auth','0005_alter_user_last_login_null','2026-04-13 06:38:52.847662'),(16,'auth','0006_require_contenttypes_0002','2026-04-13 06:38:52.853835'),(17,'auth','0007_alter_validators_add_error_messages','2026-04-13 06:38:52.870473'),(18,'auth','0008_alter_user_username_max_length','2026-04-13 06:38:52.985444'),(19,'auth','0009_alter_user_last_name_max_length','2026-04-13 06:38:53.279828'),(20,'auth','0010_alter_group_name_max_length','2026-04-13 06:38:53.335636'),(21,'auth','0011_update_proxy_permissions','2026-04-13 06:38:53.358114'),(22,'auth','0012_alter_user_first_name_max_length','2026-04-13 06:38:53.453623'),(23,'notifications','0001_initial','2026-04-13 06:38:53.587331'),(24,'sessions','0001_initial','2026-04-13 06:38:53.646048');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('880fvtb2dwz3hx26c0rr5i6atwl1d48p','.eJxVjDsOwyAQRO9CHSFgZT4p0-cMaHeB4CTCkrErK3ePLblIypn3ZjYRcV1qXHue45jEVRhx-e0I-ZXbAdIT22OSPLVlHkkeijxpl_cp5fftdP8OKva6rzlpYz07TGCdDWYAy0UXr7ynMKDFnDHvUREAMAQmDc4RhKRCCYrE5wviTDff:1wE9SK:21bWSWam55WXwZol_A-NKeKQnLPEw0YFJ8H1-JoTi5Q','2026-05-02 17:27:44.538144'),('nm2tts15wsua7hnhx85t9fwdb8843agm','.eJxVjDEOAiEQRe9CbQhEgcHS3jOQgZmRVQPJslsZ766bbKHtf-_9l0q4LjWtg-c0kTorqw6_W8by4LYBumO7dV16W-Yp603ROx362omfl939O6g46rd2bOQUCwYC9vHoPYIgBh8csUdmJ8RgwbgsOQCIdeAgoxgREwGKen8AA9U4xQ:1wDiJs:YVNS1MSwraE3FRTvaUAnxBUZTWUlHwNm9EphPqBJCaw','2026-05-01 12:29:12.532930'),('qmsfixe2alhuukqg7ezzffhzqg51db16','.eJxVjDsOwyAQRO9CHSFgZT4p0-cMaHeB4CTCkrErK3ePLblIypn3ZjYRcV1qXHue45jEVRhx-e0I-ZXbAdIT22OSPLVlHkkeijxpl_cp5fftdP8OKva6rzlpYz07TGCdDWYAy0UXr7ynMKDFnDHvUREAMAQmDc4RhKRCCYrE5wviTDff:1wE9qo:TzoJ7xPCevQZgCbmmUazJBnOf0WLGvxKb3iFpQ8RoXc','2026-05-02 17:53:02.856598');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_event`
--

DROP TABLE IF EXISTS `events_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_event` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `address_text` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `city_id` bigint DEFAULT NULL,
  `created_by_id` int NOT NULL,
  `district_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `events_event_city_id_3c8b63c9_fk_core_city_id` (`city_id`),
  KEY `events_event_created_by_id_2c28ea90_fk_auth_user_id` (`created_by_id`),
  KEY `events_event_district_id_3fee4ae8_fk_core_district_id` (`district_id`),
  CONSTRAINT `events_event_city_id_3c8b63c9_fk_core_city_id` FOREIGN KEY (`city_id`) REFERENCES `core_city` (`id`),
  CONSTRAINT `events_event_created_by_id_2c28ea90_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `events_event_district_id_3fee4ae8_fk_core_district_id` FOREIGN KEY (`district_id`) REFERENCES `core_district` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_event`
--

LOCK TABLES `events_event` WRITE;
/*!40000 ALTER TABLE `events_event` DISABLE KEYS */;
INSERT INTO `events_event` VALUES (1,'event1','','','2026-04-06','2026-04-13',1,'2026-04-13 06:41:53.969698',3,2,6),(2,'event 2','','','2026-04-13','2026-04-16',1,'2026-04-16 05:48:59.171883',1,2,1);
/*!40000 ALTER TABLE `events_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_eventposition`
--

DROP TABLE IF EXISTS `events_eventposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_eventposition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `slots_total` int unsigned NOT NULL,
  `requires_car` tinyint(1) NOT NULL,
  `requires_night_shift` tinyint(1) NOT NULL,
  `requires_physical_work` tinyint(1) NOT NULL,
  `requires_heavy_lifting` tinyint(1) NOT NULL,
  `avoid_large_crowds_sensitive` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `direction_id` bigint DEFAULT NULL,
  `event_id` bigint NOT NULL,
  `task_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `events_eventposition_direction_id_728a7064_fk_core_volu` (`direction_id`),
  KEY `events_eventposition_event_id_1757e488_fk_events_event_id` (`event_id`),
  KEY `events_eventposition_task_type_id_8ab3552d_fk_core_tasktype_id` (`task_type_id`),
  CONSTRAINT `events_eventposition_direction_id_728a7064_fk_core_volu` FOREIGN KEY (`direction_id`) REFERENCES `core_volunteerdirection` (`id`),
  CONSTRAINT `events_eventposition_event_id_1757e488_fk_events_event_id` FOREIGN KEY (`event_id`) REFERENCES `events_event` (`id`),
  CONSTRAINT `events_eventposition_task_type_id_8ab3552d_fk_core_tasktype_id` FOREIGN KEY (`task_type_id`) REFERENCES `core_tasktype` (`id`),
  CONSTRAINT `events_eventposition_chk_1` CHECK ((`slots_total` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventposition`
--

LOCK TABLES `events_eventposition` WRITE;
/*!40000 ALTER TABLE `events_eventposition` DISABLE KEYS */;
INSERT INTO `events_eventposition` VALUES (2,'Роль1','',1,0,1,0,0,0,'2026-04-15 14:53:28.000383',NULL,1,NULL),(3,'Помощник в школе','',1,0,0,0,0,0,'2026-04-15 17:38:08.540320',NULL,1,NULL),(5,'Роль 1','это описание роли',2,0,0,0,0,0,'2026-04-17 12:39:14.501584',4,2,4);
/*!40000 ALTER TABLE `events_eventposition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_eventpositionavailabilityrequirement`
--

DROP TABLE IF EXISTS `events_eventpositionavailabilityrequirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_eventpositionavailabilityrequirement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `weekday` smallint unsigned NOT NULL,
  `time_of_day` varchar(16) NOT NULL,
  `position_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `events_eventpositionavai_position_id_weekday_time_0cb5ca34_uniq` (`position_id`,`weekday`,`time_of_day`),
  CONSTRAINT `events_eventposition_position_id_faf981dd_fk_events_ev` FOREIGN KEY (`position_id`) REFERENCES `events_eventposition` (`id`),
  CONSTRAINT `events_eventpositionavailabilityrequirement_chk_1` CHECK ((`weekday` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=227 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionavailabilityrequirement`
--

LOCK TABLES `events_eventpositionavailabilityrequirement` WRITE;
/*!40000 ALTER TABLE `events_eventpositionavailabilityrequirement` DISABLE KEYS */;
INSERT INTO `events_eventpositionavailabilityrequirement` VALUES (6,1,'MORNING',2),(7,2,'MORNING',2),(8,3,'MORNING',2),(9,4,'MORNING',2),(10,5,'MORNING',2),(207,1,'DAY',5),(208,1,'EVENING',5),(206,1,'MORNING',5),(210,2,'DAY',5),(211,2,'EVENING',5),(209,2,'MORNING',5),(213,3,'DAY',5),(214,3,'EVENING',5),(212,3,'MORNING',5),(216,4,'DAY',5),(217,4,'EVENING',5),(215,4,'MORNING',5),(219,5,'DAY',5),(220,5,'EVENING',5),(218,5,'MORNING',5),(222,6,'DAY',5),(223,6,'EVENING',5),(221,6,'MORNING',5),(225,7,'DAY',5),(226,7,'EVENING',5),(224,7,'MORNING',5);
/*!40000 ALTER TABLE `events_eventpositionavailabilityrequirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_eventpositionlanguagerequirement`
--

DROP TABLE IF EXISTS `events_eventpositionlanguagerequirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_eventpositionlanguagerequirement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `min_level` varchar(20) NOT NULL,
  `language_id` bigint NOT NULL,
  `position_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `events_eventpositionlang_position_id_language_id_a085b329_uniq` (`position_id`,`language_id`),
  KEY `events_eventposition_language_id_2fb0e37d_fk_core_lang` (`language_id`),
  CONSTRAINT `events_eventposition_language_id_2fb0e37d_fk_core_lang` FOREIGN KEY (`language_id`) REFERENCES `core_language` (`id`),
  CONSTRAINT `events_eventposition_position_id_daabbb4b_fk_events_ev` FOREIGN KEY (`position_id`) REFERENCES `events_eventposition` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionlanguagerequirement`
--

LOCK TABLES `events_eventpositionlanguagerequirement` WRITE;
/*!40000 ALTER TABLE `events_eventpositionlanguagerequirement` DISABLE KEYS */;
INSERT INTO `events_eventpositionlanguagerequirement` VALUES (1,'BASIC',2,2),(2,'BASIC',3,2),(3,'CONVERSATIONAL',1,2),(4,'CONVERSATIONAL',3,5),(5,'CONVERSATIONAL',2,5),(6,'CONVERSATIONAL',1,5);
/*!40000 ALTER TABLE `events_eventpositionlanguagerequirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_eventpositionoptionalskill`
--

DROP TABLE IF EXISTS `events_eventpositionoptionalskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_eventpositionoptionalskill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `min_level` varchar(20) NOT NULL,
  `position_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `events_eventpositionopti_position_id_skill_id_592ffff4_uniq` (`position_id`,`skill_id`),
  KEY `events_eventposition_skill_id_f162e928_fk_core_skil` (`skill_id`),
  CONSTRAINT `events_eventposition_position_id_d79d7617_fk_events_ev` FOREIGN KEY (`position_id`) REFERENCES `events_eventposition` (`id`),
  CONSTRAINT `events_eventposition_skill_id_f162e928_fk_core_skil` FOREIGN KEY (`skill_id`) REFERENCES `core_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionoptionalskill`
--

LOCK TABLES `events_eventpositionoptionalskill` WRITE;
/*!40000 ALTER TABLE `events_eventpositionoptionalskill` DISABLE KEYS */;
INSERT INTO `events_eventpositionoptionalskill` VALUES (1,'BEGINNER',2,3),(2,'BEGINNER',5,3),(3,'BEGINNER',5,1),(4,'BEGINNER',5,2);
/*!40000 ALTER TABLE `events_eventpositionoptionalskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_eventpositionrequiredskill`
--

DROP TABLE IF EXISTS `events_eventpositionrequiredskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events_eventpositionrequiredskill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `min_level` varchar(20) NOT NULL,
  `position_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `events_eventpositionrequ_position_id_skill_id_7e023f18_uniq` (`position_id`,`skill_id`),
  KEY `events_eventposition_skill_id_3770ae13_fk_core_skil` (`skill_id`),
  CONSTRAINT `events_eventposition_position_id_40262bc0_fk_events_ev` FOREIGN KEY (`position_id`) REFERENCES `events_eventposition` (`id`),
  CONSTRAINT `events_eventposition_skill_id_3770ae13_fk_core_skil` FOREIGN KEY (`skill_id`) REFERENCES `core_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionrequiredskill`
--

LOCK TABLES `events_eventpositionrequiredskill` WRITE;
/*!40000 ALTER TABLE `events_eventpositionrequiredskill` DISABLE KEYS */;
INSERT INTO `events_eventpositionrequiredskill` VALUES (1,'BEGINNER',2,3),(2,'BEGINNER',3,1),(4,'BEGINNER',5,3),(5,'BEGINNER',5,1);
/*!40000 ALTER TABLE `events_eventpositionrequiredskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_notification_user_id_b5e8c0ff_fk_auth_user_id` (`user_id`),
  CONSTRAINT `notifications_notification_user_id_b5e8c0ff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
INSERT INTO `notifications_notification` VALUES (11,'Новое назначение','Вас назначили на роль «Роль1» в мероприятии «event1».',0,'2026-04-15 15:12:38.017776',5),(13,'Новое назначение','Вас назначили на роль: Роль1',0,'2026-04-15 15:13:40.235699',4),(16,'Участие завершено','Ваше участие в роли «Роль1» отмечено как выполненное. Часов: 8. Оценка: 3/5.',0,'2026-04-15 15:14:59.636750',4),(17,'Участие завершено','Ваше участие в роли «Роль1» отмечено как выполненное. Часов: 10. Оценка: 4/5.',0,'2026-04-15 15:15:07.889863',5),(22,'Новое назначение','Вас назначили на роль: Уборщик',0,'2026-04-17 10:58:51.866593',5),(23,'Участие завершено','Ваше участие в роли «Уборщик» отмечено как выполненное. Часов: 5. Оценка: 5/5.',0,'2026-04-17 10:59:08.524559',5),(29,'Приглашение на роль','Организатор приглашает вас на роль: Роль 1. Подтвердите участие в личном кабинете.',0,'2026-04-18 16:31:54.365350',4);
/*!40000 ALTER TABLE `notifications_notification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-18 17:58:55
