import heapq
from Queue import Queue
import os

max_size = 10000
class Merger:
    def __init__(self, out):
        self.heap = []
        self.output_file = open(out, "w")

    def merge_two(self, file1, file2, file_out):
        try:

            f_1 = open(file1, 'r')
            f_2 = open(file2, 'r')
            chunk_1 = f_1.readlines(max_size)
            chunk_2 = f_2.readlines(max_size)
            chunk_12 = []
            i = j = 0
            while i < len(chunk_1) or j < len(chunk_2):
                if chunk_1[i] <= chunk_2[j]:
                    chunk_12.append(chunk_1[i])
                    i += 1
                else:
                    chunk_12.append(chunk_2[j])
                    j += 1
                if i == len(chunk_1):
                    chunk_1 = f_1.readlines(max_size)
                    if not chunk_1:
                            [chunk_12.append(chunk_2[p]) for p in range(j, len(chunk_2))]
                            while True:
                                try:
                                    chunk_12.append(f_2.readlines(max_size))
                                except:
                                    break
                    break
                if j == len(chunk_2):
                    chunk_2 = f_2.readlines(max_size)
                    if not chunk_2:
                        [chunk_12.append(chunk_1[p]) for p in range(i, len(chunk_1))]
                        while True:
                            try:
                                chunk_12.append(f_1.readlines(max_size))
                            except:
                                break
                    break
            [file_out.write(j) for j in chunk_12]
            f_1.close()
            f_2.close()
            os.remove(file1)
            os.remove(file2)
            return
        except Exception, err_msg:
            print "Error while merging: %s" % str(err_msg)

    def merge(self, paths_list):
        queue = Queue()
        j = 0
        for i in paths_list:
            queue.put(i)
        while not queue.empty():
            if queue.qsize() == 1:
                self.output_file.write((open(queue.get(), "r").read()).strip('\n'))
                self.output_file.close()
                return
            file_1 = queue.get()
            file_2 = queue.get()
            if queue.empty():
                self.merge_two(file_1, file_2, self.output_file)
                self.output_file.close()
                return
            merged_12 = open("temp_{0}.txt".format(j), "w+r")
            j += 1
            self.merge_two(file_1, file_2, merged_12)
            queue.put(merged_12.name)
            merged_12.close()


# def read_lines_chunk(f_in, m):
#     final_ = ""
#     while True:
#         chunk = f_in.read(m)
#         if chunk == "":
#             break
#         else:
#             if not chunk.endswith("\n"):
#                 while not chunk.endswith("\n"):
#                     f_in.seek(f_in.tell() - 1, 0)
#                     chunk = chunk[:-1]
#             final_ += chunk
#     l = final_.strip('\n').split('\n')
#     final_chunk = []
#     for i in l:
#         final_chunk.append(i + '\n')
#     return final_chunk
