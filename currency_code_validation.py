"""Create list of valid currency codes from codes listed in txt file"""

curr_codes = open("currency_codes.txt")
valid_codes = [c.strip() for c in curr_codes]
curr_codes.close()