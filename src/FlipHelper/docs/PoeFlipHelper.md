
# PoeFlipHelper general user documentation

## `run.py`
Main interface between the user and PoeFlipHelper.\
run.py takes up to 3 arguments, thought only first of them is required:
```git
python run.py -f feature -m mode -t item_type
```
`-f --feature` - the only required argument, which defines the core feature you are working with. Available options are:
- `pricecheck`
- `stack_change`
- `gems`
- `tft`
`-m --mode` - calls the certain function of the selected core feature. Available options for each feature are described in their respective sections.\
\
`-t --item_type` - specifies the item type, required by some features. Available item types are:
- `fossils`
- `deli_orbs`
- `essences`
- `oils`
- `catalysts`
- `scarabs`
Note that `stack_change` works with 2 types of `scarabs` separately: it accepts `scarabs_gilded` and `scarabs_winged` options for economy purposes.

##  `pricecheck.py`
Tool made for checking and updating prices of different types of items. \
It has following `-m --mode` modes/functions:
- `update_prices` - takes `-t` argument, which specifies a certain item type to update regular/bulk prices of all items from this category. Most item types were described in `-t` section, but `pricecheck.py` also takes `-t all` argument, which will force update all item prices of every category.

## `stack_change.py`
Tool designed to calculate expected returns of Harvest stack change gamble for all supported item types. It has several `-m --mode` modes/functions:
- `get_profits_of_rerolls` - takes no arguments, outputs a list of all item types with their expected returns per rerolled unit with retail/bulk selling profits.
- `generate_roll_table` - takes `-t` argument, which specifies a certain item type to calculate estimated value of rerolls and their expected return, returns a table with detailed data about stack changing of a certain item category.

## `alt_gems.py`
Tool made to work with skill and support gems, as well as with their alternate qualities, supports next `-m --mode` specifications:
- `parse_gems` - parses all gems with their respective stats and qualities from PoE game files. Takes no arguments, updates (or creates if doesn't exist) `alt_gems.json` file with gem data.
- `get_gems_prices` - pulls all gem prices from [poe.ninja](https://poe.ninja/challenge/skill-gems). Takes no arguments, updates `alt_gems.json` with a fresh prices.
- `generate_flip_table` - calculates expected returns for all gem quality type change combinations assuming their respective weights. Takes no argument, returns a table with detailed information about recommended flips with the most expected value.
- `generate_gems_leveling_table` - calculates the price difference between non-leveled and fully-leveled version of each existing gem-quality combination. Takes no argument, returns a table with detailed information about recommended gems to level-up with detailed info.

## `tft_notifier.py`
Tool for real-time discord TFT bulk-sell channels monitoring, fetching and parsing results. Still in development and currently not fully working. Requires installation of [Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract) and specifying path to its engine with `pytesseract.pytesseract.tesseract_cmd` object.