import wave, numpy, struct, Queue, math, time as tm
#from pygame.locals import *
#def fftMag(fftResult):
#    magnitudes = []
#    reals = numpy.real(fftResult)
#    imaginary = numpy.imag(fftResult)
#    for i in range(len(fftResult)):
#        magnitudes.append(math.sqrt(reals[i]**2 + imaginary[i]**2))
#    return magnitudes

def getAudioFrames(wav, start, length, endianess):
    wav.setpos(start)
    startPosition = wav.tell()
    leftSamples = []
    for i in range(length):
        currentFrame = wav.readframes(1)
        print start+i, hex(ord(currentFrame[0])), hex(ord(currentFrame[1])), hex(ord(currentFrame[2])), hex(ord(currentFrame[3]))
        leftString = currentFrame[:2]
        #rightString = currentFrame[2:]
        leftSample = struct.unpack(endianess, leftString)
        print hex(ord(leftString[0])), hex(ord(leftString[1]))
        print leftSample[0]
        #print "{},{}".format(ord(currentFrame[0]),ord(currentFrame[1]))
        #print leftSample
        #print type(leftSample)
        leftSamples.append(leftSample[0])
        #rightSample = struct.unpack("<h", rightString)
    return leftSamples, startPosition,start


def main():

    #mixer = pygame.mixer.init(frequency=22050, size=16, channels=2, buffer=(8*4096))
    #wav = wave.open("solo2.wav")
    wav = wave.open("SimpleSine.wav", 'r')
    numberOfFrames = wav.getnframes()
    print "Framerate:    {}".format(wav.getframerate())
    print "Samples:      {}".format(numberOfFrames)
    print "Sample Width: {}".format(wav.getsampwidth())
    print "Num Chanels:  {}".format(wav.getnchannels())
    window = []
    videoFrames = []
    fps = 30
    seconds = 4
    numVFrames = seconds * fps
    problemSamples = [11,21,22,42,44,69,73,84,88]
    #problemSamples = [1,55,11,21,22,42,44,69,73,84,88]
    problemSet = set(problemSamples)
    for i in problemSamples:
        secondStart = i/float(fps)
        audioSampleStart = secondStart * 44100
        audioSamples,a,b = getAudioFrames(wav,audioSampleStart,1024, ">h")
        if(i in problemSet):
            print "{0}, {1}, {2}, {3}:".format(i,audioSampleStart,a,b)
            print audioSamples
        #print "secondStart: {} audioSampleStart: {}".format(secondStart, audioSampleStart)
        #print audioSamples
        #fftResult = numpy.fft.rfft(audioSamples)
        #fftMagnitude = fftMag(fftResult)
        #for k in range(len(fftMagnitude)):
        #    fftMagnitude[k] = fftMagnitude[k]/5000
        #videoFrames.append(fftMagnitude)


if __name__ == "__main__":
    main()
