# SOMA Pre-orders

A phone-friendly tracker for SOMA's TikTok pre-orders: customer pays → ordered on Shein → parcel arrives from Bangkok → delivered.

The whole app is one file, `index.html`. It runs as a Claude artifact. That keeps orders in an online database, so any phone signed in to the same claude.ai account sees the same orders. Opened anywhere else (a downloaded copy, another host), it falls back to saving on that phone only and shows a banner saying so.

## Screens

- **Orders**: grouped by order date, newest day first. Filters: Active, To order, Late, No cost, All, plus search.
  - Tap a step (Paid, Ordered 💵, Arrived, Delivered) to set an order's status. Going back clears the later dates.
  - **Mark N ordered 💵** on a day header moves all of that day's Paid orders to Ordered.
  - Ordered parcels show "Day N of 8–10". Once more than 10 days have passed since ordering, they show **Late**.
  - Tap an order to open it: **Copy** (name, phone, address and item for the package), **Change delivery**, Shein cost, **Edit order**, **Delete**.
- **Add**: TikTok username, name, number, address, item, price (Nu.), date (defaults to today), optional cost. Returning customers get a one-tap "Fill details".
- **Report**: This month / Last month / All time. Shows money received, Shein cost, profit, orders at each step, losing orders and the top 5 customers.

## Data

One document per order in the `orders` collection:

| field | meaning |
|---|---|
| `tiktok`, `name`, `phone`, `address` | original details as taken on TikTok (never overwritten by a delivery change) |
| `delivery` | `null`, or `{name, phone, address, changedAt}` when the delivery details were changed |
| `item`, `price`, `cost` | prices in Nu.; `cost` is `null` until entered |
| `date` | order date `YYYY-MM-DD` (grouping key) |
| `status` | `paid` / `ordered` / `arrived` / `delivered` |
| `orderedAt`, `arrivedAt`, `deliveredAt` | `YYYY-MM-DD` when each step was reached |
| `createdAt` | ISO timestamp |

Profit only counts orders that have a cost. The report shows how many orders still need one.
