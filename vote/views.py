import os
from glob import glob
import random

from urllib3 import request

from app.models import Template
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class ImageList(TemplateView):

    template_name = 'index.html'

    def get(self, request):
        current_user = request.user

        templates = Template.objects.all()

        filename = self.image_not_used(templates, current_user)
        url = 'http://pesquisa.eastus.cloudapp.azure.com:80/media/incar/'+filename
        context = {
            'url': url,
            'filename': filename,
            'total_global_negative': self.total_votes(templates, vote=-1),
            'total_global_positive': self.total_votes(templates, vote=1),
            'total_global_neutral': self.total_votes(templates, vote=0),
            'total_user_negative': self.user_votes(templates, vote=-1, user=current_user),
            'total_user_positive': self.user_votes(templates, vote=1, user=current_user),
            'total_user_neutral': self.user_votes(templates, vote=0, user=current_user),
        }

        return render(request, self.template_name, context)

    def filename(self):
        list_files = glob(
            '/home/vsoft/BPOnlineImageAnnotation/media/incar/*.jpg')
        random_file = random.choice(list_files)
        filename = os.path.basename(random_file)

        if random_file in list_files:
            list_files.remove(random_file)
            return filename

    def image_not_used(self, templates, current_user):
        while True:
            filename = self.filename()
            images = templates.filter(filename=filename)
            single_image_user = images.filter(img_user=current_user).exists()
            if images.count() == 3 or single_image_user:
                continue
            else:
                break
        return filename

    def total_votes(self, templates, vote):
        return templates.filter(vote=vote).count()

    def user_votes(self, templates, vote, user):
        return templates.filter(vote=vote, img_user=user).count()

    def post(self, request):
        vote = request.POST.get('vote')
        filename = request.POST.get('filename')
        img_user = request.user
        new_instance = Template.objects.create(
            vote=vote, img_user=img_user, filename=filename)
        new_instance.save()
        return redirect('/')
