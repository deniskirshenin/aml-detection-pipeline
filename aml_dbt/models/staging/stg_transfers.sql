with source as (
    select
        *
    from {{ source('raw', 'raw_alchemy_transfers') }}
),

cleaned as (
    select
        blockNum::int as block_num,
        hash,
        fromAddress as from_address,
        toAddress as to_address,
        try_cast(value as double) as value,
        asset,
        category
    from source
)

select * from cleaned