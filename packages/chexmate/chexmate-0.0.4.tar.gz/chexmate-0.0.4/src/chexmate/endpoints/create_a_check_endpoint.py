import re
from typing import Literal, Optional

from chexmate.endpoints.base_endpoint import BaseEndpoint
from chexmate.endpoints.request_parameters.parameter_requirement import ParameterRequirement
from chexmate.endpoints.request_parameters.request_parameter import RequestParameter
from chexmate.endpoints.request_parameters.parameter_restriction import ParameterRestriction
from chexmate.endpoints.request_parameters.request_parameter_list import RequestParameterList
from chexmate.enums.content_type_enum import ContentType
from chexmate.enums.http_method_enum import HTTPMethod


class CreateACheckEndpoint(BaseEndpoint):

    def __init__(self, base_url: str, api_key):
        url_tail = '/v1/check/create'
        method = HTTPMethod.POST
        content_type = ContentType.APPLICATION_JSON
        super().__init__(base_url, url_tail, api_key, method, content_type)

    def create_request_header_list(self):
        header_parameters = RequestParameterList(
            RequestParameter(
                param_name='Authorization',
                param_types=str,
                param_value=self.api_key,
                restrictions=[],
                description='Authorization header containing your API key.',
                required=True
            ),
            RequestParameter(
                param_name='Content-Type',
                param_types=str,
                param_value=self.content_type.value,
                restrictions=[],
                description='It tells the server what type of data is actually sent.',
                required=False
            )
        )
        return header_parameters

    def create_request_body_list(
            self,
            *,
            number: Optional[str] = None,
            amount: float,
            memo: str,
            name: str,
            email: str = None,
            authorization_date: Optional[str] = None,
            label: Optional[str] = None,
            phone: Optional[str] = None,
            sender_address: Optional[str] = None,
            sender_city: Optional[str] = None,
            sender_state: Optional[str] = None,
            sender_zip: Optional[str] = None,
            bank_account: Optional[str] = None,
            bank_routing: Optional[str] = None,
            token: Optional[str] = None,
            store: Optional[str] = None,
            type_info: Optional[str] = None,
            recurring: Optional[Literal[0, 1]] = None,
            recurring_cycle: Optional[str] = None,
            recurring_start_date: Optional[str] = None,
            recurring_installments: Optional[int] = None,
            verify_before_save: Optional[bool] = True,
            fund_confirmation: Optional[bool] = None
    ):
        if bank_account is bank_routing is token is store is None:
            raise ValueError('You must set either bank_account and bank_routing parameters OR token and store parameters.')

        body_parameters = RequestParameterList(
            RequestParameter(
                param_name='number',
                param_types=str,
                param_value=number,
                restrictions=[
                    ParameterRestriction(lambda x: x.isdigit()),
                    ParameterRestriction(lambda x: all([1 <= int(str_num) <= 9 for str_num in x]))
                ],
                description='''The custom number of a check. If this field has not been sent, the check number will be 
                filled in automatically.''',
                required=False
            ),
            RequestParameter(
                param_name='amount',
                param_types=(int, float),
                param_value=amount,
                restrictions=[
                    ParameterRestriction(lambda x: x > 0)
                ],
                description='The amount of the check. The check amount has to be positive.',
                required=True
            ),
            RequestParameter(
                param_name='memo',
                param_types=str,
                param_value=memo,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 128)
                ],
                description='Brief description of the purpose of the check.',
                required=True
            ),
            RequestParameter(
                param_name='name',
                param_types=str,
                param_value=name,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 80)
                ],
                description='The sender’s name.',
                required=True
            ),
            RequestParameter(
                param_name='email',
                param_types=str,
                param_value=email,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 80)
                ],
                description='''The sender’s email address. (The ‘email’ field is a required field, unless ‘address’ 
                field is entered. In this case ‘email’ field can remain empty.)''',
                required=ParameterRequirement(lambda x: True if sender_address is None else False)
            ),
            RequestParameter(
                param_name='authorization_date',
                param_types=str,
                param_value=authorization_date,
                restrictions=[
                    ParameterRestriction(lambda x: re.match(r'^\d\d\d\d-\d\d-\d\d$', x) is not None)
                ],
                description='''The specified date will be displayed on the check. By default, the date of eCheck 
                creation will be presented. The authorization date can not be older than 30 days. The authorization date 
                can not be future dated.''',
                required=False
            ),
            RequestParameter(
                param_name='label',
                param_types=str,
                param_value=label,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 128)
                ],
                description='The label is useful to find similar eChecks.',
                required=False
            ),
            RequestParameter(
                param_name='phone',
                param_types=str,
                param_value=phone,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 20)
                ],
                description='The sender’s phone number.',
                required=False
            ),
            RequestParameter(
                param_name='address',
                param_types=str,
                param_value=sender_address,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 128)
                ],
                description='''The sender’s address. (The ‘address’ field is a required field, unless ‘email’ field is 
                entered. In this case ‘address’ field can remain empty. Please note: if the ‘address’ field is entered, 
                then ‘city’, ‘state’ and ‘zip’ fields must be entered too.)''',
                required=ParameterRequirement(lambda x: True if email is None else False)
            ),
            RequestParameter(
                param_name='city',
                param_types=str,
                param_value=sender_city,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 40)
                ],
                description='The sender’s city.',
                required=ParameterRequirement(lambda x: True if sender_address is not None else False)
            ),
            RequestParameter(
                param_name='state',
                param_types=str,
                param_value=sender_state,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) == 2)
                ],
                description='The sender’s state.',
                required=ParameterRequirement(lambda x: True if sender_address is not None else False)
            ),
            RequestParameter(
                param_name='zip',
                param_types=str,
                param_value=sender_zip,
                restrictions=[
                    ParameterRestriction(lambda x: 5 <= len(x) <= 10)
                ],
                description='The sender’s postal code.',
                required=ParameterRequirement(lambda x: True if sender_address is not None else False)
            ),
            RequestParameter(
                param_name='bank_account',
                param_types=str,
                param_value=bank_account,
                restrictions=[
                    ParameterRestriction(lambda x: token is store is None),
                    ParameterRestriction(lambda x: 4 <= len(x) <= 17)
                ],
                description='''The sender’s bank account. (The ‘bank_routing’ and ‘bank_account’ fields must be both 
                entered. In this case, both fields ‘token’ and ‘store’ must not be entered.)''',
                required=ParameterRequirement(lambda x: True if bank_routing is not None else False)
            ),
            RequestParameter(
                param_name='bank_routing',
                param_types=str,
                param_value=bank_routing,
                restrictions=[
                    ParameterRestriction(lambda x: token is store is None),
                    ParameterRestriction(lambda x: len(x) == 9)
                ],
                description='''The sender’s bank routing number. (The ‘bank_routing’ and ‘bank_account’ fields must be 
                both entered. In this case, both fields ‘token’ and ‘store’ must not be entered.)''',
                required=ParameterRequirement(lambda x: True if bank_routing is not None else False)
            ),
            RequestParameter(
                param_name='token',
                param_types=str,
                param_value=token,
                restrictions=[
                    ParameterRestriction(lambda x: bank_account is bank_routing is None),
                    ParameterRestriction(lambda x: len(x) == 36)
                ],
                description='''Unique encrypted identifier of client’s account details. (The ‘token’ and ‘store’ fields 
                must be both entered. In this case, both fields ‘bank_routing’ and ‘bank_account’ must not be entered.)''',
                required=ParameterRequirement(lambda x: True if store is not None else False)
            ),
            RequestParameter(
                param_name='store',
                param_types=str,
                param_value=store,
                restrictions=[
                    ParameterRestriction(lambda x: bank_account is bank_routing is None),
                ],
                description='''The store from which the requests are received. (The ‘token’ and ‘store’ fields must be 
                both entered. In this case, both fields ‘bank_routing’ and ‘bank_account’ must not be entered.) NOTE: 
                format: site.com. Just make sure to adhere to this format. Regex for this would be a pain in the ass.''',
                required=ParameterRequirement(lambda x: True if token is not None else False)
            ),
            RequestParameter(
                param_name='type_info',
                param_types=str,
                param_value=type_info,
                restrictions=[
                    ParameterRestriction(lambda x: len(x) <= 128),
                ],
                description='Optional. Enter the name of your service to identify your integration',
                required=False
            ),
            RequestParameter(
                param_name='recurring',
                param_types=int,
                param_value=recurring,
                restrictions=[
                    ParameterRestriction(lambda x: 0 <= x <= 1),
                ],
                description='''Select to enable recurring payments.
                    “0” - the fields will not be checked and validated.
                    “1” - the fields will be checked, accepted and validated.''',
                required=False
            ),
            RequestParameter(
                param_name='recurring_cycle',
                param_types=str,
                param_value=recurring_cycle,
                restrictions=[
                    ParameterRestriction(lambda x: x in ('day', 'week', 'bi-weekly', 'month')),
                ],
                description='''The recurring payment will occur with a selected frequency. The options available for 
                recurring payments are daily, weekly, bi-weekly or monthly.''',
                required=False
            ),
            RequestParameter(
                param_name='recurring_start_date',
                param_types=str,
                param_value=recurring_start_date,
                restrictions=[
                    ParameterRestriction(lambda x:  x == 'NULL' or re.search(r'^\d\d\d\d-\d\d-\d\d$', x) is not None),
                ],
                description='''The recurring payments will start on the day of its creation, if selected NULL. 
                If a start date is entered, the recurring payment will start on the start date selected.''',
                required=False
            ),
            RequestParameter(
                param_name='recurring_installments',
                param_types=int,
                param_value=recurring_installments,
                restrictions=[
                    ParameterRestriction(lambda x: x >= 0),
                ],
                description='''Submit if you require the recurring payments to occur a specific number of times or to be indefinite.
                    “0” - indefinite (ongoing until cancelled).
                    “1, 2, 3...N” - quantity of recurring installments.''',
                required=False
            ),
            RequestParameter(
                param_name='verify_before_save',
                param_types=bool,
                param_value=verify_before_save,
                restrictions=[],
                description='''Submit it if you need to verify bank account information. Response will come with a 
                verification result.''',
                required=False
            ),
            RequestParameter(
                param_name='fund_confirmation',
                param_types=bool,
                param_value=fund_confirmation,
                restrictions=[],
                description='''Submit it if you need to confirm the availability of funds. Response will come with a 
                confirmation result. NOTE! This requires an additional plan. Please refer to developers.seamlesschex.com
                for more information.''',
                required=False
            ),
        )
        return body_parameters
