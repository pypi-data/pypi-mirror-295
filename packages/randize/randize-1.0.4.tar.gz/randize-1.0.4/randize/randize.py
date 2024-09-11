import random
import string
import requests
import uuid
from datetime import datetime, timedelta, timezone
import pytz  # This module provides support for time zones
import string as str_module

class Randize:
    def __init__(self):
        pass

    @staticmethod
    def shuffle(lst):
        """
        Shuffle a list in place and return it.
        """
        random.shuffle(lst)
        return lst

    @staticmethod
    def choice(lst):
        """
        Return a random item from a list.
        """
        return random.choice(lst)

    @staticmethod
    def uuid():
        """
        Return a random UUID.
        """
        return str(uuid.uuid4())

    @staticmethod
    def number(min_value=0, max_value=100):
        """
        Return a random number between min_value and max_value.
        """
        return random.randint(min_value, max_value)

    @staticmethod
    def digit(length=1):
        """
        Return a random digit string with a given length.
        """
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def word(api_url="https://random-word-api.herokuapp.com/word?number=1"):
        """
        Fetch a random word from an external API (Random Word API).
        """
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()[0]  # Assuming the API returns a list of words
            else:
                return 'unknown'
        except requests.exceptions.RequestException:
            return 'unknown'

    @staticmethod
    def password(length=12, include_digits=True, include_punctuation=True):
        """
        Return a random password of specified length.
        Parameters:
        - include_digits: whether to include digits in the password
        - include_punctuation: whether to include punctuation in the password
        """
        chars = string.ascii_letters  # A-Z, a-z
        if include_digits:
            chars += string.digits
        if include_punctuation:
            chars += string.punctuation

        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def email(domain='gmail.com'):
        """
        Generate a realistic random email address.
        """
        first_name = Randize.word()
        username = f"{first_name}".lower().replace(' ', '')
        return f"{username}@{domain}"

    @staticmethod
    def name(api_url="https://randomuser.me/api/"):
        """
        Fetch a random name from an external API (Random User API).
        """
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                first_name = data['results'][0]['name']['first']
                last_name = data['results'][0]['name']['last']
                return f"{first_name} {last_name}"
            else:
                return 'Unknown Name'
        except requests.exceptions.RequestException:
            return 'Unknown Name'

    @staticmethod
    def payment_card():
        """
        Generate a random payment card number (16-digit Visa/MasterCard style), name, expiration date, and CVV code.
        """
        def luhn_checksum(card_number):
            """
            Implementing the Luhn algorithm to calculate the checksum for the payment card.
            """
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10

        # Generate first 15 digits randomly
        card_number = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(14)]
        # Join card number into a single integer-like string for checksum calculation
        card_number_str = ''.join(map(str, card_number))
        # Calculate check digit
        check_digit = luhn_checksum(card_number_str)
        # Append check digit to the card number
        card_number.append(check_digit)

        # Generate additional details
        card_name = Randize.name()
        expiration_date = f"{random.randint(1, 12):02}/{random.randint(23, 30)}"  # MM/YY format
        cvv = Randize.digit(3)

        # Return all card details
        return {
            'number': ''.join(map(str, card_number)),
            'name': card_name,
            'expiration_date': expiration_date,
            'cvv': cvv
        }

    @staticmethod
    def struct(custom_structure=None):
        """
        Generate a random data structure (dictionary) with randomized keys/values.
        Custom structure can be passed as a dictionary template.
        Example: {'name': 'name', 'age': 'number'}
        """
        default_structure = {'name': 'name', 'age': 'number', 'card': 'payment_card'}
        structure = custom_structure if custom_structure else default_structure

        randomized_struct = {}
        for key, value_type in structure.items():
            if value_type == 'name':
                randomized_struct[key] = Randize.name()
            elif value_type == 'number':
                randomized_struct[key] = Randize.number()
            elif value_type == 'payment_card':
                randomized_struct[key] = Randize.payment_card()
            else:
                randomized_struct[key] = None  # Undefined types handled as None

        return randomized_struct
    
    @staticmethod
    def date(start_year=2000, end_year=2023):
        from datetime import datetime
        from random import randrange
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        random_date = start_date + (end_date - start_date) * random.random()
        return random_date.strftime("%Y-%m-%d")

    @staticmethod
    def time():
        from datetime import time
        return f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}"
    
    @staticmethod
    def ipv4():
        return ".".join(str(random.randint(0, 255)) for _ in range(4))

    @staticmethod
    def ipv6():
        return ":".join(f'{random.randint(0, 65535):x}' for _ in range(8))
    
    @staticmethod
    def random_color_palette(n=5):
        """
        Generate a random color palette with 'n' colors.
        Returns a list of colors in HEX format.
        """
        return [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(n)]

    @staticmethod
    def random_coordinate(min_lat=-90, max_lat=90, min_lon=-180, max_lon=180):
        """
        Generate a random geographic coordinate (latitude, longitude).
        """
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        return {'latitude': lat, 'longitude': lon}

    @staticmethod
    def random_emoji_pair():
        """
        Generate a random pair of emojis.
        """
        emojis = ['😀', '😂', '😍', '🤣', '😊', '😎', '😢', '😭', '😡', '👍', '🔥', '✨', '🌈', '🍕', '🎉', '🚀']
        return random.choice(emojis), random.choice(emojis)

    @staticmethod
    def random_weather():
        """
        Generate random weather conditions.
        """
        conditions = ['Sunny', 'Cloudy', 'Rainy', 'Snowy', 'Stormy', 'Windy', 'Foggy', 'Hail', 'Thunderstorm']
        temperature = random.randint(-30, 40)  # Random temperature between -30 and 40 Celsius
        humidity = random.randint(0, 100)  # Random humidity percentage
        return {'condition': random.choice(conditions), 'temperature': temperature, 'humidity': humidity}

    @staticmethod
    def random_hex_code():
        """
        Generate a random HEX color code.
        """
        return f'#{random.randint(0, 0xFFFFFF):06x}'

    @staticmethod
    def random_json_object(keys=5):
        """
        Generate a random JSON-like object with a given number of keys.
        """
        return {Randize.string(length=5): Randize.choice(['text', Randize.number(), Randize.uuid(), Randize.random_coordinate()]) for _ in range(keys)}

    @staticmethod
    def random_mac_address():
        """
        Generate a random MAC address.
        """
        return ':'.join(f'{random.randint(0x00, 0xFF):02x}' for _ in range(6))

    @staticmethod
    def random_direction():
        """
        Generate a random cardinal direction.
        """
        directions = ['North', 'South', 'East', 'West']
        return random.choice(directions)

    @staticmethod
    def random_url():
        """
        Generate a more realistic random URL with a meaningful path and domain.
        """
        domain_names = ["example", "mysite", "coolblog", "app", "company"]
        paths = ["about", "contact", "products", "services", "home"]
        domains = ['.com', '.org', '.net', '.io', '.ai']
        domain = f"{random.choice(domain_names)}{random.choice(domains)}"
        path = '/'.join(Randize.word().split())
        return f"https://www.{domain}/{path}"
    
    @staticmethod
    def random_choice(options=['yes', 'no']):
        """
        Generate a random choice from a list of options.
        """
        return random.choice(options)
    
    @staticmethod
    def random_datetime(start_date='2000-01-01', end_date='2023-12-31', fmt='%Y-%m-%d %H:%M:%S', tz='UTC', granularity='seconds'):
        """
        Generate a random date and time within a specified range.
        Parameters:
        - start_date: Start date in 'YYYY-MM-DD' format.
        - end_date: End date in 'YYYY-MM-DD' format.
        - fmt: The format of the output date-time string.
        - tz: Time zone for the generated date-time.
        - granularity: Granularity for time ('seconds', 'minutes', 'hours', 'days').
        """
        # Convert input dates to datetime objects
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        # Generate a random date between start and end
        delta = end - start
        random_days = random.randint(0, delta.days)
        random_date = start + timedelta(days=random_days)

        # Adjust time part based on granularity
        if granularity == 'seconds':
            random_time = timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
        elif granularity == 'minutes':
            random_time = timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        elif granularity == 'hours':
            random_time = timedelta(hours=random.randint(0, 23))
        else:
            random_time = timedelta()

        random_datetime = random_date + random_time

        # Set the time zone
        tz_info = pytz.timezone(tz)
        random_datetime = tz_info.localize(random_datetime)

        return random_datetime.strftime(fmt)

    @staticmethod
    def random_user_agent():
        """
        Generate a random user-agent string for web scraping or testing.
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 11; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        ]
        return random.choice(user_agents)
    
    @staticmethod
    def string(length=8, include_digits=True, include_punctuation=False):
        """
        Generate a random string of a given length.
        """
        characters = string.ascii_letters  # Start with all letters (both lowercase and uppercase)

        if include_digits:
            characters += string.digits

        if include_punctuation:
            characters += string.punctuation

        return ''.join(random.choices(characters, k=length))