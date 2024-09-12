"""
quantumdiceware.py
Diceware passphrases generated from quantum random data.
http://github.com/justinsloan/qdg

Requires Python 3.6 or better

# Create the distribution
python setup.py sdist

# Upload to PyPi
twine upload ./dist/path-to-tar.gz

##########################################################################
# PUBLIC DOMAIN RELEASE                                                  #
##########################################################################
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
##########################################################################
"""

__version__ = "0.4.4"
__date__ = "8 SEPTEMBER 2024"
__author__ = "Justin M. Sloan"

from fileinput import lineno
from dotenv import load_dotenv
from tqdm import tqdm
import requests
import json
import argparse
import time
import os

# Load the standard wordlist file
from .diceware_word_list import WORD_DICT

 # Load environment variables from .env
load_dotenv()

# Specify the location of the word list inside the package
RESOURCE_NAME = __package__
#PATH = "diceware_word_list.txt"
WORD_LIST_FILE = ""  #importlib.resources.path(RESOURCE_NAME, PATH)

# Build the argument parser
parser = argparse.ArgumentParser(
    description="Generate Diceware passphrases using quantum random data.",
    epilog=f"QDG v.{__version__} | by {__author__}")
parser.add_argument("-c", "--count", nargs="?", default=1, type=int, help="number of passphrases to generate")
parser.add_argument("-w", "--words", nargs="?", default=6, type=int, help="number of words per passphrase")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
parser.add_argument("-f", "--file", nargs="?", default=WORD_LIST_FILE, help="specify the word list to use")
parser.add_argument("--char", action="store", default="-", type=str, help="set the character between words")
parser.add_argument("--pretext", action="store", default="", type=str, help="specify text to appear before the passphrase")
parser.add_argument("--posttext", action="store", default="", type=str, help="specify text to appear after the passphrase")
parser.add_argument("--version", action="version", version=f"QDG v.{__version__}, {__date__}")
args = parser.parse_args()

# Set the mode options
VERBOSE = bool(args.verbose) # Sets VERBOSE to True if arg is provided, False if not
#VERBOSE = True

# Check for a custom wordlist file and load it
if not WORD_LIST_FILE == "":
    WORD_DICT = {}
    with open(args.file) as f:
        for line in f.readlines():
            index, word = line.strip().split('\t')
            WORD_DICT[int(index)] = word


def __verbose(text):
    """
    If verbose mode is enabled, print the message to stdout.
    """
    if VERBOSE:
        print(text)


def __reprint(text):
    print(text, end='\r')


def __save_execution_timestamp():
    current_timestamp = time.time()
    os.environ["LAST_EXECUTION"] = str(current_timestamp)
    with open(".env", "a") as env_file:
        env_file.write(f"LAST_EXECUTION={current_timestamp}\n")


def __get_last_execution_timestamp():
    if not os.getenv("LAST_EXECUTION", "0"):
        __save_execution_timestamp()

    return float(os.getenv("LAST_EXECUTION", "0"))


def __get_block(entropy):
    block = iter(entropy)
    try:
        return next(block)
    except StopIteration:
        print("Error: end of block list.")


def get_entropy(blocks_count=1):
    """
    Collect entropy from the ANU QRNG and return a list of 4-digit
    hexadecimal numbers
    - we need a way to limit requests to once per minute
    -- environment variables?
    -- pause function that counts down time if needed?
    """
    __verbose(f"Getting {blocks_count} blocks of entropy...")
    response = requests.get(f"https://qrng.anu.edu.au/API/jsonI.php?length={blocks_count}&type=hex16&size=1024")
    if response.status_code == 200:
        __verbose("The request was successful!")
        __save_execution_timestamp()
        request = json.loads(response.text)
        blocks = request['data']
        count_check = len(blocks)
        if count_check == blocks_count:
            __verbose("Block count validated.")
            combined_entropy = ''.join(blocks)
            entropy = [combined_entropy[i:i+4] for i in range(0, len(combined_entropy), 4)]
            __verbose(entropy)

            return entropy
        else:
            __save_execution_timestamp()
            print(f"Error: {blocks_count} block(s) were requested but {count_check} blocks were returned.")
            exit(1)
    else:
        print("Error: entropy requests can only be made once every 2 minutes.")
        __verbose(f"Request failed with status code {response.status_code}.")
        exit(1)


def calculate_entropy(phrase_count=1, word_count=6):
    """
    Calculate how much entropy data is needed and return an int of
    how many blocks to request
    Formula: Num_Blocks = (Words * 5) * Num_Phrases
    - minimum block request is 1
    - we can get 512 rolls per block
    - each word requires 5 rolls
    """
    # sanitize input
    phrase_count = int(phrase_count) # truncate
    word_count = int(word_count) # truncate

    # do some error checking
    if phrase_count < 1 or word_count < 1:
        print(f"Error {lineno}: Word Count ({word_count}) or Phrase Count ({phrase_count}) cannot be less than 1.")
        exit(1)
    elif phrase_count > 100:
        print(f"Error {lineno}: Phrase Count cannot be greater than 100.")
        exit(1)
    elif word_count > 30:
        print(f"Error {lineno}: Word Count cannot be greater than 30.")
        exit(1)

    # do the math
    roll_count = (word_count * 5) * phrase_count
    block_count = roll_count / 512
    blocks = int(block_count + 1) # truncate and round up
    __verbose(f"Blocks calculated: {blocks}")

    return blocks


def generate_password(entropy, word_count=6, char=" ", pre="", post=""):
    """
    Generate a single password and return as a string
    """
    dice_words = []
    dice = []
    numbers = []

    block_count = word_count * 5              # get enough blocks for the number of words
    blocks = entropy[:block_count]            # slice block_count items from entropy
    del entropy[:block_count]                 # delete the sliced items from entropy

    rand_num_count = word_count               # get enough blocks for use a base10 numbers
    num_blocks = entropy[:rand_num_count]     # slice rand_num_count items from entropy
    del entropy[:rand_num_count]              # delete the sliced items from entropy

    for block in blocks:                      # convert hexadecimal blocks to mod6
        die = int(block, 16) % 6 + 1
        dice.append(str(die))

    for num in num_blocks:                    # convert hexadecimal blocks to mod99
        number = int(num, 16) % 99
        numbers.append(str(number))

    dice = ''.join(dice)
    roll = [str(dice)[i:i + 5] for i in range(0, len(str(dice)), 5)]
    num_loop = 0
    for i in roll:
        __verbose(f"Dice Rolls: {i}")
        # TODO make capitalization an arg option
        token = WORD_DICT[int(i)]
        rand_number = numbers[num_loop]
        num_loop += 1
        __verbose(str(token + rand_number))
        word = token[0].upper() + token[1:] + str(rand_number)
        dice_words.append(word)

    password = pre + char.join(dice_words) + post

    return entropy, password

def main():
    """
    The main function
    """
    # Get the time so we can calculate how long it takes
    start_time = time.time()

    args.count = 10

    __verbose("INPUT ARGUMENTS:")
    __verbose(f"Arg input - phrase count: {args.count}")
    __verbose(f"Arg input - word count:   {args.words}")
    __verbose(f"Arg input - word file:    {args.file}")
    __verbose(f"Arg input - verbose:      {args.verbose}")

    time_stamp = __get_last_execution_timestamp()
    stamp = int(time.time() - time_stamp)
    __verbose(f"Last execution: {stamp} seconds ago.")

    print("Requesting entropy, please wait...")

    # regulate entropy collection, limit to once every 130 seconds
    if stamp < 130:
        __verbose("Entropy request threshold exceeded.")
        __verbose(f"Pausing for {130 - stamp} seconds to request entropy.")
        for i in tqdm(range(130 - stamp)):
            time.sleep(1)
        print("Processing request...")

    blocks = calculate_entropy(args.count, args.words)
    entropy = get_entropy(blocks)

    # Loop until requested number of passphrases are generated
    for i in range(0, args.count):
        entropy, password = generate_password(entropy, args.words, str(args.char), str(args.pretext), str(args.posttext))
        print(password)

    # Calculate how long it took and print if Verbose mode is on
    run_time = int((time.time() - start_time) * 10) / 10
    __verbose(f"--- Finished in {run_time} seconds ---")
