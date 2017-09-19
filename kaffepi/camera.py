import os
import subprocess
import tempfile
import time


def grab_snapshot(
    raspistill='/usr/bin/raspistill',
    width=1600,
    height=1200,
    quality=70,
):
    temp_name = os.path.join(tempfile.gettempdir(), 'kaffepi-%d.jpg' % time.time())

    print('Invoking raspistill...')
    subprocess.check_call([
        raspistill,
        '--nopreview',
        '--width', str(width),
        '--height', str(height),
        '--quality', str(quality),
        '--timeout', '1000',
        '--output', temp_name,
    ])
    return temp_name
