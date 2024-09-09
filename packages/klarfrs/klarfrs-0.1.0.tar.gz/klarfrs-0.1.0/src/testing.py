import klarfrs
from klarf_reader.klarf import Klarf
import time
import os

directory = '/workspaces/rust-2/klarfrs/files/'
file_names = os.listdir(directory)

# t2 = time.process_time()
# for f in file_names:
#     filename = f"files/{f}"
#     content = Klarf.load_from_file(filename)

# elapsed_time2 = time.process_time() - t2
# print(elapsed_time2)
# t = time.process_time()



# for f in file_names:
#     filename = f"files/{f}"
#     klarf_data.parse(filename)
# elapsed_time = time.process_time() - t
# print(elapsed_time)
#................................................



filename = f"tests/klarf01.txt"
# t2 = time.process_time()
# content = Klarf.load_from_file(filename)
# print(content)
# elapsed_time2 = time.process_time() - t2

# t = time.process_time()
klarf = klarfrs.parse(filename)
    #klarf_list.append(klarf)
print(klarf)
