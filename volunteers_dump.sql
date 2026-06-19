-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: volunteers_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (1,'ADMIN','+77000000001','',1),(2,'ORG','+77000000002','Добрый штаб',2),(3,'VOLUNTEER','+77778965237','',3),(4,'VOLUNTEER','+77076240414','',4),(5,'VOLUNTEER','+77075621283','',5),(6,'VOLUNTEER','+77776844539','',6),(7,'VOLUNTEER','+77075822415','',7),(8,'VOLUNTEER','+77075874596','',8),(9,'VOLUNTEER','+77777896325','',9),(10,'VOLUNTEER','+77778521478','',10),(11,'VOLUNTEER','+77088963215','',11),(12,'VOLUNTEER','+77075824785','',12),(13,'ORG','','',13),(14,'VOLUNTEER','+77777412356','',14),(15,'VOLUNTEER','+77773569172','',15),(16,'VOLUNTEER','+77000000003','',16);
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
) ENGINE=InnoDB AUTO_INCREMENT=276 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteeravailability`
--

LOCK TABLES `accounts_volunteeravailability` WRITE;
/*!40000 ALTER TABLE `accounts_volunteeravailability` DISABLE KEYS */;
INSERT INTO `accounts_volunteeravailability` VALUES (2,1,'DAY',2),(3,1,'EVENING',2),(1,1,'MORNING',2),(5,2,'DAY',2),(6,2,'EVENING',2),(4,2,'MORNING',2),(8,3,'DAY',2),(9,3,'EVENING',2),(7,3,'MORNING',2),(11,4,'DAY',2),(12,4,'EVENING',2),(10,4,'MORNING',2),(14,5,'DAY',2),(15,5,'EVENING',2),(13,5,'MORNING',2),(17,6,'DAY',2),(18,6,'EVENING',2),(16,6,'MORNING',2),(20,7,'DAY',2),(21,7,'EVENING',2),(19,7,'MORNING',2),(113,1,'DAY',3),(112,1,'MORNING',3),(115,2,'DAY',3),(114,2,'MORNING',3),(117,3,'DAY',3),(116,3,'MORNING',3),(119,4,'DAY',3),(118,4,'MORNING',3),(121,5,'DAY',3),(120,5,'MORNING',3),(104,2,'DAY',4),(105,2,'EVENING',4),(103,2,'MORNING',4),(107,4,'DAY',4),(108,4,'EVENING',4),(106,4,'MORNING',4),(110,6,'DAY',4),(111,6,'EVENING',4),(109,6,'MORNING',4),(123,1,'DAY',5),(124,1,'EVENING',5),(122,1,'MORNING',5),(126,2,'DAY',5),(127,2,'EVENING',5),(125,2,'MORNING',5),(129,3,'DAY',5),(130,3,'EVENING',5),(128,3,'MORNING',5),(132,4,'DAY',5),(133,4,'EVENING',5),(131,4,'MORNING',5),(135,5,'DAY',5),(136,5,'EVENING',5),(134,5,'MORNING',5),(138,6,'DAY',5),(139,6,'EVENING',5),(137,6,'MORNING',5),(141,7,'DAY',5),(142,7,'EVENING',5),(140,7,'MORNING',5),(143,1,'DAY',6),(144,1,'EVENING',6),(145,2,'DAY',6),(146,2,'EVENING',6),(147,3,'DAY',6),(148,3,'EVENING',6),(149,4,'DAY',6),(150,4,'EVENING',6),(151,5,'DAY',6),(152,5,'EVENING',6),(153,6,'DAY',6),(154,6,'EVENING',6),(155,7,'DAY',6),(156,7,'EVENING',6),(158,1,'DAY',7),(159,1,'EVENING',7),(157,1,'MORNING',7),(161,2,'DAY',7),(162,2,'EVENING',7),(160,2,'MORNING',7),(164,3,'DAY',7),(165,3,'EVENING',7),(163,3,'MORNING',7),(167,4,'DAY',7),(168,4,'EVENING',7),(166,4,'MORNING',7),(170,5,'DAY',7),(171,5,'EVENING',7),(169,5,'MORNING',7),(173,6,'DAY',7),(174,6,'EVENING',7),(172,6,'MORNING',7),(176,7,'DAY',7),(177,7,'EVENING',7),(175,7,'MORNING',7),(179,1,'DAY',8),(180,1,'EVENING',8),(178,1,'MORNING',8),(182,2,'DAY',8),(183,2,'EVENING',8),(181,2,'MORNING',8),(185,3,'DAY',8),(186,3,'EVENING',8),(184,3,'MORNING',8),(188,4,'DAY',8),(189,4,'EVENING',8),(187,4,'MORNING',8),(191,5,'DAY',8),(192,5,'EVENING',8),(190,5,'MORNING',8),(194,6,'DAY',8),(195,6,'EVENING',8),(193,6,'MORNING',8),(197,7,'DAY',8),(198,7,'EVENING',8),(196,7,'MORNING',8),(200,1,'DAY',9),(201,1,'EVENING',9),(199,1,'MORNING',9),(203,2,'DAY',9),(204,2,'EVENING',9),(202,2,'MORNING',9),(206,3,'DAY',9),(207,3,'EVENING',9),(205,3,'MORNING',9),(209,4,'DAY',9),(210,4,'EVENING',9),(208,4,'MORNING',9),(212,5,'DAY',9),(213,5,'EVENING',9),(211,5,'MORNING',9),(215,1,'DAY',10),(216,1,'EVENING',10),(214,1,'MORNING',10),(218,2,'DAY',10),(219,2,'EVENING',10),(217,2,'MORNING',10),(221,3,'DAY',10),(222,3,'EVENING',10),(220,3,'MORNING',10),(224,4,'DAY',10),(225,4,'EVENING',10),(223,4,'MORNING',10),(227,5,'DAY',10),(228,5,'EVENING',10),(226,5,'MORNING',10),(230,6,'DAY',10),(231,6,'EVENING',10),(229,6,'MORNING',10),(233,7,'DAY',10),(234,7,'EVENING',10),(232,7,'MORNING',10),(236,1,'DAY',12),(237,1,'EVENING',12),(235,1,'MORNING',12),(239,2,'DAY',12),(240,2,'EVENING',12),(238,2,'MORNING',12),(242,3,'DAY',12),(243,3,'EVENING',12),(241,3,'MORNING',12),(245,4,'DAY',12),(246,4,'EVENING',12),(244,4,'MORNING',12),(248,5,'DAY',12),(249,5,'EVENING',12),(247,5,'MORNING',12),(251,6,'DAY',12),(252,6,'EVENING',12),(250,6,'MORNING',12),(254,7,'DAY',12),(255,7,'EVENING',12),(253,7,'MORNING',12),(267,1,'DAY',13),(266,1,'MORNING',13),(269,2,'DAY',13),(268,2,'MORNING',13),(271,3,'DAY',13),(270,3,'MORNING',13),(273,4,'DAY',13),(272,4,'MORNING',13),(275,5,'DAY',13),(274,5,'MORNING',13);
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerlanguage`
--

LOCK TABLES `accounts_volunteerlanguage` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerlanguage` DISABLE KEYS */;
INSERT INTO `accounts_volunteerlanguage` VALUES (1,'FLUENT',1,2),(2,'BASIC',2,2),(3,'CONVERSATIONAL',3,2),(25,'FLUENT',1,4),(26,'FLUENT',2,4),(27,'FLUENT',3,4),(28,'CONVERSATIONAL',1,3),(29,'BASIC',2,3),(30,'FLUENT',3,3),(31,'BASIC',1,5),(32,'FLUENT',2,5),(33,'BASIC',3,5),(34,'FLUENT',1,6),(35,'BASIC',2,6),(36,'FLUENT',3,6),(37,'BASIC',1,7),(38,'FLUENT',2,7),(39,'CONVERSATIONAL',1,8),(40,'FLUENT',2,8),(41,'FLUENT',1,9),(42,'BASIC',2,9),(43,'FLUENT',3,9),(44,'FLUENT',1,10),(45,'CONVERSATIONAL',2,12),(46,'CONVERSATIONAL',1,12),(50,'FLUENT',2,13),(51,'FLUENT',1,13),(52,'CONVERSATIONAL',3,13);
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile`
--

LOCK TABLES `accounts_volunteerprofile` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile` VALUES (1,'',NULL,NULL,NULL,0,0,0,1,1,'',0,0,0,'','',0,0,0.00,0.00,0,0,0,'2026-06-02 18:42:53.742790','2026-06-02 18:42:53.742808',3,6,3),(2,'MALE',2001,'2026-06-10','2026-06-30',1,1,1,1,1,'',0,0,0,'SOCIAL','Мне нравиться помогать людям.',0,0,0.00,0.00,0,100,1,'2026-06-02 18:49:45.281917','2026-06-02 18:53:04.666026',1,1,4),(3,'MALE',2000,'2026-06-21','2026-06-28',0,0,0,0,1,'У меня больная спина. Поэтому для меня физические нагрузки не желательны.',1,0,0,'RESUME','Я умею организовывать мероприятия для различных целей: концерты, ярмарки и многое другое.',0,0,0.00,0.00,0,100,1,'2026-06-02 18:54:14.904456','2026-06-02 19:08:53.396752',1,4,5),(4,'MALE',2000,'2026-06-08','2026-06-30',1,0,0,0,0,'Я мерзляк.',0,1,0,'SOCIAL','Я хочу стать в будущем президентом России.',0,0,0.00,0.00,0,100,1,'2026-06-02 19:01:13.408700','2026-06-02 19:07:45.385266',1,3,6),(5,'FEMALE',1994,'2026-06-10','2026-06-28',0,0,0,0,0,'Не люблю работать ночью.',1,0,0,'PRACTICE','Хочу прославиться.',0,0,0.00,0.00,0,100,1,'2026-06-02 19:10:26.698286','2026-06-02 19:12:43.561297',1,2,7),(6,'FEMALE',2004,'2026-06-18','2026-07-26',1,0,1,0,0,'Мне нужно следить за своей прекрасной кожей.',0,1,0,'CERTIFICATE','Хочу быть богатой.',0,0,0.00,0.00,0,100,1,'2026-06-02 19:28:04.115907','2026-06-02 19:30:14.355600',1,2,8),(7,'MALE',1999,'2026-06-15','2026-07-20',1,1,1,1,1,'Я социопат.',0,0,1,'RESUME','Моя машина делает врум врум.',0,0,0.00,0.00,0,100,1,'2026-06-02 19:31:17.985495','2026-06-02 19:38:53.879014',3,6,9),(8,'FEMALE',1993,'2026-06-17','2026-07-24',0,1,0,0,0,'У меня топографический кретинизм.',1,1,0,'SOCIAL','Хочу быть нянькой.',0,0,0.00,0.00,0,100,1,'2026-06-02 20:10:44.582145','2026-06-02 20:13:00.277158',2,5,10),(9,'MALE',2007,'2026-06-22','2026-07-22',1,1,1,1,1,'Ограничений нет.',0,0,0,'CERTIFICATE','Я хорошо разбираюсь в технике.',0,0,0.00,0.00,0,100,1,'2026-06-02 20:15:55.947135','2026-06-02 20:17:54.070898',1,3,11),(10,'MALE',2007,'2026-06-17','2026-07-19',1,0,1,1,1,'Ограничений нет.',0,0,0,'RESUME','Я хочу спасать людей.',0,0,0.00,0.00,0,100,1,'2026-06-02 21:42:57.923381','2026-06-02 21:44:32.207422',1,1,12),(11,'',NULL,NULL,NULL,0,0,0,1,1,'',0,0,0,'','',0,0,0.00,0.00,0,0,0,'2026-06-02 21:46:18.381916','2026-06-02 21:46:18.381942',NULL,NULL,13),(12,'MALE',1995,'2026-01-26','2026-03-12',1,1,1,1,1,'Физически сильный и выносливый.',0,0,0,'SOCIAL','Хочу помогать людям в беде.',0,0,0.00,0.00,0,100,1,'2026-06-03 07:37:18.173992','2026-06-03 07:40:11.193482',2,5,14),(13,'FEMALE',2001,'2026-09-01','2026-09-30',0,0,0,0,0,'Могу организовывать мероприятия для разных задач.',1,0,0,'PRACTICE','Хочу приобрести навыки в сфере организации мероприятий.',0,0,0.00,0.00,0,100,1,'2026-06-03 08:16:07.161661','2026-06-03 08:26:22.653374',3,6,15),(14,'',NULL,NULL,NULL,0,0,0,1,1,'',0,0,0,'','',0,0,0.00,0.00,0,0,0,'2026-06-04 19:51:11.749423','2026-06-04 19:51:11.749446',3,6,16);
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile_preferred_directions`
--

LOCK TABLES `accounts_volunteerprofile_preferred_directions` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile_preferred_directions` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile_preferred_directions` VALUES (1,2,2),(2,2,3),(3,3,5),(4,4,5),(5,5,4),(6,5,5),(7,6,2),(8,6,3),(9,6,5),(10,7,4),(11,8,3),(12,8,5),(13,9,4),(14,9,5),(15,10,3),(16,10,4),(17,12,4),(18,13,5);
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerprofile_preferred_task_types`
--

LOCK TABLES `accounts_volunteerprofile_preferred_task_types` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerprofile_preferred_task_types` DISABLE KEYS */;
INSERT INTO `accounts_volunteerprofile_preferred_task_types` VALUES (1,2,1),(2,2,2),(3,3,2),(4,4,1),(5,4,2),(6,5,2),(7,6,1),(8,6,4),(9,7,5),(10,8,1),(11,8,4),(12,9,3),(13,9,5),(14,10,1),(15,10,2),(16,10,5),(17,12,1),(18,12,4),(19,13,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_volunteerskill`
--

LOCK TABLES `accounts_volunteerskill` WRITE;
/*!40000 ALTER TABLE `accounts_volunteerskill` DISABLE KEYS */;
INSERT INTO `accounts_volunteerskill` VALUES (1,'INTERMEDIATE',1,2),(2,'INTERMEDIATE',2,2),(3,'BEGINNER',10,2),(4,'ADVANCED',3,2),(26,'PROFESSIONAL',8,4),(27,'INTERMEDIATE',9,4),(28,'ADVANCED',6,4),(29,'ADVANCED',5,3),(30,'ADVANCED',7,3),(31,'PROFESSIONAL',6,3),(32,'INTERMEDIATE',9,5),(33,'ADVANCED',10,5),(34,'PROFESSIONAL',7,5),(35,'BEGINNER',6,5),(36,'INTERMEDIATE',5,6),(37,'INTERMEDIATE',1,6),(38,'ADVANCED',2,6),(39,'ADVANCED',9,6),(40,'PROFESSIONAL',3,6),(41,'PROFESSIONAL',4,7),(42,'INTERMEDIATE',5,8),(43,'PROFESSIONAL',2,8),(44,'ADVANCED',9,8),(45,'PROFESSIONAL',4,9),(46,'PROFESSIONAL',10,9),(47,'ADVANCED',3,10),(48,'INTERMEDIATE',5,10),(49,'ADVANCED',10,10),(50,'PROFESSIONAL',8,10),(51,'ADVANCED',2,10),(52,'INTERMEDIATE',2,12),(53,'PROFESSIONAL',10,12),(54,'BEGINNER',3,12),(60,'BEGINNER',9,13),(61,'BEGINNER',2,13),(62,'PROFESSIONAL',6,13),(63,'BEGINNER',1,13),(64,'BEGINNER',5,13);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications_application`
--

LOCK TABLES `applications_application` WRITE;
/*!40000 ALTER TABLE `applications_application` DISABLE KEYS */;
INSERT INTO `applications_application` VALUES (1,'invited','Я житель Сергеевки и хочу помочь моим соседям по несчастью.','2026-06-03 07:46:20.036711',3,12);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications_assignment`
--

LOCK TABLES `applications_assignment` WRITE;
/*!40000 ALTER TABLE `applications_assignment` DISABLE KEYS */;
INSERT INTO `applications_assignment` VALUES (1,'invited','2026-06-03 07:48:00.680553',13,3,12,NULL,0,'','2026-06-03 07:48:00.680619');
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$q8a5dM1JgDx0HnctGS5whI$pWWpH2a5gIS3NzWLwz5TqncxxadybPeceXB6x8gsah4=','2026-06-03 07:41:48.264323',1,'admin','System','Admin','admin@example.com',1,1,'2026-06-02 18:42:53.396461'),(2,'pbkdf2_sha256$720000$094Jik3H2iTvY2g94iz7j7$unkpkMWj/rvw2uDPRFcINTVvCD+KtAHDuigHqXCA5rk=',NULL,0,'org_demo','Demo','Coordinator','org@example.com',0,1,'2026-06-02 18:42:53.518929'),(3,'pbkdf2_sha256$720000$r0VjsMveClnqpONuNdg01D$ufQgYUgKO2LA87TMTAQxU6DjnBOKPZx7w12qCZJxVVI=',NULL,0,'dima','Дмитрий','Воронов','volunteer@example.com',0,1,'2026-06-02 18:42:53.000000'),(4,'pbkdf2_sha256$720000$PjZ01IN1WhifWCL35mKGvF$/OWUGkctXSghcZBHawBPnJ6mn/aJpau71F1cmxoEhKk=','2026-06-02 18:49:45.291849',0,'Ivan','Иван','Соболев','ivan.sobol@mail.ru',0,1,'2026-06-02 18:49:45.166958'),(5,'pbkdf2_sha256$720000$x35NPyskcDJvJ5o8xV3PBm$fXw8Rf31XgwjXu9PBAse8fX0mOGYw6p+TO+WmgGJKmg=','2026-06-02 19:08:47.020053',0,'Nurik','Нурлан','Сабуров','nurlan.sab@mail.ru',0,1,'2026-06-02 18:54:14.776743'),(6,'pbkdf2_sha256$720000$CRbjSlTtpMikl8UouI5RIa$eh21RZYbLw3Ii9yKiZ5sWl3G4wUgmHiwK1gGdr4a4kI=','2026-06-02 19:01:13.421834',0,'Danil','Данил','Горбаченко','danil.gorbachenko@mail.ru',0,1,'2026-06-02 19:01:13.292467'),(7,'pbkdf2_sha256$720000$v5v1ZBhuODEOmHo038gZoW$0JKWDTGL9kuCzqKgFV4lQQPaaAmmHkTQYOCX+bQS01Q=','2026-06-02 19:10:26.705753',0,'Sabina','Сабина','Канафина','sab.kan@mail.ru',0,1,'2026-06-02 19:10:26.584078'),(8,'pbkdf2_sha256$720000$1ybwBYyQyxPcHnnbnln5v2$L0CjvF3kT483Hjx7UfFS9RhbUGVHu+qDQAeZmFPF0s8=','2026-06-02 19:28:04.123744',0,'alua','Алуа','Айдаровна','alua.aidarovna@mail.ru',0,1,'2026-06-02 19:28:04.001602'),(9,'pbkdf2_sha256$720000$ekgJfAc18yY5JPANqQ9piv$f8oQDNg+5Dk4f+tfqsk1CUjOwX/9bfq7ZQt2ZSeJ8uU=','2026-06-02 19:31:17.995572',0,'kiril','Кирил','Низин','kiril.nizin@mail.ru',0,1,'2026-06-02 19:31:17.869337'),(10,'pbkdf2_sha256$720000$dEDqV7bL4U8Icl0qHDkmEH$7k3w5IDd5NUgt3rPckcOxrpn7KjXv5EX5Yc9hKmHcdY=','2026-06-02 20:10:44.592351',0,'karina','Карина','Зубарева','karina.zub@mail.ru',0,1,'2026-06-02 20:10:44.462990'),(11,'pbkdf2_sha256$720000$R41gtyTPzVoB4d0ZpwyHvd$/T09PBDRvAKHS4jbuai3zGvMqUnS1iVqE0o82nKFHFY=','2026-06-02 20:15:55.956335',0,'alex','Алексей','Зубенка','alex.zuba@mail.ru',0,1,'2026-06-02 20:15:55.824944'),(12,'pbkdf2_sha256$720000$nYU2wdFNtOJ30yKa0WLnSf$aeWUBTRrYe/5YAFkFJQmghsYpCfCCmLjtgpIbof8yuM=','2026-06-02 21:42:57.936022',0,'boris','Борис','Марьин','boris@mail.ru',0,1,'2026-06-02 21:42:57.793982'),(13,'pbkdf2_sha256$720000$GBXuir8rtD98PIidv5eTDp$qicFcgF2KmBUavi4Qn9Mbo1udroqI57srxEoeq6fWzA=','2026-06-03 08:26:50.146302',0,'max','Максим','Ферстапен','mad.max@mail.ru',0,1,'2026-06-02 21:46:18.262680'),(14,'pbkdf2_sha256$720000$76s53VKFoGiVOHUXpZILtk$gyJEgCxufjWznLSGgal8/Uzm4SM2Vz6iSdnTit51H0c=','2026-06-03 07:45:07.550310',0,'nikolai','Николай','Емельяненко','nikolai.emel@mail.ru',0,1,'2026-06-03 07:37:17.909769'),(15,'pbkdf2_sha256$720000$QZmzanG8tSTJ310QrPhAXN$CeKIfcPKmeWHNGo/4jw6q1Gim/XWfQDlAIm2qR9mjLc=','2026-06-03 08:16:07.181589',0,'aruzhan','Аружан','Мусагалиевна','aruzhan.m@mail.ru',0,1,'2026-06-03 08:16:06.945575'),(16,'pbkdf2_sha256$720000$DANHIhZQBs9S429RxvT93k$bT3Qv3g/4hjqdLj12aSVYPfznthldvCC/KiG0C2leS8=',NULL,0,'volunteer_demo','Demo','Volunteer','volunteer@example.com',0,1,'2026-06-04 19:51:11.619336');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_skill`
--

LOCK TABLES `core_skill` WRITE;
/*!40000 ALTER TABLE `core_skill` DISABLE KEYS */;
INSERT INTO `core_skill` VALUES (1,'Работа с детьми',1),(2,'Работа с пожилыми',1),(3,'Психологическая поддержка',1),(4,'Логистика',2),(5,'Регистрация участников',2),(6,'Организация мероприятий',2),(7,'SMM / Фото / Видео',3),(8,'Переводы',4),(9,'Работа с документами / ПК',5),(10,'Первая помощь',6);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-06-02 21:47:18.225313','13','max (ORG)',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',14,1),(2,'2026-06-03 07:43:55.091662','3','dima',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',4,1),(3,'2026-06-03 07:43:56.910411','3','dima (VOLUNTEER)',2,'[{\"changed\": {\"fields\": [\"Phone\"]}}]',14,1),(4,'2026-06-03 07:44:33.486026','2','org_demo (ORG)',2,'[]',14,1);
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
INSERT INTO `django_migrations` VALUES (1,'core','0001_initial','2026-06-02 18:42:47.329978'),(2,'contenttypes','0001_initial','2026-06-02 18:42:47.370156'),(3,'auth','0001_initial','2026-06-02 18:42:47.952769'),(4,'accounts','0001_initial','2026-06-02 18:42:48.910222'),(5,'admin','0001_initial','2026-06-02 18:42:49.058332'),(6,'admin','0002_logentry_remove_auto_add','2026-06-02 18:42:49.068143'),(7,'admin','0003_logentry_add_action_flag_choices','2026-06-02 18:42:49.079800'),(8,'events','0001_initial','2026-06-02 18:42:50.016625'),(9,'applications','0001_initial','2026-06-02 18:42:50.427012'),(10,'applications','0002_assignment_fields','2026-06-02 18:42:50.727318'),(11,'contenttypes','0002_remove_content_type_name','2026-06-02 18:42:50.833464'),(12,'auth','0002_alter_permission_name_max_length','2026-06-02 18:42:50.902869'),(13,'auth','0003_alter_user_email_max_length','2026-06-02 18:42:50.931284'),(14,'auth','0004_alter_user_username_opts','2026-06-02 18:42:50.944462'),(15,'auth','0005_alter_user_last_login_null','2026-06-02 18:42:51.002320'),(16,'auth','0006_require_contenttypes_0002','2026-06-02 18:42:51.006519'),(17,'auth','0007_alter_validators_add_error_messages','2026-06-02 18:42:51.018045'),(18,'auth','0008_alter_user_username_max_length','2026-06-02 18:42:51.103956'),(19,'auth','0009_alter_user_last_name_max_length','2026-06-02 18:42:51.216093'),(20,'auth','0010_alter_group_name_max_length','2026-06-02 18:42:51.245300'),(21,'auth','0011_update_proxy_permissions','2026-06-02 18:42:51.272488'),(22,'auth','0012_alter_user_first_name_max_length','2026-06-02 18:42:51.352494'),(23,'notifications','0001_initial','2026-06-02 18:42:51.441951'),(24,'sessions','0001_initial','2026-06-02 18:42:51.483457');
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
INSERT INTO `django_session` VALUES ('6za3cmt0slldchuwc125y5b1j9qwmk7u','.eJxVjDsOwjAQBe_iGlm7TtYfSnrOYK29Dg6gRIqTCnF3iJQC2jcz76Uib2uNWytLHEWdFXbq9Dsmzo8y7UTuPN1mnedpXcakd0UftOnrLOV5Ody_g8qtfmuXk0EjYnOXBuvBhoEcEZAfANgj9zY4Wwg5IIJAKsGbvidxXUYAr94f7j424A:1wUgw6:UjF7H8_qt7dEYIgC0-fbC8TAVPvVCbE0qDjWqCzsX_8','2026-06-17 08:26:50.153817'),('u985siek0tppc6kfnvoozfwgu27ivj8u','.eJxVjEEOwiAQRe_C2pACM2Xq0r1nIMBMpWpoUtqV8e7apAvd_vfef6kQt7WErckSJlZnZdTpd0sxP6TugO-x3mad57ouU9K7og_a9HVmeV4O9--gxFa-NRF7IJcQMIKlzllLnh0N0NseohFMxqMIYsZMyfM4jJItOgDCTkS9P63JNv8:1wUU9L:l8rZOcRgwoZce5RtVeZVXGo5A48aY6kTq22HzNCsrcw','2026-06-16 18:47:39.285328');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_event`
--

LOCK TABLES `events_event` WRITE;
/*!40000 ALTER TABLE `events_event` DISABLE KEYS */;
INSERT INTO `events_event` VALUES (1,'Помощь пожилым людям','Помогать с хозяйством одиноко живущим пожилым людям.','ул. Рабочая 112 - ул. Рабочая 143','2026-06-08','2026-07-08',1,'2026-06-02 21:52:28.053101',1,13,4),(2,'Видеограф на концерте на площади','Видео съемка для новостных каналах в соц. сетях.','ул. Мира 1','2026-06-15','2026-06-17',1,'2026-06-02 21:59:16.096463',1,13,2),(3,'Помощь в устранении паводков','При сильных паводков оказывать помощь в соответствующих областях.','','2026-02-01','2026-02-28',1,'2026-06-03 07:24:17.632310',2,13,5),(4,'Организация фестиваля','Фестиваль по случаю дня сбора урожая','','2026-09-01','2026-09-30',1,'2026-06-03 08:00:46.580257',3,13,6);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventposition`
--

LOCK TABLES `events_eventposition` WRITE;
/*!40000 ALTER TABLE `events_eventposition` DISABLE KEYS */;
INSERT INTO `events_eventposition` VALUES (1,'Волонтер','Помощь в облагораживании огорода и колка дров.',5,1,0,1,1,0,'2026-06-02 21:54:41.289333',3,1,1),(2,'Видеограф','Требуется отснять концерт от начала до конца.',1,0,0,0,0,1,'2026-06-02 22:01:55.308645',5,2,3),(3,'Помощник','Помогать воздвигать плотины из мешков с песком, помогать пострадавшим от сильных паводков.',10,0,1,1,1,0,'2026-06-03 07:29:15.539137',4,3,4),(4,'Помощник организатора мероприятия','Нужно помочь организатору организовать мероприятие, составить расписание всех выступлений и помощь обустроить места для посетителей.',1,0,0,0,0,1,'2026-06-03 08:04:53.921121',5,4,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionavailabilityrequirement`
--

LOCK TABLES `events_eventpositionavailabilityrequirement` WRITE;
/*!40000 ALTER TABLE `events_eventpositionavailabilityrequirement` DISABLE KEYS */;
INSERT INTO `events_eventpositionavailabilityrequirement` VALUES (22,1,'DAY',1),(21,1,'MORNING',1),(24,2,'DAY',1),(23,2,'MORNING',1),(26,3,'DAY',1),(25,3,'MORNING',1),(28,4,'DAY',1),(27,4,'MORNING',1),(30,5,'DAY',1),(29,5,'MORNING',1),(32,1,'DAY',2),(31,1,'MORNING',2),(34,2,'DAY',2),(33,2,'MORNING',2),(36,3,'DAY',2),(35,3,'MORNING',2),(38,4,'DAY',2),(37,4,'MORNING',2),(40,5,'DAY',2),(39,5,'MORNING',2),(42,1,'DAY',3),(43,1,'EVENING',3),(41,1,'MORNING',3),(45,2,'DAY',3),(46,2,'EVENING',3),(44,2,'MORNING',3),(48,3,'DAY',3),(49,3,'EVENING',3),(47,3,'MORNING',3),(51,4,'DAY',3),(52,4,'EVENING',3),(50,4,'MORNING',3),(54,5,'DAY',3),(55,5,'EVENING',3),(53,5,'MORNING',3),(57,6,'DAY',3),(58,6,'EVENING',3),(56,6,'MORNING',3),(60,7,'DAY',3),(61,7,'EVENING',3),(59,7,'MORNING',3),(63,1,'DAY',4),(62,1,'MORNING',4),(65,2,'DAY',4),(64,2,'MORNING',4),(67,3,'DAY',4),(66,3,'MORNING',4),(69,4,'DAY',4),(68,4,'MORNING',4),(71,5,'DAY',4),(70,5,'MORNING',4);
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionlanguagerequirement`
--

LOCK TABLES `events_eventpositionlanguagerequirement` WRITE;
/*!40000 ALTER TABLE `events_eventpositionlanguagerequirement` DISABLE KEYS */;
INSERT INTO `events_eventpositionlanguagerequirement` VALUES (5,'CONVERSATIONAL',1,1),(6,'CONVERSATIONAL',2,1),(7,'CONVERSATIONAL',1,2),(8,'CONVERSATIONAL',2,2),(9,'CONVERSATIONAL',2,3),(10,'CONVERSATIONAL',1,3),(11,'FLUENT',2,4),(12,'FLUENT',1,4),(13,'CONVERSATIONAL',3,4);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionoptionalskill`
--

LOCK TABLES `events_eventpositionoptionalskill` WRITE;
/*!40000 ALTER TABLE `events_eventpositionoptionalskill` DISABLE KEYS */;
INSERT INTO `events_eventpositionoptionalskill` VALUES (5,'BEGINNER',1,3),(6,'ADVANCED',1,2),(7,'PROFESSIONAL',2,7),(8,'INTERMEDIATE',3,2),(9,'INTERMEDIATE',3,3),(10,'ADVANCED',3,10),(11,'BEGINNER',4,9),(12,'BEGINNER',4,2),(13,'BEGINNER',4,1),(14,'PROFESSIONAL',4,6),(15,'BEGINNER',4,5);
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_eventpositionrequiredskill`
--

LOCK TABLES `events_eventpositionrequiredskill` WRITE;
/*!40000 ALTER TABLE `events_eventpositionrequiredskill` DISABLE KEYS */;
INSERT INTO `events_eventpositionrequiredskill` VALUES (3,'ADVANCED',1,2),(4,'PROFESSIONAL',2,7),(5,'ADVANCED',3,10),(6,'PROFESSIONAL',4,6),(7,'BEGINNER',4,5);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_notification`
--

LOCK TABLES `notifications_notification` WRITE;
/*!40000 ALTER TABLE `notifications_notification` DISABLE KEYS */;
INSERT INTO `notifications_notification` VALUES (1,'Новый отклик','На роль «Помощник» откликнулся Николай Емельяненко.',1,'2026-06-03 07:46:20.055128',13),(2,'Приглашение на роль','Организатор приглашает вас на роль «Помощник» в мероприятии «Помощь в устранении паводков». Подтвердите или отклоните участие в личном кабинете.',0,'2026-06-03 07:48:00.719532',14);
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

-- Dump completed on 2026-06-04 19:59:39
