import requests
import hashlib
import sys

def request_api_data(query_char):
    """
    Fetches data from the Pwned Passwords API for a given prefix of a SHA-1 hash.

    Args:
        query_char (str): The first 5 characters of the SHA-1 hashed password.

    Returns:
        Response: The HTTP response object containing the hash data.

    Raises:
        RuntimeError: If the API request fails (non-200 response status).
    """
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, Check the API response and try again")
    return res


def get_password_leak_count(hashes, hash_to_check):
    """
    Parses the hash data from the API and checks for the occurrence of the given hash.

    Args:
        hashes (Response): The response object containing hash data from the API.
        hash_to_check (str): The suffix of the SHA-1 hashed password to check.

    Returns:
        int: The number of times the password has been leaked. Returns 0 if not found.
    """
    hashes_split = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes_split:
        if h == hash_to_check:
            return int(count)
    return 0


def pwned_api_check(password):
    """
    Checks whether a password has been exposed in a data breach by querying the Pwned Passwords API.

    Args:
        password (str): The password to check.

    Returns:
        int: The number of times the password has been leaked. Returns 0 if not found.
    """
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leak_count(response, tail)


def main(args):
    """
    Main function to check multiple passwords provided as command-line arguments.

    Args:
        args (list): A list of passwords passed as command-line arguments.

    Returns:
        str: A completion message indicating the script has finished.
    """
    if len(args) < 1:
        print('Too few arguments!')
        
    for arg in args:
        count = pwned_api_check(arg)
        if count:
            print(f'{arg} was found {count} times. You should change your password!')
        else:
            print(f'{arg} was not found. You are safe!')
    return 'done'


if __name__ == "__main__":
    # Exits the program with the return value from main() when provided with command-line arguments.
    sys.exit(main(sys.argv[1:]))
