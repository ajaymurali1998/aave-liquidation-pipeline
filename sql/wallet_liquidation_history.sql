CREATE OR REPLACE TABLE `ajay-blockchain-projects.aave_decoded.wallet_liquidation_history` AS
SELECT
  borrower                    AS wallet_address,
  COUNT(*)                    AS times_liquidated,
  MIN(block_timestamp)        AS first_liquidation,
  MAX(block_timestamp)        AS last_liquidation,
  COUNT(DISTINCT debt_name)  AS distinct_debt_assets
FROM `ajay-blockchain-projects.aave_decoded.liquidation_events_formatted`
GROUP BY 1
ORDER BY 2 DESC
