from tts import TextToSpeech

if __name__ == '__main__':
    a = TextToSpeech()
    wav = a.post('haha')
    print '-'*100
    print wav
    print '-'*100
    a.play(istream=wav)
