from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from PIL import Image, ImageFile
from sys import exit, stderr
from os.path import getsize, isfile, isdir, join
from os import remove, rename, walk, stat
from stat import S_IWRITE
from shutil import move
from argparse import ArgumentParser
from abc import ABCMeta, abstractmethod
import os

def home(request):
    return render(request, 'core/home.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        img = Image.open(myfile)
        filename = myfile.name
        backupname = filename + '.' + 'compressimages-backup'
 
        if isfile(backupname):
            print 'Ignoring file "' + filename + '" for which existing backup file is present.'
            return False
 
            rename(filename, backupname)

        ImageFile.MAXBLOCK = img.size[0] * img.size[1]
        pathname = os.path.join( os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/') + myfile.name
        img.save(pathname, quality=50, optimize=True)
        # filename = fs.save(myfile.name, myfile)
        uploaded_file_url = '/media/' + myfile.name
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')

def delete_image(request):
    documents = Document.objects.all()
    pathname = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/') 
    all_images = os.listdir(pathname)
    if request.method == 'POST':
       file_requested_delete = request.POST.getlist('services')[0]
       
       os.remove(pathname+ file_requested_delete)
       return render(request, 'core/delete_file.html', { 'message': 'Requested Image Successfully Deleted', 'all_images': all_images })
    elif request.method == 'GET':
        pathname = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media/')        
        return render(request, 'core/delete_file.html', { 'all_images': all_images })