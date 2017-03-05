-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 21, 2017 at 05:30 PM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pig`
--
CREATE DATABASE IF NOT EXISTS `pig` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pig`;

-- --------------------------------------------------------

--
-- Table structure for table `boar`
--

CREATE TABLE `boar` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `ear_tag` int(11) UNSIGNED DEFAULT NULL COMMENT '耳标',
  `ear_lack` int(11) UNSIGNED DEFAULT NULL COMMENT '耳缺',
  `birthday` date DEFAULT NULL,
  `entryday` date DEFAULT NULL,
  `dormitory_id` int(11) UNSIGNED DEFAULT NULL,
  `category_id` int(11) UNSIGNED DEFAULT NULL,
  `breed_num` int(11) UNSIGNED DEFAULT NULL COMMENT '配种次数',
  `breed_acceptability` float DEFAULT NULL COMMENT '配种合格率',
  `source_id` int(11) UNSIGNED DEFAULT NULL COMMENT '来源',
  `note` varchar(255) DEFAULT NULL COMMENT '备注',
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` bigint(20) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `breed_record`
--

CREATE TABLE `breed_record` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `sow_id` bigint(20) UNSIGNED NOT NULL COMMENT '母猪id',
  `boar_id` bigint(20) UNSIGNED NOT NULL COMMENT '公猪id',
  `date` date NOT NULL,
  `staff_id` int(11) UNSIGNED NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` bigint(20) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(36) NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` int(11) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory`
--

CREATE TABLE `dormitory` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(36) NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` int(11) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `parturition_record`
--

CREATE TABLE `parturition_record` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `sow_id` bigint(20) UNSIGNED NOT NULL COMMENT '母猪id',
  `piglet_num` int(11) UNSIGNED NOT NULL COMMENT '仔猪数量',
  `date` date NOT NULL,
  `staff_id` int(11) UNSIGNED NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` bigint(20) UNSIGNED DEFAULT 0 
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `return_record`
--

CREATE TABLE `return_record` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `sow_id` bigint(20) UNSIGNED NOT NULL COMMENT '母猪id',
  `type` int(11) UNSIGNED NOT NULL COMMENT '空留返类型',
  `date` date NOT NULL,
  `staff_id` int(11) UNSIGNED NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` int(20) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `source`
--

CREATE TABLE `source` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(36) NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` int(11) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sow`
--

CREATE TABLE `sow` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `ear_tag` int(11) UNSIGNED DEFAULT NULL COMMENT '耳标',
  `ear_lack` int(11) UNSIGNED DEFAULT NULL COMMENT '耳缺',
  `birthday` date DEFAULT NULL,
  `entryday` date DEFAULT NULL,
  `dormitory_id` int(11) UNSIGNED DEFAULT NULL,
  `category_id` int(11) UNSIGNED DEFAULT NULL,
  `gestational_age` int(11) UNSIGNED DEFAULT NULL COMMENT '胎龄',
  `accum_return` int(11) UNSIGNED DEFAULT NULL COMMENT '累积返情次数',
  `state_id` int(11) UNSIGNED DEFAULT NULL COMMENT '状态',
  `state_day` int(11) UNSIGNED DEFAULT NULL COMMENT '状态天数',
  `source_id` int(11) UNSIGNED DEFAULT NULL COMMENT '来源',
  `note` varchar(255) DEFAULT NULL COMMENT '备注',
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` bigint(20) UNSIGNED DEFAULT 0 
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(36) NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` int(11) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `state`
--

CREATE TABLE `state` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(36) NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` int(11) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `weaning_record`
--

CREATE TABLE `weaning_record` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `sow_id` bigint(20) UNSIGNED NOT NULL COMMENT '母猪id',
  `rate` float NOT NULL COMMENT '断奶合格率',
  `date` date NOT NULL,
  `staff_id` int(11) UNSIGNED NOT NULL,
  `created_at` date DEFAULT NULL,
  `updated_at` date DEFAULT NULL,
  `deleted_at` date DEFAULT NULL,
  `deleted` bigint(20) UNSIGNED DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `boar`
--
ALTER TABLE `boar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `breed_record`
--
ALTER TABLE `breed_record`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dormitory`
--
ALTER TABLE `dormitory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `parturition_record`
--
ALTER TABLE `parturition_record`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `return_record`
--
ALTER TABLE `return_record`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `source`
--
ALTER TABLE `source`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sow`
--
ALTER TABLE `sow`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `state`
--
ALTER TABLE `state`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `weaning_record`
--
ALTER TABLE `weaning_record`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `boar`
--
ALTER TABLE `boar`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `breed_record`
--
ALTER TABLE `breed_record`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `dormitory`
--
ALTER TABLE `dormitory`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `parturition_record`
--
ALTER TABLE `parturition_record`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `return_record`
--
ALTER TABLE `return_record`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `source`
--
ALTER TABLE `source`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `sow`
--
ALTER TABLE `sow`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `state`
--
ALTER TABLE `state`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `weaning_record`
--
ALTER TABLE `weaning_record`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
