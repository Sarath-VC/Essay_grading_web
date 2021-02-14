import os


from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import EssayupForm, TopicForm, BowForm
from .models import Essays, Topics, Bow, Report
from .aegmodel import stopword, tfidf, grammarcheck
from django.core.files import File
from fpdf import FPDF
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
    if request.method == 'POST':
        val1 = int(request.POST['btneval'])
        evaluate(val1)
    essays = Essays.objects.all().order_by('topic')
    reports=Report.objects.all()
    context={'essays': essays,'reports':reports }
    return render(request, 'essaylist.html', context)
def upload_essay(request):
    if request.method == 'POST':
        form = EssayupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('essay_list')
    else:
        form = EssayupForm()
    return render(request, 'uploadessay.html', {'form': form})

def topic_list(request):
    topics = Topics.objects.all().order_by('title')
    return render(request, 'topiclist.html', {'topics': topics})
def generate_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'generatetopic.html', {'form': form})

def bow_list(request):
    bows = Bow.objects.all().order_by('topic')

    return render(request, 'bowlist.html', {'bows': bows})
def generate_bow(request):
    if request.method == 'POST':
        form = BowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generate_bow')
    else:
        form = BowForm()
    return render(request, 'generatebow.html', {'form': form})

def evaluate(ids):
    objessay= Essays.objects.get(id=ids)
    tite = objessay.topic
    tites=str(tite)
    pdffile = objessay.pdf
    rev = stopword(pdffile)
    bestlist = []
    avglist = []
    comlist = []
    for wrd in Bow.objects.filter(topic=tite):
       if wrd.priority == 'B':
           bestlist = bestlist + [wrd.word]
       elif wrd.priority == 'A':
           avglist = avglist + [wrd.word]
       else:
           comlist = comlist + [wrd.word]

    voc = {'best':bestlist, 'average':avglist, 'common':comlist}
    coss = tfidf(rev, voc)
    gramdict = grammarcheck(pdffile)
    nam = pdffile.name
    idss = ids
    # print(idss)
    stat=pdfcreater(nam,coss,gramdict,tite,idss)
    if stat:
        objessay.evaluated=True
        objessay.save(update_fields=['evaluated'])

def pdfcreater(nam,coss,gramdict,tite,idss):
    print('here')
    print(idss)
    pdf = FPDF()
    tot=0
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.add_font('DejaVu', '', 'styles/font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)

    fullname = nam
    fullnam = fullname.split("_")
    regnum = fullnam[0]
    regnums=regnum.split('/')
    topicname = fullnam[1].split(".")[0]

    heading = "Essay name :" + topicname
    reg = "Register number : " + regnums[2]
    pdf.cell(200, 10, txt=heading, ln=1)
    pdf.cell(200, 10, txt=reg, ln=2)
    stval = str(coss)
    cosstr = "Word Weight Value : " + stval
    pdf.cell(200, 10, txt=cosstr, ln=3)
    w = nam.split(".")
    wnew = w[0].split("/")
    tot = tot + coss
    stval2 = str(gramdict)
    tot = tot + gramdict
    gramstr = "Grammatical Score : " + stval2
    pdf.cell(200, 10, txt=gramstr, ln=4)
    totstr = "Total Score : " + str(tot)
    pdf.cell(200, 10, txt=totstr, ln=5)
    pdf.cell(200, 10, txt="Grammatical Errors : ", ln=6)

    filepath = os.path.join('media/Essays/Report', wnew[2] + '.txt')
    f1 = open(filepath, "r")

    # insert the texts in pdf
    for x in f1:
        # print(x)
        pdf.cell(200, 10, txt=x, ln=7)

    f1.close()
    del f1
    directory = str(tite)
    if not os.path.exists('media/Essays/Report/' + str(tite)):
        # Parent Directory path
        parent_dir = "media/Essays/Report/"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        # path.close()
        del path
    else:
        pass

    pdf.output("media/Essays/Report/" + str(tite) + "/" + wnew[2]+".pdf")
    # fil=open("media/Essays/Report/" +str(tite) + "/" + wnew[2]+".pdf",encoding='utf-8')
    # filepdf = File(fil)
    # print(filepdf)
    pdfobj = Report(essay=Essays.objects.get(id=idss),report="Essays/Report/" + str(tite) + "/" + wnew[2]+".pdf")
    # pdfobj.report.save(wnew[2]+".pdf",filepdf)
    pdfobj.save()
    # pdfobj.report=filepdf
    pdf.close()
    del pdf
    os.remove("media/Essays/Report/" + wnew[2] + ".txt")
    return True




