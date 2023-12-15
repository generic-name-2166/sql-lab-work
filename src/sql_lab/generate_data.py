import numpy as np


ALPHABET = set("0123456789abcdef")
YEAR_START = 1577836800
YEAR_END = 1609459200 - 1
N = 10_000


def generate_test() -> None:
    return [
        {
            "user_id": "0000000000000001",
            "order_id": "0000000000000001",
            "order_time": 1,
            "order_cost": 10,
            "success_order_flg": True
        },
        {
            "user_id": "0000000000000002",
            "order_id": "0000000000000002",
            "order_time": 1,
            "order_cost": 200,
            "success_order_flg": True
        },
        {
            "user_id": "0000000000000001",
            "order_id": "0000000000000003",
            "order_time": 10_000_000,
            "order_cost": 30,
            "success_order_flg": True
        },
        {
            "user_id": "0000000000000001",
            "order_id": "0000000000000003",
            "order_time": 20_000_000,
            "order_cost": 1000,
            "success_order_flg": True
        },
    ]


def generate_string(rng: np.random.Generator) -> str:
    new_arr = list(ALPHABET)
    rng.shuffle(new_arr)
    return "".join(new_arr)


def generate_users(rng: np.random.Generator, avg: int, total: int) -> list[str]:
    id_num = int(total / avg)
    unique_user_ids = [generate_string(rng) for _ in range(id_num)]
    id_counts = rng.normal(loc=avg, scale=1, size=id_num).round().astype(dtype=np.int_)  # rng.poisson(avg, id_num)

    user_ids = np.repeat(unique_user_ids, id_counts)

    if user_ids.size < total:
        return np.concatenate((user_ids, rng.choice(unique_user_ids, size=(total-user_ids.size))))
    elif user_ids.size > total:
        return user_ids[:total]
    return user_ids


def generate_row(rng: np.random.Generator, user_id: np.str_) -> dict:
    return {
        "user_id": str(user_id),
        "order_id": generate_string(rng),
        "order_time": rng.integers(YEAR_START, YEAR_END, dtype=int),
        "order_cost": rng.uniform(10.0, 100.0),
        "success_order_flg": True if rng.uniform() >= 0.1 else False
    }


def generate_data() -> list[dict]:
    rng = np.random.default_rng()

    USER_OCCURENCE_NUM = 4
    users = generate_users(rng=rng, avg=USER_OCCURENCE_NUM, total=N)
    data = [
        generate_row(rng=rng, user_id=users[i]) for i in range(N)
    ]

    assert np.unique(np.array([x["order_id"] 
                               for x in data])).size == N, "Not unique"
    
    return data


def main():
    data = generate_data()
    print(np.unique(np.array([x["user_id"] for x in data])).size)
    # print([(x[0], type(x[1])) for x in data[0].items()])


if __name__ == "__main__":
    main()
