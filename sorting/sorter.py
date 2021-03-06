import math


class Statistics:
    swaps = 0
    comparisons = 0

    @staticmethod
    def reset():
        Statistics.swaps = 0
        Statistics.comparisons = 0

    @staticmethod
    def report():
        return {
            'comparisons': Statistics.comparisons,
            'swaps': Statistics.swaps
        }

    @staticmethod
    def add_swaps(n=1):
        Statistics.swaps += n

    @staticmethod
    def add_comparisons(n=1):
        Statistics.comparisons += n

class Verbose:
    enabled = False

    @staticmethod
    def print(*string):
        if Verbose.enabled:
            print(*string)



class Sorter:
    algorithm_names = [
        'counting_sort',
        'heap_sort',
        'insertion_sort',
        'merge_sort',
        'selection_sort',
        'shell_sort',
        'quick_sort',
    ]

    # zlozonosc O(n+k)
    @staticmethod
    def counting_sort(array):
        array_size = len(array)
        max_element = array[0]

        Statistics.add_comparisons(array_size - 1)

        for i in range(1, array_size):
            if array[i] > max_element:
                max_element = array[i]

        count_array = [0] * (max_element + 1)

        for i in range(0, array_size):
            count_array[array[i]] += 1

        occurences_before = [0] * (max_element + 1)
        occurences_before[0] = count_array[0]
        for i in range(1, max_element + 1):
            occurences_before[i] = occurences_before[i - 1] + count_array[i]

        final_array = [0] * array_size
        for i in range(0, len(array))[::-1]:
            final_array[array_size - occurences_before[array[i]]] = array[i]
            occurences_before[array[i]] -= 1
        return final_array

    # zlozonosc O(nlogn)
    # h = log(n, 2)
    @staticmethod
    def heap_sort(array):
        def fix_tree(tree, n):
            Statistics.add_comparisons(n)  # debug
            for i in range(1, n + 1)[::-1]:
                if tree[i] < tree[int((i - 1) / 2)]:
                    tree[i], tree[int((i - 1) / 2)] = tree[int((i - 1) / 2)], tree[i]
                    Statistics.add_swaps()  # debug
            return tree

        maxIndex = len(array) - 1
        while maxIndex >= 1:
            fix_tree(array, maxIndex)
            array[0], array[maxIndex] = array[maxIndex], array[0]
            Statistics.add_swaps()  # debug
            maxIndex -= 1
        return array

    # O(n) dla optymistycznej tablicy
    # O(n^2) dla pesymistycznej
    @staticmethod
    def insertion_sort(array):
        for pivot in range(0, len(array)):
            for i in range(0, pivot)[::-1]:
                Statistics.add_comparisons()  # debug
                if array[i] < array[i + 1]:
                    array[i], array[i + 1] = array[i + 1], array[i]
                    Statistics.add_swaps()  # debug
                else:
                    break
        return array

    # n-1 podziałów
    # O(nlogn)
    @staticmethod
    def merge_sort(array):
        def divide(array, start, end):
            if end - start <= 1:
                Statistics.add_comparisons()  # debug
                return array
            pivot = int((end - start) / 2) + start
            divide(array, start, pivot)
            divide(array, pivot, end)
            left = array[start:pivot]
            right = array[pivot:end]
            left_max = pivot - start - 1
            right_max = end - pivot - 1
            left_counter = 0
            right_counter = 0
            for i in range(start, end):
                Statistics.add_comparisons()  # debug
                if left_counter > left_max:
                    array[i] = right[right_counter]
                    right_counter += 1
                elif right_counter > right_max:
                    array[i] = left[left_counter]
                    left_counter += 1
                else:
                    Statistics.add_comparisons()  # debug
                    if left[left_counter] > right[right_counter]:
                        array[i] = left[left_counter]
                        left_counter += 1
                    else:
                        array[i] = right[right_counter]
                        right_counter += 1

        divide(array, 0, len(array))
        return array

    # O(nlogn)
    @staticmethod
    def quick_sort(array):
        def quicc(a, start, end):
            if end - start <= 1:
                Statistics.add_comparisons()  # debug
                if end - start == 1 and a[start] < a[end]:
                    Statistics.add_comparisons()  # debug
                    a[start], a[end] = a[end], a[start]
                    Statistics.add_swaps()
                return
            pivot_index = int((end - start) / 2) + start
            Verbose.print('  Array', a[start:end + 1],
                          ', pivot array[{}] = {}'.format(pivot_index, a[pivot_index]))
            a[end], a[pivot_index] = a[pivot_index], a[end]
            Statistics.add_swaps()
            i = start
            j = end - 1
            while i < j:
                while a[i] > a[end]:
                    Statistics.add_comparisons()  # debug
                    i += 1
                while a[j] <= a[end] and j >= 0:
                    Statistics.add_comparisons()  # debug
                    j -= 1
                Statistics.add_comparisons()  # debug
                if i < j:
                    Statistics.add_swaps()
                    a[i], a[j] = a[j], a[i]
                else:
                    break

            a[i], a[end] = a[end], a[i]
            quicc(a, start, i - 1)
            quicc(a, i+1, end)

        quicc(array, 0, len(array) - 1)
        return array

    @staticmethod
    def selection_sort(array):
        array_size = len(array)
        for pivot in range(0, array_size):
            min_element_index = pivot
            for i in range(pivot, array_size):
                Statistics.add_comparisons()  # debug
                if array[min_element_index] < array[i]:
                    min_element_index = i
            array[min_element_index], array[pivot] = array[pivot], array[min_element_index]
            Statistics.add_swaps()  # debug
        return array

    # O(n^2)
    @staticmethod
    def shell_sort(array):
        size = len(array)
        ks = []
        if size >= 3:
            # knuth
            ks = []
            k = 1
            while True:
                k_candidate = int((3**k -1) / 2)
                Statistics.add_comparisons()  # debug
                if k_candidate <= (size / 3):
                    ks.append(k_candidate)
                    k += 1
                else:
                    break
        else:
            ks = [1]
        k_index = len(ks) - 1
        k = ks[k_index]
        while k_index >= 0:
            k = ks[k_index]
            Verbose.print('  K = {}'.format(k))
            for offset in range(0, k):
                # insertion sort
                for pivot in range(offset, size, k):
                    for i in range(offset, pivot, k)[::-1]:
                        Statistics.add_comparisons()  # debug
                        if array[i] < array[i + k]:
                            Statistics.add_swaps()  # debug
                            array[i], array[i + k] = array[i + k], array[i]
                        else:
                            break
            k_index -= 1
        return array