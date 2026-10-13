{{ config(materialized='table') }}

with address_summary as (
    select * from {{ ref('int_address_summary') }}
)

select
    address,
    num_transfers,
    num_incoming_transfers,
    total_incoming_value,
    num_outgoing_transfers,
    total_outgoing_value,
    num_counterparties,
    first_transfer_block,
    last_transfer_block,
    total_incoming_value - total_outgoing_value as net_flow,
    case when num_transfers > 50 and num_counterparties <= 2 then true else false end as is_suspicious_volume_concentration
from address_summary