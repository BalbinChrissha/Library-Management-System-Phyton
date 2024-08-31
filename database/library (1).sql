-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2023 at 01:32 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `book_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `author` varchar(255) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `rack_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 1 COMMENT '1 = Available, 2 = Archive',
  `date_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_updated` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`book_id`, `name`, `isbn`, `author`, `publisher`, `cat_id`, `rack_id`, `quantity`, `status`, `date_created`, `date_updated`) VALUES
(1, 'Romeo and Juliet', 'N153D', 'William Shakespeare', 'William Shakespeare Ememe', 8, 3, 5, 1, '2023-12-16 13:42:01', '2023-12-16 13:42:01'),
(7, 'To Kill a Mockingbird', 'SB924', 'Harper Lee', 'J.B. Lippincott & Co.', 8, 4, 8, 1, '2023-12-17 13:21:49', '2023-12-17 13:21:49'),
(8, 'The Great Gatsby', 'UHW547', 'F. Scott Fitzgerald', 'Charles Scribner\'s Sons', 9, 5, 3, 1, '2023-12-17 13:22:25', '2023-12-17 13:22:25'),
(9, 'The Catcher in the Rye', 'HSDV562', 'J.D. Salinger', ' Little, Brown and Company', 10, 4, 8, 1, '2023-12-17 13:24:11', '2023-12-17 13:24:11'),
(10, 'Harry Potter and the Philosopher\'s Stone\" (or \"Harry Potter and the Sorcerer\'s Stone\"', 'HDWF647', 'J.K. Rowling', ' Bloomsbury (UK), Scholastic (US)', 9, 3, 4, 1, '2023-12-17 13:25:02', '2023-12-17 13:25:02');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `cat_id` int(11) NOT NULL,
  `cat_name` varchar(50) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`cat_id`, `cat_name`, `date_created`, `date_updated`) VALUES
(4, 'History', '2023-12-16 11:51:01', '2023-12-16 11:51:01'),
(6, 'Literature', '2023-12-16 11:51:18', '2023-12-16 11:51:18'),
(8, 'Romance', '2023-12-16 14:01:54', '2023-12-16 14:01:54'),
(9, 'Fantasy', '2023-12-17 13:19:08', '2023-12-17 13:19:08'),
(10, 'Science Fiction', '2023-12-17 13:19:16', '2023-12-17 13:19:16'),
(11, 'Thriller', '2023-12-17 13:19:27', '2023-12-17 13:19:27'),
(12, 'Mathematics', '2023-12-17 13:19:36', '2023-12-17 13:19:36'),
(13, 'Science', '2023-12-17 13:19:43', '2023-12-17 13:19:43');

-- --------------------------------------------------------

--
-- Table structure for table `issued_books`
--

CREATE TABLE `issued_books` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `number_id` varchar(20) NOT NULL,
  `fullname` varchar(50) NOT NULL,
  `expected_date` date NOT NULL,
  `status` int(11) NOT NULL DEFAULT 1 COMMENT '1 = Not Returned, 2 = Returned, 3 = Overdue',
  `date_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `issued_books`
--

INSERT INTO `issued_books` (`id`, `book_id`, `number_id`, `fullname`, `expected_date`, `status`, `date_created`, `date_updated`) VALUES
(1, 5, '20-UR-1110', 'Chrissha Mae Espenueva Balbin', '2023-12-01', 2, '2023-12-30 15:34:15', '2023-12-16 16:45:09'),
(3, 1, '20-UR-1111', 'Marlon Castillo', '2023-12-23', 2, '2023-12-16 16:46:25', '2023-12-16 16:46:32'),
(4, 5, '20-UR-1111', 'Marlon Castillo', '2023-12-09', 1, '2023-12-16 16:47:59', '2023-12-16 16:47:59'),
(5, 8, '20-UR-1111', 'Marlon Castillo', '2023-12-18', 1, '2023-12-19 12:29:35', '2023-12-19 12:29:35'),
(6, 9, '20-UR-1150', 'Jomary Davalos', '2023-12-22', 1, '2023-12-19 12:30:14', '2023-12-19 12:30:14'),
(7, 8, '20-UR-1112', 'Nicole Castillo', '2023-12-20', 1, '2023-12-19 12:31:27', '2023-12-19 12:31:27');

-- --------------------------------------------------------

--
-- Table structure for table `rack`
--

CREATE TABLE `rack` (
  `rack_id` int(11) NOT NULL,
  `rack_name` varchar(50) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rack`
--

INSERT INTO `rack` (`rack_id`, `rack_name`, `date_created`, `date_updated`) VALUES
(1, 'Rack 2', '2023-12-16 12:21:15', '2023-12-16 12:22:27'),
(3, 'Rack 3', '2023-12-16 14:01:14', '2023-12-16 14:01:14'),
(4, 'Rack 4', '2023-12-17 13:19:52', '2023-12-17 13:19:52'),
(5, 'Rack 5', '2023-12-17 13:19:57', '2023-12-17 13:19:57'),
(6, 'Rack 6', '2023-12-17 13:20:03', '2023-12-17 13:20:03');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`) VALUES
(1, 'admin', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`book_id`),
  ADD UNIQUE KEY `isbn` (`isbn`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`cat_id`);

--
-- Indexes for table `issued_books`
--
ALTER TABLE `issued_books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `rack`
--
ALTER TABLE `rack`
  ADD PRIMARY KEY (`rack_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `issued_books`
--
ALTER TABLE `issued_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `rack`
--
ALTER TABLE `rack`
  MODIFY `rack_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
