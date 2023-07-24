def nutriscore_conversion(nutriscore):
    if nutriscore < 0:
        return "A"
    elif nutriscore >= 0 and nutriscore <= 2:
        return "B"
    elif nutriscore >= 3 and nutriscore <= 10:
        return "C"
    elif nutriscore >= 11 and nutriscore <= 18:
        return "D"
    elif nutriscore >= 19:
        return "E"


def bad_point_compute(bp):
    # conversion of calorie
    if bp[0] <= 335:
        bp[0] = 0
    elif bp[0] > 335 and bp[0] <= 670:
        bp[0] = 1
    elif bp[0] > 670 and bp[0] <= 1005:
        bp[0] = 2
    elif bp[0] > 1005 and bp[0] <= 1340:
        bp[0] = 3
    elif bp[0] > 1340 and bp[0] <= 1675:
        bp[0] = 4
    elif bp[0] > 1675 and bp[0] <= 2010:
        bp[0] = 5
    elif bp[0] > 2010 and bp[0] <= 2345:
        bp[0] = 6
    elif bp[0] > 2345 and bp[0] <= 2680:
        bp[0] = 7
    elif bp[0] > 2680 and bp[0] <= 3015:
        bp[0] = 8
    elif bp[0] > 3015 and bp[0] <= 3350:
        bp[0] = 9
    elif bp[0] > 3350:
        bp[0] = 10

    # sugar
    if bp[1] <= 4.5:
        bp[1] = 0
    elif bp[1] > 4.5 and bp[1] <= 9:
        bp[1] = 1
    elif bp[1] > 9 and bp[1] <= 13.5:
        bp[1] = 2
    elif bp[1] > 13.5 and bp[1] <= 18:
        bp[1] = 3
    elif bp[1] > 18 and bp[1] <= 22.5:
        bp[1] = 4
    elif bp[1] > 22.5 and bp[1] <= 27:
        bp[1] = 5
    elif bp[1] > 27 and bp[1] <= 31:
        bp[1] = 6
    elif bp[1] > 31 and bp[1] <= 36:
        bp[1] = 7
    elif bp[1] > 36 and bp[1] <= 40:
        bp[1] = 8
    elif bp[1] > 40 and bp[1] <= 45:
        bp[1] = 9
    elif bp[1] > 45:
        bp[1] = 10

    # saturated_fat
    if bp[2] <= 1:
        bp[2] = 0
    elif bp[2] > 1 and bp[2] <= 2:
        bp[2] = 1
    elif bp[2] > 2 and bp[2] <= 3:
        bp[2] = 2
    elif bp[2] > 3 and bp[2] <= 4:
        bp[2] = 3
    elif bp[2] > 4 and bp[2] <= 5:
        bp[2] = 4
    elif bp[2] > 5 and bp[2] <= 6:
        bp[2] = 5
    elif bp[2] > 6 and bp[2] <= 7:
        bp[2] = 6
    elif bp[2] > 7 and bp[2] <= 8:
        bp[2] = 7
    elif bp[2] > 8 and bp[2] <= 9:
        bp[2] = 8
    elif bp[2] > 9 and bp[2] <= 10:
        bp[2] = 9
    elif bp[2] > 10:
        bp[2] = 10

    # sodium
    if bp[3] <= 90:
        bp[3] = 0
    elif bp[3] > 90 and bp[3] <= 180:
        bp[3] = 1
    elif bp[3] > 180 and bp[3] <= 270:
        bp[3] = 2
    elif bp[3] > 270 and bp[3] <= 360:
        bp[3] = 3
    elif bp[3] > 360 and bp[3] <= 450:
        bp[3] = 4
    elif bp[3] > 450 and bp[3] <= 540:
        bp[3] = 5
    elif bp[3] > 540 and bp[3] <= 630:
        bp[3] = 6
    elif bp[3] > 630 and bp[3] <= 720:
        bp[3] = 7
    elif bp[3] > 720 and bp[3] <= 810:
        bp[3] = 8
    elif bp[3] > 810 and bp[3] <= 900:
        bp[3] = 9
    elif bp[3] > 900:
        bp[3] = 10

    return sum(bp)


def good_point_compute(gp):
    # fibre
    if gp[0] <= 0.7:
        gp[0] = 0
    elif gp[0] > 0.7 and gp[0] <= 1.4:
        gp[0] = 1
    elif gp[0] > 1.4 and gp[0] <= 2.1:
        gp[0] = 2
    elif gp[0] > 2.1 and gp[0] <= 2.8:
        gp[0] = 3
    elif gp[0] > 2.8 and gp[0] <= 3.5:
        gp[0] = 4
    elif gp[0] > 3.5:
        gp[0] = 5

    # fibre
    if gp[1] <= 1.6:
        gp[1] = 0
    elif gp[1] > 1.6 and gp[1] <= 3.2:
        gp[1] = 1
    elif gp[1] > 3.2 and gp[1] <= 4.8:
        gp[1] = 2
    elif gp[1] > 4.8 and gp[1] <= 6.4:
        gp[1] = 3
    elif gp[1] > 6.4 and gp[1] <= 8.0:
        gp[1] = 4
    elif gp[1] > 8.0:
        gp[1] = 5

    return gp

# get_nutriscore
def calculate(nutrients):
    nutrient_values = []

    # convert calorie into 100 g
    nutrient_values.append(nutrients["grams"])

    # bad nutrients
    nutrient_values.append(nutrients["calories"])
    nutrient_values.append(nutrients["sugar"])
    nutrient_values.append(nutrients["saturated_fat"])
    nutrient_values.append(nutrients["sodium"])

    # good nutrients
    nutrient_values.append(nutrients["fiber"])
    nutrient_values.append(nutrients["protein"])

    nutrient_convert_ratio = 100 / nutrients["grams"]
    converted_calorie = (int(nutrients["calories"] * 4.184)) * nutrient_convert_ratio
    nutrient_values[1] = converted_calorie

    for i, nutrient in enumerate(nutrient_values[2:]):
        nutrient_values[i + 2] = nutrient * nutrient_convert_ratio

    nutriscore = 0
    bad_points = bad_point_compute(nutrient_values[1:5])
    good_points = good_point_compute(nutrient_values[5:7])

    # apply nutriscore
    if bad_points >= 11:
        nutriscore = bad_points - good_points[0]
    elif bad_points < 11:
        nutriscore = bad_points - sum(good_points)

    return nutriscore
