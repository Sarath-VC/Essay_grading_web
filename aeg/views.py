from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, 'Index.html');
def uploadfile(request):
    if request.method == 'POST':
        uploaded_file= request.FILES['upld']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    return render(request, 'UploadFile.html')
def essay_list(request):
    return render(request, 'essaylist.html')