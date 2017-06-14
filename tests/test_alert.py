"""Unit tests the alert methods of the Matchlight SDK."""
import datetime
import json
import uuid

import httpretty
import pytest

import matchlight


@pytest.mark.httpretty
def test_alert_get(connection, alert, alert_payload):
    """Verifies alert get responses."""
    httpretty.register_uri(
        httpretty.GET, '{}/alert/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id
        ),
        responses=[
            httpretty.Response(
                body=json.dumps(alert_payload),
                content_type='application/json',
                status=200
            ),
            httpretty.Response(
                body='{}',
                content_type='application/json',
                status=404
            ),
            httpretty.Response(
                body='{}',
                content_type='application/json',
                status=500
            ),
        ]
    )
    alert_ = connection.alerts.get(alert.id)
    assert alert.id == alert_.id

    alert_ = connection.alerts.get(alert.id)
    assert alert_ is None

    with pytest.raises(matchlight.error.ConnectionError):
        connection.alerts.get(alert.id)


@pytest.mark.httpretty
def test_alert_dates(connection, alert, alert_payload):
    """Verifies alert date objects are converted correctly."""
    httpretty.register_uri(
        httpretty.GET, '{}/alert/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id
        ),
        body=json.dumps(alert_payload),
        content_type='application/json',
        status=200
    )
    alert_ = connection.alerts.get(alert.id)
    assert isinstance(alert_.date, datetime.datetime)
    assert isinstance(alert_.last_modified, datetime.datetime)


@pytest.mark.httpretty
def test_alert_filter(connection, alert, alert_payload):
    """Verifies alert listing and filtering."""
    httpretty.register_uri(
        httpretty.GET, '{}/alerts'.format(matchlight.MATCHLIGHT_API_URL_V2),
        body=json.dumps({'data': [alert_payload]}),
        content_type='application/json',
        status=200
    )
    alerts = connection.alerts.filter()
    assert len(alerts) == 1
    assert alerts[0].id == alert.id


@pytest.mark.httpretty
def test_alert_filter_seen(connection, alert, alert_payload):
    """Verifies alert filtering on 'seen'."""
    # Create opposite alert
    unseen_payload = alert_payload.copy()
    unseen_payload['seen'] = 'false'
    unseen_payload['id'] = str(uuid.uuid4())

    # Get seen alerts
    httpretty.register_uri(
        httpretty.GET, '{}/alerts?seen=1'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        body=json.dumps({'data': [alert_payload]}),
        content_type='application/json',
        status=200
    )

    alerts = connection.alerts.filter(seen=True)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']

    # Get unseen alerts
    httpretty.register_uri(
        httpretty.GET, '{}/alerts?seen=0'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        body=json.dumps({'data': [unseen_payload]}),
        content_type='application/json',
        status=200
    )

    alerts = connection.alerts.filter(seen=False)
    assert len(alerts) == 1
    assert alerts[0].id == unseen_payload['id']


@pytest.mark.httpretty
def test_alert_filter_archived(connection, alert, alert_payload):
    """Verifies alert filtering on 'archived'."""
    # Create opposite alert
    unarchived_payload = alert_payload.copy()
    unarchived_payload['archived'] = 'false'
    unarchived_payload['id'] = str(uuid.uuid4())

    # Get archived alerts
    httpretty.register_uri(
        httpretty.GET, '{}/alerts?archived=1'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        body=json.dumps({'data': [alert_payload]}),
        content_type='application/json',
        status=200
    )

    alerts = connection.alerts.filter(archived=True)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']

    # Get unarchived alerts
    httpretty.register_uri(
        httpretty.GET, '{}/alerts?archived=0'.format(
            matchlight.MATCHLIGHT_API_URL_V2
        ),
        body=json.dumps({'data': [unarchived_payload]}),
        content_type='application/json',
        status=200
    )

    alerts = connection.alerts.filter(archived=False)
    assert len(alerts) == 1
    assert alerts[0].id == unarchived_payload['id']


@pytest.mark.httpretty
def test_alert_filter_project(connection, alert, alert_payload, project):
    """Verifies alert filtering on 'upload_token'."""
    httpretty.register_uri(
        httpretty.GET, '{}/alerts?upload_token={}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            project.upload_token
        ),
        body=json.dumps({'data': [alert_payload]}),
        content_type='application/json',
        status=200
    )

    alerts = connection.alerts.filter(project=project)
    assert len(alerts) == 1
    assert alerts[0].id == alert_payload['id']


@pytest.mark.httpretty
def test_alert_all(connection, alert, alert_payload):
    """Verifies alert listing and filtering."""
    httpretty.register_uri(
        httpretty.GET, '{}/alerts'.format(matchlight.MATCHLIGHT_API_URL_V2),
        body=json.dumps({'data': [alert_payload]}),
        content_type='application/json',
        status=200
    )
    alerts = connection.alerts.all()
    assert len(alerts) == 1
    assert alerts[0].id == alert.id


@pytest.mark.httpretty
def test_alert_iteration(connection, alert, alert_payload):
    """Verifies alert iteration."""
    httpretty.register_uri(
        httpretty.GET, '{}/alerts'.format(matchlight.MATCHLIGHT_API_URL_V2),
        body=json.dumps({'data': [alert_payload]}),
        content_type='application/json',
        status=200,
    )
    alerts_iterable = iter(connection.alerts)
    assert next(alerts_iterable).id == alert.id
    with pytest.raises(StopIteration):
        next(alerts_iterable)


@pytest.mark.httpretty
def test_alert_edit(connection, alert, alert_payload):
    """Verifies alert editing."""
    # Do nothing
    httpretty.register_uri(
        httpretty.POST, '{}/alert/{}/edit'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id,
        ),
        body=json.dumps({
            'archived': 'true',
            'seen': 'true'
        }),
        status=200
    )
    alert = connection.alerts.edit(alert)
    assert alert.seen is True
    assert alert.archived is True

    # Un-archive
    httpretty.register_uri(
        httpretty.POST, '{}/alert/{}/edit'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id,
        ),
        body=json.dumps({
            'archived': 'false',
            'seen': 'true'
        }),
        status=200
    )
    alert = connection.alerts.edit(alert, archived=False)
    assert alert.seen is True
    assert alert.archived is False

    # Un-see
    httpretty.register_uri(
        httpretty.POST, '{}/alert/{}/edit'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id,
        ),
        body=json.dumps({
            'archived': 'false',
            'seen': 'false'
        }),
        status=200
    )
    alert = connection.alerts.edit(alert, seen=False)
    assert alert.seen is False
    assert alert.archived is False

    # Both
    httpretty.register_uri(
        httpretty.POST, '{}/alert/{}/edit'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id,
        ),
        body=json.dumps({
            'archived': 'true',
            'seen': 'true'
        }),
        status=200
    )
    alert = connection.alerts.edit(alert, seen=True, archived=True)
    assert alert.seen is True
    assert alert.archived is True


@pytest.mark.httpretty
def test_alert_id_edit(connection, alert, alert_payload):
    """Verifies alert editing."""
    httpretty.register_uri(
        httpretty.GET, '{}/alert/{}'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id
        ),
        body=json.dumps(alert_payload),
        content_type='application/json',
        status=200
    )
    httpretty.register_uri(
        httpretty.POST, '{}/alert/{}/edit'.format(
            matchlight.MATCHLIGHT_API_URL_V2,
            alert.id,
        ),
        body=json.dumps({
            'archived': 'false',
            'seen': 'true'
        }),
        status=200
    )
    alert = connection.alerts.edit(alert.id, archived=False)
    assert alert.seen is True
    assert alert.archived is False
