--
-- Create model Stocks
--
CREATE TABLE `SimplyWealthApp_stocks` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `tick_symbol` varchar(5) NOT NULL, `market_value` numeric(10, 2) NOT NULL);
;

