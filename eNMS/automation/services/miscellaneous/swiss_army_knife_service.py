from flask_mail import Message
from sqlalchemy import Boolean, Column, ForeignKey, Integer

from eNMS import mail
from eNMS.automation.models import Service
from eNMS.base.models import service_classes


class SwissArmyKnifeService(Service):

    __tablename__ = 'SwissArmyKnifeService'

    id = Column(Integer, ForeignKey('Service.id'), primary_key=True)
    multiprocessing = Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'swiss_army_knife_service',
    }

    def job(self, *args):
        return getattr(self, self.name)(*args)

    # Instance call "job1" with multiprocessing set to True
    def job1(self, device, payload):
        return {'success': True, 'result': ''}

    # Instance call "job2" with multiprocessing set to False
    def job2(self, payload):
        return {'success': True, 'result': ''}

    def Start(self, *a, **kw):  # noqa: N802
        # Start of a workflow
        return {'success': True}

    def End(self, *a, **kw):  # noqa: N802
        # End of a workflow
        return {'success': True}

    def mail_feedback_notification(self, payload):
        message = Message(
            payload['job'].name,
            sender='notification@enms.fr',
            recipients=self.recipients.split(','),
            body=payload['result']
        )
        mail.send(message)

    def slack_feedback_notification(self, payload):
        # send a notification on Slack
        pass

    def mattermost_feedback_notification(self, payload):
        # send a notification on Mattermost
        pass

    def process_payload1(self, device, payload):
        get_facts = payload['get_facts']
        # we use the name of the device to get the result for that particular
        # device.
        # all of the other inventory properties of the device are available
        # to use, including custom properties.
        results = get_facts['result']['devices'][device.name]['result']
        uptime_less_than_50000 = results['get_facts']['uptime'] < 50000
        return {
            'success': True,
            'result': {
                'uptime_less_5000': uptime_less_than_50000
            }
        }


service_classes['swiss_army_knife_service'] = SwissArmyKnifeService
