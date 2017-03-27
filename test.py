from Process import Process

p_list = []
with open("input.txt") as f:
    process_list = f.readlines()[2:]
    for index, process in enumerate(process_list):
        process_sub_items = process.split(" ")
        p_list.append(Process(int(index + 1), process_sub_items[1], process_sub_items[2], int(process_sub_items[3]),
                              process_sub_items[0]))

print [x.get_arrival_time() for x in p_list]