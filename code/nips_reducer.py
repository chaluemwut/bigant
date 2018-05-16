#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import sys


local_best = 9999999
ant_number = 0
counter = 0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    number_of_ant, per_word_perplex = line.split(' ')
    # if int(number_of_alha) < int(current_min):
    #     current_min = number_of_alha
    if float(per_word_perplex) < local_best:
        local_best = float(per_word_perplex)
        ant_number = int(number_of_ant)
    
    # print line
    counter = counter+1
    if counter == 4:
        print '{} {}'.format(ant_number, local_best)

#     # convert count (currently a string) to int
#     try:
#         count = int(count)
#     except ValueError:
#         # count was not a number, so silently
#         # ignore/discard this line
#         continue

#     # this IF-switch only works because Hadoop sorts map output
#     # by key (here: word) before it is passed to the reducer
#     if current_word == word:
#         current_count += count
#     else:
#         if current_word:
#             # write result to STDOUT
#             print '%s\t%s' % (current_word, current_count)
#         current_count = count
#         current_word = word

# # do not forget to output the last word if needed!
# if current_word == word:
#     print '%s\t%s' % (current_word, current_count)