import sounddevice as sd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time

from scipy.io.wavfile import read, write
from numpy.fft import rfft, rfftfreq, irfft, fft, fftfreq, ifft

class SoundBoard:
    '''SoundBoard class. You may assume the user will only want one sound stored at a time - i.e. loading
    from a file and then recording from your microphone overwrites the sound data. However, if you want
    to make your SoundBoard class more generic you are free to do so.'''

    def __init__(self, sample_rate=44100, channels=1, freq=440, time=1):
        '''Initialization of internal variables. sample_rate is expected to be in Hz.
        Initializes with a 1sec 440Hz pure tone.'''
        self.channels = channels
        self.sample_rate = sample_rate
        self.time = time
        times = np.linspace(0,self.time, int(self.time * self.sample_rate))
        self.data = np.sin(2*np.pi*freq*times)
        pass

    def rec(self, sample_rate=44100, time=1):
        '''Make a recording from your microphone. Saves this internally as a numpy array. 
        Time is by default 1s'''
        self.data = sd.rec(time*sample_rate, channels= self.channels, samplerate= sample_rate, blocking=True)[:,0]
        self.time = time
        pass
    
    def play(self):
        '''Play the currently stored sound.'''
        sd.play(self.data, self.sample_rate, blocking=True)
        pass
    
    def save(self, path="sound.wav"):
        '''Saves the current sound data to the location inputted in path. If not provided, saves as 
        "sound.wav" to the same directory as this Jupyter Notebook is stored.'''
        write(path, self.sample_rate, self.data)
        pass
    
    def load(self, path):
        '''Takes in a string corresponding to the path to a .wav file. Loads the file into a numpy array
        internally saved to the SoundBoard class. Returns nothing'''
        file = read(path)
        self.sample_rate = file[0]
        self.data = file[1]
        self.time = len(file[1])/self.sample_rate
        pass    
    
    def reverse(self):
        '''Reverse the sound.'''
        self.data = self.data[::-1]
        pass
    
    def speed_up(self, factor):
        '''Speeds up or slows down the sound by the amount factor such that, if the sound is 1s long, it 
        will now be factor*1s long.'''       
        new_times = np.linspace(0, len(self.data)/self.sample_rate, int(len(self.data)*factor))
        self.data = np.interp(new_times, self.get_time(), self.data)
        self.time = factor*self.time
        pass
    
    def get_time(self):
        '''Returns the time array over which the sound array was sampled using the sampling rate.'''
        times = np.linspace(0, len(self.data)/self.sample_rate, len(self.data))
        return times
    
    def high_filter(self, cutoff):
        '''Performs a high-pass filter on sound data. This should simulate the passive analog high-pass
        filter. (i.e. the one using capacitors and resistors). Assumes a gain of 1.'''        
        # Make a new copy of the original waveform FFT
        fft_filt = np.fft.fftshift(np.fft.fft(self.data))
        freq_bins = np.linspace(-self.sample_rate,self.sample_rate,int(self.sample_rate*self.time))
        # Get the indices of frequencies lower than +/- cutoff Hz
        filt_ind=np.where(np.abs(freq_bins)<cutoff)
        # Then set the fft to zero for the indices you found above. This is an "ugly" filter since the cut-off is sharp
        # but it's the clearest to see what is happening in frequency space
        fft_filt[filt_ind] = 0
        self.data = np.real(np.fft.ifft(np.fft.fftshift(fft_filt)))
        pass
    
    def low_filter(self, cutoff):
        '''Performs a low-pass filter on sound data. This should simulate the passive analog low-pass
        filter. (i.e. the one using capacitors and resistors). Asssumes a gain of 1'''
        # Make a new copy of the original waveform FFT
        fft_filt = np.fft.fftshift(np.fft.fft(self.data))
        freq_bins = np.linspace(-self.sample_rate,self.sample_rate,int(self.sample_rate*self.time))
        # Get the indices of frequencies larger than +/- cutoff Hz
        filt_ind=np.where(np.abs(freq_bins)>cutoff)
        # Then set the fft to zero for the indices you found above. This is an "ugly" filter since the cut-off is sharp
        # but it's the clearest to see what is happening in frequency space
        fft_filt[filt_ind] = 0
        self.data = np.real(np.fft.ifft(np.fft.fftshift(fft_filt)))
        pass
    
    def scale(self, amp):
        '''Scale the entire sound array by an amplitude. This effectively changes the volume.'''
        self.data = amp * self.data
        pass
    
    def game(self, listen_time = 5):
        """Name Reversing Game Code. Time is the length of time the machine will listen for"""
        print("I'm going to try to say your name back to you reversed.")
        time.sleep(3)
        print("Please say your name when I tell you 'Go!'")
        time.sleep(1)
        print("I will listen for", listen_time,"seconds.")
        time.sleep(1)
        print("Ready...")
        time.sleep(1)
        print("Get Set...")
        time.sleep(1)
        print("Go!")

        board.rec(time = listen_time)
        board.reverse()
        print("Got it!")
        time.sleep(1)
        print("Your name backwards sounds like...")
        time.sleep(1)

        board.play()