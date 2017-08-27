# Item Trading Club app
is a full-stack Python Django app that creates a marketplace for items to be traded.

### User Stories
* Unauthenticated users can view all items up for trade.
* Users must register to participate in a trade.
* When a user sees an item he wants to trade for he can send a proposal
* A user can trade only when he has an item he is willing to exchange with.
* A user can upload pictures of the items he wants to trade, along with other info.
* Upon trade acceptance, both users will see each other's emails

FUTURE FEATURES :
* Websockets chat app for interacting with Club members (for now users can email each other after the trade is finalized).

### Model
```
User
|___ id INT
|___ firstname VARCHAR 20
|___ lastname VARCHAR 20
|___ username VARCHAR 20
|___ email VARCHAR 50 # for account recovery
|___ password VARCHAR
|___ location VARCHAR # to find out if trade users are near each other

Item
|___ id INT
|___ user_id INT FOREIGN-KEY
|___ name VARCHAR
|___ description TEXT
|___ picture VARCHAR

Proposal
|___ id INT
|___ sender_id INT
|___ receiver_id INT
|___ sender_book_id INT
|___ rcvr_book_id INT
|___ status

```


### Routes
```
# USERS
# -----
# login & register in 'login/register page'
/login - GET
/login - POST

# register
/register - POST

# edit / close user account in 'user admin page'
/user/edit - GET
/user/edit - POST
/user/delete - DELETE

# ITEMS
# -----
# display all items in 'item browsing page'
/items - GET

# create item in 'item add dashboard page'
/item/add - GET
/item/add - POST

# edit item 'item edit dashboard page'
/item/edit - GET
/item/edit - PUT

# delete item
/item/delete - DELETE

# TRADE
# -----
# trade transactions in 'trade dashboard page'
/items/trade - GET
/items/trade/propose - POST
/items/trade/accept - POST

# if receiver deletes proposal
/items/trade/reject - POST

# if sender deletes proposal
/items/trade/delete - POST
```

### Authors
Neptune Michael Cabelin
Artemio Cabelin

### License
MIT
