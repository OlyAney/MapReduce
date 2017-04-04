import heapq
from Queue import Queue
import os

max_size = 20
class Merger:
    def __init__(self, out):
        self.heap = []
        self.output_file = open(out, "w")

    def merge_two(self, file1, file2, file_out):
        try:
            if file1 is "":
                file_out.write(open(file2, 'r').read().strip('\n'))
                return
            elif file2 is "":
                file_out.write(open(file1, 'r').read().strip('\n'))
                return
            open_files = [open(file1, 'r'), open(file2, 'r')]
         #   chunks = read_lines_chunk(open_files[0], max_size) + read_lines_chunk(open_files[1], max_size)
            [heapq.heappush(self.heap, (f.read(), f)) for f in open_files]
          #  [heapq.heappush(self.heap, (i, open_files[0])) for i in chunks[:len(chunks)/2]]
          #  [heapq.heappush(self.heap, (i, open_files[1])) for i in chunks[len(chunks)/2:]]
            while self.heap:
                smallest = heapq.heappop(self.heap)
                file_out.write(str(smallest[0]))
                read_line = smallest[1].readline()
                # checking that this file has not ended
                #try:
                #    read_lines_chunk(smallest[1])
                #except
                #if smallest[1].tell() == os.fstat(smallest[1].fileno()).st_size:
                #    new_chunks = read_lines_chunk(smallest[1], max_size)
                if len(read_line) != 0:
                    # adding next element from current file
                    heapq.heappush(self.heap, (read_line, smallest[1]))
            [f.close() for f in open_files]
            [os.remove(f.name) for f in open_files]
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
                [os.remove("temp_{0}.txt".format(k)) for k in range(j)]
                [os.remove(p) for p in paths_list]
                self.output_file.close()
                return
            file_1 = queue.get()
            file_2 = queue.get()
            if queue.empty():
                self.merge_two(file_1, file_2, self.output_file)
                [os.remove("temp_{0}.txt".format(k)) for k in range(j)]
                [os.remove(p) for p in paths_list]
                self.output_file.close()
                return
            merged_12 = open("temp_{0}.txt".format(j), "w+r")
            j += 1
            self.merge_two(file_1, file_2, merged_12)
            queue.put(merged_12.name)
            merged_12.close()


def read_lines_chunk(f_in, m):
    while True:
        chunk = f_in.read(m)
        if chunk == "":
            break
        else:
            if not chunk.endswith("\n"):
                while not chunk.endswith("\n"):
                    f_in.seek(f_in.tell() - 1, 0)
                    chunk = chunk[:-1]
            final_ = chunk
    l = final_.strip('\n').split('\n')
    final_chunk = []
    for i in l:
        final_chunk.append(i + '\n')
    return final_chunk
