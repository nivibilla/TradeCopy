nums = [1, 11, 3, 0, 15, 5, 2, 4, 10, 7, 12, 6]
# nums.sort()
range_list = []
final_list = []
for num in nums:
    range_list.append(num)
    i = 1
    while True:
        try:
            new_index = nums.index(num + i)
            range_list.append(num + i)
            i += 1
        except ValueError:
            final_list.append(range_list)
            range_list = []
            break

print(final_list)

longest_list = max(final_list, key=len)

print("[" + str(longest_list[0]) + "," + str(longest_list[-1]) + "]")