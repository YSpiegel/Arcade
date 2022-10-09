
def in_vertically(hitbox1, hitbox2):
    return hitbox2[0][0] - 5 <= hitbox1[0][0] < hitbox1[0][1] <= hitbox2[0][1] + 5


def vertical_collusion(hitbox1, hitbox2):
    """
    Checks for a collusion
    :param hitbox1:
    :param hitbox2:
    :return: The higher hitbox or none if there's no collusion
    """

    if hitbox1[0][0] <= hitbox2[0][0] <= hitbox1[0][1] or hitbox2[0][0] <= hitbox1[0][0] <= hitbox2[0][1]:
        if hitbox1[1][0] <= hitbox2[1][0] <= hitbox1[1][1]:
            return hitbox1
        if hitbox2[1][0] <= hitbox1[1][0] <= hitbox2[1][1]:
            return hitbox2
    return 0


def horizontal_collusion(hitbox1, hitbox2):
    """
        Checks for a collusion
        :param hitbox1:
        :param hitbox2:
        :return: The left hitbox or none if there's no collusion
        """

    if hitbox1[1][0] <= hitbox2[1][0] + 1 <= hitbox1[1][1] or hitbox2[1][0] <= hitbox1[1][0] + 1 <= hitbox2[1][1]:
        if hitbox1[0][0] <= hitbox2[0][0] <= hitbox1[0][1]:
            return hitbox1
        if hitbox2[0][0] <= hitbox1[0][0] <= hitbox2[0][1]:
            return hitbox2
    return 0
