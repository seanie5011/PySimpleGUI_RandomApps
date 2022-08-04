import PySimpleGUI as sg
from pytube import YouTube
import datetime


class VideoDownloader():
    def on_complete(self, stream, file_path):
        return stream, file_path

    def on_progress(self, stream, chunk, bytes_remaining):
        return bytes_remaining, stream.filesize

    def get_details(self, url):
        ''' Takes in a YouTube url and returns a list of details associated with it.
        '''

        try:
            video_object = YouTube(url,
                                   on_complete_callback=self.on_complete,
                                   on_progress_callback=self.on_progress
                                   )
        except:
            print()
            # exception is a list of same length but full of ERROR
            return ["ERROR" for i in range(5)]
        else:  # if no exception, run this block
            self.video_object = video_object

            length = str(datetime.timedelta(seconds=video_object.length))  # converts the seconds into hours:minutes:seconds format

            details_list = [
                video_object.title,
                video_object.author,
                length,
                str(video_object.views),
                video_object.description
                ]

            return details_list

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
        #print(video_object.streams.get_by_itag(140).filesize)
        #video_object.streams.get_by_itag(140).download(output_path='testing')


def string_skipper(text, max_length):
    '''
    Takes in a string and seperates it by linebreak into 'word's
    Adds a new linebreak on any 'word' if it is > max_length
    Returns new string after recombining
    '''

    words = text.split('\n')
    words = [word + '\n' for word in words]  # split removes the \n so put em back

    new_words = []
    for word in words:
        end_new_word = word
        # make sure this part of the word is below threshold, if not, cut and append to new words
        while len(end_new_word) > max_length:
            start_new_word = end_new_word[:max_length] + "\n"
            end_new_word = end_new_word[max_length:]

            new_words.append(start_new_word)

        new_words.append(end_new_word)

    new_text = ''.join(new_words)[:-2]  # turn list into a string, remove last two letters as we have accidentally added an extra "\n"

    return new_text


def main():
    # settings and other options
    details_size = (9, 1)

    # layouts
    video_details_layout = [
        [sg.Text('Title:', size=details_size),       sg.Text('', key='-TITLE-', expand_x=True, relief='sunken')],
        [sg.Text('Channel:', size=details_size),     sg.Text('', key='-CHANNEL-', expand_x=True, relief='sunken')],
        [sg.Text('Length:', size=details_size),      sg.Text('', key='-LENGTH-', expand_x=True, relief='sunken')],
        [sg.Text('Views:', size=details_size),       sg.Text('', key='-VIEWS-', expand_x=True, relief='sunken')],
        [sg.Text('Description:', size=details_size), sg.Text('', key='-DESCRIPTION-', expand_x=True, relief='sunken')]
        ]

    tab1_layout = [
        [sg.Text('url:'), sg.Input(key='-URL_IN-', expand_x=True), sg.Button('Enter', key='-URL_BTN-')],
        [sg.Frame('Video Details', video_details_layout, expand_x=True)]
        ]

    tab2_layout = [
        [sg.T('This is inside tab 2')]
        ]

    layout = [
        [sg.TabGroup([
            [sg.Tab('Details', tab1_layout), sg.Tab('Downloads', tab2_layout)]
            ])]
        ]

    window = sg.Window('Video Downloader', layout)

    # downloader class
    downloader = VideoDownloader()

    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED:
            break

        # enter url
        if event == '-URL_BTN-':
            url = values['-URL_IN-']
            new_details = downloader.get_details(url)  # get all the details of video
            for index, detail in enumerate(video_details_layout):  # look at the lists in list
                text = detail[1]  # get the text element we want to edit, ignoring first (the static text)
                display_text = string_skipper(new_details[index], 80)  # add new lines if strings are too long
                window[text.key].update(display_text)

    window.close()

if __name__ == '__main__':
    main()
