# Aave V2 Liquidation Pipeline
> Raw EVM event log decoding → BigQuery analytics 

---

## Overview

This project reconstructs **Aave V2 LiquidationCall events** directly from raw Ethereum event logs stored in BigQuery's public `crypto_ethereum` dataset — without any third-party indexer, RPC endpoint, or Dune Analytics.

The pipeline decodes raw on-chain data using Python ABI decoding (`eth_abi`), writes structured output back to BigQuery, and builds aggregated analytical tables on top for protocol-level insights.

NOTE: Because of Bigquery free tier querying limitation, The period for which the Blockchain data considered is H1 2025.

---

## Architecture

```
bigquery-public-data.crypto_ethereum.logs
            │
            │  Filter by:
            │  - Aave V2 LendingPool address
            │  - LiquidationCall event signature hash
            │
            ▼
  Python ABI Decoder (Google Colab)
            │
            ▼
  ajay-blockchain-projects.aave_decoded.liquidation_events
            │
            ▼
  BigQuery SQL (Aggregation Layer)
  ├── aave_decoded.liquidation_events_formatted
  └── aave_decoded.wallet_liquidation_history
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Raw Data Source | BigQuery Public Dataset — `crypto_ethereum.logs` |
| ABI Decoding | Python — `eth_abi`, `web3.py` |
| Notebook Environment | Google Colab |
| Data Warehouse | Google BigQuery |
| Token Metadata | BigQuery Public Dataset — `crypto_ethereum.tokens` |
| Version Control | GitHub |

---

## Output Tables

### `aave_decoded.liquidation_events`
One row per liquidation event. Decoded directly from raw EVM event logs.


### `aave_decoded.liquidation_events_formatted`
Token MetaData included events data

### `aave_decoded.wallet_liquidation_history`
Per-wallet liquidation history — useful for risk and compliance analysis.


## How to Run

### Prerequisites
- Google Cloud account with BigQuery enabled
- GCP Service Account with roles: `BigQuery Data Editor` + `BigQuery Job User`
- Service account JSON key downloaded

### Step 1 — Create BigQuery Dataset
In GCP Console → BigQuery → Create Dataset:
```
Dataset ID: aave_decoded
Location:   US (multi-region)
```

### Step 2 — Run the Decoder Notebook
Open `notebooks/aave_liquidation_decoder.ipynb` in Google Colab:
1. Upload your service account JSON key to `/content/`
2. Update the `credentials` file path and `project` ID in Cell 2
3. Run all cells top to bottom

This will:
- Pull raw `LiquidationCall` logs from `bigquery-public-data.crypto_ethereum.logs`
- Decode topics and data fields using ABI
- Join token metadata for human-readable asset names and decimals
- Write decoded rows to `aave_decoded.liquidation_events`

### Step 3 — Run Aggregation SQL
In BigQuery SQL Workspace, run in order:
```
sql/daily_liquidation_summary.sql
sql/wallet_liquidation_history.sql
```


## Why Raw EVM Logs vs RPC / Dune

Rather than using Dune Analytics or an RPC endpoint, this pipeline works directly from raw Ethereum event logs in BigQuery's `crypto_ethereum` public dataset. This mirrors how production blockchain data infrastructure actually works — ingesting raw on-chain data and building structured datasets from scratch.

The ABI decoder reconstructs the `LiquidationCall` event by:
1. Matching `topics[0]` against the keccak256 event signature hash
2. Extracting indexed parameters from `topics[1,2,3]` (addresses zero-padded to 32 bytes)
3. ABI-decoding the `data` field for non-indexed parameters (`uint256`, `address`, `bool`)

This approach gives full control over data freshness, schema design, and historical backfill — none of which are possible when relying on a third-party indexer.

---

## Repo Structure

```
aave-liquidation-pipeline/
├── README.md
├── notebooks/
│   └── aave_liquidation_decoder.ipynb
├── sql/
│   ├── 01_raw_logs_exploration.sql
│   ├── 02_daily_liquidation_summary.sql
│   └── 03_wallet_liquidation_history.sql
├── src/
│   └── decoder.py
└── requirements.txt
```

---

## Contract Reference

| Item | Value |
|---|---|
| Protocol | Aave V2 |
| Contract | LendingPool |
| Address | `0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9` |
| Event | `LiquidationCall` |
| Signature Hash | `0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286` |
| Data Range | 2025-01-01 to 2025-07-01 |

---

## Author

**Ajay Murali** — Data Scientist / Analytics Engineer  
[github.com/ajaymurali1998](https://github.com/ajaymurali1998) · [LinkedIn](https://linkedin.com/in/ajay-murali-304344163) · [Dune](https://dune.com/ajay_murali)
