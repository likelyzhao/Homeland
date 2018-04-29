from __future__ import division
from __future__ import print_function

import argparse
import errno
import json
import os
import subprocess


def convertframe2time(time):
    hour = int(time / 3600)
    minutes = int((time - 3600 * hour) / 60)
    seconds = time - 3600 * hour - 60 * minutes

    return '{0:02}:{1:02}:{2:02}'.format(hour,minutes,seconds)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise OSError('mkdir failed', path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split videos!')
    parser.add_argument('--input_dir', required=True, help='Path to json files.')
    parser.add_argument('--acc', '-a', action='store_true', help='Need Accelerate Download.')
    parser.add_argument('--bucket', '-b', default='p5vond2ys.bkt.clouddn.com', help='Bucket for video download.')
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    video_source_dir = input_dir + '/source'
    video_clips_dir = input_dir + '/clips'
    if os.path.isdir(input_dir):
        mkdir_p(video_source_dir), mkdir_p(video_clips_dir)
        file_names = []
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".json"):
                file_names.append(os.path.join(input_dir, file_name))
        for file_name in file_names:
            with open(file_name) as json_file:
                json_str = json.load(json_file)
            video_relevant_name = json_str['url']
            video_name = os.path.basename(video_relevant_name)
            video_path = video_source_dir + '/' + video_name
            if not os.path.exists(video_path):
                if args.acc:
                    command = 'curl -s http://xsio.qiniu.io/' + video_relevant_name + ' -H \'Host:' + args.bucket + '\' -o ' + video_path
                else:
                    command = 'wget -q http://' + args.bucket + '/' + video_relevant_name + ' -O ' + video_path
                success = subprocess.call(command, shell=True)
                if success != 0:
                    print('Download error: ' + video_relevant_name)
            clips = json_str['clips']['data']
            for index, clip in enumerate(clips):
                segment = clip['segment']
                start, end = float(segment[0]), float(segment[1])
                period = end - start
                clip_video_path = video_clips_dir + '/' + video_name.replace('.', '_' + '{0:02d}'.format(index) + '.')
                command = 'ffmpeg -loglevel panic -y -ss ' + convertframe2time(start) + ' -i ' + video_path + ' -vcodec copy -acodec copy -t ' + convertframe2time(period) + ' ' + clip_video_path
                success = subprocess.call(command, shell=True)
                if success != 0:
                    print('Split error: ' + command)
                print(start, end, clip_video_path)
