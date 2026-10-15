{{ config(materialized='table') }}

with addresses as (
    select * from {{ ref('dim_addresses_enriched') }}
    where aml_risk_level in ('High', 'Medium')
),

transfers as (
    select * from {{ ref('fct_transfers') }}
)

select
    t.hash,
    t.block_num,
    t.from_address,
    t.to_address,
    t.asset,
    t.value,

    case
        when a_from.aml_risk_level = 'High' or a_to.aml_risk_level = 'High' then 'High'
        else 'Medium'
    end as alert_severity
from transfers t
left join addresses a_from on t.from_address = a_from.address
left join addresses a_to on t.to_address = a_to.address  