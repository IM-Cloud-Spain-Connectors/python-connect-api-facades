import os

import pytest
from connect.client import ClientError
from rndi.connect.business_objects.adapters import Asset, Request
from rndi.connect.api_facades.facade import ConnectOpenAPIFacade

BAD_REQUEST_400 = "400 Bad Request"
ASSET_REQUEST_FILE = '/request_asset.json'


def test_asset_helper_should_retrieve_an_asset_by_id(sync_client_factory, response_factory):
    asset = Asset()
    asset.with_id('AS-9091-4850-9712')

    client = sync_client_factory([
        response_factory(value=asset.raw(), status=200),
    ])

    asset = ConnectOpenAPIFacade(client).find_asset('AS-9091-4850-9712')

    assert isinstance(asset, Asset)
    assert asset.id() == 'AS-9091-4850-9712'


def test_asset_helper_should_retrieve_an_asset_request_by_id(sync_client_factory, response_factory):
    asset = Asset()
    asset.with_id('AS-9091-4850-9712')

    request = Request()
    request.with_id('PR-9091-4850-9712-001')
    request.with_type('purchase')
    request.with_status('pending')
    request.with_asset(asset)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    request = ConnectOpenAPIFacade(client).find_asset_request('PR-9091-4850-9712-001')

    assert isinstance(request, Request)
    assert request.id() == 'PR-9091-4850-9712-001'


def test_asset_helper_should_approve_an_asset_request(sync_client_factory, response_factory):
    asset = Asset()
    asset.with_id('AS-8027-7606-7082')
    asset.with_status('active')

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_type('purchase')
    request.with_status('approved')
    request.with_asset(asset)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    asset = request.asset()
    asset.with_status('processing')

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_type('purchase')
    request.with_status('pending')
    request.with_asset(asset)

    request = ConnectOpenAPIFacade(client).approve_asset_request(request, 'TL-662-440-096')

    assert request.id() == 'PR-8027-7606-7082-001'
    assert request.status() == 'approved'


def test_asset_helper_should_fail_approving_an_asset_request(sync_client_factory, response_factory):
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
    request.with_id('PR-8027-7606-7082-001')
    request.with_asset(Asset())

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).approve_asset_request(request, 'TL-662-440-096')


def test_asset_helper_should_fail_an_asset_request(sync_client_factory, response_factory):
    reason = 'I don\'t like you :P'

    asset = Asset()
    asset.with_id('AS-8027-7606-7082')
    asset.with_status('processing')

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_type('purchase')
    request.with_status('failed')
    request.with_asset(asset)
    request.with_reason(reason)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_status('pending')
    request.with_asset(asset)

    request = ConnectOpenAPIFacade(client).fail_asset_request(request, reason)

    assert request.id() == 'PR-8027-7606-7082-001'
    assert request.status() == 'failed'
    assert request.reason() == reason


def test_asset_helper_should_fail_failing_an_asset_request(sync_client_factory, response_factory):
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
    request.with_asset(Asset())

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).fail_asset_request(request, 'This is not going to work')


def test_asset_helper_should_inquire_an_asset_request(sync_client_factory, response_factory):
    asset = Asset()
    asset.with_id('AS-8027-7606-7082')
    asset.with_status('processing')

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_type('purchase')
    request.with_status('inquiring')
    request.with_asset(asset)

    client = sync_client_factory([
        response_factory(value=request.raw(), status=200),
    ])

    request = Request()
    request.with_id('PR-8027-7606-7082-001')
    request.with_type('purchase')
    request.with_status('pending')
    request.with_asset(asset)

    ConnectOpenAPIFacade(client).inquire_asset_request(request, 'TL-662-440-097')

    assert request.id() == 'PR-8027-7606-7082-001'
    assert request.status() == 'inquiring'


def test_asset_helper_should_fail_inquiring_an_asset_request(sync_client_factory, response_factory):
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
    request.with_asset(Asset())

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).inquire_asset_request(request, 'TL-662-440-097')


def test_asset_helper_should_update_a_request_asset_params(
        sync_client_factory,
        response_factory,
        load_json,
):
    after_update = Request(load_json(os.path.dirname(__file__) + ASSET_REQUEST_FILE))
    asset = after_update.asset()
    asset.with_param('CAT_SUBSCRIPTION_ID', 'AS-8790-0160-2196')
    after_update.with_asset(asset)

    client = sync_client_factory([
        response_factory(value=after_update.raw(), status=200),
    ])

    request = Request(load_json(os.path.dirname(__file__) + ASSET_REQUEST_FILE))

    request = ConnectOpenAPIFacade(client).update_asset_request_parameters(request, [{
        'id': 'CAT_SUBSCRIPTION_ID',
        'value': 'AS-8790-0160-2196',
    }])

    assert request.asset().param('CAT_SUBSCRIPTION_ID', 'value') == 'AS-8790-0160-2196'


def test_asset_helper_should_raise_exception_on_updating_request_asset_params(
        sync_client_factory,
        response_factory,
        load_json,
):
    exception = ClientError(
        message=BAD_REQUEST_400,
        status_code=400,
        error_code="REQ_003",
        errors=[
            "Only pending, draft or inquiring Fulfillments ",
            "with enabled validation capability can be updated.",
        ],
    )

    client = sync_client_factory([
        response_factory(exception=exception, status=exception.status_code),
    ])

    request = Request(load_json(os.path.dirname(__file__) + ASSET_REQUEST_FILE))

    with pytest.raises(ClientError):
        ConnectOpenAPIFacade(client).update_asset_request_parameters(request, [{
            'id': 'CAT_SUBSCRIPTION_ID',
            'value': 'AS-8790-0160-2196',
        }])
