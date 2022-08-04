# PySimpleGUI_RandomApps

## This project contains various apps with GUI created using PySimpleGUI

This project is an umbrella containing various apps using PySimpleGUI. These are small apps, with basic functions. They are listed as follows:

1. [UnitConverter.py](#unitconverterpy)
2. [Calculator.py](#calculatorpy)
3. [TextEditor.py](#texteditorpy)
4. [VideoDownloader.py](videodownloaderpy)

### UnitConverter.py

This simple app can take user inputted data to convert from one unit to another. It can take any **floating point** number given in units of *kg* and convert it to *lbs*. It can also convert *kg to tonne*, and vice versa.

Showcase of initial running of app:

![github_ReadME_PySimpleGUI](https://user-images.githubusercontent.com/72211395/182453225-c4b168a1-e541-4f45-872c-753b61b1fd6a.png)

### Calculator.py

This app can perform basic mathematical operations such as addition, subtraction, multiplication, etc. It also has features to change the theme of the layout by right-clicking the output text.

![github_ReadME_Calculator](https://user-images.githubusercontent.com/72211395/182464367-e57fe813-deb2-41e2-a1bd-a6095c79567d.png)

### TextEditor.py

This app can display text inputted by the user. It can save and open text files, measure the word count of the file, and has additional symbols that can be added from a menu.

![github_ReadME_TextEditor](https://user-images.githubusercontent.com/72211395/182471258-f49538b8-6b90-4421-b0f0-8619a716f24d.png)

### VideoDownloader.py

This app can take in the url of a YouTube video to be downloaded using pytube. It can give video details like channel, title, views, etc. In the second tab it displays all the available streams / versions that can be downloaded, showcasing filetype, filesize and more. The user can add filters such as progressive (video and audio), adaptive (only video or only audio), audio tracks, and mp4 files only. Upon finding a stream the user would like to download, they identify the *tag* and can input this to download the video to a desired location, as determined in a popup for the user.

**EXTRA:**
Some more work could be done on exception handling, and perhaps adding a progress bar to indicate when a download is finished.

![github_ReadME_VideoDownloader_tab1](https://user-images.githubusercontent.com/72211395/182928657-eec70bad-b0f0-4e6b-bebc-cea947e3fb89.png)
![github_ReadME_VideoDownloader_tab2](https://user-images.githubusercontent.com/72211395/182928684-4699a666-5ba1-4020-82b2-8095988a6d41.png)

## User Instructions

1. Clone this project
2. Install **PySimpleGUI** and **pytube** using *pip*  
``pip install PySimpleGUI``  
``pip install pytube``  
3. Run the desired scripts as listed above
