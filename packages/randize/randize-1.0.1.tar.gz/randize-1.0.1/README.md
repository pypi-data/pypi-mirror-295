# 🌟 Randize: The Ultimate Python Randomizer Library 🌟

Welcome to **Randize** — your all-in-one solution for generating random data in Python! This library offers a wide variety of functions to produce random numbers, strings, names, emails, colors, coordinates, and much more. Perfect for testing, simulations, and fun projects! 🎉

## 📚 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Basic Randomization](#basic-randomization)
  - [Advanced Randomization](#advanced-randomization)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Random Number Generation**: Generate random integers, floats, dates, times, and UUIDs.
- **Random String Utilities**: Create random strings, passwords, and emails.
- **Data Structure Generators**: Generate random dictionaries, JSON objects, and more.
- **Web Testing Utilities**: Random user agents, URLs, and HTTP request data.
- **Custom Data Mocks**: Random color palettes, coordinates, weather conditions, and more!
- **Flexible API**: Easy-to-use static methods to integrate with your code.

## 🔧 Installation

Install **Randize** via pip:

```bash
pip install randize
```

Or, clone the repository and install manually:

```bash
git clone https://github.com/BlazeDevelop/randize.git
cd randize
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Randomization
First, import the library in your Python script:

```python
from randize import Randize
```

#### Generate a Random Number

```python
random_number = Randize.number(1, 100)  # Returns a random number between 1 and 100
print(random_number)
```

#### Generate a Random Password

```python
password = Randize.password(length=16, include_digits=True, include_punctuation=True)
print(password)  # Example: 'aB3$dEfGhI8!K@Lm'
```

### Advanced Randomization

#### Create a Random User Profile

```python
user_profile = Randize.struct({
    'name': 'name',
    'email': 'email',
    'birthdate': 'date',
    'address': 'random_coordinate'
})
print(user_profile)
```

#### Generate a Random Payment Card

```python
payment_card = Randize.payment_card()
print(payment_card)
```

## 📋 Examples

Here's a quick example of how you can use **Randize** to generate random data:

```python
# Generate a random color palette
color_palette = Randize.random_color_palette(n=5)
print(f"🎨 Color Palette: {color_palette}")

# Generate a random date between 2000 and 2023
random_date = Randize.date(start_year=2000, end_year=2023)
print(f"📅 Random Date: {random_date}")
```

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or have found a bug, feel free to [open an issue](https://github.com/BlazeDevelop/randize/issues) or submit a pull request. Please read our [contributing guide](CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

✨ Happy Randomizing! ✨