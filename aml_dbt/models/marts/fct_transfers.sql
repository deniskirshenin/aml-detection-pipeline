{{ config (materialized='table') }}

with staging as (
    select * from {{ ref('stg_transfers') }}
)

select 
    block_num,
    hash,
    from_address,
    to_address,
    value,
    asset,
    category,
    case when value >= 100 then true else false end as is_large_transfer 
from staging