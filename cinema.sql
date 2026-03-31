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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asientos`
--

LOCK TABLES `asientos` WRITE;
/*!40000 ALTER TABLE `asientos` DISABLE KEYS */;
INSERT INTO `asientos` VALUES (1,'A1','A',1,1),(2,'A2','A',2,1),(3,'A3','A',3,1),(4,'A4','A',4,1),(5,'A5','A',5,1),(6,'B1','B',1,2),(7,'B2','B',2,2),(8,'B3','B',3,2),(9,'B4','B',4,2),(10,'B5','B',5,2),(11,'C1','C',1,3),(12,'C2','C',2,3),(13,'C3','C',3,3),(14,'C4','C',4,3),(15,'C5','C',5,3);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_tiquete`
--

LOCK TABLES `detalle_tiquete` WRITE;
/*!40000 ALTER TABLE `detalle_tiquete` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funciones`
--

LOCK TABLES `funciones` WRITE;
/*!40000 ALTER TABLE `funciones` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservas_temporales`
--

LOCK TABLES `reservas_temporales` WRITE;
/*!40000 ALTER TABLE `reservas_temporales` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiquetes`
--

LOCK TABLES `tiquetes` WRITE;
/*!40000 ALTER TABLE `tiquetes` DISABLE KEYS */;
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

-- Dump completed on 2026-03-31 17:14:03
