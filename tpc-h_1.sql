/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50622
Source Host           : localhost:3306
Source Database       : tpc-h

Target Server Type    : MYSQL
Target Server Version : 50622
File Encoding         : 65001

Date: 2018-12-24 20:35:49
*/

SET FOREIGN_KEY_CHECKS=0;
USE dbhomework;
-- ----------------------------
-- Table structure for `customer`
-- ----------------------------
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `C_CUSTKEY` int(11) NOT NULL AUTO_INCREMENT,
  `C_NAME` varchar(25) DEFAULT NULL,
  `C_ADDRESS` varchar(40) DEFAULT NULL,
  `C_NATIONKEY` int(11) DEFAULT NULL,
  `C_PHONE` varchar(16) DEFAULT NULL,
  `C_ACCTBAL` float DEFAULT NULL,
  `C_MKTSEGMENT` varchar(10) DEFAULT NULL,
  `C_COMMENT` varchar(117) DEFAULT NULL,
  PRIMARY KEY (`C_CUSTKEY`),
  KEY `C_NATIONKEY` (`C_NATIONKEY`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`C_NATIONKEY`) REFERENCES `nation` (`N_NATIONKEY`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of customer
-- ----------------------------
INSERT INTO `customer` VALUES ('1', 'Magic W', '地址是多少', '1', '18382001006', '12342', '中国', '中国');
INSERT INTO `customer` VALUES ('2', '朴德霜', '地址是多少', '1', '19908020202', '12342', '中国', 'good');

-- ----------------------------
-- Table structure for `lineitem`
-- ----------------------------
DROP TABLE IF EXISTS `lineitem`;
CREATE TABLE `lineitem` (
  `L_ORDERKEY` int(11) NOT NULL,
  `L_PARTKEY` int(11) DEFAULT NULL,
  `L_SUPPKEY` int(11) DEFAULT NULL,
  `L_LINENUMBER` int(11) NOT NULL,
  `L_QUANTITY` float DEFAULT NULL,
  `L_EXTENDEDPRICE` float DEFAULT NULL,
  `L_DISCOUNT` float DEFAULT NULL,
  `L_TAX` float DEFAULT NULL,
  `L_RETURNFLAG` varchar(1) DEFAULT NULL,
  `L_LINESTATUS` varchar(1) DEFAULT NULL,
  `L_SHIPDATE` datetime DEFAULT NULL,
  `L_COMMITDATE` datetime DEFAULT NULL,
  `L_RECEIPTDATE` datetime DEFAULT NULL,
  `L_SHIPINSTRUCT` varchar(25) DEFAULT NULL,
  `L_SHIPMODE` varchar(25) DEFAULT NULL,
  `L_COMMENT` varchar(44) DEFAULT NULL,
  PRIMARY KEY (`L_ORDERKEY`,`L_LINENUMBER`),
  KEY `L_PARTKEY` (`L_PARTKEY`),
  KEY `L_SUPPKEY` (`L_SUPPKEY`),
  CONSTRAINT `lineitem_ibfk_1` FOREIGN KEY (`L_ORDERKEY`) REFERENCES `orders` (`O_ORDERKEY`),
  CONSTRAINT `lineitem_ibfk_2` FOREIGN KEY (`L_PARTKEY`) REFERENCES `partsupp` (`PS_PARTKEY`),
  CONSTRAINT `lineitem_ibfk_3` FOREIGN KEY (`L_PARTKEY`) REFERENCES `partsupp` (`PS_SUPPKEY`),
  CONSTRAINT `lineitem_ibfk_4` FOREIGN KEY (`L_SUPPKEY`) REFERENCES `partsupp` (`PS_PARTKEY`),
  CONSTRAINT `lineitem_ibfk_5` FOREIGN KEY (`L_SUPPKEY`) REFERENCES `partsupp` (`PS_SUPPKEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of lineitem
-- ----------------------------
INSERT INTO `lineitem` VALUES ('1', '2', '1', '2', '70', '119', '0.85', '20', '否', '未', '2018-12-21 00:00:00', '2018-12-29 00:00:00', '2018-12-30 00:00:00', '吨', '船', '3');
INSERT INTO `lineitem` VALUES ('1', '1', '1', '3', '8', '74.8', '0.85', '20', '否', '未', '1996-01-01 00:00:00', '2018-12-27 00:00:00', '2018-12-30 00:00:00', '吨', '船', '1');

-- ----------------------------
-- Table structure for `nation`
-- ----------------------------
DROP TABLE IF EXISTS `nation`;
CREATE TABLE `nation` (
  `N_NATIONKEY` int(11) NOT NULL AUTO_INCREMENT,
  `N_NAME` varchar(25) DEFAULT NULL,
  `N_REGIONKEY` int(11) DEFAULT NULL,
  `N_COMMENT` varchar(152) DEFAULT NULL,
  PRIMARY KEY (`N_NATIONKEY`),
  KEY `N_REGIONKEY` (`N_REGIONKEY`),
  CONSTRAINT `nation_ibfk_1` FOREIGN KEY (`N_REGIONKEY`) REFERENCES `region` (`R_REGIONKEY`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of nation
-- ----------------------------
INSERT INTO `nation` VALUES ('1', '中国', '1', 'good');
INSERT INTO `nation` VALUES ('2', '英国', '3', 'good');
INSERT INTO `nation` VALUES ('3', '美国', '4', 'hhhh');
INSERT INTO `nation` VALUES ('4', '埃及', '2', '3');
INSERT INTO `nation` VALUES ('5', '澳大利亚', '5', 'hhhh');

-- ----------------------------
-- Table structure for `orders`
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `O_ORDERKEY` int(11) NOT NULL AUTO_INCREMENT,
  `O_CUSTKEY` int(11) DEFAULT NULL,
  `O_ORDERSTATUS` varchar(1) DEFAULT NULL,
  `O_TOTALPRICE` float DEFAULT NULL,
  `O_ORDERDATE` datetime DEFAULT NULL,
  `O_ORDERPRIORITY` varchar(15) DEFAULT NULL,
  `O_CLERK` varchar(15) DEFAULT NULL,
  `O_SHIPPRIORITY` int(11) DEFAULT NULL,
  `O_COMMENT` varchar(79) DEFAULT NULL,
  PRIMARY KEY (`O_ORDERKEY`),
  KEY `O_CUSTKEY` (`O_CUSTKEY`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`O_CUSTKEY`) REFERENCES `customer` (`C_CUSTKEY`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES ('1', '1', '1', '193.8', '2018-12-20 00:00:00', '1', 'j', '1', 'hhhh');
INSERT INTO `orders` VALUES ('2', '2', '3', '0', '2018-12-05 00:00:00', '2', 't', '2', 'hhhh');

-- ----------------------------
-- Table structure for `part`
-- ----------------------------
DROP TABLE IF EXISTS `part`;
CREATE TABLE `part` (
  `P_PARTKEY` int(11) NOT NULL AUTO_INCREMENT,
  `P_NAME` varchar(55) DEFAULT NULL,
  `P_MFGR` varchar(25) DEFAULT NULL,
  `P_BRAND` varchar(10) DEFAULT NULL,
  `P_TYPE` varchar(25) DEFAULT NULL,
  `P_SIZE` int(11) DEFAULT NULL,
  `P_CONTAINER` varchar(10) DEFAULT NULL,
  `P_RETAILPRICE` float DEFAULT NULL,
  `P_COMMENT` varchar(23) DEFAULT NULL,
  PRIMARY KEY (`P_PARTKEY`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of part
-- ----------------------------
INSERT INTO `part` VALUES ('1', 'a', '1', 'TE', '汽车零件', '3', '周转包装', '11', 'good');
INSERT INTO `part` VALUES ('2', 'b', '4', 'TE', '普通零件', '2', '一次性包装', '2', 'good');
INSERT INTO `part` VALUES ('3', 'c', '1', 'TE', '电脑零件', '5', '周转包装', '15', 'hhhh');

-- ----------------------------
-- Table structure for `partsupp`
-- ----------------------------
DROP TABLE IF EXISTS `partsupp`;
CREATE TABLE `partsupp` (
  `PS_PARTKEY` int(11) NOT NULL,
  `PS_SUPPKEY` int(11) NOT NULL,
  `PS_AVAILQTY` int(11) DEFAULT NULL,
  `PS_SUPPLYCOST` float DEFAULT NULL,
  `PS_COMMENT` varchar(199) DEFAULT NULL,
  PRIMARY KEY (`PS_PARTKEY`,`PS_SUPPKEY`),
  KEY `PS_SUPPKEY` (`PS_SUPPKEY`),
  CONSTRAINT `partsupp_ibfk_1` FOREIGN KEY (`PS_PARTKEY`) REFERENCES `part` (`P_PARTKEY`),
  CONSTRAINT `partsupp_ibfk_2` FOREIGN KEY (`PS_SUPPKEY`) REFERENCES `supplier` (`S_SUPPKEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of partsupp
-- ----------------------------
INSERT INTO `partsupp` VALUES ('1', '1', '1250', '13', 'hhhh');
INSERT INTO `partsupp` VALUES ('2', '2', '1600', '5', '3');

-- ----------------------------
-- Table structure for `region`
-- ----------------------------
DROP TABLE IF EXISTS `region`;
CREATE TABLE `region` (
  `R_REGIONKEY` int(11) NOT NULL AUTO_INCREMENT,
  `R_NAME` varchar(25) DEFAULT NULL,
  `R_COMMENT` varchar(152) DEFAULT NULL,
  `PS_SUPPLYCOST` float DEFAULT NULL,
  `PS_COMMENT` varchar(199) DEFAULT NULL,
  PRIMARY KEY (`R_REGIONKEY`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of region
-- ----------------------------
INSERT INTO `region` VALUES ('1', '亚洲', '哈哈哈', '12', '哈哈哈哈');
INSERT INTO `region` VALUES ('2', '非洲', '哈哈哈哈', '13', '哈哈哈哈');
INSERT INTO `region` VALUES ('3', '欧洲', '哈哈哈哈', '15', '哈哈哈哈');
INSERT INTO `region` VALUES ('4', '美洲', '哈哈哈哈', '33', '哈哈哈哈');
INSERT INTO `region` VALUES ('5', '大洋洲', '哈哈哈哈', '25', '哈哈哈哈');

-- ----------------------------
-- Table structure for `supplier`
-- ----------------------------
DROP TABLE IF EXISTS `supplier`;
CREATE TABLE `supplier` (
  `S_SUPPKEY` int(11) NOT NULL AUTO_INCREMENT,
  `S_NAME` varchar(25) DEFAULT NULL,
  `S_ADDRESS` varchar(40) DEFAULT NULL,
  `S_NATIONKEY` int(11) DEFAULT NULL,
  `S_PHONE` varchar(15) DEFAULT NULL,
  `S_ACCTBAL` float DEFAULT NULL,
  `S_COMMENT` varchar(101) DEFAULT NULL,
  PRIMARY KEY (`S_SUPPKEY`),
  KEY `S_NATIONKEY` (`S_NATIONKEY`),
  CONSTRAINT `supplier_ibfk_1` FOREIGN KEY (`S_NATIONKEY`) REFERENCES `nation` (`N_NATIONKEY`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of supplier
-- ----------------------------
INSERT INTO `supplier` VALUES ('1', '潘柳燕', '不知道地址', '1', '18382001006', '23213', '好供应商');
INSERT INTO `supplier` VALUES ('2', '朴德霜', '不知道地址', '1', '19908020202', '112332', '3');
