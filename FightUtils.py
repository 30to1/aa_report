from Objs import Fight

# get units associated with a fight as: [born=[...], reinforce=[...], dead=[...]]
def get_fight_participants(game, fight, final_frame):

    # very bad loop, causes us to loop over every unit for every fight.
    # this costs 33 seconds in 100,000 calls. There are 2.3 million units in that data set.
    # an average of 10 fights per game, means that I'm executing the loop body 23 million times at a cost of 1.5 sec/mil

    born, reinforce, dead = [], [], []
    for aa in game.aa_list:
        if aa.born_frame < fight.start_frame <= aa.died_frame:
            born.append(aa)
        elif fight.start_frame <= aa.born_frame <= fight.end_frame:
            reinforce.append(aa)
        if fight.start_frame <= aa.died_frame <= fight.end_frame and aa.died_frame < final_frame:
            dead.append(aa)
    return born, reinforce, dead

# iterate over blocks of "died frames" with no gap less than max_gap_frames
def iter_fights(game, max_gap_frames):
    aa_list = game.aa_list
    start_index = None
    fight_index = 0

    for i in range( len(aa_list) ):
        aa = aa_list[i]
        previous_aa = aa_list[i-1] if i > 0 else aa

        current_frame = aa.died_frame
        previous_frame = previous_aa.died_frame
        max_frame = previous_frame + max_gap_frames

        if current_frame < previous_frame:
            raise Exception("aunit_list is unsorted, please sort by last_frame")

        if start_index == None:                                                     # True on initial pass
            start_index = i
        elif max_frame >= current_frame:                                            # Next end_frame is within fight bounds
            continue
        else:                                                                       # Return and Update start_index
            end_index = i -1
            start_frame = aa_list[start_index].died_frame
            end_frame = aa_list[end_index].died_frame

            yield Fight(game.game_id, start_index, end_index, start_frame, end_frame)
            fight_index += 1
            start_index = i
    else:                                                                           # Don't drop last batch just because iteration ended!
        if start_index and not start_index == len(aa_list):
            end_index = len(aa_list) -1
            start_frame = aa_list[start_index].died_frame
            end_frame = aa_list[end_index].died_frame
            yield Fight(game.game_id, start_index, end_index, start_frame, end_frame)
