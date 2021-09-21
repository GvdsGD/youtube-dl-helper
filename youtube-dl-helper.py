#!/usr/bin/env python3


import os
import sys
import time

# Useful functions
def filter(strList, filter):
    out = []
    for string in strList:
        if filter in string:
            out.append(string)
    return out


def getAllowedFormats(string):
    out = []
    input = string.split("\n")
    for line in input:
        out.append(line.split(" ")[0])
    return out

# Defaults for if options are given
url = ""
writeThumbnail = False
writeDescription = False
writeSub = False
webmOrM4aAudio = "webm"
webmOrMp4Video = "webm"
webmOrMp4Output = "mp4"
outputFileName = ""
deleteAV = True

# Options
usageString = "Usage: youtube-dl-helper [OPTIONS]"
args = sys.argv

optionsGiven = False

def printDefaultErrorMessage():
    print(usageString)
    print("Use --help to see more options.")
    exit()

# Help text
if ("--help" in args) or ("-h" in args):
    print(usageString + """

Using any options will set all other options to their defaults

Options:
    -h, --help                  Print this help text and exit
    -u, --url URL               Set url
    -o, --output FILENAME       Set output filename (without extension)
    -k, --keep                  Keep the audio-only and video-only files
    --write-thumbnail           Write thumbnail image to disk
    --write-description         Write video description to a .description file
    --write-sub                 Write subtitle file
    -ax, --audio-ext EXT        Set extension for the audio-only file
    -vx, --video-ext EXT        Set extension for the video-only file
    -ox, --output-ext EXT       Set extension for the output file
    """)
    exit()

if len(args) >= 2:
    optionsGiven = True
    for i in range(1, len(args)):
        # Set url
        if args[i] == "-u" or args[i] == "--url":
            try:
                assert not args[i + 1].startswith("-")
                url = args[i + 1]
            except Exception: printDefaultErrorMessage()
            i += 1
            continue

        # Set output filename
        if args[i] == "-o" or args[i] == "--output":
            try:
                assert not args[i + 1].startswith("-")
                outputFileName = args[i + 1]
            except Exception: printDefaultErrorMessage()
            i += 1
            continue

        if args[i] == "-k" or args[i] == "--keep":
            deleteAV = False
            continue

        # Output extension
        if args[i] == "-ox" or args[i] == "--output-ext":
            try:
                assert not args[i + 1].startswith("-")
                webmOrMp4Output = args[i + 1]
            except Exception: printDefaultErrorMessage()
            i += 1
            continue

        # Audio extension
        if args[i] == "-ax" or args[i] == "--audio-ext":
            try:
                assert not args[i + 1].startswith("-")
                webmOrM4aAudio = args[i + 1]
            except Exception: printDefaultErrorMessage()
            i += 1
            continue

        # Video extension
        if args[i] == "-vx" or args[i] == "--video-ext":
            try:
                assert not args[i + 1].startswith("-")
                webmOrMp4Video = args[i + 1]
            except Exception: printDefaultErrorMessage()
            i += 1
            continue

        # Write thumbnail
        if args[i] == "--write-thumbnail":
            writeThumbnail = True
            continue

        # Write description
        if args[i] == "--write-description":
            writeDescription = True
            continue

        # Write subtitles
        if args[i] == "--write-sub":
            writeSub = True
            continue



print("********************")
print("* YoutubeDL Helper *")
print("********************")
print()

# Ask for the URL if not given in commandline options
if url == "":
    url = input("Please enter the URL of the video: ")

    print()

# Ask some things if there are no commandline options
if not optionsGiven:
    writeThumbnail = True if input("Download the thumbnail [y/N]? ").lower().startswith("y") else False
    writeDescription = True if input("Download the description [y/N]? ").lower().startswith("y") else False
    writeSub = True if input("Download the subtitle file [y/N]? ").lower().startswith("y") else False

    print()

    webmOrM4aAudio = "m4a" if input("Do you want the audio to be .webm or .m4a [W/m]? ").lower().startswith("m") else "webm"
    webmOrMp4Video = "mp4" if input("Do you want the video to be .webm or .mp4 [W/m]? ").lower().startswith("m") else "webm"
    webmOrMp4Output = "webm" if input("Do you want the audio and video COMBINED (the output) to be .webm or .mp4 [w/M]? ").lower().startswith("w") else "mp4"

    print()

ffmpegFlagCVCopy = True
if webmOrMp4Output == "webm" and webmOrMp4Video == "mp4":
    if os.name.endswith("ix"): os.system("tput setaf 228; tput bold")
    print("WARNING: The output extension is webm and the video extension is mp4. \n\
The combining will be slower, because ffmpeg doesn't want \"-c:v copy\" in this situation.")
    ffmpegFlagCVCopy = False
    if os.name.endswith("ix"): os.system("tput sgr0")
    print()

print("Please wait, getting information...")
# Get formats
ytdlFormats = os.popen("youtube-dl " + url + " -F").read()

print()

ytdlSoundFormats = "\n".join(filter(filter(ytdlFormats.split("\n"), "audio only"), webmOrM4aAudio))
allowedFormats = getAllowedFormats(ytdlSoundFormats)
print("Audio options:")
print("format code  extension  resolution note")
print(ytdlSoundFormats)
if len(ytdlSoundFormats) == 0: print("Congratulations, you softlocked yourself!")
print()

# Ask for format code of the audio
ytdlFormatCodeSound = input("Please enter the format code for the audio you want: ").strip()
while not ytdlFormatCodeSound in allowedFormats:
    print()
    print("I'm sorry Dave, I'm afraid I can't do that.")
    print()
    ytdlFormatCodeSound = input("Please enter the format code for the audio you want: ").strip()

print()

ytdlVideoFormats = "\n".join(filter(filter(ytdlFormats.split("\n"), "video only"), webmOrMp4Video)) # Magic
allowedFormats = getAllowedFormats(ytdlVideoFormats)
print("Video options:")
print("format code  extension  resolution note")
print(ytdlVideoFormats)
if len(ytdlVideoFormats) == 0: print("Congratulations, you softlocked yourself!")
print()

# Ask for format code of the video
ytdlFormatCodeVideo = input("Please enter the format code for the video you want: ").strip()
while not ytdlFormatCodeVideo in allowedFormats:
    print()
    print("I'm sorry Dave, I'm afraid I can't do that.")
    print()
    ytdlFormatCodeVideo = input("Please enter the format code for the audio you want: ").strip()


ytdlOptions = ("--write-thumbnail" if writeThumbnail else "") + (" --write-description" if writeDescription else "") + (" --write-sub" if writeSub else "")

# Set output filename to default if not set with commandline option
if outputFileName == "":
    outputFileName = os.popen("youtube-dl " + url + " --get-filename -f " + ytdlFormatCodeVideo).read().split(".")
    outputFileName = "".join(outputFileName[0:len(outputFileName) - 1])

print()
print("Downloading audio...")
os.system("youtube-dl " + url + " -f " + ytdlFormatCodeSound + " -o \"audio-" + outputFileName + "." + webmOrM4aAudio + "\" " + ytdlOptions)
if writeDescription:
    try:
        os.rename("audio-" + outputFileName + ".description", outputFileName + ".description")
    except:
        if os.name.endswith("ix"): os.system("tput setaf 228; tput bold")
        print("Something went wrong renaming the description.")
        if os.name.endswith("ix"): os.system("tput sgr0")
if writeThumbnail:
    try:
        os.rename("audio-" + outputFileName + ".webp", outputFileName + ".webp")
    except:
        if os.name.endswith("ix"): os.system("tput setaf 228; tput bold")
        print("Something went wrong renaming the thumbnail.")
        if os.name.endswith("ix"): os.system("tput sgr0")

print()
print("Downloading video...")
os.system("youtube-dl " + url + " -f " + ytdlFormatCodeVideo + " -o \"video-" + outputFileName + "." + webmOrMp4Video + "\"")

print()
print("Combining video and audio...")
# Give the user time to read the line above, because ffmpeg is too fast :)
time.sleep(0.25)
# The -c:v copy isn't necessary and it breaks the output (if the output extension is webm and the video-only extension is mp4), but it's slower without
# That's why it's disabled when the output extension is webm and the video-only extension is mp4
os.system("ffmpeg -i \"video-" + outputFileName + "." + webmOrMp4Video + "\" -i \"audio-" + outputFileName + "." + webmOrM4aAudio + "\"" +
    (" -c:v copy" if  ffmpegFlagCVCopy else "") + " \"" + outputFileName + "." + webmOrMp4Output + "\"")

print()

# Ask if user wants to delete the audio-only and video-only files if there are no commandline options
if not optionsGiven:
    deleteAV = False if input("Do you want to delete the \"audio-" + outputFileName + "." + webmOrM4aAudio + "\" and \"video-" + outputFileName + "." + webmOrMp4Video + "\" files [Y/n]? ").lower().startswith("n") else True
# Delete the audio-only and video-only files if wanted
if deleteAV:
    os.remove("audio-" + outputFileName + "." + webmOrM4aAudio)
    os.remove("video-" + outputFileName + "." + webmOrMp4Video)

# ffmpeg -i video.webm -i audio.webm -c:v copy -c:a aac output.mp4