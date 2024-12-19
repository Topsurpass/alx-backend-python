import asyncio
import aiosqlite


async def async_fetch_users():
    """
    Fetches all users from the database asynchronously.

    :return: List of all users.
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users


async def async_fetch_older_users():
    """
    Fetches users older than 40 from the database asynchronously.

    :return: List of users older than 40.
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            return older_users


async def fetch_concurrently():
    """
    Runs both `async_fetch_users` and `async_fetch_older_users` concurrently
    and prints their results.
    """
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )

    all_users, older_users = results
    print("All Users:")
    print(all_users)
    print("\nUsers Older Than 40:")
    print(older_users)


if __name__ == "__main__":
    """
    Entry point to run the concurrent fetch using asyncio.run().
    """
    asyncio.run(fetch_concurrently())
