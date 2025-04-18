from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from xhtml2pdf import pisa
from accounting.models import Transaction

# Create your views here.

def report(request):
    return render(request, 'report.html')

def pdf(request):
    # Function to be called on button click
    return render_pdf_view(request)

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)

    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        static_url = settings.STATIC_URL    # Usually /static/
        static_root = settings.STATIC_ROOT  # Usually /home/user/project_static/
        media_url = settings.MEDIA_URL      # Usually /media/
        media_root = settings.MEDIA_ROOT    # Usually /home/user/project_static/media/

        if uri.startswith(media_url):
            path = os.path.join(media_root, uri.replace(media_url, ""))
        elif uri.startswith(static_url):
            path = os.path.join(static_root, uri.replace(static_url, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise RuntimeError(
            f'media URI must start with {static_url} or {media_url}'
        )
    return path

def render_pdf_view(request):
    template_path = 'transactions-export.html'
    transactions = Transaction.objects.all()
    context = {'transactions' : transactions}

    # Create a Django response object, and set content type to PDF
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html,
       dest=response,
       link_callback=link_callback,  # defined above
    )

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
