def calculate(limit, meals):
    limit
    ratio = {}
    knapsack = []

    for key in meals:
        ratio[key] = meals[key]["nutriscore"] * meals[key]["calories"]

    sorted_ratio = dict(sorted(ratio.items(), key=lambda x: x[1]))
    print(sorted_ratio.keys())
    for i in sorted_ratio.keys():
        print("sorted: ", sorted_ratio[i])
        limit -= int(sorted_ratio[i])

        if limit <= 0:
            break

        knapsack.append(i)

    return knapsack
