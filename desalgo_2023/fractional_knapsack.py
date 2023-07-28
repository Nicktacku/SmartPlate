def calculate(limit, meals, type):
    ratio = {}
    knapsack = []
    remaining_limit = limit
    recommended = 0
    food_to_fit = None

    # type should be string of the profit (example "nutriscore" or "sugar")
    for key in meals:
        ratio[key] = meals[key][type] * meals[key]["calories"]

    sorted_ratio = dict(sorted(ratio.items(), key=lambda x: x[1]))
    print("sorted ratio: ", sorted_ratio.keys())
    print()

    for i in sorted_ratio.keys():
        print("sorted item: ", meals[i]["calories"])
        limit -= int(meals[i]["calories"])

        if limit == 0:
            break
        elif limit < 0:
            fractional_ratio = remaining_limit / meals[key]["calories"]
            recommended = (1 - fractional_ratio) * meals[key]["grams"]
            print(f"ratio %: {(fractional_ratio * 100):.2f}")
            food_to_fit = i
            print("food that may fit: ", food_to_fit)
            break

        print("included: ", i)
        print("limit: ", limit)
        print()
        remaining_limit -= int(meals[i]["calories"])
        knapsack.append(i)

    return [knapsack, recommended, food_to_fit]
