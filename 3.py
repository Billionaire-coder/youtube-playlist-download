import yt_dlp
import sys
import os

def download_content(url, cookies_file_path=None):
    """
    Downloads content (single video or entire playlist) in the highest available quality.
    
    If content is a single video, it's saved as 'Title.mp4'.
    If content is a playlist, videos are saved into a folder named after the playlist title.
    """
    print(f"Attempting to download content from URL: {url}")
    
    # --- yt-dlp Options ---
    # This setup is suitable for both single videos and playlists.
    ydl_opts = {
        # 'bestvideo+bestaudio' ensures the highest quality stream is downloaded and merged.
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        # Output template:
        # If Playlist: uses %(playlist)s folder and %(playlist_index)s prefix.
        # If Single Video: uses just %(title)s.%(ext)s.
        'outtmpl': '%(extractor)s-%(id)s/%(title)s.%(ext)s' if 'playlist' not in url.lower() and 'list' not in url.lower() else '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
        
        'merge_output_format': 'mp4',
        'ignoreerrors': True, 
        'verbose': False, # Changed to False to reduce overwhelming output
        
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    if cookies_file_path and os.path.exists(cookies_file_path):
        ydl_opts['cookiefile'] = cookies_file_path
        print(f"Loading authentication cookies from file: {cookies_file_path}...")
    elif cookies_file_path:
        print(f"Warning: Cookies file not found at '{cookies_file_path}'. Proceeding without authentication.")


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ret_code = ydl.download([url])
        
        if ret_code == 0:
            print("\n*** Download complete! ***")
            print("Check the folder created in the script's directory.")
        else:
            print(f"\n*** Download Finished, but errors were reported. ***")
            print("If you provided a private link, ensure your cookies file is correct.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    
    playlist_url_input = input("Please enter the YouTube video or playlist URL: ")
    
    # Prompt for the cookies file path
    cookies_file_path_input = input("If the content is private, enter the full path to your Netscape-format cookie file (e.g., C:\\Users\\user\\cookies.txt). Otherwise, press Enter: ")

    url_to_use = playlist_url_input.strip()
    cookies_path_to_use = cookies_file_path_input.strip() if cookies_file_path_input else None
    
    if url_to_use:
        # The revised function handles both video and playlist links
        download_content(url_to_use, cookies_path_to_use)
    else:
        print("No URL provided. Exiting.")