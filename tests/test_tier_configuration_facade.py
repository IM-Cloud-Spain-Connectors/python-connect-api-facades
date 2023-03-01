import os

import pytest
from connect.client import ClientError
from rndi.connect.business_objects.adapters import Request, TierConfiguration
from rndi.connect.api_facades.facade import ConnectOpenAPIFacade

BAD_REQUEST_400 = '400 Bad Request'
NOT_FOUND = '404 Not Found'
TIER_CONFIG_REQUEST_FILE = '/request_tier_config.json'


def test_tier_configuration_service_should_retrieve_an_tier_configuration_by_id(
        sync_client_factory,
        response_factory,
):
    tier_configuration_id = 'TC-0000-0000-0000'
    tier_configuration = Request()
    tier_configuration.with_id(tier_configuration_id)

    client = sync_client_factory([
        response_factory(value=tier_configuration.raw(), status=200),
    ])

    tier_configuration = ConnectOpenAPIFacade(client).find_tier_configuration(tier_configuration_id)

    assert isinstance(tier_configuration, TierConfiguration)
    assert tier_configuration.id() == tier_configuration_id


def test_tier_configuration_service_should_fail_finding_an_tier_configuration(
        sync_client_factory,
        response_factory,
):
    tier_configuration_id = 'TC-0000-0000-0000'

    exception = ClientError(
        message=NOT_FOUND,
        status_code=404,
        error_code="VAL_001",
        errors=[NOT_FOUND],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).find_tier_configuration(tier_configuration_id)


def test_tier_configuration_service_should_retrieve_an_tier_configuration_request_by_id(
        sync_client_factory,
        response_factory,
):
    tcr_id = 'TCR-0000-0000-0000-001'
    tc_id = 'TC-0000-0000-0000'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    request = ConnectOpenAPIFacade(client).find_tier_configuration_request(tcr_id)

    assert isinstance(request, Request)
    assert request.id() == tcr_id
    assert request.tier_configuration().id() == tc_id


def test_tier_configuration_service_should_approve_an_tier_configuration_request(
        sync_client_factory,
        response_factory,
):
    tcr_id = 'TCR-0000-0000-0000-001'
    tc_id = 'TC-0000-0000-0000'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)
    tier_configuration.with_status('active')

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('approved')
    request.with_tier_configuration(tier_configuration)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    tier_configuration = request.tier_configuration()
    tier_configuration.with_status('processing')

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    connect = ConnectOpenAPIFacade(client)
    request = connect.approve_tier_configuration_request(request, 'TL-000-000-001')

    assert request.id() == tcr_id
    assert request.tier_configuration().id() == tc_id
    assert request.status() == 'approved'


def test_tier_configuration_service_should_fail_approving_an_tier_configuration_request(
        sync_client_factory,
        response_factory,
):
    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="VAL_001",
        errors=[
            "effective_date: Datetime has wrong format. Use one of these formats ",
            "instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].",
        ],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    request = Request()
    request.with_id('TCR-0000-0000-0000-001')
    request.with_tier_configuration(TierConfiguration())

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).approve_tier_configuration_request(request, 'TL-000-000-001')


def test_tier_configuration_service_should_fail_an_tier_configuration_request(
        sync_client_factory,
        response_factory,
):
    reason = 'Get better'
    tc_id = 'TC-0000-0000-0000-001'
    tcr_id = 'TCR-0000-0000-0000-001'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)
    tier_configuration.with_status('processing')

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('failed')
    request.with_tier_configuration(tier_configuration)
    request.with_reason(reason)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    request = Request()
    request.with_id(tcr_id)
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    request = ConnectOpenAPIFacade(client).fail_tier_configuration_request(request, reason)

    assert request.id() == tcr_id
    assert request.status() == 'failed'
    assert request.reason() == reason


def test_tier_configuration_service_should_fail_an_tier_configuration_request_custom_success(
        sync_client_factory,
        response_factory,
):
    reason = 'Get better'
    tc_id = 'TC-0000-0000-0000-001'
    tcr_id = 'TCR-0000-0000-0000-001'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)
    tier_configuration.with_status('processing')

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('failed')
    request.with_tier_configuration(tier_configuration)
    request.with_reason(reason)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    request = Request()
    request.with_id(tcr_id)
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    request = ConnectOpenAPIFacade(client).fail_tier_configuration_request(
        request,
        reason,
        on_success=lambda x: x.with_reason(reason),
    )

    assert request.id() == tcr_id
    assert request.status() == 'failed'
    assert request.reason() == reason


def test_tier_configuration_service_should_fail_failing_an_tier_configuration_request(
        sync_client_factory,
        response_factory,
):
    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="REQ_005",
        errors=["Missed fields: reason."],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_tier_configuration(TierConfiguration())

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).fail_tier_configuration_request(request, 'irrelevant')


def test_tier_configuration_service_fail_failing_an_tier_configuration_request_with_custom_error(
        sync_client_factory,
        response_factory,
):
    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="REQ_005",
        errors=["Missed fields: reason."],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_tier_configuration(TierConfiguration())

    def __on_error(e):
        raise e

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).fail_tier_configuration_request(request, 'irrelevant',
                                                                     on_error=__on_error)


def test_tier_configuration_service_should_fail_updating_a_request_tier_configuration_params(
        sync_client_factory,
        response_factory,
        load_json,
):
    initial_request = Request(load_json(os.path.dirname(__file__) + TIER_CONFIG_REQUEST_FILE))
    tier_configuration = initial_request.tier_configuration()
    tier_configuration.with_param('CAT_SUBSCRIPTION_ID', 'AS-8790-0160-2196')
    initial_request.with_tier_configuration(tier_configuration)

    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="REQ_005",
        errors=["Missed fields: reason."],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).update_tier_configuration_request_parameters(
            initial_request,
            [{
                'id': 'CAT_SUBSCRIPTION_ID',
                'value': 'AS-0000-0000-0001',
            }],
        )


def test_tier_configuration_service_should_update_a_request_tier_configuration_params(
        sync_client_factory,
        response_factory,
        load_json,
):
    initial_request = Request(load_json(os.path.dirname(__file__) + TIER_CONFIG_REQUEST_FILE))
    tier_configuration = initial_request.tier_configuration()
    tier_configuration.with_param('CAT_SUBSCRIPTION_ID', 'AS-8790-0160-2196')
    initial_request.with_tier_configuration(tier_configuration)

    updated_request = Request(load_json(os.path.dirname(__file__) + TIER_CONFIG_REQUEST_FILE))
    tier_configuration = updated_request.tier_configuration()
    tier_configuration.with_param('CAT_SUBSCRIPTION_ID', 'AS-0000-0000-0001')
    updated_request.with_tier_configuration(tier_configuration)

    client = sync_client_factory([
        response_factory(value=updated_request.raw(), status=200),
    ])

    request = ConnectOpenAPIFacade(client).update_tier_configuration_request_parameters(
        initial_request,
        [{
            'id': 'CAT_SUBSCRIPTION_ID',
            'value': 'AS-0000-0000-0001',
        }],
    )

    assert request.tier_configuration().param('CAT_SUBSCRIPTION_ID', 'value') == 'AS-0000-0000-0001'


def test_tier_configuration_service_should_update_tier_configuration_params_with_custom_success(
        sync_client_factory,
        response_factory,
        load_json,
):
    initial_request = Request(load_json(os.path.dirname(__file__) + TIER_CONFIG_REQUEST_FILE))
    tier_configuration = initial_request.tier_configuration()
    tier_configuration.with_param('CAT_SUBSCRIPTION_ID', 'AS-8790-0160-2196')
    initial_request.with_tier_configuration(tier_configuration)

    updated_request = Request(load_json(os.path.dirname(__file__) + TIER_CONFIG_REQUEST_FILE))
    tier_configuration = updated_request.tier_configuration()
    tier_configuration.with_param('CAT_SUBSCRIPTION_ID', 'AS-0000-0000-0001')
    updated_request.with_tier_configuration(tier_configuration)

    client = sync_client_factory([
        response_factory(value=updated_request.raw(), status=200),
    ])

    request = ConnectOpenAPIFacade(client).update_tier_configuration_request_parameters(
        initial_request,
        [{
            'id': 'CAT_SUBSCRIPTION_ID',
            'value': 'AS-0000-0000-0001',
        }],
        on_success=lambda r: r,
    )

    assert request.tier_configuration().param('CAT_SUBSCRIPTION_ID', 'value') == 'AS-0000-0000-0001'


def test_tier_configuration_service_should_return_custom_error_on_updating_parameters(
        sync_client_factory,
        response_factory,
):
    tcr_id = 'TCR-0000-0000-0000-001'
    tc_id = 'TC-0000-0000-0000'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)
    tier_configuration.with_status('active')
    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="REQ_005",
        errors=["Missed fields: reason."],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    def __on_error(e):
        raise e

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).update_tier_configuration_request_parameters(
            request,
            [{
                'id': 'CAT_SUBSCRIPTION_ID',
                'value': 'AS-0000-0000-0001',
            }],
            on_error=__on_error,
        )


def test_tier_configuration_service_should_inquire_an_tier_configuration_request_custom_success(
        sync_client_factory,
        response_factory,
):
    tcr_id = 'TCR-0000-0000-0000-001'
    tc_id = 'TC-0000-0000-0000'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)
    tier_configuration.with_status('active')

    existing_request = Request()
    existing_request.with_id(tcr_id)
    existing_request.with_type('purchase')
    existing_request.with_status('pending')
    existing_request.with_tier_configuration(tier_configuration)

    client = sync_client_factory([
        response_factory(value=existing_request.raw(), status=200),
    ])

    tier_configuration = existing_request.tier_configuration()
    tier_configuration.with_status('processing')

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    connect = ConnectOpenAPIFacade(client)
    request = connect.inquire_tier_configuration_request(
        request,
        on_success=lambda req: req,
    )

    assert request.id() == tcr_id
    assert request.tier_configuration().id() == tc_id
    assert request.status() == 'inquiring'


def test_tier_configuration_service_should_fail_inquiring_an_tier_configuration_request(
        sync_client_factory,
        response_factory,
):
    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="REQ_003",
        errors=[
            "For marking request to inquiring status at least one parameter should be marked as invalid."],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_tier_configuration(TierConfiguration())

    def __on_error(e):
        raise e

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).inquire_asset_request(
            request,
            'TL-662-440-097',
            on_error=__on_error,
        )


def test_tier_configuration_service_should_inquire_an_tier_configuration_request(
        sync_client_factory,
        response_factory,
):
    tcr_id = 'TCR-0000-0000-0000-001'
    tc_id = 'TC-0000-0000-0000'
    tier_configuration = TierConfiguration()
    tier_configuration.with_id(tc_id)
    tier_configuration.with_status('active')

    existing_request = Request()
    existing_request.with_id(tcr_id)
    existing_request.with_type('purchase')
    existing_request.with_status('pending')
    existing_request.with_tier_configuration(tier_configuration)

    client = sync_client_factory([
        response_factory(value=existing_request.raw(), status=200),
    ])

    tier_configuration = existing_request.tier_configuration()
    tier_configuration.with_status('processing')

    request = Request()
    request.with_id(tcr_id)
    request.with_type('purchase')
    request.with_status('pending')
    request.with_tier_configuration(tier_configuration)

    connect = ConnectOpenAPIFacade(client)
    request = connect.inquire_tier_configuration_request(request)

    assert request.id() == tcr_id
    assert request.tier_configuration().id() == tc_id
    assert request.status() == 'inquiring'
