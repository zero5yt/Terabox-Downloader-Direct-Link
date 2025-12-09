# ® ALMARAS TERABOX DOWNLOADER (Termux/Python) 

Isang simpleng CLI (Command Line Interface) tool na ginawa gamit ang Python para i-bypass ang Terabox share link at kumuha ng direct download link gamit ang RapidAPI, na may kasamang automatic filename detection at download progress bar.

** Disclaimer:** Ang tool na ito ay gumagamit ng third-party RapidAPI service. Responsibilidad mo ang paggamit ng iyong sariling API key at ang pagsunod sa terms and conditions ng service provider.

##  Prerequisites (Kailangan Bago Mag-start)

Para gumana ito sa iyong Android phone (via Termux):

1.  **Termux App:** I-install ang Termux mula sa Google Play Store o F-Droid.
2.  **RapidAPI Key:** Kailangan mo ng **Active API Key** mula sa sumusunod na RapidAPI service (Free Tier):
    *   **API:** `Terabox Downloader | Direct Download Link Generator` (Host: `terabox-downloader-direct-download-link-generator.p.rapidapi.com`)

##  Installation & Setup (Paano I-install)

Sundin ang mga command na ito sa Termux:

### Step 1: Termux Basic Setup

I-update ang Termux packages at i-install ang Python:

```bash
pkg update && pkg upgrade -y
pkg install python git nano -y
pip install requests

---

## ⭐️ Features

-   ✅ Gumagamit ng **POST Method** para sa stability.
-   ✅ Automatic **Content-Disposition** Filename detection.
-   ✅ Iwas **.bin** file extension.
-   ✅ Download Progress Bar.
-   ✅ Auto-generate **`mv` command** para sa madaling paglipat ng file.

## 📝 License ©almaras