# Given an integer square matrix. Determine:
# 1) the sum of elements in those lines that do not contain negative elements:
# 2) the minimum of the sums of the elements of the diagonals parallel to the main diagonal

def determine_properties_1(matrix):

    def sum_of_rows_without_negative(matrix):
        # [section_1 section_2 optional(section_3)]
        # [content loop condition]
        # [i for i in range(10) if i % 2 == 0]
        sums = []
        for row in matrix:
            if not any(x < 0 for x in row):
                sums.append(sum(row))
        return [sum(row) for row in matrix if not any(x < 0 for x in row)]

    def diagonal_sums(matrix):
        n = len(matrix)
        # for k in range(1-n, n):
        #     diagonal = [matrix[i][i + k] for i in range(max(0, -k), min(n, n - k))]
        #     sums.append(sum(diagonal))
        return [sum([matrix[i][i + k] for i in range(max(0, -k), min(n, n - k))]) for k in range(1-n, n)]

    print(f'\nSum of rows without negatives: {sum_of_rows_without_negative(matrix)}')

    print(f'\n Sums of diagonal parallel to main diagonal: {diagonal_sums(matrix)}')

    print(f'\n Minimum sum among sums: {min(diagonal_sums(matrix))}')


# two-dimensional list that represents a matrix
matrix = [
    [2, -4, 6, 0],
    [4, -2, 1, 5],
    [7, 0, 5, -3],
    [1, 4, 5, 3]
]

print('\n#1')
list(map(print, matrix))
determine_properties_1(matrix)


# Given an integer rectangular matrix. Determine:
# 1) the number of columns containing at least one zero element;
# 2) number of the line in which there is the longest series of identical elements.

def determine_properties_2(matrix):
    def count_columns_with_zeros(matrix):
        return sum(1 for j in range(len(matrix[0])) if any(matrix[i][j] == 0 for i in range(len(matrix))))

    def longest_series_row(matrix):
        max_series_length = 0
        row_with_max_series = -1

        for row_index, row in enumerate(matrix):
            current_series_length = 1

            for j in range(1, len(row)):
                current_series_length = current_series_length + 1 if row[j] == row[j - 1] else 1

                if current_series_length > max_series_length:
                    max_series_length, row_with_max_series = current_series_length, row_index

        return row_with_max_series

    print(f'\nNumber of columns with zero elements: {count_columns_with_zeros(matrix)}')

    print(f'\nThe row number with the longest series of identical elements: {longest_series_row(matrix)}')


matrix = [
    [1, 2, 1, 3, 0],
    [1, 1, 1, 0, 4],
    [0, -6, 0, 5, 0],
    [1, 1, 1, 1, 1],
    [0, 3, 0, 0, 1]
]

print('\n#2')
list(map(print, matrix))

determine_properties_2(matrix)

# Cyclic shift of the elements of the rectangular matrix by n elements to the right or
# down (depending on the entered mode), n may be more elements in a row or column.


def cyclic_shift(matrix, n, direction='right'):
    if direction == 'right':
        for row in matrix:
            row[:] = row[-n:] + row[:-n]
    elif direction == 'down':
        matrix[:] = matrix[-n:] + matrix[:-n]


matrix = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [7, 8, 9, 10],
    [10, 11, 12, 13]
]

print('\n#3')
list(map(print, matrix))

direction = input('Enter the direction (right or down):')
n = int(input('Enter the number of positions to shift:'))

cyclic_shift(matrix, n, direction)

print(f'\nThe matrix after a cyclic shift by {n} positions in the direction {direction}:')
list(map(print, matrix))
