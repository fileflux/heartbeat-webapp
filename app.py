import logging
from logging.config import dictConfig
from flask import Flask, request, jsonify
from db import get_db
from flask.logging import default_handler

app = Flask(__name__)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    node_name = data.get('node_name')
    zpool_name = data.get('zpool_name')
    total_space = data.get('total_space')
    available_space = data.get('available_space')

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO nodes (node_name, zpool_name, total_space, available_space, last_heartbeat) "
        "VALUES (%s, %s, %s, %s, current_timestamp) "
        "ON CONFLICT (node_name) DO UPDATE SET "
        "zpool_name = EXCLUDED.zpool_name, "
        "total_space = EXCLUDED.total_space, "
        "available_space = EXCLUDED.available_space, "
        "last_heartbeat = EXCLUDED.last_heartbeat",
        (node_name, zpool_name, total_space, available_space)
    )

    db.commit()
    cursor.close()

    app.logger.info(f"Node '{node_name}' registered/updated successfully")
    return jsonify({"message": "Node registered/updated successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
