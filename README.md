# SOMA Pre-orders

A phone-friendly tracker for SOMA's TikTok pre-orders: customer pays → ordered on Shein → parcel arrives from Bangkok → delivered.

The whole app is one file, `index.html`. It runs as a Claude artifact. That keeps orders in an online database, so any phone signed in to the same claude.ai account sees the same orders. Opened anywhere else (a downloaded copy, another host), it falls back to saving on that phone only and shows a banner saying so.

## Screens

- **Orders**: one line per day ("Orders of 07 Nov · 4 orders · Nu. 3,600", with to-order / not-arrived / late / to-deliver / all-delivered tags), newest first. Today is open; tap any day to open or close it (remembered on that phone). Filters and search open every day. Filters: Active, To order, Not arrived, Late, To deliver, No cost, All, plus search. Status is per order, so parcels from one day can arrive on different days; day lines show "N not arrived" and "N to deliver".
  - Tap a step (Paid, Ordered 💵, Arrived, Delivered) to set an order's status. Going back clears the later dates.
  - **Place Shein order 💵** on a day header opens the cart step. Tick the orders that went into one Shein checkout (that day's are ticked; older unordered ones can be added), enter the total paid in Baht and, optionally, the Shein order number. Item prices already entered on an order are filled in. With no total typed, each order keeps its own item price and the cart total is their sum. A typed total (for shipping or discounts) is split across the ticked orders by item price when every one has one, otherwise by what each customer paid. The ticked orders move to Ordered with their cost filled in.
  - Ordered parcels show "Day N of 8–10". Once more than 10 days have passed since ordering, they show **Late**.
  - Tap an order to open it: **Copy** (name, phone, address and item for the package), **Change delivery**, Shein cost, **Edit order**, **Delete**.
- **Add**: TikTok username, name, number, address, item, price (Nu.), date (defaults to today), optional Shein cost in Baht. Returning customers get a one-tap "Fill details". Saving shows an "Order saved" screen with **Add another order** and **See orders**.
- **Report**: sets the Baht rate (฿1 = Nu. …, default 2.85). This month / Last month / All time show money received, Shein cost, profit, orders at each step, losing orders and the top 5 customers.

## Baht costs

Shein costs are typed in Baht and converted to Nu. with the rate on the Report screen. Each order saves the rate in force when its cost was entered, so changing the rate later does not change past profit.

## Data

One document per order in the `orders` collection:

| field | meaning |
|---|---|
| `tiktok`, `name`, `phone`, `address` | original details as taken on TikTok (never overwritten by a delivery change) |
| `delivery` | `null`, or `{name, phone, address, changedAt}` when the delivery details were changed |
| `item`, `price` | price paid in Nu. |
| `costBaht`, `rate`, `cost` | Shein cost in Baht, the Nu.-per-Baht rate used, and the cost in Nu. (`costBaht × rate`, rounded); all `null` until entered |
| `date` | order date `YYYY-MM-DD` (grouping key) |
| `status` | `paid` / `ordered` / `arrived` / `delivered` |
| `orderedAt`, `arrivedAt`, `deliveredAt` | `YYYY-MM-DD` when each step was reached |
| `sheinOrder` | `{id, no, totalBaht, count, placedAt}` for the Shein checkout the order went in, or absent |
| `createdAt` | ISO timestamp |

The rate lives in `settings/main` as `{rate}`.

Profit only counts orders that have a cost. The report shows how many orders still need one.
