-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 16, 2022 at 11:07 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `e_commerce`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `CART_ID` int(11) NOT NULL,
  `CUST_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`CART_ID`, `CUST_ID`) VALUES
(1, 10001),
(4, 10016);

-- --------------------------------------------------------

--
-- Table structure for table `cart_products`
--

CREATE TABLE `cart_products` (
  `CP_ID` int(11) NOT NULL,
  `CART_ID` int(11) NOT NULL,
  `P_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `C_ID` int(11) NOT NULL,
  `C_NAME` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`C_ID`, `C_NAME`) VALUES
(1, 'phone'),
(2, 'grocery'),
(3, 'household'),
(4, 'PC'),
(5, 'Beauty'),
(6, 'clothings'),
(7, 'footwears'),
(8, 'Watches'),
(9, 'va'),
(10, 'electronics');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `CUST_ID` int(11) NOT NULL,
  `F_NAME` varchar(50) NOT NULL,
  `L_NAME` varchar(50) NOT NULL,
  `ADDRESS` text NOT NULL,
  `PH_NO` bigint(20) NOT NULL,
  `E_MAIL` varchar(50) NOT NULL,
  `GENDER` varchar(10) NOT NULL,
  `USERNAME` varchar(50) NOT NULL,
  `PASSWORD` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CUST_ID`, `F_NAME`, `L_NAME`, `ADDRESS`, `PH_NO`, `E_MAIL`, `GENDER`, `USERNAME`, `PASSWORD`) VALUES
(10001, 'fname', 'lname', 'Example house\r\ntemp city\r\ntest street', 1111111111, 'email@gmail.com', 'male', 'username', 'password'),
(10016, 'test', 'name', 'location', 2222222222, 'test@example.com', 'male', 'usernme', 'asdfghj');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `O_ID` int(11) NOT NULL,
  `CUST_ID` int(11) NOT NULL,
  `S_ID` int(11) NOT NULL,
  `P_ID` int(11) NOT NULL,
  `STATE` varchar(50) NOT NULL,
  `DISTRICT` varchar(50) NOT NULL,
  `CITY` varchar(50) NOT NULL,
  `STREET` varchar(50) NOT NULL,
  `PIN_CODE` int(6) NOT NULL,
  `DATE` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `P_ID` int(11) NOT NULL,
  `P_NAME` varchar(50) NOT NULL,
  `COST` double NOT NULL,
  `COUNT` int(11) NOT NULL,
  `S_ID` int(11) NOT NULL,
  `C_ID` int(11) NOT NULL,
  `P_IMG` varchar(100) NOT NULL,
  `P_DESC` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`P_ID`, `P_NAME`, `COST`, `COUNT`, `S_ID`, `C_ID`, `P_IMG`, `P_DESC`) VALUES
(18, 'Asus Laptop', 454544534, 5, 101, 1, 'psw', 'adsfsfdgsfgsfdg'),
(19, 'REDMI', 4254524, 52, 101, 1, '2020-10-20 (12).png', 'iuhipu9'),
(20, 'REDMI', 4534534534, 5, 101, 1, '2020-10-20 (22).png', 'Note 9 Pro Max'),
(22, 'REDMI', 6486453678, 65, 101, 1, '2020-10-20 (21).png', 'Note 9 Pro Max');

-- --------------------------------------------------------

--
-- Table structure for table `product_delivery`
--

CREATE TABLE `product_delivery` (
  `DEL_ID` int(11) NOT NULL,
  `DEL_ADDRESS` text NOT NULL,
  `P_ID` int(11) NOT NULL,
  `S_ID` int(11) NOT NULL,
  `CUST_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `seller`
--

CREATE TABLE `seller` (
  `S_ID` int(11) NOT NULL,
  `F_NAME` varchar(50) NOT NULL,
  `L_NAME` varchar(30) NOT NULL,
  `S_ADDRESS` text NOT NULL,
  `PH_NO` int(11) NOT NULL,
  `E_MAIL` varchar(50) NOT NULL,
  `GENDER` varchar(8) NOT NULL,
  `USERNAME` varchar(20) NOT NULL,
  `PASSWORD` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `seller`
--

INSERT INTO `seller` (`S_ID`, `F_NAME`, `L_NAME`, `S_ADDRESS`, `PH_NO`, `E_MAIL`, `GENDER`, `USERNAME`, `PASSWORD`) VALUES
(101, 'temp', 'lname', 'abcd house\r\nefgh village', 1111111111, 'email@gmail.com', 'male', 'username', 'password'),
(102, 'test', 'name', 'location', 2147483647, 'test@example.com', 'male', 'pudar', 'password');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `T_ID` int(11) NOT NULL,
  `AMOUNT` double NOT NULL,
  `STATUS` varchar(20) NOT NULL,
  `P_ID` int(11) NOT NULL,
  `CUST_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`CART_ID`,`CUST_ID`),
  ADD KEY `CUST_ID` (`CUST_ID`);

--
-- Indexes for table `cart_products`
--
ALTER TABLE `cart_products`
  ADD PRIMARY KEY (`CP_ID`),
  ADD KEY `CART_ID` (`CART_ID`),
  ADD KEY `P_ID` (`P_ID`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`C_ID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CUST_ID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`O_ID`),
  ADD KEY `P_ID` (`P_ID`),
  ADD KEY `CUST_ID` (`CUST_ID`),
  ADD KEY `S_ID` (`S_ID`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`P_ID`),
  ADD KEY `S_ID` (`S_ID`),
  ADD KEY `C_ID` (`C_ID`);

--
-- Indexes for table `product_delivery`
--
ALTER TABLE `product_delivery`
  ADD PRIMARY KEY (`DEL_ID`),
  ADD KEY `P_ID` (`P_ID`),
  ADD KEY `S_ID` (`S_ID`),
  ADD KEY `CUST_ID` (`CUST_ID`);

--
-- Indexes for table `seller`
--
ALTER TABLE `seller`
  ADD PRIMARY KEY (`S_ID`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`T_ID`),
  ADD KEY `CUST_ID` (`CUST_ID`),
  ADD KEY `P_ID` (`P_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `CART_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cart_products`
--
ALTER TABLE `cart_products`
  MODIFY `CP_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `C_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `CUST_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10018;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `O_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `P_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `product_delivery`
--
ALTER TABLE `product_delivery`
  MODIFY `DEL_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `seller`
--
ALTER TABLE `seller`
  MODIFY `S_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `T_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`CUST_ID`) REFERENCES `customer` (`CUST_ID`);

--
-- Constraints for table `cart_products`
--
ALTER TABLE `cart_products`
  ADD CONSTRAINT `cart_products_ibfk_1` FOREIGN KEY (`CART_ID`) REFERENCES `cart` (`CART_ID`),
  ADD CONSTRAINT `cart_products_ibfk_2` FOREIGN KEY (`P_ID`) REFERENCES `products` (`P_ID`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `products` (`P_ID`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`CUST_ID`) REFERENCES `customer` (`CUST_ID`),
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`S_ID`) REFERENCES `seller` (`S_ID`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`S_ID`) REFERENCES `seller` (`S_ID`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`C_ID`) REFERENCES `category` (`C_ID`);

--
-- Constraints for table `product_delivery`
--
ALTER TABLE `product_delivery`
  ADD CONSTRAINT `product_delivery_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `products` (`P_ID`),
  ADD CONSTRAINT `product_delivery_ibfk_2` FOREIGN KEY (`S_ID`) REFERENCES `seller` (`S_ID`),
  ADD CONSTRAINT `product_delivery_ibfk_3` FOREIGN KEY (`CUST_ID`) REFERENCES `customer` (`CUST_ID`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`CUST_ID`) REFERENCES `customer` (`CUST_ID`),
  ADD CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`P_ID`) REFERENCES `products` (`P_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
