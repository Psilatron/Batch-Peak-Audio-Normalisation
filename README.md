# Batch-Peak-Audio-Normalisation
A python script which will batch process .wav files and carry out peak normalisation using a gain value in dBFS defined by the user.

This script will process a directory of .wav files in either mono or stereo format and normalise their peaks based on the value set by by the user. 

Stereo audio files will be normalised by using the peak value taken from channel with the highest peak as a reference. That means that if the one channel has a lower peak than the other this difference will be preserved and scaled accordingly.


## How to use
Run BatchPeakWavNormalise.py. You will prompted to enter a target normalisation value in dBFS. There are no restrictions on the normalization value, however a gain > 0 will result in distortion; for standard operation keep this value 0dB or below, and ensure that you include -ve sign for negative values.

After entering desired normalisation value, use the popup window to choose the location of you .wav files. The normalised files will be written to directory 'OUTPUT' within the chosen directory.

Wav files will be automatically detected as mono or stereo. 

## Requirements and info
- Files do not need to be the same sample rate.
- Only mono and Stereo supported. Multi channel .wav files can exist amongst other mono and stereo files in input director, however these will be ignored.
- A log file detailing information about the normalisation process will be written in the OUTPUT directory.
- If silent tracks are detected a warning will be written to the log.
