from django import forms
from django.contrib.auth.models import Group

from users.models import CustomUser

from .tasks import send_emails_task

groups = Group.objects.all()

GROUP_CHOICES = [(g.name, g.name) for g in groups]


class FeedbackForm(forms.Form):
    users_group = forms.CharField(
        label='Users group', widget=forms.Select(choices=GROUP_CHOICES)
    )
    subject = forms.CharField(
        label="Subject", widget=forms.Textarea(attrs={'rows': 1})
    )
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={'rows': 5})
    )
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def send_email(self):
        # try to trick spammers by checking whether the honeypot field is
        # filled in; not super complicated/effective but it works
        if self.cleaned_data['honeypot']:
            return False

        users = CustomUser.objects.filter(
            groups__name=self.cleaned_data['users_group']
        )
        emails = [u.email for u in users]
        send_emails_task.delay(
            emails, self.cleaned_data['subject'], self.cleaned_data['message']
        )
