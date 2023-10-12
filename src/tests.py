
import os
import time
import pytest
from rdb_store.dbops import get_db, SessionLocal
from main_app import application_intro


class TestApplication:

    @pytest.mark.asyncio
    async def test_tables_initialized_successfully(self, mocker):
        mocker.patch('os.system')
        result = await application_intro()
        os.system.assert_called_once_with(f"PGPASSWORD={os.getenv('POSTGRES_PASSWORD')} psql -h {os.getenv('POSTGRES_HOST')} -U postgres -q -f init.sql")
        assert result == {
            "Message": "Tables initialized - users, items and carts"
        }

    def test_generates_database_session(self):
        db = get_db()
        assert db is not None
