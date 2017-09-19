import os


def read_envfile(filename='.env'):
    # Poor man's dotenv
    if os.path.isfile(filename):
        with open(filename, 'r') as infp:
            kvs = [
                [a.strip() for a in line.split('=', 1)]
                for line in infp
                if '=' in line and not line.startswith('#')
            ]
            os.environ.update(dict(kvs))


def get_config():
    return dict(
        OUTPUT_DIR=(
            os.environ.get('OUTPUT_DIR') or
            os.path.realpath(os.path.join(os.path.dirname(__file__), 'shots'))
        ),
        RASPISTILL=os.environ.get('RASPISTILL', '/usr/bin/raspistill'),
        S3_BUCKET=os.environ.get('S3_BUCKET'),
    )
