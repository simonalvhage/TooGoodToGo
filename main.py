from tgtg import TgtgClient
from datetime import datetime, timedelta

class TgtgItemFetcher:
    def __init__(self, user_id, refresh_token, access_token, cookie, offset_hours=2):
        self.client = TgtgClient(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            cookie=cookie
        )
        self.offset_hours = offset_hours

    def convert_to_local_time(self, dt_str):
        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
        local_dt = dt + timedelta(hours=self.offset_hours)
        return local_dt

    def fetch_and_display_items(self):
        items = self.client.get_items()
        for item in items:
            if int(item['items_available']) > 0:
                self.display_item_info(item)

    def display_item_info(self, item):
        line_to_print = []
        line_to_print.append(item['item']['description'])
        line_to_print.append(item['display_name'])

        price = str(item['item']['price_including_taxes']['minor_units'])
        formatted_price = price[:-2] + ',' + price[-2:] + "kr"
        line_to_print.append(formatted_price)

        line_to_print.append(item['pickup_location']['address']['address_line'])
        line_to_print.append(f"Kassar kvar: {item['items_available']}")

        try:
            start_time = self.convert_to_local_time(item['pickup_interval']['start'])
            end_time = self.convert_to_local_time(item['pickup_interval']['end'])
            formatted_pickup_time = f"{start_time.day} {start_time.strftime('%B')} {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
            line_to_print.append(formatted_pickup_time)
        except Exception as e:
            line_to_print.append("No pickup interval")

        print('\n'.join(map(str, line_to_print)))
        print('-' * 40)  # Separator for better readability

# Usage
user_id = "VerySecretUserID"
refresh_token = "VerySecretRefreshToken"
access_token = "VerySecretAccessToken"
cookie = 'VerySecretCookie'

fetcher = TgtgItemFetcher(user_id=user_id, refresh_token=refresh_token, access_token=access_token, cookie=cookie)
fetcher.fetch_and_display_items()
