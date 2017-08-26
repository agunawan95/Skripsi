-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 26, 2017 at 01:36 PM
-- Server version: 10.1.25-MariaDB
-- PHP Version: 7.1.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `auto_analytics`
--

-- --------------------------------------------------------

--
-- Table structure for table `enterprise`
--

CREATE TABLE `enterprise` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `filesize_limit` int(11) NOT NULL,
  `user_limit` int(11) NOT NULL,
  `admin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `enterprise`
--

INSERT INTO `enterprise` (`id`, `name`, `address`, `email`, `phone`, `filesize_limit`, `user_limit`, `admin`) VALUES
(1, 'MM Bersatu', 'P226B', 'mm@astapz.com', '+62899123345', 50, 50, 5),
(2, 'Studio', 'P203', 'studio@astapz.com', '+62895543221', 70, 50, 10),
(3, 'PG', 'P206', 'pg@astapz.com', '+628997766552', 100, 70, 19),
(6, 'Joy', 'Joy St. Number 45', 'joy@astapz.com', '+62 895-4654-35', 50, 50, 28);

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `owner` int(11) NOT NULL,
  `added` date NOT NULL,
  `location` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `files`
--

INSERT INTO `files` (`id`, `name`, `owner`, `added`, `location`) VALUES
(3, 'hr.csv', 1, '2017-08-22', '806412bb3a7223b12e5661bbfb01d1/files/hr.csv'),
(4, 'house_price.csv', 1, '2017-08-22', '806412bb3a7223b12e5661bbfb01d1/files/house_price.csv'),
(7, 'west_nile.csv', 1, '2017-08-22', '806412bb3a7223b12e5661bbfb01d1/files/west_nile.csv'),
(8, 'weather.csv', 1, '2017-08-22', '806412bb3a7223b12e5661bbfb01d1/files/weather.csv'),
(9, 'spray.csv', 1, '2017-08-22', '806412bb3a7223b12e5661bbfb01d1/files/spray.csv'),
(10, 'weather.csv', 5, '2017-08-23', 'da40853e0f5b28565273529ebda0cb/files/weather.csv');

-- --------------------------------------------------------

--
-- Table structure for table `shared_files`
--

CREATE TABLE `shared_files` (
  `id` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_file` int(11) NOT NULL,
  `shared_at` date NOT NULL,
  `permission` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `shared_files`
--

INSERT INTO `shared_files` (`id`, `id_user`, `id_file`, `shared_at`, `permission`) VALUES
(1, 5, 3, '2017-08-23', 'w'),
(2, 7, 10, '2017-08-23', 'w'),
(6, 10, 3, '2017-08-23', 'w'),
(7, 19, 3, '2017-08-23', 'w'),
(8, 5, 4, '2017-08-23', 'w'),
(9, 5, 7, '2017-08-24', 'r');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `home_folder` varchar(150) NOT NULL,
  `auth` varchar(50) NOT NULL,
  `admin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `home_folder`, `auth`, `admin`) VALUES
(1, 'Andre', 'meong123', '806412bb3a7223b12e5661bbfb01d1', 'root', 0),
(5, 'juan', 'hastag', 'da40853e0f5b28565273529ebda0cb', 'admin', 0),
(7, 'yece', 'scmkb', '324340355985d50410140238ad5d1e', 'user', 5),
(8, 'satria', 'admin', '78d23cef825aebf373ee5c5c387c1f', 'user', 5),
(9, 'sanitya', 'admin', 'f8d60fea1cf84fc9fd7901d804675f', 'user', 5),
(10, 'dewe', 'meong', '93aba667267213099f17e80b2d8f93', 'admin', 0),
(11, 'dave', 'hastag', 'b0c32ba18ae392ec1978360105bc39', 'user', 5),
(12, 'darian', 'admin', '51890508da71c0bd77ef6cd927044b', 'user', 10),
(19, 'angel', 'meong', 'af214430ca4b98f81195c2f5f26803', 'admin', 0),
(20, 'bram', 'hastag', '4939ab90dfdf5211642a9bd3c85fba', 'user', 5),
(28, 'anya', 'taylor', '57db4b30bbd72dc582a1687659f924', 'admin', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `enterprise`
--
ALTER TABLE `enterprise`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shared_files`
--
ALTER TABLE `shared_files`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `enterprise`
--
ALTER TABLE `enterprise`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `shared_files`
--
ALTER TABLE `shared_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
