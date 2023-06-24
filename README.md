## User Access Management

## Setup

```bash
git clone git@github.com:realvaibhav/Identity-Access-Management.git
cd identity-access-management
pip3 install -r requirements.txt
```

- Setup and run mongo server
- Update the .env variables
- Run `uvicorn main:app --reload`

## Collections

![db]

(https://user-images.githubusercontent.com/54521023/234565503-1cdad4e0-d437-4084-bc98-8b17050d48c5.png)

## Endpoints

- https://${BASE_URL}


### Users

#### ``POST`` Create new user
- https://${BASE_URL}/user/


```
{
  "name": "vaibhav",
  "email": "realvaibhav2002@gmail.com"
}
```

#### ``GET`` Get user by ID
- https://${BASE_URL}/user/6449157fbc73adf705e6c418


#### ``GET`` Get user by Email
- https://${BASE_URL}/user/?email=realvaibhav



#### ``GET`` List of oraganisations for a user
- https://${BASE_URL}/user/6449157fbc73adf705e6c418/organisations?limit=10&offset=0


## Organisation

#### ``POST`` Create new organisation
- https://${BASE_URL}/organisation/

```
{
  "name": "My App"
}
```

#### ``GET`` Get organisation by ID 
- https://${BASE_URL}/organisation/644917edbc73adf705e6c419


#### ``GET`` Get organisation by Name
- https://${BASE_URL}/organisation/?name=My%20App



#### ``GET`` List of users from an organisation
- https://${BASE_URL}/organisation/644917edbc73adf705e6c419/users?limit=10&offset=0


#### ``GET`` List of organisations
- https://${BASE_URL}/organisation/?limit=10&offset=0


### Permissions

#### ``POST`` Add user(s) to an organisation
- https://${BASE_URL}/permissions/644917edbc73adf705e6c419

```
[
  "6449157fbc73adf705e6c418", "6449123dbc73adf705e6c417"
]
```

#### ``PUT`` Update user(s) permissions
- https://${BASE_URL}/permissions/644917edbc73adf705e6c419?access_level=READ

```
[
  "6449157fbc73adf705e6c418", "6449123dbc73adf705e6c417"
]
```

#### ``DELETE`` Delete user(s) from an organisation
- https://${BASE_URL}/api/permissions/644917edbc73adf705e6c419

```
[
  "6449157fbc73adf705e6c418", "6449123dbc73adf705e6c417"
]
```