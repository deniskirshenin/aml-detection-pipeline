{{ config(materialized='table') }}

with summary as (
    select * from {{ ref('int_address_summary') }}
),

risk_features as (
    select * from {{ ref('int_address_risk_features') }}
)

select
    s.address,
    s.num_transfers,
    s.num_outgoing_transfers,
    s.total_outgoing_value,
    s.num_incoming_transfers,
    s.total_incoming_value,
    s.num_counterparties,
    s.total_incoming_value - s.total_outgoing_value as net_flow,
    coalesce(rf.is_high_velocity_burst, false) as is_high_velocity_burst,
    coalesce(rf.is_potential_structuring, false) as is_potential_structuring,
    case 
        when s.total_incoming_value > 1000
        and abs(s.total_incoming_value - s.total_outgoing_value) < (total_incoming_value * 0.01)
        then true
        else false
    end as is_pass_through_mixer_node,
    (
        case when s.num_counterparties <= 2 and s.num_transfers > 15 then 25 else 0 end +
        case when coalesce(rf.is_high_velocity_burst, false) then 25 else 0 end +
        case when coalesce(rf.is_potential_structuring, false) then 25 else 0 end +
        case when (s.total_incoming_value > 1000
            and abs(s.total_incoming_value - s.total_outgoing_value) < (total_incoming_value * 0.01)) then 25 else 0 end
    ) as aml_risk_score,
    case
        when aml_risk_score >= 75 then 'High'
        when aml_risk_score >= 50 then 'Medium'
        when aml_risk_score >= 25 then 'Low'
        else 'None'
    end as aml_risk_level,
    rf.first_transfer_block,
    rf.last_transfer_block
from summary s
left join risk_features rf on s.address = rf.address
