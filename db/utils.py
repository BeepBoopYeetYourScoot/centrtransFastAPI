from db.conf import LocalSession


async def get_session():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    session = get_session()
