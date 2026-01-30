import os
from moviepy.editor import VideoFileClip, AudioFileClip

# --- Prerequisites ---
# This script requires the 'moviepy' library.
# Install it using:
# pip install moviepy
# Note: moviepy automatically uses FFmpeg, which may need to be installed separately
# on some systems if it's not detected (though usually moviepy handles this).

def merge_audio_to_video(video_path: str, audio_path: str, output_path: str):
    """
    Merges a new audio file into an existing video file, keeping the video properties.

    Args:
        video_path (str): The file path to the input video (e.g., 'input.mp4').
        audio_path (str): The file path to the input audio (e.g., 'new_track.mp3').
        output_path (str): The file path for the resulting merged video (e.g., 'output_merged.mp4').
    """
    print(f"--- Starting Merge Process ---")
    print(f"Input Video: {video_path}")
    print(f"Input Audio: {audio_path}")

    try:
        # 1. Load the video clip
        video_clip = VideoFileClip(video_path)
        
        # 2. Load the new audio clip
        audio_clip = AudioFileClip(audio_path)

        # 3. Ensure the audio duration matches the video duration
        # If the audio is shorter, it will loop. If longer, it will be cut.
        if audio_clip.duration > video_clip.duration:
             print(f"Cutting audio to match video duration ({video_clip.duration:.2f} seconds).")
             audio_clip = audio_clip.subclip(0, video_clip.duration)
        elif audio_clip.duration < video_clip.duration:
             # The new audio will play until it ends, and the video will continue without sound.
             print(f"New audio is shorter than the video. Audio will stop at {audio_clip.duration:.2f} seconds.")


        # 4. Set the new audio for the video clip
        final_clip = video_clip.set_audio(audio_clip)

        # 5. Write the final file, preserving video properties.
        # We use standard codecs (libx264 for video, aac for audio) for wide compatibility.
        print(f"Writing merged file to: {output_path}. This may take a moment...")
        
        final_clip.write_videofile(
            output_path,
            codec='libx264',           # Video codec (standard for MP4)
            audio_codec='aac',         # Audio codec (standard for MP4)
            temp_audiofile='temp-audio.m4a', # Temporary audio file for FFmpeg to use
            remove_temp=True,          # Clean up the temporary audio file
            # fps=video_clip.fps,      # You can explicitly set FPS if needed
            # threads=4                # Increase this for faster rendering
        )

        # 6. Close clips to free up resources
        audio_clip.close()
        video_clip.close()

        print(f"\n✅ Success! Video merged and saved to {output_path}")

    except FileNotFoundError:
        print("❌ Error: One or both input files were not found. Please check your paths.")
        print("Ensure you provide the correct, full file path for both inputs.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        print("Tip: If moviepy reports an error, ensure FFmpeg is correctly installed.")


if __name__ == "__main__":
    print("\n--- Audio/Video Merger Setup ---")
    
    # Get user inputs for file paths
    video_path = input("Enter the FULL path to the video file (e.g., C:/Users/Me/video.mp4): ")
    audio_path = input("Enter the FULL path to the audio file (e.g., C:/Users/Me/audio.mp3): ")
    
    # Prompt for the output file name, providing a sensible default
    default_output = "merged_output.mp4"
    output_path = input(f"Enter the name/path for the OUTPUT video (default: {default_output}): ")
    
    # Use the default output path if the user input is empty
    if not output_path.strip():
        output_path = default_output
    
    # Call the main function
    merge_audio_to_video(video_path.strip(), audio_path.strip(), output_path.strip())