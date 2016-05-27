#!/usr/bin/python

# -*- coding: utf-8 -*-

"""
    biilaoelectricitybillcalculator

    author: bii811

    (C) 2016 Bii811

"""

import locale

###################
# GLOBAL VARIABLE #
###################

TAX = 10/100    # Tax 10%
RANGE_PER_LEVEL = [25, 150]     # 0-25; 26-150; >150
COST_PER_LEVEL = [348, 414, 999]    # Currency LAK, per KWH
RENT_COST_PER_TYPE_DICT = {
    '1 Phase 3/9A': 1400,
    '1 Phase 5/40A': 4200,
    '1 Phase 5/80A': 5200,
    '3 Phase direct': 14000,
    '3 Phase via 0.4 kV CT': 84400,
    '3 Phase via 22 kV PT & CT': 84400,
    '3 Phase via 115 kV PT & CT': 84400,
    'AMR via 22 kV PT & CT': 125300,
    'AMR via 115 kV PT & CT': 125300
}   # Electricity Meter Type with rent cost in LAK
TYPE_SELECTED = 2   # Select 3 Phase Direct


def calculate_bill(prev, curr):
    usage = curr - prev
    usage_per_level = []

    if usage <= RANGE_PER_LEVEL[0]:
        usage_per_level.append(usage)
    else:
        usage_per_level.append(RANGE_PER_LEVEL[0])
        if usage < RANGE_PER_LEVEL[1]:
            usage_per_level.append(usage - usage_per_level[0])
        else:
            usage_per_level.append(RANGE_PER_LEVEL[1] - RANGE_PER_LEVEL[0])
            usage_per_level.append(usage - usage_per_level[0] - usage_per_level[1])

    cost = 0
    for i, u in enumerate(usage_per_level):
        cost += u * COST_PER_LEVEL[i]

    cost += sorted(list(RENT_COST_PER_TYPE_DICT.values()))[TYPE_SELECTED]

    taxed = cost * TAX
    total_cost = cost + taxed

    return usage_per_level, taxed, total_cost


if __name__ == '__main__':
    print(
        """
        ##############################
        # Domestic Electricity Meter #
        ##############################
        """
    )
    previous = int(input('Previous Meter Reading: '))
    current = int(input('Current Meter Reading: '))
    result = calculate_bill(previous, current)
    locale.setlocale(locale.LC_ALL, '')
    print("Usage: {}".format(result[0]))
    print("Tax: {} LAK".format(str(locale.format("%d", result[1], grouping=True))))
    print("Total Bill: {} LAK".format(str(locale.format("%d", result[2], grouping=True))))
