from tts import TextToSpeech

if __name__ == '__main__':
    a = TextToSpeech()
    wav = a.post('haha', 'a.wav')
    print '-'*100
    a.play(filename='a.wav')
