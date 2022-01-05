from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_blockchain import Blockchain

DATABASE='blokx_schema'

import jsonpickle
if not Blockchain.get_backup():
    # Backup chain
    CHAIN=Blockchain()
    frozen=jsonpickle.encode(CHAIN)
    backup_id=Blockchain.create_backup(frozen)
    query="UPDATE blockchain_backup SET id=1 WHERE id=%(id)s;"
    connectToMySQL(DATABASE).query_db(query, {"id":backup_id}, show_query=False)
else:
    # Get chain backup
    frozen=Blockchain.get_backup()
    # print("FROZEN*******************")
    # print(frozen['blockchain'])
    CHAIN=jsonpickle.decode(frozen['blockchain'])


if not Blockchain.get_txn_backup():
    # create txn backup
    CHAIN.pending_txns=[]
    frozen=jsonpickle.encode(CHAIN.pending_txns)
    backup_id=Blockchain.create_txn_backup(frozen)
    Blockchain.reset_txn_backup_id(backup_id)
else:
    # Get txn backup
    frozen=Blockchain.get_txn_backup()
    CHAIN.pending_txns=jsonpickle.decode(frozen['txn'])