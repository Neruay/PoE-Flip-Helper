
![Logo](https://user-images.githubusercontent.com/42499003/225960767-236689d2-d85e-4e27-879e-e42227f5302f.png)


# PoeFlipHelper

PoeFlipHelper is a tool to help you with calculating PoE market margins, finding best deals & profitable item flips.

Features include:
- Updating and storing prices of different types of items;
- Auto-generated overview of expected returns of Harvest stack change option for different types of items;
- Gem options advisor for Gem Leveling / Alternate quality flipping;
- TFT Discord Bulk Selling messages live parsing & evaluating;

All price data is pulled from [pathofexile.com/trade](https://www.pathofexile.com/trade/) and [poe.ninja](https://poe.ninja/) from SC trade and stored in corresponding .json files locally in `/price_info`.


## Installation

Clone the project

```bash
  $ git clone https://github.com/Neruay/PoE-Flip-Helper.git
```

Go to the project directory

```bash
  $ cd Poe-Flip-Helper
```

Create and enter virtual environment
```bash
  $ python.exe -m venv venv
  $ cd venv/
  $ source ./Scripts/activate
```
Install dependencies

```bash
  $ pip install -r requirements.txt
```

## Usage/Examples

Firstly, start-off with updating item prices
```bash
  $ python run.py -f pricecheck -m update_prices -t all
```
After doing that, you might want to get some stats about flipping items with Harvest stack change
```bash
  $ python run.py -f stack_change -m get_profits_of_rerolls
```
Then you may want to get more detailed info about certain flip type, lets say fossils
```bash
  $ python run.py -f stack_change -m generate_roll_table -t fossils
```
After doing some profitable flips, you suddenly realize that your weapon-swap sockets are collecting dust instead of generating passive profit for you by leveling gems in them. Not a problem anymore! Run the Gem Advisor to find the best candidates to level-up for profit.\
\
Start with parsing gem info and updating prices

```bash
  $ python run.py -f gems -m parse_gems
  $ python run.py -f gems -m get_gems_prices
```
Then you can generate a fancy table of gem types with all stats you need
```bash
  $ python run.py -f gems -m generate_gems_leveling_table
```
Complete usage guide can be found in [docs]().