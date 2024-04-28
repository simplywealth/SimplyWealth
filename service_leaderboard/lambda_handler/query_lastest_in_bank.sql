with temp as (
select 
	user_id, 
    amount,
	row_number() over (partition by user_id order by timestamp desc) as trans_num
from SimplyWealthApp_transaction
)

select * from temp
where trans_num = 1
