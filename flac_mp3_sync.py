#! /usr/bin/env python3

import pathlib as p
import subprocess

def _main(argv):
    """main
    """
    cv = Flac2Mp3Converter("ffmpeg")
    df = DiffFlacMp3("./flac", "./mp3")
    for source, dest in df.check_diff():
        print("source:%s")
        print("dest:  %s")
        cv.convert(source, dest)
        print("done!")

class DiffFlacMp3:

    def __init__(self, flac_root, mp3_root):
        # settings
        self.flac_root = p.Path(flac_root)
        self.mp3_root  = p.Path(mp3_root)

    def convFlacPathToMp3Path(self, path):
        mp3_path = self.mp3_root
        for el in path.parts[1:]:
            mp3_path = mp3_path / el
        return mp3_path.with_suffix(".mp3")

    def check_diff(self):
        flac_files = self.flac_root.rglob("*.flac")
        self.diff = [(el, self.convFlacPathToMp3Path(el)) \
            for el in flac_files if not(self.convFlacPathToMp3Path(el).is_file())]
        return self.diff

class Flac2Mp3Converter:

    def __init__(self, ffmpeg_bin_name):
        self.ffmpeg_bin_name = ffmpeg_bin_name

    def convert(self, source_pathobj, dest_pathobj):
        # create dest folder
        dest_pathobj.parent.mkdir(parents=True, exist_ok=True)
        print("%s %s %s %s %s %s %s %s " % (self.ffmpeg_bin_name, "-i", str(source_pathobj.resolve()), "-codec:a", "libmp3lame", "-q:a", "0", str(dest_pathobj.resolve())))
        subprocess.call([self.ffmpeg_bin_name, "-i", str(source_pathobj.resolve()), "-codec:a", "libmp3lame", "-q:a", "0", str(dest_pathobj.resolve())])

if __name__ == '__main__':
    import sys
    _main(sys.argv)
