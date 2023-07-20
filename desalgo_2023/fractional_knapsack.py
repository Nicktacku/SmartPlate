def calculate(limit, meals, type):
    ratio = {}
    knapsack = []
    recommended = 0
    food_to_fit = None

    # type should be string of the profit (example "nutriscore" or "sugar")
    for key in meals:
        ratio[key] = meals[key][type] * meals[key]["calories"]

    sorted_ratio = dict(sorted(ratio.items(), key=lambda x: x[1]))
    print(sorted_ratio.keys())

    for i in sorted_ratio.keys():
        print("sorted: ", meals[i]["calories"])
        limit -= int(meals[i]["calories"])

        if limit == 0:
            break
        elif limit < 0:
            fractional_ratio = min(limit, meals[key]["calories"]) / max(
                limit, meals[key]["calories"]
            )
            print("ratio", fractional_ratio)
            recommended = 1 - abs(fractional_ratio)
            food_to_fit = i
            break

        knapsack.append(i)

    return [knapsack, abs(recommended), food_to_fit]
