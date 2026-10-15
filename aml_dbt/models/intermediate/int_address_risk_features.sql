{{ config(materialized='table') }}

with unstacked as (
    select * from {{ ref('int_address_transfers_unstacked') }}
),

address_stats as (
    select
        address,
        count(distinct hash) as num_transfers,
        count(distinct counterparty_address) as num_counterparties,
        avg(value) as avg_transfer_value,
        max(value) as max_transfer_value,
        sum(value) as total_transfer_value,
        min(block_num) as first_transfer_block,
        max(block_num) as last_transfer_block,
        (max(block_num) - min(block_num)) as transfer_block_span
    from unstacked
    group by 1
)

select 
    address,
    num_transfers,
    num_counterparties,
    avg_transfer_value,
    max_transfer_value,
    total_transfer_value,
    transfer_block_span,
    first_transfer_block,
    last_transfer_block,
    case
        when transfer_block_span < 20 and num_transfers > 10 then true
        else false
    end as is_high_velocity_burst,

    case
        when max_transfer_value > (avg_transfer_value * 15) and num_transfers > 5 then true
        else false
    end as is_potential_structuring
from address_stats