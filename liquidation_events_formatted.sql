CREATE OR REPLACE TABLE 
`ajay-blockchain-projects.aave_decoded.liquidation_events_formatted` as

SELECT
  l.block_timestamp,
  l.transaction_hash,
  l.borrower,
  l.liquidator,

  -- Collateral asset details
  c.symbol   AS collateral_symbol,
  c.name     AS collateral_name,
  c.decimals AS collateral_decimals,

  -- Debt asset details
  d.symbol   AS debt_symbol,
  d.name     AS debt_name,
  d.decimals AS debt_decimals,
  receive_atoken, 

  -- Raw amounts (divide by decimals to get human-readable)
  CAST(l.debt_to_cover AS NUMERIC) / POW(10, CAST(d.decimals AS INT64))             AS debt_to_cover_token,
  CAST(l.liquidated_collateral_amt AS NUMERIC) / POW(10, CAST(c.decimals AS INT64)) AS collateral_amount_token

FROM `ajay-blockchain-projects.aave_decoded.liquidation_events` l
LEFT JOIN `bigquery-public-data.crypto_ethereum.amended_tokens` c
  ON LOWER(l.collateral_asset) = LOWER(c.address)
LEFT JOIN `bigquery-public-data.crypto_ethereum.amended_tokens` d
  ON LOWER(l.debt_asset) = LOWER(d.address) 
