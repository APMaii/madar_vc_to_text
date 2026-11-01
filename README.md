# madar_vc_to_text 🎙️❤️

A tiny hobby script to turn Persian podcasts into text, made for my mother.

My mother wanted me to convert a podcast into text, so I wrote this little Python script. I am sharing it because maybe someone else wants to help their mother too. 🙂

**Madar (مادر) means “mother” in Persian.** This is a small personal project, and contributions that keep it simple and useful are welcome.

## What it does

- Transcribes Persian MP3 files using [faster-whisper](https://github.com/SYSTRAN/faster-whisper).
- Lets you choose the `small` or `medium` multilingual model.
- Runs on CPU with `int8` computation, without a paid transcription API.
- Prints recognized speech and saves a UTF-8 `transcript_fa.txt`.
- Lets you select a file if the folder contains several MP3s.

The first run needs internet access to download the selected model. Subsequent runs normally reuse its local cache. Audio processing runs locally; this script does not upload your podcast to a transcription service.

## Setup

Python 3.12 is a reasonable starting point for this setup. Use a separate environment, especially if you normally work in Conda's `base` environment.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead.

If you prefer Conda:

```bash
conda create -n madar-vc python=3.12
conda activate madar-vc
python -m pip install -r requirements.txt
```

Choose either environment approach. No separate system FFmpeg installation is normally needed because PyAV supplies the decoding libraries.

## Usage

Put your audio file beside the script:

- `vc_to_text.py`
- `podcast.mp3` — your own local audio
- `requirements.txt`
- `README.md`

Run from that folder:

```bash
python vc_to_text.py
```

Choose `small` or `medium` when prompted. Press Enter to use `small`.

| Model | Practical trade-off |
| --- | --- |
| `small` | Lighter and usually faster; start here. |
| `medium` | Larger and slower; may improve recognition, depending on the recording. |

The result is written to `transcript_fa.txt`. If that file already exists, the script asks before replacing it. Transcription may take a while on CPU. After “Starting transcription”, there may be a pause before the first segment appears.

## Problems I ran into

These are compatibility workarounds for specific errors, rather than a promise that every future package combination will work. Dependencies are constrained where needed, but this is not a fully pinned lockfile.

### 1. Hugging Face token warning

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This warning alone is not an error. Public model downloads can work without a token, although anonymous requests have lower rate limits. Do not put tokens in your code or commit them to Git.

### 2. Stuck at “Downloading/loading the small model...”

The first model download can take time. A VPN, proxy, or unreliable connection may also interfere. Check access with:

```bash
curl -I -L --connect-timeout 10 --max-time 30 \
  https://huggingface.co/Systran/faster-whisper-small/resolve/main/model.bin
```

A final `200` response means the URL is reachable for this request; it does not guarantee Python can complete the whole download. Timeouts suggest a connectivity issue. SSL errors need certificate/proxy troubleshooting; do not disable certificate verification.

You can also inspect the usual cache location:

```bash
du -sh ~/.cache/huggingface/hub/models--Systran--faster-whisper-small
```

An unchanged folder size alone does not prove the download is stuck: temporary download data may be elsewhere.

### 3. `TypeError: process() takes no keyword arguments`

We encountered this while the HTTP client was decoding downloaded data, with Brotli 1.0.9 installed. Updating Brotli resolved that error in our setup:

```bash
python -m pip install --upgrade "Brotli>=1.2.0"
```

### 4. `TypeError: open() got an unexpected keyword argument 'metadata_errors'`

This can happen when an older faster-whisper decoding path meets PyAV 19, which removed that argument. The workaround used here is:

```bash
python -m pip install --upgrade "av>=11,<19"
```

See the [upstream issue](https://github.com/SYSTRAN/faster-whisper/issues/1589). Newer faster-whisper versions may support PyAV 19; this project keeps the compatibility constraint for now.

### 5. No MP3 found

Run the script from the folder containing your MP3. The script looks for lowercase `*.mp3` files in the current working directory.

### 6. Still getting an error?

Collect the traceback and package versions before changing more packages:

```bash
python --version
python -m pip show faster-whisper av Brotli huggingface-hub
python -m pip check
```

## Clean up the Persian transcript with ChatGPT

Small models can confuse words, names, punctuation, and sentence boundaries. After transcription, you can give `transcript_fa.txt` to ChatGPT for language cleanup. This step is manual and optional; the script itself does not call GPT.

My original request was:

> این متن رو بر اساس زبان فارسی مرتبش کن و درستش کن و بده.

For more controlled editing, use this improved prompt:

```text
این متن خروجی خام تبدیل گفتار یک پادکست فارسی به متن است. لطفاً آن را با حفظ معنا و لحن اصلی ویرایش کن.

۱. غلط‌های املایی، فاصله‌گذاری، نیم‌فاصله و نشانه‌گذاری را اصلاح کن.
۲. خطاهای آشکار تبدیل گفتار به متن را فقط زمانی اصلاح کن که واژهٔ موردنظر از بافت جمله روشن باشد.
۳. جمله‌ها و پاراگراف‌ها را مرتب کن، اما متن را خلاصه نکن و هیچ نکته یا مثالی به آن اضافه نکن.
۴. لحن گفتاری را به شکل روان و خوانا حفظ کن؛ آن را بی‌دلیل رسمی یا ادبی نکن.
۵. نام‌ها، اعداد و اصطلاحات تخصصی را بدون اطمینان تغییر نده. اگر عبارتی مبهم است، آن را با [نامشخص: عبارت خام] مشخص کن و حدس قطعی نزن.
۶. ادعاهای علمی یا محتوایی گوینده را در متن تغییر نده. اگر موردی نیاز به بررسی دارد، آن را جداگانه و کوتاه در پایان ذکر کن.
۷. عنوان یا بخش‌بندی تازه نساز، مگر اینکه ساختار آن به‌وضوح در متن وجود داشته باشد.
۸. ابتدا متن کامل ویرایش‌شده را بده و در پایان فقط موارد مبهمی را که نیاز به شنیدن دوبارهٔ صوت دارند فهرست کن.

متن خام:
[متن transcript_fa.txt را اینجا قرار بده یا فایل را پیوست کن]
```

GPT can improve readability, but it cannot reliably recover missing words from text alone. Check uncertain passages against the recording. For private recordings, consider what you are comfortable sending to an external service.


## Contributions

If this helps you help your mother—or anyone who prefers reading to listening—feel free to suggest improvements. Better Persian recognition, clearer setup instructions, and simple usability fixes are especially welcome.

## Credits

Built with [faster-whisper](https://github.com/SYSTRAN/faster-whisper), which runs [OpenAI Whisper](https://github.com/openai/whisper) models through CTranslate2. This is an independent hobby project.
