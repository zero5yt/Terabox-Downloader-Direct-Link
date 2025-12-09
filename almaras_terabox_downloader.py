# -*- coding: utf-8 -*-
import requests
import os
import sys
import re # Idagdag ang re para sa filename parsing

# ==============================================================================
#                      I. RAPIDAPI CONFIGURATION (THE WORKING VERSION)
# ==============================================================================

# IYONG KEY AT HOST/ENDPOINT (GET METHOD)
RAPIDAPI_KEY = "e34a3ea2c6msh0d27fd9eebd75e6p16b31ajsn8e3dc920cb0d" 
RAPIDAPI_HOST = "terabox-downloader-direct-download-link-generator2.p.rapidapi.com" 
API_ENDPOINT = f"https://{RAPIDAPI_HOST}/url" # GET Endpoint

# ==============================================================================
#                        II. FUNCTIONS
# ==============================================================================

def get_direct_link(terabox_url):
    """Hakbang 1: I-convert ang Terabox URL sa Direct Download Link gamit ang RapidAPI."""
    
    querystring = {"url": terabox_url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    print("Status: Almaras Kinukuha ang Direct Link mula sa Terabox Link...")
    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=querystring, timeout=15)
        response.raise_for_status() 
        
        raw_data = response.json()
        direct_link = None
        
        # FINAL PARSING FIX: Handle List/Array Response
        if isinstance(raw_data, list) and len(raw_data) > 0:
            data_object = raw_data[0]
        elif isinstance(raw_data, dict):
            data_object = raw_data
        else:
            print(f"Error sa API Response (Unexpected type): {raw_data}")
            return None
        
        # FINAL PARSING: Hanapin ang 'fastdlink' o 'url' o 'link'
        direct_link = data_object.get("fastdlink") or data_object.get("url") or data_object.get("link")
        
        if direct_link:
            print("Status:   Almaras Matagumpay na nakuha ang Direct Link.")
            return direct_link
        else:
            print(f"Error sa API Response (Walang Link sa fields): {raw_data}")
            return None
            
    except requests.exceptions.HTTPError as err:
        print(f"\n  HTTP Error! Code: {err.response.status_code}. (Key invalid, o URL mali)")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\n  Connection Error/Timeout: {e}")
        return None
    except Exception as e:
        print(f"\n  Parsing/General Error: {e}")
        return None

def download_file(direct_url, filename="downloaded_terabox_file"):
    """Hakbang 2: I-download ang file gamit ang Direct Link (with final filename logic)."""
    
    final_filename = None
    
    # Final User-Agent at Filename Logic
    download_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    try:
        # Step 1: Kuhanin ang filename mula sa Content-Disposition header
        head_response = requests.head(direct_url, headers=download_headers, timeout=10)
        content_disposition = head_response.headers.get('Content-Disposition')
        
        if content_disposition:
            fname_match = re.search('filename="(.+?)"', content_disposition)
            if fname_match:
                final_filename = fname_match.group(1).replace('"', '').replace("'", "")

        # Fallback at .bin Fix
        if not final_filename or final_filename.endswith(('.bin', 'download', 'file')) or '.' not in final_filename:
            base_name = os.path.basename(direct_url.split('?')[0])
            if base_name.endswith('.bin'):
                 base_name = base_name[:-4] + '.mp4'
            
            final_filename = base_name if '.' in base_name else f"Terabox_Video_{os.urandom(4).hex()}.mp4"


        print(f"\nStatus: Sinisimulan ang pag-download. Ise-save bilang: {final_filename}")
        
        # Step 2: Actual download
        response = requests.get(direct_url, stream=True, headers=download_headers, timeout=3600) 
        response.raise_for_status() 
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        with open(final_filename, 'wb') as file:
            print(f"File Size: {total_size / (1024*1024):.2f} MB")
            
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk: 
                    file.write(chunk)
                    downloaded += len(chunk)
                    progress = int(50 * downloaded / total_size) if total_size > 0 else 0
                    sys.stdout.write(f"\rDownloading: [{'#' * progress}{'.' * (50 - progress)}] {downloaded * 100 / total_size if total_size > 0 else 0:.2f}%")
                    sys.stdout.flush()
        
        print(f"\n  Almaras SUCCESS: Tapos na ang pag-download! Ang file ay na-save sa: {os.path.abspath(final_filename)}")
        print(f"I-move sa Downloads: mv \"{final_filename}\" storage/downloads/") 

    except requests.exceptions.RequestException as e:
        print(f"\n  ERROR sa Pag-download: {e}")
    except Exception as e:
        print(f"\n  May nangyaring error habang nagda-download: {e}")

# ==============================================================================
#                             III. MAIN APP
# ==============================================================================

def main_downloader():
    print("\n--- TERMUX TERABOX DOWNLOADER APP (PYTHON) ---")
    terabox_url = input("Ipasok ang Terabox Share URL: ").strip()
    
    if not terabox_url:
        print("Walang URL na inilagay. Lumabas sa App.")
        return
        
    direct_link = get_direct_link(terabox_url)
    
    if direct_link:
        download_file(direct_link)
    else:
        print("\n  FAILED: Hindi maipagpatuloy ang pag-download.")


if __name__ == "__main__":
    main_downloader()