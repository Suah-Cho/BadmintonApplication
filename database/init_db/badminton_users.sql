-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: badminton
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` varchar(36) NOT NULL DEFAULT (uuid()),
  `id` varchar(255) NOT NULL,
  `username` varchar(30) NOT NULL,
  `nickname` varchar(30) NOT NULL,
  `password` text NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `profile_image_url` text,
  `create_ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `delete_ts` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
-- INSERT INTO `users` VALUES ('07572f68-2e12-11f0-881a-f2dc77be5366','test1','홍길동','길동이','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test1@gmail.com',NULL,NULL,'2025-05-11 02:45:41','2025-05-11 02:51:03',NULL),('42be914d-2ef8-11f0-a973-0050568bae2f','test5','배드팬','배드팬','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test5@gmail.com',NULL,NULL,'2025-05-12 06:13:45','2025-05-12 06:13:45',NULL),('76229496-2ef8-11f0-a973-0050568bae2f','test6','수원러버','수원러버','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test6@gmail.com',NULL,NULL,'2025-05-12 06:15:11','2025-05-12 06:15:11',NULL),('b63538e8-2ef7-11f0-a973-0050568bae2f','test3','라켓러버','라켓러버','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test3@gmail.com',NULL,NULL,'2025-05-12 06:09:49','2025-05-12 06:09:49',NULL),('c44a8101-2ef8-11f0-a973-0050568bae2f','test7','클럽매니저','클럽매니저','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test7@gmail.com',NULL,NULL,'2025-05-12 06:17:22','2025-05-12 06:17:22',NULL),('cc63fd68-2e12-11f0-881a-f2dc77be5366','test2','춘향이','성심당','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test2@gmail.com',NULL,NULL,'2025-05-11 02:51:12','2025-05-11 02:51:12',NULL),('f6d3610d-2ef7-11f0-a973-0050568bae2f','test4','코치김','코치김','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','test4@gmail.com',NULL,NULL,'2025-05-12 06:11:38','2025-05-12 06:11:38',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-12 15:21:21
