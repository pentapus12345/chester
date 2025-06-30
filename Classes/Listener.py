import sys
import sounddevice as sd
import time
import sherpa_ncnn
import numpy as np
from scipy.signal import resample

class Listener(object):
    def __init__(self):
        model_path = "../sherpa-ncnn/sherpa-ncnn-streaming-zipformer-20M-2023-02-17"
        self.recognizer = sherpa_ncnn.Recognizer(
            tokens=f"{model_path}/tokens.txt",
            encoder_param=f"{model_path}/encoder_jit_trace-pnnx.ncnn.param",
            encoder_bin=f"{model_path}/encoder_jit_trace-pnnx.ncnn.bin",
            decoder_param=f"{model_path}/decoder_jit_trace-pnnx.ncnn.param",
            decoder_bin=f"{model_path}/decoder_jit_trace-pnnx.ncnn.bin",
            joiner_param=f"{model_path}/joiner_jit_trace-pnnx.ncnn.param",
            joiner_bin=f"{model_path}/joiner_jit_trace-pnnx.ncnn.bin",
            num_threads=4,
        )
        self.mic_rate = 48000 
        self.mic_index = 0
        self.verbose = False
        self.print_to_screen=False

    def setVerbose( self, verbose: bool)->None:
        self.verbose = verbose
    
    def set_print_to_screen(self, print_to_screen: bool):
        self.print_to_screen = print_to_screen


    def listen(self, silence_timeout: float = 2.0) -> str:
        """
        Block until the user stops speaking for `silence_timeout` seconds.
        Return the final recognised text (may be "").
        """
        window   = 0.1                                    # seconds per chunk
        frames   = int(window * self.mic_rate)
        last_txt = ""
        last_t   = None

        with sd.InputStream(device=self.mic_index,
                        samplerate=self.mic_rate,
                        channels=1,
                        dtype="float32") as stream:
            if self.verbose:
                print("🎙  Listening…")
            while True:
                buf, _ = stream.read(frames)
                mono   = np.squeeze(buf)

                pcm = resample(mono, int(len(mono) * 16000 / self.mic_rate)).astype("float32")
                self.recognizer.accept_waveform(16000, pcm)

                text = self.recognizer.text
                now  = time.monotonic()

                # Voice activity whenever recogniser's partial text changes
                if text and text != last_txt:
                    last_txt = text
                    last_t   = now
                    if self.verbose:
                       print("🗣️ ", text)

                # If we've been idle > silence_timeout s, stop and return result
                if last_t is not None and (now - last_t) > silence_timeout:
                    if self.verbose:
                        print(f"🛑  {silence_timeout}s silence – final: {last_txt}")
                    clean = last_txt.strip().upper()
                    self.recognizer.reset()
                    if self.print_to_screen:
                        print( f"You: {clean}")
                    return clean
                


    f="""
    def listen(self)->str:
        sample_rate = self.recognizer.sample_rate
        samples_per_read = int(0.1 * self.recognizer.sample_rate) #100 ms
        last_result = ""
        with sd.InputStream(
             channels=1, dtype="float32", samplerate=sample_rate
        ) as s:
            while True:
                samples, _ = s.read(samples_per_read)
                samples = samples.reshape(-1)
                self.recognizer.accept_waveform(sample_rate, samples)
                result = self.recognizer.text

                if last_result != result:
                    last_result = result
                    print( result )"""