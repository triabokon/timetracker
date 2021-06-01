import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from tracker.celery import app


def my_monitor(celery_app):
    state = celery_app.events.State()

    def handle_event(event):
        state.event(event)

        task = state.tasks.get(event['uuid'])

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "celery_events",
            {
                "type": "task_message",
                'message': json.dumps(
                    {
                        'id': task.uuid,
                        'args': task.kwargs,
                        'result': task.result,
                        'state': task.state,
                        'time': datetime.utcfromtimestamp(
                            task.timestamp
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                    }
                ),
            },
        )

    with celery_app.connection() as connection:
        recv = celery_app.events.Receiver(
            connection,
            handlers={
                'task-failed': handle_event,
                'task-succeeded': handle_event,
            },
        )
        recv.capture(limit=None, timeout=None, wakeup=True)


my_monitor(app)
