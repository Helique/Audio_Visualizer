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
    wav.setpos(start)
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
    return leftSamples


def main():
    # my code here
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((1799, 300))
    pygame.display.set_caption('Hello, world!')

    WHITE = (255, 255, 255)
    GREEN = (  0, 255,   0)
    BLUE  = (  0,   0, 128)

    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('Hello, world!', True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)

    mixer = pygame.mixer.init(frequency=22050, size=16, channels=2, buffer=(8*4096))
    wav = wave.open("solo2.wav")
    numberOfFrames = wav.getnframes()
    videoClock = pygame.time.Clock()
    print "Framerate:    {}".format(wav.getframerate())
    print "Samples:      {}".format(numberOfFrames)
    print "Sample Width: {}".format(wav.getsampwidth())
    print "Num Chanels:  {}".format(wav.getnchannels())

    print "Time: {}".format(TIMER_RESOLUTION)
    '''for i in range(numberOfFrames):
        currentFrame = wav.readframes(1)
        leftString = currentFrame[:2]
        rightString = currentFrame[2:]
        leftSample = struct.unpack("<h", leftString)
        rightSample = struct.unpack("<h", rightString)
        #leftSample = (ord(currentFrame[0]) << 8) + ord(currentFrame[1])
        #rightSample = (ord(currentFrame[2]) << 8) + ord(currentFrame[3])
        ##print("{},{}".format(leftSample, rightSample))
    '''
    sound = pygame.mixer.Sound(file="solo2.wav")

    #mixer.play()
    window = []
    videoFrames = []
    fps = 30
    seconds = 4
    numVFrames = seconds * fps
    for i in range(numVFrames):
        secondStart = i/float(fps)
        audioSampleStart = secondStart * 44100
        audioSamples = getAudioFrames(wav,audioSampleStart,1024)
        #print "secondStart: {} audioSampleStart: {}".format(secondStart, audioSampleStart)
        #print audioSamples
        fftResult = numpy.fft.rfft(audioSamples)
        fftMagnitude = fftMag(fftResult)
        videoFrames.append(fftMagnitude)

        #print fftMagnitude
        #print len(fftMagnitude)

    print "VideoFrames: {}".format(len(videoFrames))

    sound.play()
    startTime = pygame.time.get_ticks()
    msBetween = (1/float(fps))*1000;

    while True:
        DISPLAYSURF.fill(WHITE)
        #DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        time = pygame.time.get_ticks()-startTime
        frameNumber = int(time/msBetween)
        if(frameNumber<120):
            for i in range(len(videoFrames[frameNumber])):
                pygame.draw.rect(DISPLAYSURF,BLUE,[i*7,50,5,videoFrames[frameNumber][i]])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        videoClock.tick(30)

        #print videoClock.get_fps()

if __name__ == "__main__":
    main()
