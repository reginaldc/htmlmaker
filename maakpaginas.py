import os
import uuid
import webbrowser
import makehtm as stuff
import re
import pdb
import shutil
import platform
import myvar

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    print()
    # Print New Line on Complete
    if iteration == total:
        print()

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^a-zA-Z0-9-_.]', '',s)

def renameInvalid(root):
    for f in os.listdir(root):
        try:
            #pdb.set_trace()
            old = f
            f = f.replace(" ", "_")
            if os.path.isfile(f):
                f = re.sub(r'[^a-zA-Z0-9-_.]', '',f)
            if os.path.isdir(f):
                f = re.sub(r'[^a-zA-Z0-9-_]', '',f)
            if old != f:
                    if os.path.isdir(old):
                        if os.path.exists(f):
                            aanhangsel = str(uuid.uuid4())[:8]
                            f = f + aanhangsel
                    os.rename(old,f)
                    print(Fore.RED + "renamed ")
                    print(Style.RESET_ALL)
                    print(old)
                    print(Fore.RED + " to ")
                    print(Style.RESET_ALL)
                    print( f )
            if os.path.isdir(f):
                os.chdir(f)
                renameInvalid(".")
                os.chdir("..")
        except:
            f = f.encode('utf-8', 'surrogateescape').decode('ISO-8859-1')

def recursive_copy(src, dst):
    os.chdir(src)
    for item in os.listdir():
        if os.path.isfile(item):
            shutil.copy(item, dst)
        elif os.path.isdir(item):
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            recursive_copy(os.path.abspath(item), new_dst)
            os.chdir("..")



vid_ext = (".avi", ".AVI", ".divx", ".mpg", ".mpeg", ".VOB", ".m4v", ".mp4", ".flv", ".webm",\
 ".mov", ".WMV", ".divx (ongeldige codering)", ".mp4 (ongeldige codering)",\
  ".avi (ongeldige codering)", ".wmv", ".mkv", ".MP4", ".avii")
pic_ext = (".jpg", ".png", ".JPEG", ".jpeg", ".JPG", ".PNG", ".bmp", ".BMP", ".gif", ".GIF")
movie_ext = (".mkv", ".mp4", ".mk4", ".MP4", ".MKV", ".m4v", ".M4V")
doc_ext = (".pdf", ".xps", ".cbz", ".epub")

renameInvalid(".")
foldergrootte = get_size()
folsz = sizeof_fmt(foldergrootte)
print("grootte van de map is " + folsz)
chunk = int(foldergrootte / 100)
chnk = sizeof_fmt(chunk)
print("chunk is : " + chnk)
tsize = 0
progres = 0
printProgressBar(progres,100,prefix = 'Progress:', suffix = 'Complete')

currentdir = myvar.current
htmldir = currentdir + "/htmloutput"
thumb_dir = htmldir + "/thumbs/"
pdf_thumbdir = htmldir + "/pdfthumbs/"
errors = 0

vidthumbs = []
picthumbs = []
docthumbs = []
totalSize = 0
minSize = 5000
klein = 0
if not os.path.exists(htmldir):
    os.makedirs(htmldir)
if not os.path.exists(pdf_thumbdir):
    os.makedirs(pdf_thumbdir)
if not os.path.exists(thumb_dir):
    os.makedirs(thumb_dir)
recursive_copy("/home/reginald/gallerij",htmldir + "/")
i = 1
teller = 0
cnt = 1
for root, dirs, files in os.walk(currentdir, topdown=True):
    exclude = {"htmloutput","temp"}
    dirs[:] = [d for d in dirs if d not in exclude]
    for file in files:
        try:
            teller += 1
            ifile = str(os.path.join(root, file))
            print (ifile)
            extension = os.path.splitext(ifile)[1]
            base = os.path.basename(ifile)
            zonder = os.path.splitext(base)[0]
            fileSize = os.path.getsize(ifile)
            tsize += fileSize
            totalSize += fileSize
            if tsize >= chunk:
                pgs = tsize // chunk
                progres += pgs
                printProgressBar(progres,100,prefix = 'Progress:', suffix = 'Complete')
                tsize = tsize - (pgs * chunk)
            if teller >= 101:
                thumb_dir = htmldir + "/thumbs" + str(cnt) + "/"
                if not os.path.exists(thumb_dir):
                    os.makedirs(thumb_dir)
                    cnt += 1
                    teller = 1
            if extension in vid_ext:
                vid_ofile = thumb_dir + zonder + ".jpg"
                pagina = ""
                print (("Generating thumbnail for: " + ifile))
                fftoptions = " -f -s 256"
                ifile = '"' + ifile + '"'
                vid_ofile = '"' + vid_ofile + '"'
                try:
                    command = "ffmpegthumbnailer -i %s -o %s %s" % (ifile, vid_ofile, fftoptions)
                    p = os.popen(command, "r")
                    while 1:
                        line = p.readline()
                        if not line:
                            break
                        print (line)
                except:
                    vid_ofile = htmldir + "/images/broken.png"
                    pass
                if extension in movie_ext:
                    #pdb.set_trace()
                    htmdir = htmldir + "/pages/"
                    idx = htmldir + "/index.html"
                    moviefile = ifile[(len(currentdir)+1):]
                    moviefile = "../.." + moviefile
                    pagina = stuff.createVidplayer(moviefile, i, template=idx, folder=htmdir)
                    i += 1
                    ifile = ifile[len(currentdir):]
                tupvidthumb = (ifile, vid_ofile, pagina)
                vidthumbs.append(tupvidthumb)
            if extension in pic_ext:
                if fileSize < minSize:
                    klein += 1
                    continue
                uniek = str(uuid.uuid4())[:8]
                unique_str =  uniek + base
                #pdb.set_trace()
                pic_ofile = thumb_dir+ "/" + unique_str
                stuff.createThumbnail(ifile, unique_str, thumb_dir)
                tupthumb = (ifile, pic_ofile)
                picthumbs.append(tupthumb)
            if extension in doc_ext:
                fname_no_ext = os.path.splitext(base)[0]
                pdf_ofile = pdf_thumbdir + fname_no_ext + ".png"
                pdf_ofile = "'" + pdf_ofile + "'"
                ifile = "'" + ifile + "'"
                commando  = "mutool draw -o " + pdf_ofile + " -h 256 " + ifile + " 1"
                p = os.popen(commando, "r")
                while 1:
                    line = p.readline()
                    if not line:
                        break
                    print (line)
                tuppdf = (ifile, pdf_ofile)
                docthumbs.append(tuppdf)
            if (get_free_space_mb(currentdir) < 10):
                break
        except (UnicodeEncodeError, IOError, ValueError) as e:
            print(e)
            errors += 1
            pass



outputpic = htmldir + "/gallery_"
sz = 75
vds = False
dcs = False
pcs = False
if docthumbs:
    dcs = True
if picthumbs:
    pcs = True
if vidthumbs:
    vds = True
    aantal = len(vidthumbs)
    print("aantal videobestanden is %d" % aantal)
    outputvid = htmldir + "/vidgallery_"
    stuff.createJustifiedVideoPage(vidthumbs, htmldir + "/vidgallery_templ.html",output=outputvid ,pics=pcs ,docs=dcs)
    webbrowser.open("file:////" + outputvid + "1.html")

if picthumbs:
    count = len(picthumbs)
    print ("aantal afbeeldingen is %d" % count)
    #pdb.set_trace()
    totaal = int(count / sz) + 1
    teller = 1
    begin = 1
    nummer = 1
    while teller < count:
        if count <= sz:
            stuff.createJustifiedGallery(picthumbs,htmldir + "/gallery_templ.html",nummer,totaal,output=outputpic,vids=vds,docs=dcs)
            break
        else:
            teller += sz
            tempthumb = picthumbs[begin:teller]
            #stuff.createWebpage(temptumb, '/home/reginald/scripts/html/fotoToDb.html', nummer)
            stuff.createJustifiedGallery(tempthumb,htmldir + "/gallery_templ.html",nummer,totaal,output=outputpic,vids=vds,docs=dcs)
            nummer += 1
            begin += sz
    webbrowser.open("file:////" + htmldir + "/gallery_1.html")

if docthumbs:
    count = len(docthumbs)
    print("aantal pdfbestanden is %d" % count)
    size = 24
    numpages = count/size
    totaal = int(numpages) + 1
    tel = 1
    begin = 1
    num = 1
    template = htmldir + "/pdfToDb.html"
    outpage = htmldir + "/outputPdfPages"
    while tel < count:
        if count <= sz:
            stuff.createPdfWebpage(docthumbs ,template ,total=totaal ,nr=num ,out=outpage ,vids=vds , pics=pcs)
            break
        else:
            tel += size
            tempthumb = docthumbs[begin:tel]
            begin += size
            stuff.createPdfWebpage(tempthumb ,template ,total=totaal ,nr=num ,out=outpage ,vids=vds ,pics=pcs)
            num += 1
    webbrowser.open("file://" + htmldir + "/outputPdfPages1.html")

print("aantal fouten : " + str(errors))
print("aantal kleine bestanden : " + str(klein))



