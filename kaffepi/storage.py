import os
import shutil

import boto3


def save_s3(
    source_path,
    bucket,
    key,
    latest_key=None,
    latest_public=False,
):
    size = os.stat(source_path).st_size
    print('Uploading {size} bytes to s3://{bucket}/{key}'.format(
        size=size,
        bucket=bucket,
        key=key,
    ))
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=open(source_path, 'rb'),
        Bucket=bucket,
        Key=key,
    )
    if latest_key:
        print('Creating "latest" copy in S3.')
        copy_args = dict(
            Bucket=bucket,
            Key=latest_key,
            CopySource={'Bucket': bucket, 'Key': key},
            StorageClass='REDUCED_REDUNDANCY',
        )
        if latest_public:
            copy_args['ACL'] = 'public-read'
        s3_client.copy_object(**copy_args)


def generate_file_path(timestamp):
    filename = timestamp.strftime('%Y%m%d-%H%M%S.jpg')
    return '{year}-{month}/{filename}'.format(
        year=timestamp.strftime('%Y'),
        month=timestamp.strftime('%m'),
        day=timestamp.strftime('%d'),
        filename=filename,
    )


def save_local(source_path, root_dir, dest_rel_path):
    file_path = os.path.join(root_dir, dest_rel_path)
    output_dir = os.path.dirname(file_path)
    latest_path = os.path.join(root_dir, 'latest.jpg')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for dest_path in (file_path, latest_path):
        shutil.copy(source_path, dest_path)
        print('--> %s' % dest_path)
