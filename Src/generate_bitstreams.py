import os
import wave
import argparse
import numpy as np

def convert_bitstream(source_path:str, save_path:str):
    '''
    Convert the audio file to a bitstream and save it to the save_path

    Args:
        source_path (str): The path of the audio file
        save_path (str): The path to save the bitstream
    
    '''

    audio_file_name = source_path.rsplit(os.path.sep, 1)[1].split('.')[0]

    new_directory = os.path.join(save_path, audio_file_name)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    # Open the audio file
    with wave.open(source_path, 'rb') as wav_file:

        # Get the audio file parameters
        n_channels = wav_file.getnchannels()  # Get number of channels (1 for mono, 2 for stereo)
        n_frames = wav_file.getnframes()      # Number of audio frames
        sample_width = wav_file.getsampwidth()  # Sample width (bytes per sample)
        frame_rate = wav_file.getframerate()   # Frame rate
        size_of_audio = n_frames * n_channels * sample_width

        # Create a log file 

        with open(os.path.join(new_directory, f'{audio_file_name}.log'), 'w') as log_file:
            log_file.write(f'Number of channels: {n_channels}\n')
            log_file.write(f'Number of frames: {n_frames}\n')
            log_file.write(f'Sample width: {sample_width}\n')
            log_file.write(f'Frame rate: {frame_rate}\n')
            log_file.write(f'Size of audio: {size_of_audio}\n')
    
        # Read the audio file
        audio_data = wav_file.readframes(n_frames)

        # Convert the audio data to a numpy array
        audio_samples = np.frombuffer(audio_data, dtype=np.int16)

        # Separate the channels
        if n_channels == 2:
            # For stereo (2 channels), de-interleave the data
            left_channel = audio_samples[0::2]   # Take every second sample starting from the first
            right_channel = audio_samples[1::2]  # Take every second sample starting from the second
        else:
            # For mono (1 channel), just use the single channel
            left_channel = audio_samples
            right_channel = None

        # Save the bitstream

        left_channel_bits = [format(x & 0xFFFF, '016b') for x in left_channel]

        with open(os.path.join(new_directory, 'left_channel_bits.mem'), 'w') as f:
            for item in left_channel_bits:
                f.write("%s\n" % item)


        if right_channel is not None:
            right_channel_bits = [format(x & 0xFFFF, '016b') for x in right_channel]

            with open(os.path.join(new_directory, 'right_channel_bits.mem'), 'w') as f:
                for item in right_channel_bits:
                    f.write("%s\n" % item)


if __name__ == '__main__':
    
    args = argparse.ArgumentParser()
    args.add_argument('--source_path', type=str, help='The path of the audio file')
    args.add_argument('--save_path', type=str, help='The path to save the bitstream')

    args = args.parse_args()

    convert_bitstream(args.source_path, args.save_path)


