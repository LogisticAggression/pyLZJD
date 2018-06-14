"""
Python implementation of Lempel Ziv Jaccard Distance


"""

import mmh3
import heapq

class LZJD_Hashifier:
    def __init__(self, k=1024):
        self.k = k

    def build_lz_set(self, buffer):
        lzset = set([])
        start_index = 0
        end_index = 1
        while end_index < len(buffer):
            if buffer[start_index:end_index] not in lzset:
                lzset.add(buffer[start_index:end_index])
                start_index = end_index
            end_index = end_index + 1
        return lzset

    def get_min_hashes(self, lzset):
        return set(heapq.nsmallest(self.k, [mmh3.hash(x, signed=False) for x in lzset]))

    def get_signature(self, min_hashes):
        return ''.join(['{:02x}'.format(x).zfill(8) for x in min_hashes])

    def get_min_hashes_from_signature(self, signature):
        return set([int(signature[i:i+8], 16) for i in range(0, len(signature), 8)])


def get_lzjd_dist(buff1, buff2):
    hasher = LZJD_Hashifier()
    setA = hasher.get_min_hashes(buff1)
    setB = hasher.get_min_hashes(buff2)
    return len(setA.intersection(setB)) / len(setA.union(setB))

def compare_file_to_signature(signature, filename):
    hasher = LZJD_Hashifier()
    setA = hasher.get_min_hashes_from_signature(signature)
    setB = hasher.get_min_hashes(open(filename, "rb"))
    return len(setA.intersection(setB)) / len(setA.union(setB))



if __name__ == "__main__":
    file1 = "c://Windows/System32/calc.exe"
    file2 = "c://Windows/System32/cmd.exe"
    hasher = LZJD_Hashifier()
    test = hasher.get_min_hashes(open(file1, "rb"))
    print(test)
    test2 = hasher.get_signature(hasher.get_min_hashes(open(file1, "rb")))
    print(test2)
    print(compare_file_to_signature(test2, file1))
    print(compare_file_to_signature(test2, file2))