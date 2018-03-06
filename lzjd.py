import xxhash
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

    def hash_buffer(self, buffer):
        hasher = xxhash.xxh32()
        hasher.update(buffer)
        return hasher.intdigest()

    def get_min_hashes(self, lzset):
        return heapq.nsmallest(self.k, [self.hash_buffer(x) for x in lzset])

    def get_signature_from_buffer(self, buffer):
        return set(self.get_min_hashes(self.build_lz_set(buffer)))


def get_lzjd_dist(buff1, buff2):
    hasher = LZJD_Hashifier()
    setA = hasher.get_signature_from_buffer(buff1)
    setB = hasher.get_signature_from_buffer(buff2)
    return len(setA.intersection(setB)) / len(setA.union(setB))