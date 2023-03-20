from .schema import ma

class TransactionSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "status", "origin","destiny","created")