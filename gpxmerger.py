import sys
import logging
import logging.config
import gpxpy
import gpxpy.parser as parser
from gpxpy.gpx import GPXTrackPoint
from os import path
import glob   # new logic

# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'gpxmerger.log',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '__main__': {  # name my module
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['file']
        }
    }
})

target_filename = 'merged.gpx'


def is_gpx(filename):
    logger = logging.getLogger(__name__)
    ext = path.splitext(filename)[1]

    logger.debug('checking {f}'.format(f=filename))
    return ext == '.gpx'


def load_points(filename):
    logger = logging.getLogger(__name__)
    points = []
    with open(filename, 'r') as gpx_file:
        gpx_parser = parser.GPXParser(gpx_file)
        gpx_parser.parse()
        gpx = gpx_parser.gpx
        for track in gpx.tracks:
            for segment in track.segments:
                points.extend(segment.points)

    logger.debug('loaded {s} points from {f}'.format(s=len(points), f=filename))
    return points


def to_xml(points):
    logger = logging.getLogger(__name__)
    logger.debug('converting {s} points to XML'.format(s=len(points)))
    gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Add points:
    gpx_segment.points.extend(points)

    return gpx.to_xml()


def get_all_points(track_files):
    logger = logging.getLogger(__name__)
    points = []
    for f in track_files:
        points.extend(load_points(f))

    logger.debug('loaded a total of {s} points'.format(s=len(points)))
    return points


def get_target(files):
    logger = logging.getLogger(__name__)
    file = files[0]
    dir_name = path.dirname(file)
    target = path.join(dir_name, target_filename)
    logger.debug("write result to: {f}".format(f=target))
    return target


def main(argv):
    logger = logging.getLogger(__name__)
    logger.info("start new merge process")

    # Original logic 
    # track_files = [f for f in argv if is_gpx(f)]

    # New logic
    target_file = get_target(argv)
    target_dir = path.dirname(target_file)
    track_files = glob.glob(target_dir + '/*.gpx')

    points = get_all_points(track_files)
    points = filter(lambda x: x.time is not None, points)
    sorted_points = sorted(points, key=lambda p: p.time)
    xml = to_xml(sorted_points)

    with open(target_file, 'w') as fp:
        logger.debug('saving "{f}"'.format(f=target_file))
        fp.write(xml)
        logger.debug('done saving')

    logger.info("Finish")


if __name__ == '__main__':
    main(sys.argv[1:])
