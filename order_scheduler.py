from datetime import datetime
import time
from order_automation import order_automation
import asyncio


async def schedule_order(items:[]):
    
    for drugs in items:
        drug_name = drugs[0]
        number_of_order = drugs[1]
        delivery_time = drugs[2]

        datetime_format = "%Y-%m-%d  %H:%M:%S"
        order_time = datetime.strptime(delivery_time, datetime_format)

        current_time = datetime.now()
        print(current_time)

        # Calculate the time difference until the order_time
        time_difference = order_time - current_time
        if time_difference.total_seconds() > 0:
            print(f"Waiting for {time_difference.total_seconds()} seconds until {order_time}")
            await asyncio.sleep(time_difference.total_seconds())
            print("Placing order now!")
            ordering = order_automation([(drug_name,number_of_order)])
        else:
            print('cannot place order because order has passed!!!!!!!!!')




if __name__ == '__main__':

    loop = asyncio.get_event_loop() # Create an event loop

    loop.run_until_complete(schedule_order([('Postinor *2 Tabs',3,'2024-01-29 04:46:2')]))

