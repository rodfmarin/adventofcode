grid = """30373
25512
65332
33549
35390"""

# grid = grid.split("\n")
#
# for index, item in enumerate(grid):
#     for jindex, jitem in enumerate(item):
#         print(f"Working on line {index}, for char {jindex}")
#         print(jitem)
#
# print(grid)


test = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

col_len = len(test[0])
row_len = len(test[0])

for col in range(col_len):
    print(f"column should be {col}")
    for row in range(row_len):
        print(f"row should be {row}")
        print(test[row][col])
    #
    #
    # for col_index in range(tree_grid.column_count):
    #     for row_index in range(tree_grid.line_count):
    #         """
    #         0,0    0,1    0,2
    #         1,0    1,1    1,2
    #         2,0    2,1    2,2
    #         """
# this is busted:
#(2, 1) 5 False True True True
"""
30373
25512
65332 < This 5 should only be seen from the right it is being seen from down and left
33549
35390
"""

print(print(reversed(range(7))))

for i in reversed(range(0)):
    print(i)