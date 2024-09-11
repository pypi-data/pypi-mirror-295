"""
    Policy decision point implementation
"""

from copy import deepcopy

from .call_api import CallAPI
from .policy import PolicySchema, AccessType
from .policy.utils import Utils
from .result_access import ResultAccess
from .config import RedisClient, Timer


class PolicyDecisionPoint(object):
    """
        Policy decision point
    """

    class AccountType:
        SYSTEM = "system"
        NORMAL = "normal"

    class AccessLevel:
        LIST = "list"
        READ = "read"
        ADD = "add"
        EDIT = "edit"
        DELETE = "delete"
        OTHER = "other"

    class AuthorizationType:
        BASIC = 'basic'
        BEARER = 'bearer'
        DIGEST = 'digest'

    def __init__(self,
                 merchant_id: str = None, resource: str = None, action: str = None, account_id: str = None,
                 user_info: dict = None, data_before: dict = None, data_after: dict = None, environment: dict = None,
                 account_type=AccountType.NORMAL):
        if not resource:
            raise ValueError("resource required")
        if not action:
            raise ValueError("action required")
        pass_policy = False
        if account_type == self.AccountType.NORMAL and (not merchant_id or not account_id):
            auth_type, json_token = Utils.get_info_jwt()
            if auth_type == self.AuthorizationType.BEARER:
                merchant_id = json_token.get("merchant_id")
                account_id = json_token.get("account_id")
            else:
                account_type = self.AccountType.SYSTEM
        if account_type == PolicyDecisionPoint.AccountType.NORMAL:
            if not merchant_id:
                raise ValueError("merchant_id required")
            if not account_id:
                raise ValueError("account normal account_id required")
            if not user_info:
                user_info = CallAPI.admin_get_account_info(merchant_id, account_id)
            # if not self.check_merchant_use_abac(merchant_id):
            #     pass_policy = True
        elif account_type == PolicyDecisionPoint.AccountType.SYSTEM:
            pass_policy = True

        self.pass_policy = pass_policy
        self.account_type = account_type
        self.merchant_id = merchant_id
        self.account_id = account_id
        self.resource = resource
        self.action = action
        self.request_access = {}
        self.result_access = ResultAccess()
        self.request_access.update({
            "user": user_info if user_info else {},
            "env": self.get_info_environment(environment),
            self.resource: data_before if data_before else {}
        })
        self.data_after = data_after if data_after else {}
        self.data_before = data_before if data_before else {}
        self.access_level = ""
        self.service = ""
        self.result_access.data_log = {
            "merchant_id": self.merchant_id,
            "account_id": self.account_id,
            "action": "LOG_ENGINE_ABAC",
            "other": {
                "resource": self.resource,
                "action": self.action,
                "data_before": self.data_before,
                "data_after": self.data_after,
            },
        }
        self.resource_valid = ["user", "env", resource]
        self.check_info_action()

    # TODO: bo su dung ham nay tren production
    @classmethod
    def check_merchant_use_abac(cls, merchant_id):
        # set merchant_use_abac '972e6e1d-8891-4fdb-9d02-8a7855393298;87d9e1f3-6da0-415f-b418-9ba9f4fe5523;1b99bdcf-d582-4f49-9715-1b61dfff3924;10350f12-1bd7-4369-9750-46d35c416a46'
        use_abac = False
        data_cache = RedisClient().get_value(RedisClient.KeyCache.MERCHANT_USE_ABAC)
        if data_cache:
            data_merchant = str(data_cache.decode("utf-8")).split(";")
        else:
            data_merchant = ["972e6e1d-8891-4fdb-9d02-8a7855393298", "87d9e1f3-6da0-415f-b418-9ba9f4fe5523",
                             "10350f12-1bd7-4369-9750-46d35c416a46"]
        if merchant_id in data_merchant:
            use_abac = True
        return use_abac

    def get_policy_statement_for_target(self):
        list_statement = CallAPI.admin_get_list_statement(self.merchant_id, self.account_id,
                                                          self.resource, self.action, self.service)
        if not list_statement:
            print("abac_sdk list_statement not found merchant_id: {} , account_id: {} , "
                  "resource: {} , action: {} , service: {} ".format(self.merchant_id, self.account_id,
                                                                    self.resource, self.action, self.service))
        self.result_access.data_log.get("other", {}).update({"list_statement": list_statement})
        return list_statement

    def is_allowed(self):
        """
            Check if authorization request is allowed

            :param request: request object
            :return: True if authorized else False
        """
        # time_run = Timer()
        # time_run.start()
        try:
            if self.pass_policy:
                self.result_access.set_allow_access(True)
                return self.result_access
            list_statement = self.get_policy_statement_for_target()
            if list_statement:
                if self.access_level == PolicyDecisionPoint.AccessLevel.ADD:
                    self.data_after.update(self.data_before)
                statement_check_allow, statement_check_deny = self.get_statement_by_type(list_statement)
                if statement_check_deny:
                    if self.check_list_statement_is_deny(statement_check_deny):
                        self.result_access.set_allow_access(False)
                        return self.result_access
                if statement_check_allow:
                    self.result_access.set_allow_access(self.check_list_statement_is_allow(statement_check_allow))
                else:
                    self.result_access.set_allow_access(False)
            else:
                self.result_access.set_allow_access(False)
        except Exception as err:
            msg_err = "abac_sdk is_allowed err: {}".format(err)
            print(msg_err)
            self.result_access.add_log_error(msg_err)
            self.result_access.set_allow_access(False)
        # time_run.stop()
        return self.result_access

    @classmethod
    def get_info_environment(cls, environment):
        if not environment:
            environment = Utils.get_info_from_header_request()
            # if environment:
            #     if environment.get("env:user_agent"):
            #         environment.update(Utils.parse_user_agent(environment.get("env:user_agent")))
        environment = environment if environment else {}
        environment.update({"current_time": Utils.get_date_utcnow()})
        if not environment.get("device_type"):
            environment.update({"device_type": "web"})
        return environment

    def get_value_from_variable(self, str_variable):
        if isinstance(str_variable, str) and Utils.check_field_is_variable(str_variable):
            variables = Utils.get_field_key_from_variable(str_variable)
            if variables:
                if len(variables) == 1:
                    field_value = self.get_value_from_field(variables[0])
                    if isinstance(field_value, str):
                        field_value_format = Utils.replace_variable_to_value(variables[0], field_value, str_variable)
                        return field_value_format
                    return field_value
                for field_key in variables:
                    field_value = self.get_value_from_field(field_key)
                    if field_value is not None:
                        field_value = str(field_value)
                        str_variable = Utils.replace_variable_to_value(field_key, field_value, str_variable)
        return str_variable

    def get_value_from_field(self, field_key):
        resource_name, resource_key = Utils.split_delemiter_resource(field_key)
        if resource_name and resource_key:
            if self.request_access.get(resource_name) and isinstance(self.request_access.get(resource_name), dict):
                data_resource = self.request_access.get(resource_name)
                value = Utils.get_nested_value(data_resource, resource_key)
                return value
        return None

    def get_statement_by_type(self, list_statement: list, check_list=False):
        statement_check_allow, statement_check_deny = [], []
        for statement in list_statement:
            condition_valid = []
            for cond_check in statement.get("condition"):
                resource_name, resource_key = Utils.split_delemiter_resource(cond_check.get("field"))
                if resource_name in self.resource_valid:
                    condition_valid.append(cond_check)
            statement["condition"] = condition_valid
            statement_copy = deepcopy(statement)
            fields = []
            if statement_copy.get("resource_field") and statement_copy.get("resource_field").get(self.resource):
                fields = statement_copy.get("resource_field").get(self.resource)
            if fields:
                statement_copy["fields"] = fields
            if self.access_level in [PolicyDecisionPoint.AccessLevel.LIST,
                                     PolicyDecisionPoint.AccessLevel.OTHER, ]:
                condition_check = []
                condition_filter = []
                if check_list:
                    condition_check = statement_copy.get("condition")
                else:
                    for item_cond in statement_copy.get("condition"):
                        if item_cond.get("field").startswith("user") or item_cond.get("field").startswith("env"):
                            condition_check.append(item_cond)
                        else:
                            values = []
                            for i in item_cond.get("values"):
                                value_from_variable = self.get_value_from_variable(i)
                                if isinstance(value_from_variable, list):
                                    values.extend(value_from_variable)
                                else:
                                    values.append(value_from_variable)
                            item_cond["values"] = values
                            condition_filter.append(item_cond)
                if condition_filter:
                    statement_copy["condition_filter"] = condition_filter
                if statement_copy.get("effect") == AccessType.ALLOW_ACCESS:
                    statement_check_allow.append({
                        **statement_copy,
                        "condition": condition_check
                    })
                else:
                    statement_check_deny.append({
                        **statement_copy,
                        "condition": condition_check
                    })

            elif self.access_level in [PolicyDecisionPoint.AccessLevel.READ,
                                       PolicyDecisionPoint.AccessLevel.DELETE]:
                if statement_copy.get("effect") == AccessType.ALLOW_ACCESS:
                    statement_check_allow.append(statement_copy)
                else:
                    statement_check_deny.append(statement_copy)
            else:
                if self.resource in ["profile", "company"] and self.action == "Add":
                    # voi profile va company khi them moi bo qua dieu kien product_holding
                    condition_check = []
                    for item_cond in statement_copy.get("condition"):
                        if item_cond.get("sub_resource") and item_cond.get("sub_resource") == "product_holding":
                            continue
                        else:
                            condition_check.append(item_cond)
                    statement_copy["condition"] = condition_check

                if fields:
                    statement_copy["check_field"] = 1
                if statement_copy.get("effect") == AccessType.ALLOW_ACCESS:
                    statement_check_allow.append(statement_copy)
                else:
                    statement_check_deny.append(statement_copy)
        return statement_check_allow, statement_check_deny

    def check_list_statement_is_deny(self, list_statement: list, check_list=False):
        result_deny = False
        for statement in list_statement:
            try:
                # if self.access_level == PolicyDecisionPoint.AccessLevel.EDIT:
                #     statement["request_access"] = self.request_access
                #     try:
                #         policy_schema = PolicySchema().load(statement)
                #         statement_allow = policy_schema.is_allowed()
                #         statement["condition_convert"] = policy_schema.get_condition_convert()
                #     except:
                #         statement_allow = False
                #     if not statement_allow:
                #         request_access_after = deepcopy(self.request_access)
                #         request_access_after.get(self.resource, {}).update(
                #             self.data_after if self.data_after else {}
                #         )
                #         statement["request_access"] = request_access_after
                #         policy_schema = PolicySchema().load(statement)
                #         statement_allow = policy_schema.is_allowed()
                # else:
                statement["request_access"] = self.request_access
                policy_schema = PolicySchema().load(statement)
                statement_allow = policy_schema.is_allowed()
                statement["condition_convert"] = policy_schema.get_condition_convert()
                if statement_allow:
                    statement_deny = {
                        "policy_name": statement.get("policy_name", ""),
                        "condition": statement.get("condition", [])
                    }
                    if self.access_level == PolicyDecisionPoint.AccessLevel.READ:
                        # tìm tất cả các cấu hình ẩn hiện field nếu có
                        if statement.get("fields"):
                            self.result_access.add_display_config({
                                "effect": statement.get("effect"),
                                "fields": statement.get("fields"),
                            })
                            continue
                    elif self.access_level in [PolicyDecisionPoint.AccessLevel.LIST,
                                               PolicyDecisionPoint.AccessLevel.OTHER, ]:
                        if statement.get("fields"):
                            self.result_access.add_display_config({
                                "effect": statement.get("effect"),
                                "fields": statement.get("fields"),
                            })
                        # tìm tất cả các điều kiện bộ lọc với action list
                        if statement.get("condition_filter"):
                            self.result_access.add_filter_config(
                                {"effect": statement.get("effect"),
                                 "condition": statement.get("condition_filter")})
                            continue
                    else:
                        # nếu ko có field nào ở cấu hình policy nằm trong dữ liệu gửi lên thì cho qua
                        if statement.get("check_field") and statement.get("fields"):
                            if self.access_level == PolicyDecisionPoint.AccessLevel.ADD:
                                fields_deny = Utils.add_field_in_body_request(statement.get("fields"), self.data_after)
                                if not fields_deny:
                                    continue
                            else:
                                fields_deny = Utils.field_in_body_request(statement.get("fields"), self.data_after)
                                if not fields_deny:
                                    continue
                            statement_deny.update({
                                "fields_deny": fields_deny
                            })
                    if not check_list:
                        self.result_access.add_log_deny(statement)
                    self.result_access.add_data_deny({
                        "data_after": self.data_after,
                        "data_before": self.data_before,
                        "policy": [statement_deny],
                        "effect": AccessType.DENY_ACCESS
                    })
                    result_deny = True
                    break
            except Exception as err:
                msg_err = "abac_sdk check_list_statement_is_deny err: {}".format(err)
                print(msg_err)
                self.result_access.add_log_error(
                    msg_err + " - policy_name: {}".format(statement.get("policy_name", "")))
                # result_deny = False
        return result_deny

    def check_list_statement_is_allow(self, list_statement: list, check_list=False):
        result_allow = False
        policy_fail = []
        for statement in list_statement:
            try:
                # if self.access_level == PolicyDecisionPoint.AccessLevel.EDIT:
                #     statement["request_access"] = self.request_access
                #     policy_schema = PolicySchema().load(statement)
                #     statement_allow = policy_schema.is_allowed()
                #     statement["condition_convert"] = policy_schema.get_condition_convert()
                #     if statement_allow:
                #         request_access_after = deepcopy(self.request_access)
                #         request_access_after.get(self.resource, {}).update(
                #             self.data_after if self.data_after else {}
                #         )
                #         statement["request_access"] = request_access_after
                #         policy_schema = PolicySchema().load(statement)
                #         statement_allow = policy_schema.is_allowed()
                # else:
                statement["request_access"] = self.request_access
                policy_schema = PolicySchema().load(statement)
                statement_allow = policy_schema.is_allowed()
                statement["condition_convert"] = policy_schema.get_condition_convert()

                if statement_allow:
                    result_allow = True
                    if not check_list:
                        self.result_access.add_log_allow(statement)
                    if self.access_level == PolicyDecisionPoint.AccessLevel.READ:
                        # tìm tất cả các cấu hình ẩn hiện field nếu có
                        if statement.get("fields"):
                            self.result_access.add_display_config({
                                "effect": statement.get("effect"),
                                "fields": statement.get("fields"),
                            })
                            continue
                    elif self.access_level in [PolicyDecisionPoint.AccessLevel.LIST,
                                               PolicyDecisionPoint.AccessLevel.OTHER, ]:
                        if statement.get("fields"):
                            self.result_access.add_display_config({
                                "effect": statement.get("effect"),
                                "fields": statement.get("fields"),
                            })
                        # tìm tất cả các điều kiện bộ lọc với action list
                        # if statement.get("condition_filter"):
                        self.result_access.add_filter_config(
                            {"effect": statement.get("effect"),
                             "condition": statement.get("condition_filter", [])})
                        continue
                    else:
                        # kiểm tra thông tin field dữ liệu gửi lên với cấu hình field trong policy,
                        # nếu field gửi lên ko nằm trong tập con của cấu hình field thì reject statement
                        if statement.get("check_field") and statement.get("fields"):
                            list_field_data_after = []
                            if self.access_level == PolicyDecisionPoint.AccessLevel.ADD:
                                for k, v in self.data_after.items():
                                    if Utils.check_value_valid_check_action_add(v):
                                        list_field_data_after.append(k)
                            else:
                                list_field_data_after = list(self.data_after.keys())
                            if not set(list_field_data_after).issubset(statement.get("fields")):
                                policy_fail.append({
                                    "policy_name": statement.get("policy_name", ""),
                                    "condition": [],
                                    "fields_deny": list(set(list_field_data_after) - set(statement.get("fields")))
                                })
                                result_allow = False
                                continue
                        break
                else:
                    policy_fail.append({
                        "policy_name": statement.get("policy_name", ""),
                        "condition": statement.get("condition", []),
                    })
            except Exception as err:
                msg_err = "abac_sdk check_list_statement_is_allow err: {}".format(err)
                print(msg_err)
                self.result_access.add_log_error(
                    msg_err + " - policy_name: {}".format(statement.get("policy_name", "")))
                # result_allow = False
        if not result_allow:
            self.result_access.add_data_deny({
                "data_after": self.data_after,
                "data_before": self.data_before,
                "policy": policy_fail,
                "effect": AccessType.ALLOW_ACCESS
            })
        return result_allow

    def check_info_action(self):
        action_info = CallAPI.admin_get_json_action(merchant_id=self.merchant_id)
        key_check = self.resource + ":" + self.action
        if not action_info:
            raise ValueError("action for merchant_id {} not found".format(self.merchant_id))
        if not action_info.get(key_check):
            raise ValueError("action {} not found".format(key_check))
        self.access_level = action_info.get(key_check, {}).get("access_level", "").lower()
        if not self.access_level:
            raise ValueError("access_level {} not valid".format(key_check))
        self.service = action_info.get(key_check, {}).get("service", "")
        if not self.service:
            raise ValueError("service {} not valid".format(self.service))

    def is_allowed_list(self, data: list):
        """
            Check if authorization request is allowed data
        """
        # time_run = Timer()
        # time_run.start()
        try:
            if self.pass_policy:
                self.result_access.set_allow_access(True)
                self.result_access.data_allow = data
                return self.result_access
            list_statement = self.get_policy_statement_for_target()
            if list_statement:
                statement_check_allow, statement_check_deny = self.get_statement_by_type(
                    list_statement, check_list=True)
                if (self.resource in ["profile_product_holding", "company_product_holding"]
                        and self.action in ["List"]):
                    self.check_data_from_product_holding(
                        data, statement_check_deny, statement_check_allow, check_list=True)
                else:
                    for item_data in data:
                        self.data_after = item_data.get("data_after", {})
                        self.data_before = item_data.get("data_before", {})
                        self.request_access.update({
                            self.resource: self.data_before if self.data_before else {}
                        })
                        if self.access_level == PolicyDecisionPoint.AccessLevel.ADD:
                            self.data_after.update(self.data_before)
                        if statement_check_deny:
                            if self.check_list_statement_is_deny(statement_check_deny, check_list=True):
                                continue
                        if statement_check_allow:
                            if self.check_list_statement_is_allow(statement_check_allow, check_list=True):
                                self.result_access.add_data_allow(item_data)
                        else:
                            self.result_access.add_data_deny({
                                "data_after": self.data_after,
                                "data_before": self.data_before,
                                "policy": [],
                                "effect": AccessType.ALLOW_ACCESS
                            })
                # bo sung key cho resource product holding
                # if self.resource in ["profile_product_holding", "company_product_holding"]:
                #     field_key = "system_product_line_status"
                #     self.result_access.data_extra.update({
                #         field_key: {
                #             "deny": self.get_all_value_field_in_statement(statement_check_deny, field_key),
                #             "allow": self.get_all_value_field_in_statement(statement_check_allow, field_key),
                #         }
                #     })
                if data:
                    if self.result_access.get_data_allow():
                        self.result_access.set_allow_access(True)
                    else:
                        self.result_access.set_allow_access(False)
                else:
                    if statement_check_deny:
                        if self.check_list_statement_is_deny(statement_check_deny, check_list=True):
                            self.result_access.set_allow_access(False)
                            return self.result_access
                    if statement_check_allow:
                        if self.check_list_statement_is_allow(statement_check_allow, check_list=True):
                            self.result_access.set_allow_access(True)
            else:
                self.result_access.set_allow_access(False)
        except Exception as err:
            msg_err = "abac_sdk is_allowed_list err: {}".format(err)
            print(msg_err)
            self.result_access.add_log_error(msg_err)
            self.result_access.set_allow_access(False)
        # time_run.stop()
        return self.result_access

    @classmethod
    def get_all_value_field_in_statement(cls, statement_list, field_key):
        values = []
        for statement_allow in statement_list:
            if isinstance(statement_allow.get("condition"), list):
                for condition in statement_allow.get("condition"):
                    resource_name, resource_key = Utils.split_delemiter_resource(condition.get("field"))
                    if field_key == resource_key and isinstance(condition.get("values"), list):
                        values.extend(condition.get("values"))
        return list(set(values))

    def check_data_from_product_holding(self, data, statement_check_deny, statement_check_allow, check_list=True):
        id_exclude = []
        list_result_check = []
        for item_data in data:
            self.data_before = item_data.get("data_before", {})
            self.request_access.update({
                self.resource: self.data_before if self.data_before else {}
            })
            product_line_id = self.data_before.get("product_line")
            if product_line_id and product_line_id in id_exclude:
                continue
            if statement_check_deny:
                if self.check_list_statement_is_deny(statement_check_deny, check_list=check_list):
                    id_exclude.append(product_line_id)
                    continue
            list_result_check.append(item_data)
        for item_data in list_result_check:
            self.data_before = item_data.get("data_before", {})
            self.request_access.update({
                self.resource: self.data_before if self.data_before else {}
            })
            product_line_id = self.data_before.get("product_line")
            if product_line_id and product_line_id in id_exclude:
                continue
            if statement_check_allow and self.check_list_statement_is_allow(
                    statement_check_allow, check_list=check_list):
                self.result_access.add_data_allow(item_data)

    def get_resource_field_need_check(self):
        """
        lay thong tin cac resource va field key can truyen vao data before
        :return:
        """
        data_return = {}
        list_statement = self.get_policy_statement_for_target()
        if list_statement:
            for statement in list_statement:
                for cond_check in statement.get("condition"):
                    resource_name, resource_key = Utils.split_delemiter_resource(cond_check.get("field"))
                    # if resource_name in ["user", "env"]:
                    #     continue
                    if cond_check.get("sub_resource"):
                        resource_name = cond_check.get("sub_resource")
                    if resource_name in data_return:
                        data_return.get(resource_name).append(resource_key)
                    else:
                        data_return[resource_name] = [resource_key]
        return data_return
