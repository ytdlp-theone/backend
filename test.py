import yt_dlp

def download_video(url, download_path="."):
    try:
        # Define the options for yt-dlp
        ydl_opts = {
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # Save video with its title and proper extension
            'noplaylist': True,  # Don't download playlist if URL is a playlist
        }

        # Initialize yt-dlp with the specified options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information (including available formats)
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

            # Categorize formats by extension type
            formats_by_extension = {'mp4': [], 'webm': [], 'other': []}

            # Categorize formats based on their extension
            for fmt in formats:
                ext = fmt.get('ext')
                if ext == 'mp4':
                    formats_by_extension['mp4'].append(fmt)
                elif ext == 'webm':
                    formats_by_extension['webm'].append(fmt)
                else:
                    formats_by_extension['other'].append(fmt)

            # Ask the user which extension they want
            print("Choose the extension type you want to download:")
            print("1. MP4")
            print("2. WEBM")
            print("3. Other")
            extension_choice = int(input("Enter the number of the extension you want (1-3): "))

            # Get the list of formats based on the user's choice
            if extension_choice == 1:
                selected_formats = formats_by_extension['mp4']
            elif extension_choice == 2:
                selected_formats = formats_by_extension['webm']
            elif extension_choice == 3:
                selected_formats = formats_by_extension['other']
            else:
                print("Invalid choice. Exiting.")
                return

            # If no formats are available in the chosen category
            if not selected_formats:
                print(f"No formats available for {['MP4', 'WEBM', 'Other'][extension_choice - 1]} extension.")
                return

            # List available formats within the selected extension category
            print(f"Available formats for {'MP4' if extension_choice == 1 else 'WEBM' if extension_choice == 2 else 'Other'}:")
            for i, fmt in enumerate(selected_formats):
                format_id = fmt.get('format_id')
                resolution = fmt.get('height', 'N/A')  # Resolution or 'N/A' if not available
                print(f"{i+1}. Format ID: {format_id}, Resolution: {resolution}p, Extension: {fmt['ext']}")

            # Ask the user to select a format
            choice = int(input(f"Enter the number of the format you want to download (1-{len(selected_formats)}): "))
            selected_format = selected_formats[choice - 1]

            # Download the selected format
            selected_format_id = selected_format.get('format_id')
            print(f"Downloading video in selected format: {selected_format_id}...")
            ydl_opts['format'] = selected_format_id  # Set the selected format in options

            # Initialize yt-dlp with the updated options and download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print("Download complete!")

    except Exception as e:
        print(f"Error: {e}")

# Example Usage
video_url = input("Enter the YouTube video URL: ")
download_video(video_url, download_path="path_to_save_video")  # Specify the path where you want to save
