from .schema import ma

class transactionSchemaSaveApplicationID(ma.Schema):
    
    class Meta:
        fields = ("id", "application_id", "dt_log")