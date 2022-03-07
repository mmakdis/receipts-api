"""Redis client module."""
from redis import asyncio, Redis
from helpers import receipt

class DB():
    """Interface for the API's db. Uses Redis.

    Autoconnect with DB.connect() to connect to localhost.
    """

    def __init__(self):
        self.conn = None
    
    def __str__(self) -> str:
        """Pretty-prints the instance object.

        Returns:
            str: "host:port"
        """
        if self.conn:
            return f"{self.get_host()}:{self.get_port()}"
        else:
            return "Not connected to the database, please connect!"
        
    def get_port(self):
        """Get the port quickly

        Returns:
            int: the port.
        """
        return self.conn.get_connection_kwargs()["port"]
    
    def get_host(self):
        """Get the host quickly

        Returns:
            str: the host
        """
        return self.conn.get_connection_kwargs()["host"]
    
    def connect(self, host=None, port=None):
        if host and port:
            self.conn = Redis(host=host, port=port)
        else:
            self.conn = Redis()
        return self.conn
    
    def ping(self):
        return "PONG" if self.conn.ping() else "NAH"
    
    def receipt_safe(self, receipt_data: dict):
        for r in self.conn.smembers("receipts"):
            receipt_dict2 = receipt.get_dict(r)
            score = receipt.receipts_similarity(receipt_data, receipt_dict2)
            if score > 0.70:
                return False
        return True
    
    def add_receipt(self, receipt_data: dict):
        if not self.receipt_safe(receipt_data):
            return {"detail": "High chance of receipt already existing!"}
        if self.conn.sadd("receipts", receipt.get_json(receipt_data)):
            return {"detail": "OK"}
        else:
            return {"detail": "something went wrong when adding the receipt"}
    
    def get_receipt(self):
        pass

async def redis_pool(host: str, password: str):
    redis = asyncio.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
