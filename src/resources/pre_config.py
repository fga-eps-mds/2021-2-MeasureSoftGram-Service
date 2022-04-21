import requests
import mongoengine as me
from flask import request
from flask_restful import Resource
from src.model.pre_config import PreConfig
from src.resources.utils import simple_error_response


DUPLICATED_PRE_CONFIG_NAME_MSG = "The pre config name is already in use"


class PreConfigs(Resource):
    def post(self):
        data = request.get_json(force=True)

        try:
            pre_config = PreConfig(
                name=data.get("name", None),
                characteristics=data["characteristics"],
                subcharacteristics=data["subcharacteristics"],
                measures=data["measures"],
            )

            pre_config.save()
        except me.errors.NotUniqueError:
            return simple_error_response(
                DUPLICATED_PRE_CONFIG_NAME_MSG, requests.codes.unprocessable_entity
            )

        return pre_config.to_json(), requests.codes.created

    def patch(self, pre_config_id):
        pre_config, error_msg = self.get_pre_config(pre_config_id)

        if pre_config is None:
            return simple_error_response(error_msg, requests.codes.not_found)

        data = request.get_json(force=True)

        try:
            updated_entries = pre_config.update(**data)

            if updated_entries == 0:
                return simple_error_response(
                    "Update failed, please try again later",
                    requests.codes.internal_server_error,
                )

            pre_config.reload()

            return pre_config.to_json(), requests.codes.ok
        except me.errors.NotUniqueError:
            return simple_error_response(
                DUPLICATED_PRE_CONFIG_NAME_MSG, requests.codes.unprocessable_entity
            )
        except me.errors.ValidationError as error:
            return simple_error_response(
                f"{str(error.value)}", requests.codes.unprocessable_entity
            )

    def get_pre_config(self, pre_config_id):
        try:
            pre_config = PreConfig.objects.with_id(pre_config_id)

            if pre_config is None:
                return None, f"There is no pre configurations with ID {pre_config_id}"

            return pre_config, None
        except me.errors.ValidationError:
            return None, f"{pre_config_id} is not a valid ID"
