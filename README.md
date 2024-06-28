# JS Keeper

JS Keeper is a Python script designed to parse HTML responses from given URLs, find all referenced JavaScript files, download them, and save them using their original filenames. The script supports threading, HTTP headers, and rate limiting.

## Features

- Parse HTML and find JavaScript files
- Download JavaScript files with their original filenames
- Support for threading to download files concurrently
- Customizable HTTP headers
- Rate limiting for requests

## Usage

### Command Line Arguments

- `-u, --url`: Single URL to parse
- `-l, --list`: File containing a list of URLs to parse
- `-t, --threads`: Number of threads to use (default: 1)
- `-h, --headers`: HTTP headers to be used with requests in JSON format
- `-n, --rate`: Number of requests per second (default: no limit)
- `-help, --help`: Display help information

### Examples

1. **Single URL:**
   ```sh
   python js_keeper.py -u http://example.com

2. **List of URLs:**
   ```sh
   python js_keeper.py -l urls.txt

3. **Using Threads:**
   ```sh
   python js_keeper.py -u http://example.com -t 4

4. **Custom HTTP Headers:**
   ```sh
   python js_keeper.py -u http://example.com -h '{"User-Agent": "Mozilla/5.0"}'

5. **Rate Limiting:**
   ```sh
   python js_keeper.py -u http://example.com -n 2

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/js_keeper.git
   cd js_keeper

2. **Install the required packages:**
   ```sh
   pip install -r requirements.txt


### Contributing:

Contributions are welcome! Please create an issue or pull request if you have any improvements or suggestions.

