l20_l_min = [-1.57, 0, 0, 0, 0, 0, -0.26, -0.26, -0.26, -0.26, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
l20_l_max = [0, 1.57, 1.57, 1.57, 1.57, 1.57, 0.26, 0.26, 0.26, 0.26, 0, 0, 0, 0, 0, 1.57, 1.57, 1.57, 1.57, 1.57]
l20_l_derict = [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1]
l20_r_min = [0, 0, 0, 0, 0, -1.57, -0.26, -0.26, -0.26, -0.26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
l20_r_max = [1.57, 1.57, 1.57, 1.57, 1.57, 0, 0.26, 0.26, 0.26, 0.26, 1, 0, 0, 0, 0, 1.57, 1.57, 1.57, 1.57, 1.57]
l20_r_derict = [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1]

l10_l_min = [-1.45,    0,    0,    0,    0,    0,    0, -0.26, -0.26, -1.01]
l10_l_max = [    0, 1.43, 1.62, 1.62, 1.62, 1.62, 0.26,     0,     0,  0.52]
l10_l_derict = [    0,   -1,   -1,   -1,   -1,   -1,    0,    -1,    -1,     0]


l10_r_min = [   0, -1.43,    0,    0,    0,    0, -0.26,    0,    0, -0.52]
l10_r_max = [0.75,     0, 1.62, 1.62, 1.62, 1.62,     0, 0.13, 0.26,  1.01]
l10_r_derict = [  -1,     0,   -1,   -1,   -1,   -1,    -1,    0,    0,    -1]

def range_to_arc_right(hand_range_r):
    hand_arc_r = [0] * 20
    for i in range(20):
        if 11 <= i <= 14: continue
        val_r = is_within_range(hand_range_r[i], 0, 255)
        if l20_r_derict[i] == -1:
            hand_arc_r[i] = scale_value(val_r, 0, 255, l20_r_max[i], l20_r_min[i])
        else:
            hand_arc_r[i] = scale_value(val_r, 0, 255, l20_r_min[i], l20_r_max[i])
    return hand_arc_r


def range_to_arc_left(hand_range_l):
    hand_arc_l = [0] * 20
    for i in range(20):
        if 11 <= i <= 14: continue
        val_l = is_within_range(hand_range_l[i], 0, 255)
        if l20_l_derict[i] == -1:
            hand_arc_l[i] = scale_value(val_l, 0, 255, l20_l_max[i], l20_l_min[i])
        else:
            hand_arc_l[i] = scale_value(val_l, 0, 255, l20_l_min[i], l20_l_max[i])
    return hand_arc_l


def arc_to_range_right(hand_arc_r):
    hand_range_r = [0] * 20
    for i in range(20):
        if 11 <= i <= 14: continue
        val_r = is_within_range(hand_arc_r[i], l20_r_min[i], l20_r_max[i])
        if l20_r_derict[i] == -1:
            hand_range_r[i] = scale_value(val_r, l20_r_min[i], l20_r_max[i], 255, 0)
        else:
            hand_range_r[i] = scale_value(val_r, l20_r_min[i], l20_r_max[i], 0, 255)
    return hand_range_r


def arc_to_range_left(hand_arc_l):
    hand_range_l = [0] * 20
    for i in range(20):
        if 11 <= i <= 14: continue
        val_l = is_within_range(hand_arc_l[i], l20_l_min[i], l20_l_max[i])
        if l20_l_derict[i] == -1:
            hand_range_l[i] = scale_value(val_l, l20_l_min[i], l20_l_max[i], 255, 0)
        else:
            hand_range_l[i] = scale_value(val_l, l20_l_min[i], l20_l_max[i], 0, 255)

    return hand_range_l


def range_to_arc_right_10(hand_range_r):
    hand_arc_r = [0] * 10
    for i in range(10):
        val_r = is_within_range(hand_range_r[i], 0, 255)
        if l10_r_derict[i] == -1:
            hand_arc_r[i] = scale_value(val_r, 0, 255, l10_r_max[i], l10_r_min[i])
        else:
            hand_arc_r[i] = scale_value(val_r, 0, 255, l10_r_min[i], l10_r_max[i])

    return hand_arc_r


def range_to_arc_left_10(hand_range_l):
    hand_arc_l = [0] * 10
    for i in range(10):
        val_l = is_within_range(hand_range_l[i], 0, 255)
        if l10_l_derict[i] == -1:
            hand_arc_l[i] = scale_value(val_l, 0, 255, l10_l_max[i], l10_l_min[i])
        else:
            hand_arc_l[i] = scale_value(val_l, 0, 255, l10_l_min[i], l10_l_max[i])
    return hand_arc_l


def arc_to_range_right_10(hand_arc_r):
    hand_range_r = [0] * 10
    for i in range(10):
        val_r = is_within_range(hand_arc_r[i], l10_r_min[i], l10_r_max[i])
        if l10_r_derict[i] == -1:
            hand_range_r[i] = scale_value(val_r, l10_r_min[i], l10_r_max[i], 255, 0)
        else:
            hand_range_r[i] = scale_value(val_r, l10_r_min[i], l10_r_max[i], 0, 255)
    return hand_range_r


def arc_to_range_left_10(hand_arc_l):
    hand_range_l = [0] * 10
    for i in range(10):
        val_l = is_within_range(hand_arc_l[i], l10_l_min[i], l10_l_max[i])
        if l10_l_derict[i] == -1:
            hand_range_l[i] = scale_value(val_l, l10_l_min[i], l10_l_max[i], 255, 0)
        else:
            hand_range_l[i] = scale_value(val_l, l10_l_min[i], l10_l_max[i], 0, 255)

    return hand_range_l


def scale_value(original_value, a_min, a_max, b_min, b_max):
    return (original_value - a_min) * (b_max - b_min) / (a_max - a_min) + b_min


def is_within_range(value, min_value, max_value):
    return min(max_value, max(min_value, value))
