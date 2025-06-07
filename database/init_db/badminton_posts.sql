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
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `post_id` varchar(36) NOT NULL DEFAULT (uuid()),
  `writer_id` varchar(36) NOT NULL,
  `title` text,
  `content` text,
  `category` enum('notice','court','equipment','etc') DEFAULT NULL,
  `create_ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `delete_ts` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
-- INSERT INTO `posts` VALUES ('2eb8d153-2ef8-11f0-a973-0050568bae2f','f6d3610d-2ef7-11f0-a973-0050568bae2f','스매시 기술 향상을 위한 팁','스매시 파워와 정확도를 높이는 연습 방법을 알려드립니다','etc','2025-05-02 06:13:11','2025-05-02 06:13:11',NULL),('5b53b562-2ef8-11f0-a973-0050568bae2f','42be914d-2ef8-11f0-a973-0050568bae2f','배드민턴 국제 대회 일정','올해 남은 국제 대회 일정을 공유합니다.','etc','2025-05-02 06:14:26','2025-05-02 06:14:26',NULL),('61027fc9-2ef8-11f0-a973-0050568bae2f','42be914d-2ef8-11f0-a973-0050568bae2f','배드민턴 국제 대회 일정2','올해 남은 국제 대회 일정을 공유합니다.','etc','2025-05-03 06:14:36','2025-05-03 06:14:36',NULL),('7add2d1d-2ef7-11f0-a973-0050568bae2f','cc63fd68-2e12-11f0-881a-f2dc77be5366','서울 강남구 실내 코트 추천합니다.','강남구에 있는 좋은 배드민턴 코드를 소개합니다.','court','2025-05-12 06:08:10','2025-05-12 06:08:10',NULL),('88366bf5-2ef8-11f0-a973-0050568bae2f','76229496-2ef8-11f0-a973-0050568bae2f','경기도 수원시 배드민턴 코트 정보','수원에 새로 오픈한 배드민턴 코트를 소개합니다','court','2025-04-28 06:15:42','2025-04-28 06:15:42',NULL),('a195e8d9-2ef8-11f0-a973-0050568bae2f','76229496-2ef8-11f0-a973-0050568bae2f','비용 대비 성능 좋은 셔틀콕 추천','여러 종류의 셔틀콕을 비교 분석했습니다.','equipment','2025-04-25 06:16:24','2025-04-25 06:16:24',NULL),('b80f60e8-2ef8-11f0-a973-0050568bae2f','f6d3610d-2ef7-11f0-a973-0050568bae2f','초보자를 위한 풋워크 가이드','효율적인 코트 이동 방법을 배워보세요','etc','2025-04-20 06:17:02','2025-04-20 06:17:02',NULL),('d4b06210-2ef8-11f0-a973-0050568bae2f','c44a8101-2ef8-11f0-a973-0050568bae2f','배드민턴 동호회 가입 방법','지역별 배드민턴 동호회 가입 방법을 알려드립니다.','etc','2025-04-15 03:32:02','2025-04-15 03:32:02',NULL),('e8a7f814-2ef7-11f0-a973-0050568bae2f','b63538e8-2ef7-11f0-a973-0050568bae2f','요넥스 신상 라켓 사용 후기','최근 구매한 요넥스 라켓 사용 후 장단점을 공유합니다. 최근 구매한 요넥스 라켓 사용 후 장단점을 공유합니다. 최근 구매한 요넥스 라켓 사용 후 장단점을 공유합니다. 최근 구매한 요넥스 라켓 사용 후 장단점을 공유합니다.','equipment','2025-05-03 06:11:14','2025-05-03 06:11:14',NULL),('eb224f8e-2e33-11f0-b2a1-0242ac120002','07572f68-2e12-11f0-881a-f2dc77be5366','배드민턴 클럽 모임 안내','매주 토요일 요전 10시부터 12시까지 모임이 있습니다.\n많은 참여부탁드립니다!!\n\n궁금하신 점은 아래 연락처로 연락주시면 상세하게 알려드리겠습니다!!?\n(010-0000-0000, test1@gmail.com)','notice','2025-05-11 06:48:17','2025-05-11 06:48:17',NULL);
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
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
