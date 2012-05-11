import math
import FightUtils

# get [PlayerFightCosts, PlayerFightCosts] for a given fight, skipping deaths near the end of the game.
def get_player_fight_costs(game, fight, ignore_end_frames):
    final_frame = game.aa_list[ len(game.aa_list)-1].died_frame - ignore_end_frames
    born,rein,dead = FightUtils.get_fight_participants(game,fight, final_frame)

    # this method gets called around 100,000 times in 10k games
    # run time is aprox 45 seconds
    #   - 35 of which is get_fight_participants
    #   - 3 of which is sum, 5 of which is generator
    # get_fight_participants loops through every unit in game per call. Total loop iter ~ 23 million for this set.

    p1_born = sum( aa.simple_cost for aa in born if aa.player_index == 0 )
    p2_born = sum( aa.simple_cost for aa in born if aa.player_index == 1 )

    p1_rein = sum( aa.simple_cost for aa in rein if aa.player_index == 0 )
    p2_rein = sum( aa.simple_cost for aa in rein if aa.player_index == 1 )

    p1_dead = sum( aa.simple_cost for aa in dead if aa.player_index == 0 )
    p2_dead = sum( aa.simple_cost for aa in dead if aa.player_index == 1 )

    return [PlayerFightCosts(game.game_id, player_index=0, start_cost=p1_born, rein_cost=p1_rein, dead_cost=p1_dead),
            PlayerFightCosts(game.game_id, player_index=1, start_cost=p2_born, rein_cost=p2_rein, dead_cost=p2_dead)]


# get a set of allocated costs
class PlayerFightCosts(object):
    __slots__ = ["game_id", "player_index", "dead_cost", "rein_cost", "start_cost",
                 "remaining_cost" ]
    def __init__(self, game_id, player_index, start_cost, rein_cost, dead_cost):
        self.game_id = game_id
        self.player_index = player_index
        self.dead_cost = dead_cost
        self.rein_cost = rein_cost
        self.start_cost = start_cost
        self.remaining_cost = start_cost + rein_cost - dead_cost

        if self.remaining_cost < 0:
            raise Exception('dead cost is greater than start + rein')

# get a set of net allocated costs from the perspective of the larger army (reference_player_index)
class NetFightCosts(object):
    __slots__ = ["reference_player_index", "army_ratio", "army_ratio_after", "log_ratio_change", "net_start",
                 "net_rein", "net_remaining", "net_kills", "gross_kills", "gross_start", "gross_remain", "gross_rein" ]
    def __init__(self, p1, p2):
        if p1.start_cost == 0 or p2.start_cost == 0 or p1.remaining_cost == 0 or p2.remaining_cost == 0:
            self.army_ratio = 0
            return

        # we calculate everything in terms of the larger army
        if p1.start_cost < p2.start_cost:
            p1, p2 = p2, p1 # this works in python!
            self.reference_player_index = 1
        else:
            self.reference_player_index = 0

        self.army_ratio = p1.start_cost / float(p2.start_cost)
        self.army_ratio_after = p1.remaining_cost / float(p2.remaining_cost)
        if self.army_ratio_after > self.army_ratio * 1.5:
            self.army_ratio_after = self.army_ratio * 1.5

        if self.army_ratio == 0 or self.army_ratio_after == 0 :
            self.log_ratio_change = None
        else:
            self.log_ratio_change = math.log(self.army_ratio) - math.log(self.army_ratio_after)

        self.net_start = p1.start_cost - p2.start_cost
        self.net_rein = p1.rein_cost - p2.rein_cost
        self.net_remaining = p1.remaining_cost - p2.remaining_cost
        self.net_kills = -(p1.dead_cost - p2.dead_cost)
        self.gross_kills = p1.dead_cost + p2.dead_cost
        self.gross_start = p1.start_cost + p2.start_cost
        self.gross_remain = p1.remaining_cost + p2.remaining_cost
        self.gross_rein = p1.rein_cost + p2.rein_cost
