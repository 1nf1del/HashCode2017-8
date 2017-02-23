#!/usr/bin/env python
# coding=utf-8

def parse_file(file_name):

    f = open(file_name)

    ### Parse numbers:

    numbers = f.readline().split()
    V = int(numbers[0])
    E = int(numbers[1])
    R = int(numbers[2])
    C = int(numbers[3])
    X = int(numbers[4])

    size_videos = f.readline().split() # V numbers, one for each video (size in Mb)

    ### Parse endpoints:

    endpoints = []
    for i in range(E):
        LDK = f.readline().split()
        Ld = int(LDK[0]) # Latency of serving a video request from the data center to its endpoint
        K = int(LDK[1]) # Number of cache servers at this endpoint

        cache_servers_at_endpoint_i = []
        for j in range(K):
            CLC = f.readline().split()
            C = int(CLC[0]) # Id (we don't care, it's just the position in the array)
            Lc = int(CLC[1])
            cache_servers_at_endpoint_i.append((C, Lc))

        endpoints.append( (Ld, K, cache_servers_at_endpoint_i) )

    ### Parse requests:

    requests = []
    for i in range(R):
        RRR = f.readline().split()
        Rv = int(RRR[0])
        Re = int(RRR[1])
        Rn = int(RRR[2])
        requests.append((Rv, Re, Rn))


    return V, E, R, C, X, size_videos, endpoints, requests


def countRequest():
    file_name = "Data/me_at_the_zoo.in"

    V, E, R, C, X, size_videos, endpoints, requests = parse_file(file_name)
    
    #print(requests)
    #print(endpoints[requests[0][1]][2][0])
    
    caches = []
    
    for c in range(C):
        caches.append([])
    
    print(caches)
    
    for r in requests:
        # r[0] is video #
        # r[1] is is endpoint
        # r[2] is # of request
        for c in endpoints[r[1]][2]:
            # c[0] is the cache,
            # c[1] is the latency
            print(c[0])
            caches[c[0]].append((r[0], c[1] * r[2]))
            
		
		
    


if __name__ == '__main__':
    countRequest()
