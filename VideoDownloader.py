import PySimpleGUI as sg
from pytube import YouTube
import datetime
import math


class VideoDownloader():
    def __init__(self):
        self.video_object = None

    def on_complete(self, stream, file_path):
        return stream, file_path

    def on_progress(self, stream, chunk, bytes_remaining):
        return bytes_remaining, stream.filesize

    def get_video_details(self, url):
        ''' Takes in a YouTube url and returns a list of details associated with it.
        '''

        try:
            video_object = YouTube(url,
                                   on_complete_callback=self.on_complete,
                                   on_progress_callback=self.on_progress
                                   )
        except:
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

    def get_stream_details(self, stream):
        ''' Get all relevant stream details like:
        tag, adaptive/progressive, video/audio, filetype,
        filesize, resolution || bitrate
        '''

        try:  # if stream.tag fails then stream is invalid, otherwise likely fine
            tag = str(stream.itag)  # is returned as int
        except:
            # exception is a list of same length but full of ERROR
            return ["ERROR" for i in range(6)]
        else:
            # whether stream is progressive or adaptive
            if stream.is_adaptive:
                ad_pro = 'adaptive'
            else:
                ad_pro = 'progressive'

            # whether has video, audio or both - set resolution and bitrate accordingly
            if stream.includes_audio_track and stream.includes_video_track:  # if has both
                vid_aud = 'both'
                res_bit = stream.resolution
            elif stream.includes_audio_track:  # audio has bitrate but not resolution
                vid_aud = 'audio'
                res_bit = stream.abr
            else:  # must be video
                vid_aud = 'video'
                res_bit = stream.resolution

            filetype = stream.subtype

            # filesize - get order of number and seperate into kilobytes, megabytes, gigabytes
            unfiltered_filesize = stream.filesize  # int
            order = int(math.floor(math.log10(unfiltered_filesize)))  # rounds order to lowest and casts int

            unit = 'B'  # default unit is byte
            if order >= 9:
                unfiltered_filesize *= 1e-9
                unit = 'GB'
            elif order >= 6:
                unfiltered_filesize *= 1e-6
                unit = 'MB'
            elif order >= 3:
                unfiltered_filesize *= 1e-3
                unit = 'KB'

            filesize = str(round(unfiltered_filesize, 1)) + unit  # round it to 1 decimal place

            stream_details = [[tag], [ad_pro], [vid_aud], [filetype], [filesize], [res_bit]]
            return stream_details

    def filter_streams(self, pro=None, ad=None, aud=None, mp4=None):
        ''' Returns the streams object with filters applied
        '''

        # if it is an mp4 file, set necessary string
        if mp4:
            mp4 = 'mp4'

        filtered_streams = self.video_object.streams.filter(progressive=pro, adaptive=ad, subtype=mp4, only_audio=aud)
        return filtered_streams

    def download_stream(self, tag, path):
        ''' Downloads the video specified by the tag to the path specified
        '''

        try:  # any error just dont do it
            video = self.video_object.streams.get_by_itag(tag)
            video.download(output_path=path)
        except:
            return


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

    new_text = ''.join(new_words)[:-1]  # turn list into a string, remove last two letters as we have accidentally added an extra "\n"

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

    table_header = [['tag'], ['progressive/adaptive'], ['video/audio'], ['filetype'], ['filesize'], ['resolution/bitrate']]  # row 0 of headers
    col_widths = [4, 16, 12, 8, 12, 16]  # widths of each column in order

    tab2_layout = [
        [sg.Text('Filters: '), sg.Button('progressive', key='-PRO_BTN-'), sg.Button('adaptive', key='-AD_BTN-'), sg.Button('audio', key='-AUD_BTN-'), sg.Button('mp4', key='-MP4_BTN-')],
        [sg.Table([], headings=table_header, key='-STREAMS-', justification='center', col_widths=col_widths, auto_size_columns=False, expand_x=True, expand_y=True)],
        [sg.Text('Tag: '), sg.Input(key='-TAG_IN-', expand_x=True), sg.Button('Download', key='-DOWN_BTN-')]
        ]

    layout = [
        [sg.TabGroup([
            [sg.Tab('Details', tab1_layout), sg.Tab('Downloads', tab2_layout)]
            ])]
        ]

    window = sg.Window('Video Downloader', layout)

    # downloader class
    downloader = VideoDownloader()

    # variables to decide filtering
    pro = False
    ad = False
    aud = False
    mp4 = False

    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED:
            break

        # enter url
        if event == '-URL_BTN-':
            # tab1: get video details
            url = values['-URL_IN-']
            new_details = downloader.get_video_details(url)  # get all the details of video
            for index, detail in enumerate(video_details_layout):  # look at the lists in list
                text = detail[1]  # get the text element we want to edit, ignoring first (the static text)
                display_text = string_skipper(new_details[index], 80)  # add new lines if strings are too long
                window[text.key].update(display_text)

            # tab2: get all stream details
            old_rows = []
            for stream in downloader.video_object.streams:
                add_row = downloader.get_stream_details(stream)

                old_rows.append(add_row)
                window['-STREAMS-'].update(old_rows)

        # filter buttons
        if event == '-PRO_BTN-':
            pro = not pro
            ad = False  # cant have adaptive and progressive
        if event == '-AD_BTN-':
            ad = not ad
            pro = False
        if event == '-AUD_BTN-':
            aud = not aud
        if event == '-MP4_BTN-':
            mp4 = not mp4
        # now perform filtering
        streams = downloader.filter_streams(pro=pro, ad=ad, aud=aud, mp4=mp4)

        old_rows = []
        for stream in streams:
            add_row = downloader.get_stream_details(stream)

            old_rows.append(add_row)
            window['-STREAMS-'].update(old_rows)

        # download button
        if event == '-DOWN_BTN-':
            try:
                tag = int(values['-TAG_IN-'])
            except ValueError:  # if input value is not int-like
                print("ValueError: the value inputted is not of correct form type float.")
            else:
                path = sg.popup_get_folder('Select Folder', no_window=True)
                downloader.download_stream(tag, path)

    window.close()

if __name__ == '__main__':
    main()
