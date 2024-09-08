<div align="center">
  <h1>tiktokautouploader</h1>
</div>


### AUTOMATE TIKTOK UPLOADS 🤖. USE TRENDING SOUNDS 🔊, ADD WORKING HASHTAGS 💯, SCHEDULE UPLOADS 🗓️, AUTOSOLVES CAPTCHAS 🧠, AND MORE 🎁

[![PyPI version](https://img.shields.io/pypi/v/tiktokautouploader.svg)](https://pypi.org/project/tiktokautouploader/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<p align="center">
  <img src="READMEimage/Image.png" alt="" width="400"/>
</p>

## 🚀 Features

- **🔐 Bypass/Auto Solve Captchas:** No more manual captcha solving; fully automated process!
- **🎵 Use TikTok Sounds:** Seamlessly add popular TikTok sounds to your videos.
- **🗓 Schedule Uploads:** Upload videos at specific times or upto 10 days in advance with our scheduling feature.
- **🔍 Copyright Check:** Ensure your video is safe from copyright claims before uploading.
- **🏷 Add Working Hashtags:** Increase your reach by adding effective hashtags that actually work.


## 📦 Installation

1. **Python Installation:** Install the package using `pip`:

```bash
pip install tiktokautouploader
```

---

## ⚙️ Pre-requisites

1. **Node.js:** You must have Node.js installed on your system, as some parts of this package rely on JavaScript code. If you don't have Node.js installed, you can download it from [nodejs.org](https://nodejs.org/).

   - **Note:** The necessary JavaScript dependencies (`playwright`,`playwright-extra`, `puppeteer-extra-plugin-stealth`) will be AUTOMATICALLY installed the first time you run the function, so you don't need to install them manually. Make sure that `npm` (Node.js package manager) is available in your system's PATH.


2. **Browser Binaries:** If you don't have them already, you'll need to install the chromium browser binary for `playwright`.

To do so, just run the following command AFTER installing the package:

```bash
python -m playwright install chromium
```


## 📝 Quick-Start

Here's how to upload a video to TikTok with hashtags using `tiktokautouploader`:

NOTE: It is highly recommended you read DOCUMENTATION.md before using the library.

The first time you run the code, you will be prompted to log-in, this will only occur the first time the function is used. Check documentation for more info.

```python
from tiktokautouploader import upload_tiktok

video_path = 'path/to/your/video.mp4'
description = 'Check out my latest TikTok video!'
hashtags = ['#fun', '#viral']

upload_tiktok(video=video_path, description=description, hashtags=hashtags)

```

### Upload with TikTok Sound

```python
upload_tiktok(video=video_path, description=description, sound_name='trending_sound', sound_aud_vol='main')
```

PLEASE READ DOCUMENTATION FOR MORE INFO.

### Schedule an Upload

```python
upload_tiktok(video=video_path, description=description, schedule='03:10', day=11)
```

PLEASE READ DOCUMENTATION FOR MORE INFO

### Perform Copyright Check Before Uploading

```python
upload_tiktok(video=video_path, description=description, hashtags=hashtags, copyrightcheck=True)
```

## 🎯 Why Choose `autotiktokuploader`?

- **No more captchas:** Fully automated uploads without interruptions, If captchas do show up, no worries, they will be solved. (read documentation for more info)
- **Maximize your reach:** Add popular sounds and effective hashtags that work to boost visibility.
- **Stay compliant:** Built-in copyright checks to avoid unforeseen takedowns.
- **Convenient scheduling:** Post at the right time, even when you're away.

## 🛠 Dependencies

This library requires the following dependencies:

- `playwright`
- `requests`
- `Pillow`
- `scikit-learn`
- `inference`

These will be automatically installed when you install the package.

## 👤 Author

Created by **Haziq Khalid**. Feel free to reach out at [haziqmk123@gmail.com](mailto:haziqmk123@gmail.com) or my LinkedIn.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
```
