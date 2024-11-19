import json
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from dotenv import load_dotenv
import logging

class EbayPriceComparer:
    def __init__(self, app_id):
        self.app_id = app_id
        self.finding_api = Finding(appid=self.app_id, config_file=None)

    def search_items(self, query, category_id=None, max_results=10, sold_only=False):
        """
        Search for items on eBay based on a query and optional category ID.
        """
        try:
            api_request = {
                'keywords': query,
                'paginationInput': {
                    'entriesPerPage': max_results
                },
                'itemFilter': []
            }

            if category_id:
                api_request['categoryId'] = category_id

            if sold_only:
                api_request['itemFilter'].append({
                    'name': 'SoldItemsOnly',
                    'value': True
                })

            response = self.finding_api.execute('findCompletedItems', api_request)
            items = response.dict()['searchResult']['item']
            return items
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            return []

    def get_item_prices(self, items):
        """
        Extract item prices from the search results.
        """
        prices = []
        for item in items:
            price = float(item['sellingStatus']['currentPrice']['value'])
            prices.append(price)
        return prices

    def compare_prices(self, current_prices, historical_prices):
        """
        Compare current prices to historical prices.
        """
        comparisons = []
        for price in current_prices:
            comparison = {
                'current_price': price,
                'historical_average': sum(historical_prices) / len(historical_prices),
                'is_above_average': price > sum(historical_prices) / len(historical_prices)
            }
            comparisons.append(comparison)
        return comparisons

    def display_comparisons(self, comparisons):
        """
        Display the price comparisons.
        """
        for comparison in comparisons:
            print(f"Current Price: ${comparison['current_price']:.2f}")
            print(f"Historical Average: ${comparison['historical_average']:.2f}")
            print(f"Above Historical Average: {comparison['is_above_average']}")
            print('-' * 40)

# Example usage
if __name__ == "__main__":
    # Replace 'ebay_app_id' with your actual eBay developer app ID
    app_id = ebay_app_id
    comparer = EbayPriceComparer(app_id)

    query = "laptop"
    current_items = comparer.search_items(query)
    current_prices = comparer.get_item_prices(current_items)

    # Get historical prices from completed listings
    completed_items = comparer.search_items(query, sold_only=True)
    historical_prices = comparer.get_item_prices(completed_items)

    comparisons = comparer.compare_prices(current_prices, historical_prices)
    comparer.display_comparisons(comparisons)
