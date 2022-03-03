"""Redis client module."""
from redis import asyncio, Redis
from helpers import hashing
class DB():
    def __init__(self):
        self.conn = None
    
    def __str__(self):
        if self.conn:
            return f"{self.get_host()}|{self.get_port()}"
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
    
    def receipt_safe(self, receipt: dict):
        for r in self.conn.smembers("receipts"):
            receipt_dict = hashing.get_dict(r)
            score = hashing.receipts_similarity(receipt, receipt_dict)
            print(score)
            if score > 0.70:
                return False
        return True
    
    def add_receipt(self, receipt: dict):
        if self.receipt_safe(receipt):
            if self.conn.sadd("receipts", hashing.get_json(receipt)):
                return {"detail": "OK"}
            else:
                return {"detail": "something went wrong when adding the receipt"}
        else:
            return {"detail": "High chance of receipt already existing!"}
    
    def get_receipt(self):
        pass

async def redis_pool(host: str, password: str):
    redis = asyncio.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
