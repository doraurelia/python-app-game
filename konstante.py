IGRAC_X = "X"
IGRAC_O = "O"
PRAZNO = "-"
BROJ_FIGURA = 9

POZICIJE_PO_BROJU = (
    #vanjski krug
    0, 1, 2, 
    8, 9, 10, 
    16, 17, #0
    #središnji krug
    18, 7, 15, 
    23, 19, 11, 
    3, 22, #18
    #unutrašnji krug
    21, 20, 14, 
    13, 12, 6, 
    5, 4, #21
)
BROJEVI_PO_POZICIJI = tuple(POZICIJE_PO_BROJU.index(pozicija) + 1 for pozicija in range(24))

KOORDINATE = (
    (0, 0), (15, 0), (30, 0), (30, 3), (30, 6), (15, 6), (0, 6), (0, 3),
    (5, 1), (15, 1), (25, 1), (25, 3), (25, 5), (15, 5), (5, 5), (5, 3),
    (10, 2), (15, 2), (20, 2), (20, 3), (20, 4), (15, 4), (10, 4), (10, 3),
)

MLINOVI = tuple(
    tuple(pozicija - 1 for pozicija in mlin)
    for mlin in (
        (1, 2, 3), (3, 4, 5), (5, 6, 7), (7, 8, 1),
        (9, 10, 11), (11, 12, 13), (13, 14, 15), (15, 16, 9),
        (17, 18, 19), (19, 20, 21), (21, 22, 23), (23, 24, 17),
        (2, 10, 18), (4, 12, 20), (6, 14, 22), (8, 16, 24),
    )
)

VEZE = (
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1),
    (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15),
    (15, 16), (16, 9),
    (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23),
    (23, 24), (24, 17),
    (2, 10), (10, 18), (4, 12), (12, 20),
    (6, 14), (14, 22), (8, 16), (16, 24),
)

SUSJEDI = {pozicija: set() for pozicija in range(24)}
for prva, druga in VEZE:
    SUSJEDI[prva - 1].add(druga - 1)
    SUSJEDI[druga - 1].add(prva - 1)