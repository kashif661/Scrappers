/*
 Navicat MySQL Data Transfer

 Source Server         : OVHServer2
 Source Server Type    : MySQL
 Source Server Version : 50742
 Source Host           : 51.161.15.62:3306
 Source Schema         : LeadFuzionDatabase

 Target Server Type    : MySQL
 Target Server Version : 50742
 File Encoding         : 65001

 Date: 21/08/2023 02:51:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for I_Address_Shorts
-- ----------------------------
DROP TABLE IF EXISTS `I_Address_Shorts`;
CREATE TABLE `I_Address_Shorts` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `std_abbreviation` varchar(50) DEFAULT NULL,
  `possible_values` text,
  `value_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  FULLTEXT KEY `index1_IAS` (`possible_values`)
) ENGINE=InnoDB AUTO_INCREMENT=537 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of I_Address_Shorts
-- ----------------------------
BEGIN;
INSERT INTO `I_Address_Shorts` VALUES (2, 'ALY', '[\"ALLEE\", \"ALLEY\", \"ALLEY\", \"ALLY\", \"ALY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (3, 'ANX', '[\"ANEX\", \"ANEX\", \"ANNEX\", \"ANNX\", \"ANX\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (4, 'ARC', '[\"ARC\\u00a0\", \"ARCADE\", \"ARCADE\\u00a0\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (5, 'AVE', '[\"AV\", \"AVENUE\", \"AVE\", \"AVEN\", \"AVENU\", \"AVENUE\", \"AVN\", \"AVNUE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (6, 'BCH', '[\"BCH\", \"BEACH\", \"BEACH\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (7, 'BG', '[\"BURG\", \"BURG\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (8, 'BGS', '[\"BURGS\", \"BURGS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (9, 'BLF', '[\"BLF\", \"BLUFF\", \"BLUF\", \"BLUFF\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (10, 'BLFS', '[\"BLUFFS\\u00a0\", \"BLUFFS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (11, 'BLVD', '[\"BLVD\", \"BOULEVARD\", \"BOUL\", \"BOULEVARD\\u00a0\", \"BOULV\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (12, 'BND', '[\"BEND\", \"BEND\", \"BND\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (13, 'BR', '[\"BR\", \"BRANCH\", \"BRNCH\", \"BRANCH\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (14, 'BRG', '[\"BRDGE\", \"BRIDGE\", \"BRG\", \"BRIDGE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (15, 'BRK', '[\"BRK\", \"BROOK\", \"BROOK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (16, 'BRKS', '[\"BROOKS\\u00a0\", \"BROOKS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (17, 'BTM', '[\"BOT\", \"BOTTOM\", \"BTM\", \"BOTTM\", \"BOTTOM\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (18, 'BYP', '[\"BYP\", \"BYPASS\", \"BYPA\", \"BYPAS\", \"BYPASS\", \"BYPS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (19, 'BYU', '[\"BAYOO\", \"BAYOU\", \"BAYOU\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (20, 'CIR', '[\"CIR\", \"CIRCLE\", \"CIRC\", \"CIRCL\", \"CIRCLE\", \"CRCL\", \"CRCLE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (21, 'CIRS', '[\"CIRCLES\", \"CIRCLES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (22, 'CLB', '[\"CLB\", \"CLUB\", \"CLUB\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (23, 'CLF', '[\"CLF\", \"CLIFF\", \"CLIFF\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (24, 'CLFS', '[\"CLFS\", \"CLIFFS\", \"CLIFFS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (25, 'CMN', '[\"COMMON\", \"COMMON\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (26, 'CMNS', '[\"COMMONS\", \"COMMONS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (27, 'COR', '[\"COR\", \"CORNER\", \"CORNER\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (28, 'CORS', '[\"CORNERS\", \"CORNERS\", \"CORS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (29, 'CP', '[\"CAMP\", \"CAMP\", \"CP\", \"CMP\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (30, 'CPE', '[\"CAPE\", \"CAPE\", \"CPE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (31, 'CRES', '[\"CRESCENT\", \"CRESCENT\", \"CRES\", \"CRSENT\", \"CRSNT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (32, 'CRK', '[\"CREEK\", \"CREEK\", \"CRK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (33, 'CRSE', '[\"COURSE\", \"COURSE\", \"CRSE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (34, 'CRST', '[\"CREST\", \"CREST\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (35, 'CSWY', '[\"CAUSEWAY\", \"CAUSEWAY\", \"CAUSWA\", \"CSWY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (36, 'CT', '[\"COURT\", \"COURT\", \"CT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (37, 'CTR', '[\"CEN\", \"CENTER\", \"CENT\", \"CENTER\", \"CENTR\", \"CENTRE\", \"CNTER\", \"CNTR\", \"CTR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (38, 'CTRS', '[\"CENTERS\\u00a0\", \"CENTERS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (39, 'CTS', '[\"COURTS\", \"COURTS\", \"CTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (40, 'CURV', '[\"CURVE\\u00a0\", \"CURVE\\u00a0\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (41, 'CV', '[\"COVE\", \"COVE\", \"CV\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (42, 'CVS', '[\"COVES\", \"COVES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (43, 'CYN', '[\"CANYN\", \"CANYON\", \"CANYON\", \"CNYN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (44, 'DL', '[\"DALE\\u00a0\", \"DALE\", \"DL\\u00a0\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (45, 'DM', '[\"DAM\\u00a0\", \"DAM\", \"DM\\u00a0\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (46, 'DR', '[\"DR\", \"DRIVE\", \"DRIV\", \"DRIVE\", \"DRV\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (47, 'DRS', '[\"DRIVES\", \"DRIVES\\u00a0\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (48, 'DV', '[\"DIV\", \"DIVIDE\", \"DIVIDE\", \"DV\", \"DVD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (49, 'EST', '[\"EST\", \"ESTATE\", \"ESTATE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (50, 'ESTS', '[\"ESTATES\", \"ESTATES\", \"ESTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (51, 'EXPY', '[\"EXP\", \"EXPRESSWAY\", \"EXPR\", \"EXPRESS\", \"EXPRESSWAY\", \"EXPW\", \"EXPY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (52, 'EXT', '[\"EXT\", \"EXTENSION\", \"EXTENSION\", \"EXTN\", \"EXTNSN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (53, 'EXTS', '[\"EXTS\", \"EXTENSIONS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (54, 'FALL', '[\"FALL\", \"FALL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (55, 'FLD', '[\"FIELD\", \"FIELD\", \"FLD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (56, 'FLDS', '[\"FIELDS\", \"FIELDS\", \"FLDS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (57, 'FLS', '[\"FALLS\", \"FALLS\", \"FLS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (58, 'FLT', '[\"FLAT\", \"FLAT\", \"FLT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (59, 'FLTS', '[\"FLATS\", \"FLATS\", \"FLTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (60, 'FRD', '[\"FORD\", \"FORD\", \"FRD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (61, 'FRDS', '[\"FORDS\", \"FORDS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (62, 'FRG', '[\"FORG\", \"FORGE\", \"FORGE\", \"FRG\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (63, 'FRGS', '[\"FORGES\", \"FORGES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (64, 'FRK', '[\"FORK\", \"FORK\", \"FRK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (65, 'FRKS', '[\"FORKS\", \"FORKS\", \"FRKS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (66, 'FRST', '[\"FOREST\", \"FOREST\", \"FORESTS\", \"FRST\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (67, 'FRY', '[\"FERRY\", \"FERRY\", \"FRRY\", \"FRY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (68, 'FT', '[\"FORT\", \"FORT\", \"FRT\", \"FT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (69, 'FWY', '[\"FREEWAY\", \"FREEWAY\", \"FREEWY\", \"FRWAY\", \"FRWY\", \"FWY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (70, 'GDN', '[\"GARDEN\", \"GARDEN\", \"GARDN\", \"GRDEN\", \"GRDN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (71, 'GDNS', '[\"GARDENS\", \"GARDENS\", \"GDNS\", \"GRDNS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (72, 'GLN', '[\"GLEN\", \"GLEN\", \"GLN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (73, 'GLNS', '[\"GLENS\", \"GLENS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (74, 'GRN', '[\"GREEN\", \"GREEN\", \"GRN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (75, 'GRNS', '[\"GREENS\", \"GREENS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (76, 'GRV', '[\"GROV\", \"GROVE\", \"GROVE\", \"GRV\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (77, 'GRVS', '[\"GROVES\", \"GROVES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (78, 'GTWY', '[\"GATEWAY\", \"GATEWAY\", \"GATEWY\", \"GATWAY\", \"GTWAY\", \"GTWY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (79, 'HBR', '[\"HARB\", \"HARBOR\", \"HARBOR\", \"HARBR\", \"HBR\", \"HRBOR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (80, 'HBRS', '[\"HARBORS\", \"HARBORS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (81, 'HL', '[\"HILL\", \"HILL\", \"HL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (82, 'HLS', '[\"HILLS\", \"HILLS\", \"HLS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (83, 'HOLW', '[\"HLLW\", \"HOLLOW\", \"HOLLOW\", \"HOLLOWS\", \"HOLW\", \"HOLWS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (84, 'HTS', '[\"HT\", \"HEIGHTS\", \"HTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (85, 'HVN', '[\"HAVEN\", \"HAVEN\", \"HVN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (86, 'HWY', '[\"HIGHWAY\", \"HIGHWAY\", \"HIGHWY\", \"HIWAY\", \"HIWY\", \"HWAY\", \"HWY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (87, 'INLT', '[\"INLT\", \"INLET\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (88, 'IS', '[\"IS\", \"ISLAND\", \"ISLAND\", \"ISLND\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (89, 'ISLE', '[\"ISLE\", \"ISLE\", \"ISLES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (90, 'ISS', '[\"ISLANDS\", \"ISLANDS\", \"ISLNDS\", \"ISS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (91, 'JCT', '[\"JCT\", \"JUNCTION\", \"JCTION\", \"JCTN\", \"JUNCTION\", \"JUNCTN\", \"JUNCTON\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (92, 'JCTS', '[\"JCTNS\", \"JUNCTIONS\", \"JCTS\", \"JUNCTIONS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (93, 'KNL ', '[\"KNL\", \"KNOLL\", \"KNOL\", \"KNOLL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (94, 'KNLS', '[\"KNLS\", \"KNOLLS\", \"KNOLLS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (95, 'KY', '[\"KEY\", \"KEY\", \"KY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (96, 'KYS', '[\"KEYS\", \"KEYS\", \"KYS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (97, 'LAND', '[\"LAND\", \"LAND\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (98, 'LCK', '[\"LCK\", \"LOCK\", \"LOCK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (99, 'LCKS', '[\"LCKS\", \"LOCKS\", \"LOCKS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (100, 'LDG', '[\"LDG\", \"LODGE\", \"LDGE\", \"LODG\", \"LODGE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (101, 'LF', '[\"LF\", \"LOAF\", \"LOAF\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (102, 'LGT', '[\"LGT\", \"LIGHT\", \"LIGHT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (103, 'LGTS', '[\"LIGHTS\", \"LIGHTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (104, 'LK', '[\"LK\", \"LAKE\", \"LAKE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (105, 'LKS', '[\"LKS\", \"LAKES\", \"LAKES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (106, 'LN', '[\"LANE\", \"LANE\", \"LN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (107, 'LNDG', '[\"LANDING\", \"LANDING\", \"LNDG\", \"LNDNG\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (108, 'LOOP', '[\"LOOP\", \"LOOP\", \"LOOPS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (109, 'MALL', '[\"MALL\", \"MALL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (110, 'MDW', '[\"MEADOW\", \"MEADOW\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (111, 'MDWS', '[\"MDW\", \"MEADOWS\", \"MDWS\", \"MEADOWS\", \"MEDOWS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (112, 'MEWS', '[\"MEWS\", \"MEWS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (113, 'ML', '[\"MILL\", \"MILL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (114, 'MLS', '[\"MILLS\", \"MILLS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (115, 'MNR', '[\"MNR\", \"MANOR\", \"MANOR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (116, 'MNRS', '[\"MANORS\", \"MANORS\", \"MNRS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (117, 'MSN', '[\"MISSN\", \"MISSION\", \"MSSN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (118, 'MT', '[\"MNT\", \"MOUNT\", \"MT\", \"MOUNT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (119, 'MTN', '[\"MNTAIN\", \"MOUNTAIN\", \"MNTN\", \"MOUNTAIN\", \"MOUNTIN\", \"MTIN\", \"MTN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (120, 'MTNS', '[\"MNTNS\", \"MOUNTAINS\", \"MOUNTAINS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (121, 'MTWY', '[\"MOTORWAY\", \"MOTORWAY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (122, 'NCK', '[\"NCK\", \"NECK\", \"NECK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (123, 'OPAS', '[\"OVERPASS\", \"OVERPASS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (124, 'ORCH', '[\"ORCH\", \"ORCHARD\", \"ORCHARD\", \"ORCHRD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (125, 'OVAL', '[\"OVAL\", \"OVAL\", \"OVL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (126, 'PARK', '[\"PARK\", \"PARK\", \"PRK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (127, 'PARK', '[\"PARKS\", \"PARKS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (128, 'PASS', '[\"PASS\", \"PASS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (129, 'PATH', '[\"PATH\", \"PATH\", \"PATHS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (130, 'PIKE', '[\"PIKE\", \"PIKE\", \"PIKES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (131, 'PKWY', '[\"PARKWAY\", \"PARKWAY\", \"PARKWY\", \"PKWAY\", \"PKWY\", \"PKY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (132, 'PKWY', '[\"PARKWAYS\", \"PARKWAYS\", \"PKWYS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (133, 'PL', '[\"PL\", \"PLACE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (134, 'PLN', '[\"PLAIN\", \"PLAIN\", \"PLN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (135, 'PLNS', '[\"PLAINS\", \"PLAINS\", \"PLNS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (136, 'PLZ', '[\"PLAZA\", \"PLAZA\", \"PLZ\", \"PLZA\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (137, 'PNE ', '[\"PINE\", \"PINE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (138, 'PNES', '[\"PINES\", \"PINES\", \"PNES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (139, 'PR', '[\"PR\", \"PRAIRIE\", \"PRAIRIE\", \"PRR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (140, 'PRT', '[\"PORT\", \"PORT\", \"PRT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (141, 'PRTS', '[\"PORTS\", \"PORTS\", \"PRTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (142, 'PSGE', '[\"PASSAGE\", \"PASSAGE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (143, 'PT', '[\"POINT\", \"POINT\", \"PT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (144, 'PTS', '[\"POINTS\", \"POINTS\", \"PTS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (145, 'RADL', '[\"RAD\", \"RADIAL\", \"RADIAL\", \"RADIEL\", \"RADL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (146, 'RAMP', '[\"RAMP\", \"RAMP\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (147, 'RD', '[\"RD\", \"ROAD\", \"ROAD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (148, 'RDG', '[\"RDG\", \"RIDGE\", \"RDGE\", \"RIDGE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (149, 'RDGS', '[\"RDGS\", \"RIDGES\", \"RIDGES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (150, 'RDS', '[\"ROADS\", \"ROADS\", \"RDS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (151, 'RIV', '[\"RIV\", \"RIVER\", \"RIVER\", \"RVR\", \"RIVR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (152, 'RNCH', '[\"RANCH\", \"RANCH\", \"RANCHES\", \"RNCH\", \"RNCHS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (153, 'ROW', '[\"ROW\", \"ROW\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (154, 'RPD', '[\"RAPID\", \"RAPID\", \"RPD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (155, 'RPDS', '[\"RAPIDS\", \"RAPIDS\", \"RPDS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (156, 'RST', '[\"REST\", \"REST\", \"RST\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (157, 'RTE', '[\"ROUTE\", \"ROUTE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (158, 'RUE', '[\"RUE\", \"RUE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (159, 'RUN', '[\"RUN\", \"RUN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (160, 'SHL', '[\"SHL\", \"SHOAL\", \"SHOAL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (161, 'SHLS', '[\"SHLS\", \"SHOALS\", \"SHOALS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (162, 'SHR', '[\"SHOAR\", \"SHORE\", \"SHORE\", \"SHR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (163, 'SHRS', '[\"SHOARS\", \"SHORES\", \"SHORES\", \"SHRS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (164, 'SKWY', '[\"SKYWAY\", \"SKYWAY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (165, 'SMT', '[\"SMT\", \"SUMMIT\", \"SUMIT\", \"SUMITT\", \"SUMMIT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (166, 'SPG', '[\"SPG\", \"SPRING\", \"SPNG\", \"SPRING\", \"SPRNG\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (167, 'SPGS', '[\"SPGS\", \"SPRINGS\", \"SPNGS\", \"SPRINGS\", \"SPRNGS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (168, 'SPUR', '[\"SPUR\", \"SPUR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (169, 'SPUR', '[\"SPURS\", \"SPURS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (170, 'SQ', '[\"SQ\", \"SQUARE\", \"SQR\", \"SQRE\", \"SQU\", \"SQUARE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (171, 'SQS', '[\"SQRS\", \"SQUARES\", \"SQUARES\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (172, 'ST', '[\"STREET\", \"STREET\", \"STRT\", \"ST\", \"STR\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (173, 'STA', '[\"STA\", \"STATION\", \"STATION\", \"STATN\", \"STN\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (174, 'STRA', '[\"STRA\", \"STRAVENUE\", \"STRAV\", \"STRAVEN\", \"STRAVENUE\", \"STRAVN\", \"STRVN\", \"STRVNUE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (175, 'STRM', '[\"STREAM\", \"STREAM\", \"STREME\", \"STRM\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (176, 'STS', '[\"STREETS\", \"STREETS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (177, 'TER', '[\"TER\", \"TERRACE\", \"TERR\", \"TERRACE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (178, 'TPKE', '[\"TRNPK\", \"TURNPIKE\", \"TURNPIKE\", \"TURNPK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (179, 'TRAK', '[\"TRACK\", \"TRACK\", \"TRACKS\", \"TRAK\", \"TRK\", \"TRKS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (180, 'TRCE', '[\"TRACE\", \"TRACE\", \"TRACES\", \"TRCE\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (181, 'TRFY', '[\"TRAFFICWAY\", \"TRAFFICWAY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (182, 'TRL', '[\"TRAIL\", \"TRAIL\", \"TRAILS\", \"TRL\", \"TRLS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (183, 'TRLR', '[\"TRAILER\", \"TRAILER\", \"TRLR\", \"TRLRS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (184, 'TRWY', '[\"THROUGHWAY\", \"THROUGHWAY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (185, 'TUNL', '[\"TUNEL\", \"TUNNEL\", \"TUNL\", \"TUNLS\", \"TUNNEL\", \"TUNNELS\", \"TUNNL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (186, 'UN', '[\"UN\", \"UNION\", \"UNION\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (187, 'UNS', '[\"UNIONS\", \"UNIONS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (188, 'UPAS', '[\"UNDERPASS\", \"UNDERPASS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (189, 'VIA', '[\"VDCT\", \"VIADUCT\", \"VIA\", \"VIADCT\", \"VIADUCT\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (190, 'VIS', '[\"VIS\", \"VISTA\", \"VIST\", \"VISTA\", \"VST\", \"VSTA\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (191, 'VL', '[\"VILLE\", \"VILLE\", \"VL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (192, 'VLG', '[\"VILL\", \"VILLAGE\", \"VILLAG\", \"VILLAGE\", \"VILLG\", \"VILLIAGE\", \"VLG\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (193, 'VLGS', '[\"VILLAGES\", \"VILLAGES\", \"VLGS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (194, 'VLY', '[\"VALLEY\", \"VALLEY\", \"VALLY\", \"VLLY\", \"VLY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (195, 'VLYS', '[\"VALLEYS\", \"VALLEYS\", \"VLYS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (196, 'VW', '[\"VIEW\", \"VIEW\", \"VW\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (197, 'VWS', '[\"VIEWS\", \"VIEWS\", \"VWS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (198, 'WALK', '[\"WALK\", \"WALK\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (199, 'WALK', '[\"WALKS\", \"WALKS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (200, 'WALL', '[\"WALL\", \"WALL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (201, 'WAY', '[\"WY\", \"WAY\", \"WAY\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (202, 'WAYS', '[\"WAYS\", \"WAYS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (203, 'WL ', '[\"WELL\", \"WELL\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (204, 'WLS', '[\"WELLS\", \"WELLS\", \"WLS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (205, 'XING', '[\"CROSSING\", \"CROSSING\", \"CRSSNG\", \"XING\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (206, 'XRD', '[\"CROSSROAD\", \"CROSSROAD\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (207, 'XRDS', '[\"CROSSROADS\", \"CROSSROADS\"]', 'street_suffix');
INSERT INTO `I_Address_Shorts` VALUES (504, 'N', '[\"NORTH\",\"N\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (505, 'NE', '[\"NORTHEAST\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (506, 'NW', '[\"NORTHWEST\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (507, 'S', '[\"SOUTH\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (508, 'SE', '[\"SOUTHEAST\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (509, 'SW', '[\"SOUTHWEST\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (510, 'E', '[\"EAST\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (511, 'W', '[\"WEST\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (512, 'APT', '[\"Apartment\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (513, 'BSMT', '[\"Basement\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (514, 'BLDG', '[\"Building\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (515, 'DEPT', '[\"Department\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (516, 'FL', '[\"Floor\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (517, 'FRNT', '[\"Front\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (518, 'HNGR', '[\"Hanger\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (519, 'KEY', '[\"Key\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (520, 'LBBY', '[\"Lobby\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (521, 'LOT', '[\"Lot\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (522, 'LOWR', '[\"Lower\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (523, 'OFC', '[\"Office\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (524, 'PH', '[\"Penthouse\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (525, 'PIER', '[\"Pier\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (526, 'REAR', '[\"Rear\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (527, 'RM', '[\"Room\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (528, 'SIDE', '[\"Side\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (529, 'SLIP', '[\"Slip\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (530, 'SPC', '[\"Space\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (531, 'STOP', '[\"Stop\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (532, 'STE', '[\"Suite\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (533, 'TRLR', '[\"Trailer\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (534, 'UNIT', '[\"Unit\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (535, 'UPPR', '[\"Upper\"]', 'direction');
INSERT INTO `I_Address_Shorts` VALUES (536, '#', '[\"#\"]', 'direction');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
