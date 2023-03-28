# MagicHelper (@backend)

## What it is?

This is the main component of [MagicHelper system](https://github.com/MagicRustHelper). The work of the other components depends on him. The MagicHelper system digitilize [Magic Rust](https://vk.com/magicowrust) for moderators and helps them to communicate with peoples and watch the server.

### What it does?

Provides REST API interface for communicate with database and services.
The API build by **FASTAPI**.

### Services 

Services at the moment provide to communicate with other API's and getting easy to use interface:
* Magic Rust
* [RustCheatCheck](http://rustcheatcheck.ru/)
* [Steam](https://steamcommunity.com/dev)
* VK oauth2

For HTTP responses, use **HTTPX**.  
To desribe a response entities, use **pydantic**.

### Database 

This project uses a Postgres.   
For interacting **SQLAlchemy** + **asyncpg**. And **alembic** for migrations.

## How to run

### Requirements
* Docker compose
* Python ^3.10

For start up the project configure `.env.example` and rename to `.env.dev`. And write make command:
```
make dev
```

# Deploy
...

