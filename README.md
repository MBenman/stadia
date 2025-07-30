# Stadia
A REST API for sports stadiums

# Local Setup
* Clone repo
  `git@github.com:MBenman/stadia.git`
* Run make file
  `make run`
* Visit API docs at `http://127.0.0.1:8000/api/docs`

# Methods
## GET
`/api/stadiums`
* Show all stadiums
Attributes:
* `id` int: ID
* `name` string: Name of stadium
* `sport` string: Primary sport played at stadium
* `city` string: City
* `state` string: State
* `capacity` int: Capacity for primary sport

`/api/stadiums/{stadium_id}`
* Get Stadium by ID
## POST
`/api/stadiums`
* Create Stadium
Attributes:
* `name` string: Name of stadium
* `sport` string: Primary sport played at stadium
* `city` string: City
* `state` string: State
* `capacity` int: Capacity for primary sport
## PUT
`/api/stadiums/{stadium_id}`
* Update Stadium by ID
## DELETE
`/api/stadiums/{stadium_id}`
* Delete Stadium by ID