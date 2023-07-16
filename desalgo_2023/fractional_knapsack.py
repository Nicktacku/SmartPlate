def calculate(limit, meals):
    ratio = {}
    knapsack = []
    recommended = None
    food_to_fit = None

    for key in meals:
        ratio[key] = meals[key]["nutriscore"] * meals[key]["calories"]

    sorted_ratio = dict(sorted(ratio.items(), key=lambda x: x[1]))
    print(sorted_ratio.keys())

    for i in sorted_ratio.keys():
        print("sorted: ", sorted_ratio[i])
        limit -= int(sorted_ratio[i])

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
