# src/decoder.py

from eth_abi import decode
from web3 import Web3

AAVE_V2_LENDING_POOL = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
LIQUIDATION_CALL_SIG  = '0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286'

def decode_liquidation_call(row):
    """
    Decodes a raw Aave V2 LiquidationCall event log row.
    Input:  a dict/Series with keys: block_timestamp, block_number,
            transaction_hash, topics (list), data (hex string)
    Output: decoded dict with human-readable fields, or None if decode fails
    """
    try:
        collateral_asset = '0x' + row['topics'][1][-40:]
        debt_asset       = '0x' + row['topics'][2][-40:]
        borrower         = '0x' + row['topics'][3][-40:]

        data_bytes = bytes.fromhex(row['data'][2:])
        decoded = decode(
            ['uint256', 'uint256', 'address', 'bool'],
            data_bytes
        )

        return {
            'block_timestamp':              row['block_timestamp'],
            'block_number':                 row['block_number'],
            'transaction_hash':             row['transaction_hash'],
            'collateral_asset':             Web3.to_checksum_address(collateral_asset),
            'debt_asset':                   Web3.to_checksum_address(debt_asset),
            'borrower':                     Web3.to_checksum_address(borrower),
            'debt_to_cover':                str(decoded[0]),
            'liquidated_collateral_amount': str(decoded[1]),
            'liquidator':                   decoded[2],
            'receive_atoken':               decoded[3]
        }
    except Exception:
        return None


def decode_all(df_raw):
    """
    Runs decode_liquidation_call on every row of a raw logs dataframe.
    Returns a cleaned dataframe of successfully decoded rows.
    """
    import pandas as pd
    decoded_rows = [decode_liquidation_call(row) for _, row in df_raw.iterrows()]
    return pd.DataFrame([r for r in decoded_rows if r is not None])
