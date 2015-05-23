"""
    Merge function for 2048 game.
    """

def merge(line):
    """
        Function that merges a single row or column in 2048.
        """
    prev = 0    #the last compared nonzero value
    merge_list = []   #the merge list
    for tile in line:
        if tile == prev and prev !=0: #merges
            prev = 0
            merge_list.pop()
            merge_list.append(tile*2)
        elif tile != 0:
            prev = tile
            merge_list.append(tile)
    return merge_list + [0 for dummy_x in range(len(line)-len(merge_list))]
