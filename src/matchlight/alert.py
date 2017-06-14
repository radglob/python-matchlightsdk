"""An interface for creating and retrieving alerts in Matchlight."""
from __future__ import absolute_import

import datetime
import json

import matchlight.error


__all__ = (
    'Alert',
    'AlertMethods',
)


class Alert(object):
    """Represents an alert."""

    def __init__(self, id, number, url, url_metadata, ctime, mtime, seen,
                 archived):
        """Initializes a new alert.

        Args:
            id (:obj:`str`): A 128-bit UUID.
            number (:obj:`int`): The account specific alert number.
            url (:obj:`str`): The url where the match was found.
            score (:obj:`int`): The matchlight score (1-800).
            ctime (:obj:`int`, optional): A Unix timestamp of the
                alert creation timestamp.
            mtime (:obj:`int`, optional): A Unix timestamp of the
                alert last modification date timestamp.
            seen (:obj:`bool`): User specific flag.
            archived (:obj:`bool`): User specific flag.

        """
        self.id = id
        self.number = number
        self.url = url
        self.url_metadata = url_metadata
        self.ctime = ctime
        self.mtime = mtime
        self.seen = seen
        self.archived = archived

    @classmethod
    def from_mapping(cls, mapping):
        """Creates a new alert instance from the given mapping."""
        return cls(
            id=mapping['id'],
            number=mapping['alert_number'],
            url=mapping['url'],
            url_metadata=mapping['url_metadata'],
            ctime=mapping['ctime'],
            mtime=mapping['mtime'],
            seen=True if mapping['seen'] == 'true' else False,
            archived=True if mapping['archived'] == 'true' else False,
        )

    @property
    def last_modified(self):
        """:class:`datetime.datetime`: The last modified timestamp."""
        return datetime.datetime.fromtimestamp(self.mtime)

    @property
    def date(self):
        """:class:`datetime.datetime`: The date created timestamp."""
        return datetime.datetime.fromtimestamp(self.ctime)

    def __repr__(self):  # pragma: no cover
        return '<Alert(number="{}", id="{}")>'.format(
            self.number,
            self.id
        )


class AlertMethods(object):
    """Provides methods for interfacing with the alerts API.

    Examples:

        Get alert by alert id::

            >>> alert = ml.alerts.get("0760570a2c4a4ea68d526f58bab46cbd")
            >>> alert
            <Alert(number=1024,
            id="0760570a2c4a4ea68d526f58bab46cbd")>

        Archive an alert::

            >>> alert
            <Alert(number=1024,
            id="0760570a2c4a4ea68d526f58bab46cbd")>
            >>> ml.alert.edit(alert, archived=True)

    """

    def __init__(self, ml_connection):  # noqa: D205,D400
        """Initializes an alerts interface with the given Matchlight
        connection.

        Args:
            ml_connection (:class:`~.Connection`): A Matchlight
                connection instance.

        """
        self.conn = ml_connection

    def all(self):
        """Returns all alerts associated with the account."""
        return self.filter()

    def filter(self, seen=None, archived=None, project=None):
        """Returns a list of alerts.

        Providing an optional **seen** keyword argument will only
        return alerts that match that property

        Providing an optional **archived** keyword argument will only
        return alerts that match that property

        Providing an optional **project** keyword argument will only
        return alerts that are associated with a specific project.

        Example:
            Request all unseen alerts::

                >>> ml.alerts.filter(seen=False)
                [<Alert(number="1024",
                id="625a732ad0f247beab18595z951c2088a3")>,
                Alert(number="1025",
                id="f9427dd5a24d4a98b2069004g04c2977")]

            Request all alerts for a project::

                >>> my_project
                <Project(name="Super Secret Algorithm", type="source_code")>
                >>> ml.alerts.filter(project=my_project)
                [<Alert(number="1024",
                id="625a732ad0f247beab18595z951c2088a3")>,
                Alert(number="1025",
                id="f9427dd5a24d4a98b2069004g04c2977")]

        Args:
            seen (:obj:`bool`, optional):
            archived (:obj:`bool`, optional):
            project (:class:`~.Project`, optional): a project object.
                Defaults to all projects if not specified.

        Returns:
            :obj:`list` of :class:`~.Alert`: List of alerts that
                are associated with a project.

        """
        if seen is not None:
            seen_int = 1 if seen is True else 0
        else:
            seen_int = None

        if archived is not None:
            archived_int = 1 if archived is True else 0
        else:
            archived_int = None

        if project is not None:
            upload_token = project.upload_token
        else:
            upload_token = None

        response = self.conn.request(
            '/alerts',
            params={
                'seen': seen_int,
                'archived': archived_int,
                'upload_token_filter': upload_token
            }
        )
        alerts = []
        for payload in response.json().get('data', []):
            alerts.append(Alert.from_mapping(payload))
        return alerts

    def get(self, alert_id):
        """Returns an alert by the given alert ID.

        Args:
            alert_id (:obj:`str`): The alert identifier.

        Returns:
           :class:`~.Alert`: A alert instance.

        """
        try:
            response = self.conn.request('/alert/{}'.format(alert_id))
            return Alert.from_mapping(response.json())
        # for consistency since records.get() returns None if not found.
        except matchlight.error.APIError as err:
            if err.args[0] == 404:
                return
            else:
                raise

    def edit(self, alert, seen=None, archived=None):
        """Edits an alert.

        Arguments:
            alert (:class:`~.Alert` or :obj:`str`): An alert instance or id.
            seen (:obj:`bool`, optional):
            archived (:obj:`bool`, optional):

        Returns:
            :class:`~.Alert`: Updated alert instance.

            Note that this method mutates any alert instances passed.

        """
        if not isinstance(alert, Alert):
            alert = self.get(alert)

        data = {}
        if seen is not None:
            data['seen'] = 1 if seen is True else 0

        if archived is not None:
            data['archived'] = 1 if archived is True else 0

        response = self.conn.request(
            '/alert/{}/edit'.format(alert.id),
            data=json.dumps(data)
        )
        response = response.json()

        alert.seen = True if response['seen'] == 'true' else False
        alert.archived = True if response['archived'] == 'true' else False
        return alert

    def __iter__(self):
        return iter(self.filter())
