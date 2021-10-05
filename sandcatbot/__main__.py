import glob, os.path
from argparse     import ArgumentParser
from configparser import ConfigParser
from dataclasses  import dataclass
from datetime     import datetime
from random       import Random

from twitter      import Api

@dataclass
class Config(object):
    consumer_key:    str
    consumer_secret: str
    access_key:      str
    access_secret:   str

    files:           str
    random_seed:     str

def _log(message: str):
    print(datetime.utcnow().isoformat(), message)

def main(config: Config, state_fname: str):
    files = glob.glob(config.files)
    Random(config.random_seed).shuffle(files)

    if os.path.isfile(state_fname):
        with open(state_fname, "r") as state_file:
            call_count = int(state_file.readline().strip())
    else:
        call_count = 0
    _log(f"call count {call_count}")

    index = call_count % len(files)
    fname = files[index]

    _log(f"tweeting {fname}")
    tweet = Api(
        consumer_key        =config.consumer_key,
        consumer_secret     =config.consumer_secret,
        access_token_key    =config.access_key,
        access_token_secret =config.access_secret
    )
    with open(fname, "rb") as tweet_media:
        tweet.PostUpdate("", media=tweet_media)

    with open(state_fname, "w") as state_file:
        state_file.write(f"{call_count+1}\n")

if __name__ == "__main__":
    aparse = ArgumentParser()
    aparse.add_argument("config", help="config file")
    aparse.add_argument("state",  help="file to hold bot state")

    args = aparse.parse_args()
    with open(args.config, "r") as cfile:
        (cparse := ConfigParser()).read_file(cfile)

    config = Config(
        cparse["twitter"]["consumer-key"],
        cparse["twitter"]["consumer-secret"],
        cparse["twitter"]["access-key"],
        cparse["twitter"]["access-secret"],
        os.path.expanduser(cparse["other"]["files"]),
        cparse["other"]["random-seed"]
    )

    main(config, args.state)
