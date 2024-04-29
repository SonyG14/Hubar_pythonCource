# Вариант 19
# Дана целочисленная квадратная матрица. Определить:
# 1) сумму элементов в тех строках, которые не содержат отрицательных элементов:
# 2) минимум среди сумм элементов диагоналей, параллельных главной диагонали

def determine_properties_1(matrix):

    def sum_of_rows_without_negative(matrix):
        sums = []
        for row in matrix:
            if not any(x < 0 for x in row):
                sums.append(sum(row))
        return sums

    def diagonal_sums(matrix):
        sums = []
        n = len (matrix)
        for k in range(1-n, n):
            diagonal = [matrix[i][i + k] for i in range(max(0, -k), min(n, n - k))]
            sums.append(sum(diagonal))
        return sums

    sums_no_negatives = sum_of_rows_without_negative(matrix)
    print('\n Sum of rows without negatives:', sums_no_negatives)

    diagonal_sums_result = diagonal_sums(matrix)
    print('\n Sums of diagonal parallel to main diagonal:', diagonal_sums_result)

    min_diagonal_sum = min(diagonal_sums_result)
    print('\n Minimum sum among sums:', min_diagonal_sum)


matrix = [
    [2, -4, 6, 0],
    [4, -2, 1, 5],
    [7, 0, 5, -3],
    [1, 4, 5, 3]
]
print('\n#1')
print('matrix:')
for row in matrix:
    print(row)
print('\n')
determine_properties_1(matrix)


# Вариант 3
# Дана целочисленная прямоугольная матрица. Определить:
# 1) количество столбцов, содержащих хотя бы один нулевой элемент;
# 2) номер строки, в которой находится самая длинная серия одинаковых элементов.

def determine_properties_2(matrix):
    def count_columns_with_zeros(matrix):
        zero_columns_count = sum(1 for j in range(len(matrix[0])) if any(matrix[i][j] == 0 for i in range(len(matrix))))
        return zero_columns_count

    def longest_series_row(matrix):
        max_series_length = 0
        row_with_max_series = -1
        for i, row in enumerate(matrix):
            current_series_length = 1
            for j in range(1, len(row)):
                if row[j] == row[j-1]:
                    current_series_length += 1
                else:
                    if current_series_length > max_series_length:
                        max_series_length = current_series_length
                        row_with_max_series = i
                    current_series_length = 1
            if current_series_length > max_series_length:
                max_series_length = current_series_length
                row_with_max_series = i
        return row_with_max_series

    zero_columns = count_columns_with_zeros(matrix)
    print('\nNumber of columns with zero elements:', zero_columns)

    longest_series_row_num = longest_series_row(matrix)
    print('\nThe row number with the longest series of identical elements:', longest_series_row_num)


matrix = [
    [1, 2, 1, 3, 0],
    [1, 1, 1, 0, 4],
    [0, -6, 0, 5, 0],
    [1, 1, 1, 1, 1],
    [0, 3, 0, 0, 1]
]

print('\n#2')
for row in matrix:
    print(row)

determine_properties_2(matrix)

#  Вариант 13
# Осуществить циклический сдвиг элементов прямоугольной матрицы на n элементов вправо или
# вниз (в зависимости от введенного режима), n может быть больше количества элементов в строке или столбце.

def cyclic_shift(matrix, n, direction='right'):
    if direction == 'right':
        for row in matrix:
            for _ in range(n):
                row.insert(0, row.pop())
    elif direction == 'down':
        for _ in range(n):
            matrix.insert(0, matrix.pop())
    else:
        print("Unsupported shift direction.")
        return None


matrix = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [7, 8, 9, 10],
    [10, 11, 12, 13]
]

print('\n#3')
print("Initial matrix:")
for row in matrix:
    print(row)

direction = input("Enter the direction ('right' or 'down'): ")
n = int(input("Enter the number of positions to shift: "))

cyclic_shift(matrix, n, direction)

print("\nThe matrix after a cyclic shift by {} positions in the direction {}:".format(n, direction))
for row in matrix:
    print(row)