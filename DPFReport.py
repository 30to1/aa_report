import math
import Costs
import FightUtils
import main

def get_report(games, max_frame_gap = 16*20, ignore_end_frames = 16*10, minimum_gross_losses = 1000, limit_ratio_change_mult = 1.5):
    # cost_data contains 3 dict each map game to list of Fights, player_fight_costs, or NetFightCosts respectively
    cost_data = _get_fight_costs(games, max_frame_gap, ignore_end_frames, limit_ratio_change_mult)
    game_fights, game_player_fight_costs, game_net_fight_costs, game_player_fight_dpf = cost_data

    working_buckets = {}
    log_count_by_bucket = {}

    # pre-processing
    for game_id, fight_net_costs in game_net_fight_costs.iteritems():
        player_dpf = game_player_fight_dpf[game_id]

        for i in range(len(fight_net_costs)):
            net_costs = fight_net_costs[i]
            if player_dpf[i][0] and player_dpf[i][1]:
                log_net_player_dpf = math.log(player_dpf[i][0]) - math.log(player_dpf[i][1])
                if net_costs.army_ratio: # false if skipped due to zeros
                    if net_costs.gross_kills >= minimum_gross_losses:
                        key = get_rounded_bucket( math.exp(log_net_player_dpf), .1 )
                        # if domain problem, this is None, so adjust our log_count denominator accordingly
                        if net_costs.log_ratio_change:
                            log_count = log_count_by_bucket.setdefault(key, 0)
                            log_count_by_bucket[key] = log_count + 1
                        working_buckets.setdefault(key,[]).append(net_costs)

    complete_buckets = {}
    for dpf_ratio_bucket, net_costs in working_buckets.iteritems():
        count = len( net_costs )
        log_count = log_count_by_bucket[dpf_ratio_bucket] if dpf_ratio_bucket in log_count_by_bucket else 1

        # wasteful for clarity
        net_start        = sum( nc.net_start        for nc in net_costs ) / count
        net_rein         = sum( nc.net_rein         for nc in net_costs ) / count
        net_remain       = sum( nc.net_remaining    for nc in net_costs ) / count
        net_kill         = sum( nc.net_kills        for nc in net_costs ) / count
        army_ratio_after = sum( nc.army_ratio_after for nc in net_costs ) / count - dpf_ratio_bucket

        log_change       = math.exp( sum( nc.log_ratio_change for nc in net_costs if nc.log_ratio_change ) / log_count )

        gross_kills      = sum( nc.gross_kills  for nc in net_costs ) / count
        gross_start      = sum( nc.gross_start  for nc in net_costs ) / count
        gross_remain     = sum( nc.gross_remain for nc in net_costs ) / count
        gross_rein       = sum( nc.gross_rein   for nc in net_costs ) / count

        complete_buckets[dpf_ratio_bucket] = [dpf_ratio_bucket, net_start, net_rein, net_remain,
                                               net_kill, log_change, army_ratio_after, gross_kills, gross_start,
                                               gross_remain, gross_rein, count ]

    return ['dpf_ratio_bucket', 'net_start', 'net_rein', 'net_remain',
            'net_kill', 'log_change', 'army_ratio_change', 'gross_kills', 'gross_start',
            'gross_remain', 'gross rein', 'count'], complete_buckets

# get player_fight_costs, NetFightCosts, and Fights each associated by game_id
def get_player_dpf(dead_aa_list):
    def average_frequency(frame_frequency_lookup):
        total_freq = 0
        for frequency in frame_frequency_lookup.values():
            total_freq += frequency

        return total_freq / float(len(frame_frequency_lookup)) if len(frame_frequency_lookup) > 0 else None

    player_dpf_working = [{},{}]

    # make in player_dpf_working look like: [{123:5, 125:6}] -- [ [player_index]: {frame:count} ]
    for aa in dead_aa_list:
        # increment count for player and frame
        player_frame_lookup = player_dpf_working[aa.player_index]
        player_frame_lookup[ aa.died_frame ] = ( player_frame_lookup.setdefault(aa.died_frame, 0)+1 )

    return [average_frequency(frame_frequency_lookup=player_frame_lookup ) for player_frame_lookup in player_dpf_working]


def _get_fight_costs( games, max_frame_gap, ignore_end_frames, limit_ratio_change_mult ):
    game_fights = {}
    game_fight_player_costs = {}
    game_fight_net_costs = {}
    game_fight_player_dpf = {}

    for game in games:
        fights, fight_player_costs,fight_net_costs,fight_player_dpf = [],[],[],[]

        game_fights[game.game_id] = fights
        game_fight_player_costs[game.game_id] = fight_player_costs
        game_fight_net_costs[game.game_id] = fight_net_costs
        game_fight_player_dpf[game.game_id] = fight_player_dpf

        for fight in FightUtils.iter_fights(game, max_frame_gap):
            fights.append(fight)
            # fetch the fight_participant's
            final_frame = game.aa_list[ len(game.aa_list)-1].died_frame - ignore_end_frames
            born,rein,dead = FightUtils.get_fight_participants(game,fight, final_frame)

            player_costs = Costs.get_player_fight_costs(game, fight, ignore_end_frames, born=born, rein=rein, dead=dead)
            net_costs = Costs.NetFightCosts(player_costs[0], player_costs[1], limit_ratio_change_mult)

            player_dpf = get_player_dpf( dead )
            # dpf presented relative to 'reference_player'. This excludes team games.
            if net_costs.army_ratio and net_costs.reference_player_index == 1:
                player_dpf[0], player_dpf[1] = player_dpf[1], player_dpf[0]
            fight_player_dpf.append(player_dpf)

            fight_player_costs.append(player_costs)
            fight_net_costs.append(net_costs)

    return game_fights, game_fight_player_costs, game_fight_net_costs, game_fight_player_dpf


# return a number floored to width, allows floats
def get_rounded_bucket(value, width):
    sizer = int( width * 100 )
    value = int( value * 100 )
    return ( ( value / sizer ) * sizer ) / float( 100 )

if __name__ == "__main__":
    main.main( get_report )