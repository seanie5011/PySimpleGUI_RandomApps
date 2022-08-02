from pytube import YouTube

class PytubeDownloader():
    def on_complete(self, stream, file_path):
        return stream, file_path

    def on_progress(self, stream, chunk, bytes_remaining):
        return bytes_remaining, stream.filesize

    def main(self):
        video_object = YouTube('https://www.youtube.com/watch?v=ESLt3h764HE&list=LL&index=3&ab_channel=Tf2.boo.2', 
                               on_complete_callback=self.on_complete, 
                               on_progress_callback=self.on_progress
                               )

        # video information
        print(video_object)
        print(video_object.title)
        print(video_object.length)
        print(video_object.views)
        print(video_object.author)
        print(video_object.description)

        # video streams
        # progressive video streams combine both video and audio but thus usually lack in resolution
        # adaptive (or dash) streams seperate the two but are usually of higher quality
        # abr is the bitrate or bytes/s when downloading
        print("---------------------------------")
        for stream in video_object.streams:
            print(stream)

        print("---------------------------------")
        print("All progressive: ", video_object.streams.filter(progressive=True))
        print("---------------------------------")
        print("All adaptive: ", video_object.streams.filter(adaptive=True))
        print("---------------------------------")
        print("All audio: ", video_object.streams.filter(only_audio=True))
        print("---------------------------------")
        print("All mp4: ", video_object.streams.filter(file_extension='mp4'))
        print("---------------------------------")
        print("All progressive mp4: ", video_object.streams.filter(progressive=True, file_extension='mp4'))
        print("---------------------------------")
        print("All progressive mp4 audio: ", video_object.streams.filter(progressive=True, file_extension='mp4', only_audio=True))  # expect to be none
        print("---------------------------------")

        # download a file
        print(video_object.streams.get_by_itag(140).filesize)
        video_object.streams.get_by_itag(140).download(output_path='testing')

pytubing = PytubeDownloader()
pytubing.main()