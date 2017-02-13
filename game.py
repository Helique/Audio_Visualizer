import pygame, sys, wave, numpy, struct, Queue, math, time as tm
from pygame.locals import *



def fftMag(fftResult):
    magnitudes = []
    reals = numpy.real(fftResult)
    imaginary = numpy.imag(fftResult)
    for i in range(len(fftResult)):
        magnitudes.append(math.sqrt(reals[i]**2 + imaginary[i]**2))
    return magnitudes

def getAudioFrames(wav, start, length):
    #wav.setpos(start)
    startPosition = wav.tell()
    leftSamples = []
    for i in range(length):
        currentFrame = wav.readframes(1)
        leftString = currentFrame[:2]
        rightString = currentFrame[2:]
        leftSample = struct.unpack("<h", leftString)
        #print "{},{}".format(ord(currentFrame[0]),ord(currentFrame[1]))
        #print leftSample
        #print type(leftSample)
        leftSamples.append(leftSample[0])
        #rightSample = struct.unpack("<h", rightString)
    return leftSamples, startPosition,start

def getVideoFrames(fps, wav, duration, fftSize):
    videoFrames = []
    audioSamples = []
    numVFrames = duration * fps
    lastStart = 0
    toRead = 0;
    for i in range(numVFrames):
        secondStart = i/float(fps)
        audioSampleStart = secondStart * 44100
        lastStart = audioSampleStart
        wav.readframes(toRead)
        audioSamples,a,b = getAudioFrames(wav,audioSampleStart,fftSize)
        toRead = int(audioSampleStart - a)

        fftResult = numpy.fft.rfft(audioSamples)
        fftMagnitude = fftMag(fftResult)
        for i in range(len(fftMagnitude)):
            fftMagnitude[i] = fftMagnitude[i]/2500
        videoFrames.append(fftMagnitude)
    print "VideoFrames: {}".format(len(videoFrames))
    return videoFrames

def main(wavFileName, numBins, fps):
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((numBins/2*7+20, 500))
    pygame.display.set_caption('Audio Analyzer')

    WHITE = (255, 255, 255)
    GREEN = (  0, 255,   0)
    BLUE  = (  0,   0, 128)

    mixer = pygame.mixer.init(frequency=22050, size=16, channels=2, buffer=(32*1024))

    wav = wave.open(wavFileName)
    numberOfFrames = wav.getnframes()
    videoClock = pygame.time.Clock()

    runningTime = numberOfFrames/wav.getframerate()
    print "Framerate:    {}".format(wav.getframerate())
    print "Samples:      {}".format(numberOfFrames)
    print "Sample Width: {}".format(wav.getsampwidth())
    print "Num Chanels:  {}".format(wav.getnchannels())
    print "Running Time: {}".format(runningTime)
    sound = pygame.mixer.Sound(file=wavFileName)

    window = []

    videoFrames = getVideoFrames(fps, wav, runningTime, numBins)


    sound.play()
    pygame.mixer.pause()
    garbage  = True
    startTime = pygame.time.get_ticks()
    msBetween = (1/float(fps))*1000;
    numVFrames = runningTime * fps
    pygame.mixer.unpause()
    while True:
        DISPLAYSURF.fill(WHITE)
        time = pygame.time.get_ticks()-startTime
        frameNumber = int(time/(msBetween)) - 10

        if(frameNumber>0 and frameNumber<numVFrames):
            for i in range(len(videoFrames[frameNumber])):
                pygame.draw.rect(DISPLAYSURF,BLUE,[i*7,50,5,(videoFrames[frameNumber][i])])
        elif(frameNumber>0):
            startTime = pygame.time.get_ticks()
            sound.play()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        videoClock.tick(fps)

        #print videoClock.get_fps()

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print "Usage: ./game.py <wavefile> <fftsize> <fps>"
    if(int(sys.argv[2]) < 16 or int(sys.argv[2]) > 1024):
        print "fftsize should be between 16 and 1024 inclusive"
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
