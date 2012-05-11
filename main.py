import datetime
import sys
import ArmyRatioReport
import Objs
import util
import json

def load_games_from_json(filename='test.json.txt'):
    games = []
    games_raw = json.loads(util.read_text(filename))
    for raw_game in games_raw:
        games.append( Objs.Game.from_raw( raw_game ) )
    return games

def main():
    filename = "test.json.txt"
    max_frames_gap = 16*20
    ignore_end_frames = 16*10
    minimum_gross_losses = 1000
    limit_change_ratio_mult = 1.5
    delimiter = '\t'
    args = sys.argv[1:]
    if "-h" in args:
        print "main.py  -f [json games file] -m [max_frames_gap] -e [ignore_end_frames_count] -l [minimum_gross_losses] -c [limit_after_ratio_mult] -d [delimiter]"
        return
    else:
        if "-f" in args:
            filename = args[args.index('-f') + 1]
        if "-m" in args:
            max_frames_gap = args[args.index('-m') + 1]
        if "-e" in args:
            ignore_end_frames = args[args.index('-e') + 1]
        if "-d" in args:
            delimiter = args[args.index('-d') + 1]
        if "-l" in args:
            minimum_gross_losses = args[args.index('-l') + 1]
        if "-c" in args:
            limit_change_ratio_mult = args[args.index('-l') + 1]


    print "Processing Start file:{0}, max gap:{1}, end_frames:{2}, minimum_gross_losses:{3}, limit_change_ratio_mult:{4}, delimiter:'{5}'"\
    .format( filename, max_frames_gap, ignore_end_frames, minimum_gross_losses, limit_change_ratio_mult, delimiter )

    print 'start load', datetime.datetime.now()
    games = load_games_from_json( filename )
    print 'load complete', datetime.datetime.now()
    columns, bucketed_sums = ArmyRatioReport.get_report(games, max_frames_gap, ignore_end_frames, minimum_gross_losses, limit_change_ratio_mult)
    print 'completed', datetime.datetime.now()

    print delimiter.join(columns)
    keys = bucketed_sums.keys()
    keys.sort()
    for ratio in keys:
        lines = []
        for value in bucketed_sums[ratio]:
            lines.append(str(value))
        print delimiter.join(lines)

if __name__ == "__main__":
    main()