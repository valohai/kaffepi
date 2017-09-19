import os
import datetime
import subprocess
import boto3
import blinkt
from contextlib import contextmanager

# Poor man's dotenv:
if os.path.isfile('.env'):
    with open('.env', 'r') as infp:
        kvs = [
            [a.strip() for a in line.split('=', 1)]
            for line in infp
            if '=' in line and not line.startswith('#')
        ]
        os.environ.update(dict(kvs))

OUTPUT_BASE_DIR = (os.environ.get('OUTPUT_DIR') or os.path.realpath(os.path.join(os.path.dirname(__file__), 'shots')))
RASPISTILL = os.environ.get('RASPISTILL', '/usr/bin/raspistill')


def grab_snapshot():
    now = datetime.datetime.utcnow()
    filename = now.strftime('%Y%m%d-%H%M%S.jpg')
    file_rel_path = '{year}-{month}/{filename}'.format(
        output_dir=OUTPUT_BASE_DIR,
        year=now.strftime('%Y'),
        month=now.strftime('%m'),
        day=now.strftime('%d'),
        filename=filename,
    )
    file_path = os.path.join(OUTPUT_BASE_DIR, file_rel_path)
    output_dir = os.path.dirname(file_path)

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)


    print('Invoking raspistill...')
    subprocess.check_call([
        RASPISTILL,
        '--nopreview',
        '--width', '1600',
        '--height', '1200',
        '--quality', '70',
        '--timeout', '1000',
        '--output', file_path,
        '--latest', os.path.join(OUTPUT_BASE_DIR, 'latest.jpg'),
    ])

    return {
        'path': file_path,
        'rel_path': file_rel_path,
    }


@contextmanager
def lit():
    print('Turning lights on...')
    blinkt.set_all(255, 255, 255, 0.2)
    blinkt.show()
    yield
    print('Turning lights off...')
    blinkt.clear()
    blinkt.show()



def main():
    with lit():
        file_paths = grab_snapshot()
    print('Uploading to s3://{bucket}/{key}'.format(
        bucket=os.environ['S3_BUCKET'],
        key=file_paths['rel_path'],
    ))
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=open(file_paths['path'], 'rb'),
        Bucket=os.environ['S3_BUCKET'],
        Key=file_paths['rel_path'],
    )
    print('Creating "latest" copy in S3.')
    s3_client.copy_object(
        Bucket=os.environ['S3_BUCKET'],
        Key='latest.jpg',
        CopySource={'Bucket': os.environ['S3_BUCKET'], 'Key': file_paths['rel_path']},
        StorageClass='REDUCED_REDUNDANCY',
    )
    print('Done.')

if __name__ == '__main__':
    main()