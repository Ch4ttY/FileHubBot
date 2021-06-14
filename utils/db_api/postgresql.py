from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Users:

    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )
        return cls(pool)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command,  *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE       
        );        
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users (full_name, username, telegram_id) VALUES ($1, $2, $3)"
        return await self.execute(sql, full_name, username, telegram_id, execute=True)

    async def check_user(self, telegram_id):
        sql = "SELECT telegram_id FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def select_all_users(self):
        sql = "select array(SELECT telegram_id FROM Users)"
        return await self.execute(sql, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)


class Files:

    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )
        return cls(pool)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command,  *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_files(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Files(
        id SERIAL PRIMARY KEY,
        file_id VARCHAR(255) NOT NULL    
        );        
        """
        await self.execute(sql, execute=True)

    async def add_file(self, file_id):
        sql = "INSERT INTO Files (file_id) VALUES ($1)"
        return await self.execute(sql, file_id, execute=True)

    async def check_file_exists(self, file_id):
        sql = "SELECT id FROM Files WHERE id=$1"
        return await self.execute(sql, file_id, fetchval=True)

    async def get_file_id(self, file_numb):
        sql = "SELECT file_id FROM Files WHERE id=$1"
        return await self.execute(sql, file_numb, fetchval=True)

    async def get_file_numb(self, file_id):
        sql = "SELECT id FROM Files WHERE file_id=$1"
        return await self.execute(sql, file_id, fetchval=True)


class Sponsors:

    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )
        return cls(pool)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command,  *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_sponsors(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Sponsors(
        id INTEGER PRIMARY KEY,
        channel_link VARCHAR(255) NOT NULL    
        );        
        """
        await self.execute(sql, execute=True)

    async def add_sponsor(self, sponsor_link):
        sql = "UPDATE Sponsors SET channel_link=$1 WHERE id=1"
        #sql = "INSERT INTO Sponsors (id, channel_link) VALUES(1,$1)"
        return await self.execute(sql, sponsor_link, execute=True)

    async def get_channel_link(self):
        sql = "SELECT channel_link FROM Sponsors WHERE id=1"
        return await self.execute(sql, fetchval=True)


