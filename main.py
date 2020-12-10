from steerbeh.game import Game
from steerbeh.gamecfg import GameCfg
from argparse import ArgumentParser

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('-c', help='Game configuration file', type=str)
    args = ap.parse_args()

    cfg = GameCfg.load(args.c)
    Game(config=cfg).run()
