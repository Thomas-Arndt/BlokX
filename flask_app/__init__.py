from flask import Flask
import jsonpickle


from flask_app.models.model_blockchain import Blockchain

app=Flask(__name__)
app.secret_key="fd77e312-fabf-49e5-9a9f-ed9c8fb77c1e"


if not Blockchain.get_backup():
    # Backup chain
    CHAIN=Blockchain()
    frozen=jsonpickle.encode(CHAIN)
    Blockchain.create_backup(frozen)
else:
    # Get chain backup
    frozen=Blockchain.get_backup()
    # print("FROZEN*******************")
    # print(frozen['blockchain'])
    CHAIN=jsonpickle.decode(frozen['blockchain'])

