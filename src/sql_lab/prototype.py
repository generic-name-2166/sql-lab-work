
# This was created to prototype the SQL
"""
if __name__ == "__main__":
	table = pd.DataFrame(...)
	table1 = table[table['success_order_flg'] == True].sort_values(by="order_time")
	table1["prev_order_time"] = pd.Series(0, index=table1.index)

	user_start = dict()
	days = set()
	for index in table1.index:
		user = table1[index, "user_id"]
		ts = table1[index, "order_time"]
		date = datetime.fromtimestamp(ts)
		day = f"{date.year}-{date.month}-{date.day}"
		days.add(day)

		if user not in user_start.keys():
			user_start[user] = dict()
			user_start[user]["new"] = day
			user_start[user]["total_since_new"] = table1[index, "order_cost"]
			table1[index, "prev_order_time"] = pd.NA
		else:
			if ts - table1[index, "prev_order_time"] >= 7_776_000:
				if user_start.get("reactivated"):
					user_start["reactivated"].append(day)
					user_start["total_since_reactivated"].append(0)
				else:
					user_start["reactivated"] = [day]
					user_start["total_since_reactivated"] = [0]
			table1[index, "prev_order_time"] = ts

			new_order_cost = table1[index, "order_cost"]
			user_start[user]["total_since_new"] += new_order_cost
			if user_start[user].get("reactivated"):
				for i in range(len(user_start[user]["total_since_reactivated"])):
					user_start[user]["total_since_reactivated"][i] += new_order_cost
	
	final_dict = dict()
	for day in tuple(days):
		final_dict[day] = {
			"new_count": 0, 
			"new_total_cost": 0,
			"reactivated_count": 0,
			"reactivated_total_cost": 0
			}
		for user, user_dict in user_start.items():
			if user_dict["new"] == day:
				final_dict[day]["new_total_count"] += user_dict["total_since_new"]
				final_dict[day]["new_count"] += 1
				break
			elif user_dict.get("reactivated"):
				for i, day_reactivated in enumerate(user_dict["reactivated"]):
					if day_reactivated == day:
						final_dict[day]["reactivated_total_count"] += user_dict["total_since_reactivated"][i]
						final_dict[day]["reactivated_count"] += 1
						break
"""
				