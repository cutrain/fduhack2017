class TextToSpeech(object):
    def __init__(self):
        self.username = '"a0f66f19-c4de-49d5-b55f-1dd175c41328"'
        self.password = '"uSgWeUmAIOsl"'
        self.header = ['"Content-Type: application/json"', '"Accept: audio/wav"']
        self.method = "POST"
        self.api = '"https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"'

    def post(self, text, outfile=None):
        """
        curl -X POST -u "a0f66f19-c4de-49d5-b55f-1dd175c41328":"uSgWeUmAIOsl" --header "Content-Type: application/json" --header "Accept: audio/wav" --data "{\"text\":\"hello world\"}" --output hello_world.wav "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"
        """
        cmd = 'curl -X %s -u %s:%s --header %s --header %s --data "{\\"text\\":\\"%s\\"}" ' % (self.method, self.username, self.password, self.header[0], self.header[1], text)
        if outfile is not None:
            cmd += '--output %s ' % outfile
        cmd += '%s' % self.api
        import subprocess
        ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        retval = ret.wait()
        if outfile:
            return retval
        return ret.stdout.read()

    def play(self, istream=None, filename=None):
        try:
            if filename is not None:
                with open(filename, 'rb') as f:
                    istream = f.read()
            import pyaudio
            import wave
            import sys

            CHUNK = 1024

            # instantiate PyAudio (1)
            with open('temp.wav', 'wb') as f:
                f.write(istream)
            wf = wave.open('temp.wav', 'rb')
            print 1
            p = pyaudio.PyAudio()
            print 2

            # open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            print 3
            data = wf.readframes(CHUNK)
            print 4

            # play stream (3)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(CHUNK)

            print 5
            # stop stream (4)
            stream.stop_stream()
            stream.close()

            # close PyAudio (5)
            print 6
            p.terminate()
            print 'finish'
        except IOError as e:
            pass


