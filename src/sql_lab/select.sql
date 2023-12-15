WITH UserPurchases AS (
	SELECT 
		user_id,
		order_time,
		order_cost,
		LAG(order_time)
			OVER (PARTITION BY user_id ORDER BY order_time)
			AS prev_order_time
	FROM orders
	WHERE success_order_flg = TRUE
),

UserStatus AS (
	SELECT 
		user_id,
		CASE 
		WHEN prev_order_time IS NULL THEN 'new'
		WHEN order_time - prev_order_time >= 7776000 THEN 'reactivated'
		ELSE NULL
		END AS user_status,
		CASE
		WHEN (prev_order_time IS NULL) OR (order_time - prev_order_time >= 7776000)
			THEN (
				SELECT SUM(up2.order_cost)
				FROM UserPurchases AS up2
				WHERE up2.user_id = up1.user_id 
					AND up2.order_time >= up1.order_time
					AND up2.order_time < up1.order_time + 31104000
			)
		ELSE NULL
		END AS total_since_status,
		CASE 
		WHEN (prev_order_time IS NULL) OR (order_time - prev_order_time >= 7776000)
			THEN DATE_TRUNC('day', to_timestamp(order_time))
			ELSE NULL
		END AS status_since_day
	FROM UserPurchases AS up1
	WHERE (prev_order_time IS NULL) OR (order_time - prev_order_time >= 7776000)
)

SELECT
	status_since_day AS date,
	(
		SELECT SUM(total_since_status)
		FROM UserStatus AS us2
		WHERE (us2.status_since_day = us1.status_since_day) AND (us2.user_status = 'new')
	) as gmv360d_new,
	(
		SELECT SUM(total_since_status)
		FROM UserStatus AS us2
		WHERE (us2.status_since_day = us1.status_since_day) AND (us2.user_status = 'reactivated')
	) as gmv360d_reactivated,
	(
		SELECT COUNT(*)
		FROM UserStatus AS us2
		WHERE (us2.status_since_day = us1.status_since_day) AND (us2.user_status = 'new')
	) as users_count_new,
	(
		SELECT COUNT(*)
		FROM UserStatus AS us2
		WHERE (us2.status_since_day = us1.status_since_day) AND (us2.user_status = 'reactivated')
	) as users_count_reactivated
FROM UserStatus as us1
GROUP BY status_since_day
ORDER BY status_since_day
