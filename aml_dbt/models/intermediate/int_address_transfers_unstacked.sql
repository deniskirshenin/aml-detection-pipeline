{{ config(materialized='view') }}

with transfers as (
    select
        *
    from {{ ref('stg_transfers') }}
)

select block_num,
       hash,
       from_address as address,
       to_address as counterparty_address,
       value,
       asset,
       category,
       'OUTGOING' as direction
from transfers

union all

select block_num,
       hash,
       from_address as address,
       to_address as counterparty_address,
       value,
       asset,
       category,
       'INCOMING' as direction  
from transfers