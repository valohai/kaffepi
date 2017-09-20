import argparse
import atexit
import datetime
import os

from . import config
from .camera import grab_snapshot
from .illumination import lit
from .storage import generate_file_path, save_local, save_s3


def main():
    config.read_envfile('.env')
    cfg = config.get_config()
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--save-local', '-l', default=False, action='store_true')
    ap.add_argument('--local-dir', '-d', default=cfg['OUTPUT_DIR'])
    ap.add_argument('--save-s3', '-3', default=False, action='store_true')
    ap.add_argument('--s3-bucket', '-b', default=cfg['S3_BUCKET'], action='store_true')
    ap.add_argument('--s3-latest-key', default='latest.jpg')
    ap.add_argument('--s3-latest-public', default=False, action='store_true')
    ap.add_argument('--width', '-w', type=int, default=1600)
    ap.add_argument('--height', '-h', type=int, default=1200)
    ap.add_argument('--quality', '-q', type=int, default=75)
    ap.add_argument('--lights', '-L', default=False, action='store_true')
    ap.add_argument('--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')

    args = ap.parse_args()
    timestamp = datetime.datetime.now()
    dest_rel_path = generate_file_path(timestamp)

    with lit(enable=args.lights):
        snapshot_image = grab_snapshot(width=args.width, height=args.height, quality=args.quality)
        atexit.register(os.unlink, snapshot_image)

    if args.save_local:
        save_local(
            source_path=snapshot_image,
            root_dir=args.local_dir,
            dest_rel_path=dest_rel_path,
        )

    if args.save_s3:
        save_s3(
            source_path=snapshot_image,
            bucket=args.s3_bucket,
            key=dest_rel_path,
            latest_key=args.s3_latest_key,
            latest_public=args.s3_latest_public,
        )

    print('Done.')
