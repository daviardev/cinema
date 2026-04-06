-- MySQL dump 10.13  Distrib 8.0.45, for macos15 (arm64)
--
-- Host: localhost    Database: cinema
-- ------------------------------------------------------
-- Server version	8.4.8

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
-- Table structure for table `actores`
--

DROP TABLE IF EXISTS `actores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actores`
--

LOCK TABLES `actores` WRITE;
/*!40000 ALTER TABLE `actores` DISABLE KEYS */;
INSERT INTO `actores` VALUES (1,'Tom Holland'),(2,'Tom Holland'),(3,'Zendaya'),(4,'Sadie Sink'),(5,'Jon Bernthal'),(6,'Mark Ruffalo');
/*!40000 ALTER TABLE `actores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asientos`
--

DROP TABLE IF EXISTS `asientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero` varchar(5) DEFAULT NULL,
  `fila` char(1) DEFAULT NULL,
  `columna` int DEFAULT NULL,
  `tipo_id` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`),
  KEY `fk_tipo_asiento` (`tipo_id`),
  CONSTRAINT `fk_tipo_asiento` FOREIGN KEY (`tipo_id`) REFERENCES `tipos_asientos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=362 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asientos`
--

LOCK TABLES `asientos` WRITE;
/*!40000 ALTER TABLE `asientos` DISABLE KEYS */;
INSERT INTO `asientos` VALUES (1,'A1','A',1,1),(2,'A2','A',2,1),(3,'A3','A',3,1),(4,'A4','A',4,1),(5,'A5','A',5,1),(6,'B1','B',1,2),(7,'B2','B',2,2),(8,'B3','B',3,2),(9,'B4','B',4,2),(10,'B5','B',5,2),(11,'C1','C',1,3),(12,'C2','C',2,3),(13,'C3','C',3,3),(14,'C4','C',4,3),(15,'C5','C',5,3),(197,'A6','A',6,1),(198,'A7','A',7,1),(199,'A8','A',8,1),(200,'A9','A',9,1),(201,'A10','A',10,1),(202,'A11','A',11,1),(203,'A12','A',12,1),(204,'A13','A',13,1),(205,'A14','A',14,1),(206,'A15','A',15,1),(207,'A16','A',16,1),(208,'A17','A',17,1),(209,'A18','A',18,1),(210,'B6','B',6,1),(211,'B7','B',7,1),(212,'B8','B',8,1),(213,'B9','B',9,1),(214,'B10','B',10,1),(215,'B11','B',11,1),(216,'B12','B',12,1),(217,'B13','B',13,1),(218,'B14','B',14,1),(219,'B15','B',15,1),(220,'B16','B',16,1),(221,'B17','B',17,1),(222,'B18','B',18,1),(223,'C6','C',6,2),(224,'C7','C',7,2),(225,'C8','C',8,2),(226,'C9','C',9,2),(227,'C10','C',10,2),(228,'C11','C',11,2),(229,'C12','C',12,2),(230,'C13','C',13,2),(231,'C14','C',14,2),(232,'C15','C',15,2),(233,'C16','C',16,2),(234,'C17','C',17,2),(235,'C18','C',18,2),(236,'D1','D',1,2),(237,'D2','D',2,2),(238,'D3','D',3,2),(239,'D4','D',4,2),(240,'D5','D',5,2),(241,'D6','D',6,2),(242,'D7','D',7,2),(243,'D8','D',8,2),(244,'D9','D',9,2),(245,'D10','D',10,2),(246,'D11','D',11,2),(247,'D12','D',12,2),(248,'D13','D',13,2),(249,'D14','D',14,2),(250,'D15','D',15,2),(251,'D16','D',16,2),(252,'D17','D',17,2),(253,'D18','D',18,2),(254,'E1','E',1,2),(255,'E2','E',2,2),(256,'E3','E',3,2),(257,'E4','E',4,2),(258,'E5','E',5,2),(259,'E6','E',6,2),(260,'E7','E',7,2),(261,'E8','E',8,2),(262,'E9','E',9,2),(263,'E10','E',10,2),(264,'E11','E',11,2),(265,'E12','E',12,2),(266,'E13','E',13,2),(267,'E14','E',14,2),(268,'E15','E',15,2),(269,'E16','E',16,2),(270,'E17','E',17,2),(271,'E18','E',18,2),(272,'F1','F',1,2),(273,'F2','F',2,2),(274,'F3','F',3,2),(275,'F4','F',4,2),(276,'F5','F',5,2),(277,'F6','F',6,2),(278,'F7','F',7,2),(279,'F8','F',8,2),(280,'F9','F',9,2),(281,'F10','F',10,2),(282,'F11','F',11,2),(283,'F12','F',12,2),(284,'F13','F',13,2),(285,'F14','F',14,2),(286,'F15','F',15,2),(287,'F16','F',16,2),(288,'F17','F',17,2),(289,'F18','F',18,2),(290,'G1','G',1,2),(291,'G2','G',2,2),(292,'G3','G',3,2),(293,'G4','G',4,2),(294,'G5','G',5,2),(295,'G6','G',6,2),(296,'G7','G',7,2),(297,'G8','G',8,2),(298,'G9','G',9,2),(299,'G10','G',10,2),(300,'G11','G',11,2),(301,'G12','G',12,2),(302,'G13','G',13,2),(303,'G14','G',14,2),(304,'G15','G',15,2),(305,'G16','G',16,2),(306,'G17','G',17,2),(307,'G18','G',18,2),(308,'H1','H',1,3),(309,'H2','H',2,3),(310,'H3','H',3,3),(311,'H4','H',4,3),(312,'H5','H',5,3),(313,'H6','H',6,3),(314,'H7','H',7,3),(315,'H8','H',8,3),(316,'H9','H',9,3),(317,'H10','H',10,3),(318,'H11','H',11,3),(319,'H12','H',12,3),(320,'H13','H',13,3),(321,'H14','H',14,3),(322,'H15','H',15,3),(323,'H16','H',16,3),(324,'H17','H',17,3),(325,'H18','H',18,3),(326,'I1','I',1,3),(327,'I2','I',2,3),(328,'I3','I',3,3),(329,'I4','I',4,3),(330,'I5','I',5,3),(331,'I6','I',6,3),(332,'I7','I',7,3),(333,'I8','I',8,3),(334,'I9','I',9,3),(335,'I10','I',10,3),(336,'I11','I',11,3),(337,'I12','I',12,3),(338,'I13','I',13,3),(339,'I14','I',14,3),(340,'I15','I',15,3),(341,'I16','I',16,3),(342,'I17','I',17,3),(343,'I18','I',18,3),(344,'J1','J',1,3),(345,'J2','J',2,3),(346,'J3','J',3,3),(347,'J4','J',4,3),(348,'J5','J',5,3),(349,'J6','J',6,3),(350,'J7','J',7,3),(351,'J8','J',8,3),(352,'J9','J',9,3),(353,'J10','J',10,3),(354,'J11','J',11,3),(355,'J12','J',12,3),(356,'J13','J',13,3),(357,'J14','J',14,3),(358,'J15','J',15,3),(359,'J16','J',16,3),(360,'J17','J',17,3),(361,'J18','J',18,3);
/*!40000 ALTER TABLE `asientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_tiquete`
--

DROP TABLE IF EXISTS `detalle_tiquete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_tiquete` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tiquete_id` int NOT NULL,
  `asiento_id` int NOT NULL,
  `funcion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `funcion_id` (`funcion_id`,`asiento_id`),
  KEY `tiquete_id` (`tiquete_id`),
  KEY `idx_funcion` (`funcion_id`),
  KEY `idx_asiento` (`asiento_id`),
  CONSTRAINT `detalle_tiquete_ibfk_1` FOREIGN KEY (`tiquete_id`) REFERENCES `tiquetes` (`id`),
  CONSTRAINT `detalle_tiquete_ibfk_2` FOREIGN KEY (`asiento_id`) REFERENCES `asientos` (`id`),
  CONSTRAINT `detalle_tiquete_ibfk_3` FOREIGN KEY (`funcion_id`) REFERENCES `funciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_tiquete`
--

LOCK TABLES `detalle_tiquete` WRITE;
/*!40000 ALTER TABLE `detalle_tiquete` DISABLE KEYS */;
INSERT INTO `detalle_tiquete` VALUES (1,1,15,8),(2,1,5,8),(3,1,10,8),(4,2,4,2),(5,3,9,5),(6,4,4,10),(7,5,5,9),(8,6,2,10),(9,7,1,9),(10,7,7,9),(11,7,8,9),(12,8,9,2),(13,9,1,10),(14,10,8,2),(15,11,3,2),(16,12,10,5),(17,13,15,1);
/*!40000 ALTER TABLE `detalle_tiquete` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funciones`
--

DROP TABLE IF EXISTS `funciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pelicula_id` int NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` varchar(20) DEFAULT 'disponible',
  `sala` varchar(50) DEFAULT NULL,
  `tecnologia` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pelicula_id` (`pelicula_id`),
  CONSTRAINT `funciones_ibfk_1` FOREIGN KEY (`pelicula_id`) REFERENCES `peliculas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funciones`
--

LOCK TABLES `funciones` WRITE;
/*!40000 ALTER TABLE `funciones` DISABLE KEYS */;
INSERT INTO `funciones` VALUES (1,1,'2026-03-31','14:30:00',18.50,'disponible','Sala IMAX','IMAX 4K'),(2,1,'2026-03-31','17:15:00',15.00,'disponible','Sala Premium','Dolby Vision'),(3,1,'2026-03-31','20:00:00',12.50,'disponible','Sala 3','2D Digital'),(4,1,'2026-03-31','22:30:00',12.50,'disponible','Sala 5','2D Digital'),(5,1,'2026-04-01','16:00:00',18.50,'disponible','Sala IMAX','IMAX 4K'),(6,1,'2026-04-01','18:45:00',15.00,'disponible','Sala Premium','Dolby Vision'),(7,1,'2026-04-01','21:30:00',12.50,'disponible','Sala 2','2D Digital'),(8,1,'2026-04-02','15:00:00',15.00,'disponible','Sala Premium','Dolby Vision'),(9,1,'2026-04-02','18:00:00',18.50,'disponible','Sala IMAX','IMAX 4K'),(10,1,'2026-04-02','20:45:00',12.50,'disponible','Sala 4','2D Digital');
/*!40000 ALTER TABLE `funciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `generos`
--

DROP TABLE IF EXISTS `generos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `generos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generos`
--

LOCK TABLES `generos` WRITE;
/*!40000 ALTER TABLE `generos` DISABLE KEYS */;
INSERT INTO `generos` VALUES (1,'Acción'),(2,'Drama'),(3,'Ciencia Ficción'),(4,'Terror'),(5,'Comedia'),(6,'Animación');
/*!40000 ALTER TABLE `generos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pelicula_actores`
--

DROP TABLE IF EXISTS `pelicula_actores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pelicula_actores` (
  `pelicula_id` int DEFAULT NULL,
  `actor_id` int DEFAULT NULL,
  KEY `pelicula_id` (`pelicula_id`),
  KEY `actor_id` (`actor_id`),
  CONSTRAINT `pelicula_actores_ibfk_1` FOREIGN KEY (`pelicula_id`) REFERENCES `peliculas` (`id`),
  CONSTRAINT `pelicula_actores_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `actores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pelicula_actores`
--

LOCK TABLES `pelicula_actores` WRITE;
/*!40000 ALTER TABLE `pelicula_actores` DISABLE KEYS */;
INSERT INTO `pelicula_actores` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6);
/*!40000 ALTER TABLE `pelicula_actores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pelicula_generos`
--

DROP TABLE IF EXISTS `pelicula_generos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pelicula_generos` (
  `pelicula_id` int NOT NULL,
  `genero_id` int NOT NULL,
  PRIMARY KEY (`pelicula_id`,`genero_id`),
  KEY `genero_id` (`genero_id`),
  CONSTRAINT `pelicula_generos_ibfk_1` FOREIGN KEY (`pelicula_id`) REFERENCES `peliculas` (`id`),
  CONSTRAINT `pelicula_generos_ibfk_2` FOREIGN KEY (`genero_id`) REFERENCES `generos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pelicula_generos`
--

LOCK TABLES `pelicula_generos` WRITE;
/*!40000 ALTER TABLE `pelicula_generos` DISABLE KEYS */;
INSERT INTO `pelicula_generos` VALUES (1,1),(1,3);
/*!40000 ALTER TABLE `pelicula_generos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peliculas`
--

DROP TABLE IF EXISTS `peliculas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peliculas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `duracion` int NOT NULL,
  `clasificacion` varchar(10) DEFAULT NULL,
  `imagen_url` text,
  `estado` varchar(20) DEFAULT 'activa',
  `tags` json DEFAULT NULL,
  `puntuacion` decimal(3,1) DEFAULT NULL,
  `anio` int DEFAULT NULL,
  `tagline` varchar(255) DEFAULT NULL,
  `director` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peliculas`
--

LOCK TABLES `peliculas` WRITE;
/*!40000 ALTER TABLE `peliculas` DISABLE KEYS */;
INSERT INTO `peliculas` VALUES (1,'Spider-Man: Brand New Day','presenta a un Peter Parker maduro, cuatro años tras No Way Home, viviendo en solitario y sin identidad conocida. Dedicado totalmente a ser Spider-Man, enfrenta una red criminal compleja, una evolución física peligrosa y amenazas ocultas en un entorno más oscuro y urbano.',180,'PG-13','https://thecosmiccircus.com/wp-content/uploads/2025/05/spider-man-brand-new-day.jpg','Estreno','[\"Nuevo Estreno\"]',4.5,2026,'Un gran poder, conlleva una gran responsibilidad...','Destin Daniel Cretton');
/*!40000 ALTER TABLE `peliculas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservas_temporales`
--

DROP TABLE IF EXISTS `reservas_temporales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservas_temporales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `funcion_id` int DEFAULT NULL,
  `asiento_id` int DEFAULT NULL,
  `expiracion` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `funcion_id` (`funcion_id`,`asiento_id`),
  KEY `asiento_id` (`asiento_id`),
  CONSTRAINT `reservas_temporales_ibfk_1` FOREIGN KEY (`funcion_id`) REFERENCES `funciones` (`id`),
  CONSTRAINT `reservas_temporales_ibfk_2` FOREIGN KEY (`asiento_id`) REFERENCES `asientos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservas_temporales`
--

LOCK TABLES `reservas_temporales` WRITE;
/*!40000 ALTER TABLE `reservas_temporales` DISABLE KEYS */;
INSERT INTO `reservas_temporales` VALUES (15,1,10,'2026-04-01 02:49:24'),(16,1,2,'2026-04-01 02:50:00'),(17,2,10,'2026-04-01 15:33:08'),(20,3,4,'2026-04-01 18:29:07'),(21,2,5,'2026-04-01 18:40:20'),(22,3,14,'2026-04-01 19:02:57'),(23,5,4,'2026-04-01 19:06:34'),(24,5,15,'2026-04-01 19:10:30'),(25,5,5,'2026-04-01 19:36:08'),(29,3,7,'2026-04-01 20:21:38'),(43,1,8,'2026-04-01 20:43:17'),(58,5,3,'2026-04-03 16:21:57'),(59,1,5,'2026-04-03 16:55:55');
/*!40000 ALTER TABLE `reservas_temporales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_asientos`
--

DROP TABLE IF EXISTS `tipos_asientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_asientos` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) DEFAULT NULL,
  `precio` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_asientos`
--

LOCK TABLES `tipos_asientos` WRITE;
/*!40000 ALTER TABLE `tipos_asientos` DISABLE KEYS */;
INSERT INTO `tipos_asientos` VALUES (1,'estandard',12.50),(2,'premium',15.00),(3,'vip',18.50);
/*!40000 ALTER TABLE `tipos_asientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiquetes`
--

DROP TABLE IF EXISTS `tiquetes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiquetes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `funcion_id` int NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(20) DEFAULT 'activo',
  `fecha_compra` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `funcion_id` (`funcion_id`),
  CONSTRAINT `tiquetes_ibfk_1` FOREIGN KEY (`funcion_id`) REFERENCES `funciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiquetes`
--

LOCK TABLES `tiquetes` WRITE;
/*!40000 ALTER TABLE `tiquetes` DISABLE KEYS */;
INSERT INTO `tiquetes` VALUES (1,'TKT-4890-YZM30',8,'dev.daviar@gmail.com',46.00,'activo','2026-04-01 19:30:13'),(2,'TKT-9128-WQW48',2,'dsadsa@dsa.dsa',12.50,'activo','2026-04-01 20:14:42'),(3,'TKT-1626-YUF69',5,'dev.daviar@gmail.com',15.00,'activo','2026-04-03 03:35:24'),(4,'TKT-5013-UTF51',10,'dev.daviar@gmail.com',12.50,'activo','2026-04-03 03:38:44'),(5,'TKT-5308-NFK94',9,'dev.daviar@gmail.com',12.50,'activo','2026-04-03 03:48:20'),(6,'TKT-5584-WNK23',10,'dev.daviar@gmail.com',12.50,'activo','2026-04-03 03:52:48'),(7,'TKT-8232-PFZ33',9,'dev.daviar@gmail.com',42.50,'canjeado','2026-04-03 04:04:54'),(8,'TKT-5418-JFX15',2,'dev.daviar@gmail.com',15.00,'activo','2026-04-03 04:17:19'),(9,'TKT-1750-YSA44',10,'dev.daviar@gmail.com',12.50,'activo','2026-04-03 04:25:39'),(10,'TKT-4467-ZQN10',2,'dev.daviar@gmail.com',15.00,'canjeado','2026-04-03 04:38:51'),(11,'TKT-2488-WPD20',2,'dev.daviar@gmail.com',12.50,'canjeado','2026-04-03 04:46:35'),(12,'TKT-6956-ZHD14',5,'dev.daviar@gmail.com',15.00,'canjeado','2026-04-03 04:50:56'),(13,'TKT-8961-CNJ66',1,'dev.daviar@gmail.com',18.50,'canjeado','2026-04-03 18:14:32');
/*!40000 ALTER TABLE `tiquetes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-05 19:18:51
