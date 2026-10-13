{{ config( materialized='table' ) }}

with unstacked as (
    select * from {{ ref('int_address_transfers_unstacked') }}
)

select
    address,
    count(distinct hash) as num_transfers,
    count(distinct case when direction = 'INCOMING' then hash end) as num_incoming_transfers,
    coalesce(sum(case when direction = 'INCOMING' then value end), 0) as total_incoming_value,
    count(distinct case when direction = 'OUTGOING' then hash end) as num_outgoing_transfers,
    coalesce(sum(case when direction = 'OUTGOING' then value end), 0) as total_outgoing_value,
    count(distinct counterparty_address) as num_counterparties,
    min(block_num) as first_transfer_block,
    max(block_num) as last_transfer_block
from unstacked
group by 1