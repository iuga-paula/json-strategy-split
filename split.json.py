import argparse
import os
import sys
import json

countries_with_codes = {
    'Czech Republic': 'CZE', 'Belgium': 'BEL', 'United Kingdom': 'GBR',
    'Greece': 'GRC', 'Lithuania': 'LTU', 'Portugal': 'PRT',
    'Bulgaria': 'BGR', 'Spain': 'ESP', 'Luxembourg': 'LUX', 'Romania': 'ROU',
    'Czechia': 'CZE', 'France': 'FRA', 'Hungary': 'HUN', 'Slovenia': 'SVN',
    'Denmark': 'DNK', 'Croatia': 'HRV', 'Malta': 'MLT', 'Slovakia': 'SVK',
    'Germany': 'DEU', 'Italy': 'ITA', 'Netherlands': 'NLD', 'Finland': 'FIN',
    'Estonia': 'EST', 'Cyprus': 'CYP', 'Austria': 'AUT', 'Sweden': 'SWE',
    'Ireland': 'IRL', 'Latvia': 'LVA', 'Poland': 'POL',
    'Iceland': 'ISL', 'Norway': 'NOR', 'Liechtenstein': 'LIE', 'Switzerland': 'CHE',
    'Jamaica': 'JAM', 'Dominica': 'DMA', 'Trinidad and Tobago': 'TTO',
    'Peru': 'PER', 'Paraguay': 'PRY', 'Egypt': 'EGY', 'South Africa': 'ZAF',
    'Russia': 'RUS', 'New Zealand': 'NZL', 'South Korea': 'KOR', 'Uganda': 'UGA',
    'Kenya': 'KEN', 'India': 'IND', 'Saudi Arabia': 'SAU', 'Jordan': 'JOR',
    'Qatar': 'QAT', 'Panama': 'PAN', 'Costa Rica': 'CRI', 'Nigeria': 'NGA',
    'Montenegro': 'MNE', 'Bangladesh': 'BGD', 'Rwanda': 'RWA', 'Turkey': 'TUR',
    'United States of America': 'USA', 'Australia': 'AUS', 'Canada': 'CAN'
}


def split_json(path):
    country_data = {}
    with open(path, 'r') as file:
        data = json.load(file)

    for strategy_data in data:
        if 'country' not in strategy_data['latestVersion']:
            print(f"country not found for {strategy_data['id']}!")

        country = strategy_data['latestVersion']['country']['title']
        if country not in countries_with_codes:
            print(f"missing {country}!")

        for version in strategy_data['otherVersions']:
            if 'country' in version and version['country']['title'] != country:
                print(f"strategy {strategy_data['id']} has different country for and older version")

        country_code = countries_with_codes[country]
        if country_code not in country_data:
            country_data[country_code] = [strategy_data]
        else:
            country_data[country_code].append(strategy_data)

        with open(f"./data/{country_code}.json", "w") as small_json:
            json.dump(strategy_data, small_json, ensure_ascii=False, indent=4, separators=(",", ": "))  # Prevent line
            # breaks in strings
            small_json.close()

    for key in country_data:
        if len(country_data[key]) > 1:
            print(f"there are many strategies for {key}!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='The json file')
    args = parser.parse_args()

    source = args.file
    if not os.path.exists(source):
        print(f"The json file {source} cannot be found!")
        sys.exit(2)
    split_json(source)


if __name__ == "__main__":
    main()
