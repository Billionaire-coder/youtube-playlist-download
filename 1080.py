import yt_dlp
import sys
import os

def download_playlist(playlist_url, cookies_file_path=None):
    """
    Downloads all videos in a YouTube playlist, limited to a maximum resolution of 1080p,
    merging video and audio streams into a single MP4 file.
    
    If a cookies file path is provided, it attempts to load login cookies for private content.

    The files are saved into a folder named after the playlist title.
    
    NOTE: FFmpeg must be installed and in your system's PATH for video/audio merging to work.
    """
    print(f"Attempting to download playlist from URL: {playlist_url}")
    
    # yt-dlp options dictionary
    ydl_opts = {
        # 1. Format and Resolution Limit (best separate video stream <= 1080p + best audio)
        'format': 'bestvideo[height<=1080]+bestaudio/best', 
        
        # 2. Output template: saves files into a folder named after the playlist title
        'outtmpl': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
        
        # 3. Merge output: This tells yt-dlp to use FFmpeg to combine video and audio
        #    into a single .mp4 container and automatically cleans up intermediate files.
        'merge_output_format': 'mp4',
        
        'ignoreerrors': True, # Continue downloading even if one video fails
        'verbose': True,
        
        # 4. Postprocessors
        'postprocessors': [
            {
                # Ensures the merged file is converted/finalized as .mp4
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
            # Adds metadata like title and uploader to the file
            {'key': 'FFmpegMetadata'}, 
            # REMOVED: {'key': 'ExecAfterRemovals', 'exec': 'rm {}'} - This caused the Windows error.
        ],
        
        # Suppress the completion message to handle success/failure manually
        'noprogress': False, 
    }

    if cookies_file_path:
        # This option tells yt-dlp to use a Netscape-formatted cookie file for authentication.
        ydl_opts['cookiefile'] = cookies_file_path
        print(f"Loading authentication cookies from file: {cookies_file_path}...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ydl.download returns 0 on success, and non-zero on error
            ret_code = ydl.download([playlist_url])
        
        # Check the return code to confirm actual success
        if ret_code == 0:
            print("\n*** Playlist download complete! ***")
            print("Check the new folder created in the script's directory.")
        else:
            print(f"\n*** Download Finished, but errors were reported. ***")
            print("Please check the output above for specific errors.")

    except Exception as e:
        # This catches general Python errors
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    
    playlist_url_input = input("Please enter the YouTube playlist URL: ")
    
    # Updated Prompt: Ask for the cookies file path
    cookies_file_path_input = input("If the playlist is private, please enter the full path to your Netscape-format cookie file (e.g., C:\\Users\\user\\youtube_cookies.txt). Otherwise, press Enter: ")

    # Prepare inputs
    url_to_use = playlist_url_input.strip()
    cookies_path_to_use = cookies_file_path_input.strip() if cookies_file_path_input else None
    
    if url_to_use:
        # Pass the cookies file path
        download_playlist(url_to_use, cookies_path_to_use)
    else:
        print("No URL provided. Exiting.")