## Headscale API client

This module is a client for Headscale API.
It can manage all the entities of headscale, namely:

- nodes
- users
- routes
- preauthkeys
- apikeys

Wherever it was possible I used python data types, for example `datetime` is used for all the dates, while `int` is used for all IDs;

### Schemas

Using the OpenAPI specs provided by headscale, I converted them to python classes, so you can refer to the Headscale OpenAPI specification in file `headscale.openapi.json` for more details, but I will try to provide a list of classes and methods available.

#### Nodes

Methods:

- `list`: list all the nodes registered on headscale;
- `get`: retrieve a specific node by its ID
- `byUser`: retrieve all the nodes of a user, given the `username`;
- `delete`: deletes a node, by ID;
- `expire`: expire (disconnect) a node, by ID;
- `rename`: rename a node, by ID;
- `move`: assing a nide to a new user;
- `routes`: retrieve all the routes announced by a node;
- `setTags`: set tags for a node;
- `backfillips`: (currently broken in Headscale), fills the nodes table with all the IPs, to be used in rare cases;

Properties:

- `expired`: if the node is expired;
- `expireDate`: when the node is going to expire;

#### Users

Methods:

- `list`: list all users'
- `get`: get a user, by ID;
- `create`: create a new user, given a username;
- `delete`: delete a user, given the username;
- `rename`: rename a user, given the current and the new username;

#### Routes

Methods:

- `list`: get all routes;
- `delete`: deletes a route, given the ID;
- `enable`: enable a route, given the ID;
- `disable`: disable a route given the ID;

### API Keys

Methods:

- `list`: list all the API keys;
- `create`: create a new API key;
- `expire`: invalidates a new API key;
- `delete`: delete an API key;

### PreAuth keys

Methods

- `list`: list all the preauth keys for a user;
- `create`: create a new preauth key for a user;
- `expire`: expires (invalidates) a preauth key for a user;

### Configuration

To be able to access headscale the module needs the URL of the headscale portal and an API key.
These values are provided via environment variables, specifically:

- `HSAPI_SERVER`
- `HSAPI_API_TOKEN`
