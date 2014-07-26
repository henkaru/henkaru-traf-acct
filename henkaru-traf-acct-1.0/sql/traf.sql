-- MySQL dump 10.13  Distrib 5.1.70, for debian-linux-gnu (i486)
--
-- Host: 127.0.0.1    Database: traf
-- ------------------------------------------------------
-- Server version	5.1.70-0ubuntu0.10.04.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `geo`
--

DROP TABLE IF EXISTS `geo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `geo` (
  `ip_start` varchar(16) COLLATE latin1_general_ci DEFAULT NULL,
  `ip_end` varchar(16) COLLATE latin1_general_ci DEFAULT NULL,
  `ipn_start` int(11) DEFAULT NULL,
  `ipn_end` int(11) DEFAULT NULL,
  `country_code` varchar(3) COLLATE latin1_general_ci DEFAULT NULL,
  `country_name` varchar(50) COLLATE latin1_general_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `protocols`
--

DROP TABLE IF EXISTS `protocols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `protocols` (
  `demical` int(4) DEFAULT NULL,
  `keyword` varchar(20) DEFAULT NULL,
  `protocol` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `raw`
--

DROP TABLE IF EXISTS `raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw` (
  `unix_secs` int(11) unsigned NOT NULL DEFAULT '0',
  `doctets` int(11) unsigned NOT NULL DEFAULT '0',
  `srcaddr` varchar(45) CHARACTER SET latin1 NOT NULL DEFAULT '0',
  `dstaddr` varchar(45) CHARACTER SET latin1 NOT NULL DEFAULT '0',
  `srcport` smallint(5) unsigned NOT NULL DEFAULT '0',
  `dstport` smallint(5) unsigned NOT NULL DEFAULT '0',
  `prot` tinyint(3) unsigned NOT NULL DEFAULT '0',
  KEY `ip` (`dstaddr`(9)),
  KEY `src` (`srcaddr`(9)),
  KEY `addr` (`dstaddr`(9),`srcaddr`(9))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `traf`
--

DROP TABLE IF EXISTS `traf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `traf` (
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `src` varchar(45) NOT NULL DEFAULT '0',
  `dst` varchar(45) NOT NULL DEFAULT '0',
  `bytes` int(11) unsigned NOT NULL DEFAULT '0',
  KEY `dst` (`dst`(9)),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table for incoming traffic only by clients';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `user` varchar(45) DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `mac` varchar(45) DEFAULT NULL,
  `iface` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-26 22:12:56
