#!/usr/bin/env python
# encoding: utf-8
import json
import logging
import threading
import time
import uuid

from flask import Blueprint
from flask import request

from simplyblock_web import utils

from simplyblock_core import kv_store, grafana_ops


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
gf = Blueprint("grafana", __name__)
db_controller = kv_store.DBController()

@gf.route('/organizations', methods=['POST'])
def create_organization():
    data = request.json
    response = grafana_ops.create_grafana_organization(data)

    if response.status_code == 200:
        return utils.get_response(response)
    else:
        return jsonify({'error': response.text}), response.status_code

# @gf.route('/organizations/<int:org_id>', methods=['PUT'])
# def update_organization(org_id):
#     data = request.json
#     response = grafana_ops.update_grafana_organization(org_id, data)

#     if response.status_code == 200:
#         return jsonify(response.json()), 200
#     else:
#         return jsonify({'error': response.text}), response.status_code

# @gf.route('/organizations/<int:org_id>', methods=['DELETE'])
# def delete_organization(org_id):
#     response = grafana_ops.delete_grafana_organization(org_id)

#     if response.status_code == 200:
#         return jsonify({'message': 'Organization deleted successfully'}), 200
#     else:
#         return jsonify({'error': response.text}), response.status_code