import subprocess as sp
import argparse
import os

os.chdir("src/FlipHelper")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--feature",
    required=True,
    dest="feature",
    help="Select core feature. Available options are: pricecheck, stack_change, gems, tft."
)
parser.add_argument(
    "-m",
    "--mode",
    dest="mode",
    help="Select work mode of the selected feature, available options for each feature can be found in docs."
)
parser.add_argument(
    "-t",
    "--type",
    dest="item_type",
    help="Specify item type for a certain function if needed, all supported item types can be found in docs."
)
arg_list = ['python']
args = parser.parse_args()
match args.feature:
    case "pricecheck":
        arg_list.append("pricecheck.py")
    case "stack_change":
        arg_list.append("stack_change.py")
    case "gems":
        arg_list.append("alt_gems.py")
    case "tft":
        arg_list.append("tft_notifier.py")
if args.mode:
    arg_list.extend([args.mode, args.item_type]) if args.item_type else arg_list.append(args.mode)
p = sp.run(arg_list)