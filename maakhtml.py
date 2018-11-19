import os
import urllib.parse
from PIL import Image
from bs4 import BeautifulSoup
import math
import pdb
import myvar
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    


def createJustifiedGallery(lsttupthumb,template_page,nr,total,output="/home/reginald/gallery/pages/gallery_done_",vids=False,docs=False):
    req = urlopen("file:///"+ template_page)
    soup = BeautifulSoup(req.read(), 'html.parser')
    if vids:
        vlink = soup.find("div" ,{"class":"vidslink"})
        a_vid = soup.new_tag("a", href="vidgallery_1.html")
        vlink.insert(0, a_vid)
        imtag = soup.new_tag("img", src="images/vids.png")
        a_vid.insert(0, imtag)
    if docs:
        dlink = soup.find("div" ,{"class":"docslink"})
        a_doc = soup.new_tag("a", href="outputPdfPages1.html")
        dlink.insert(0, a_doc)
        imtag = soup.new_tag("img", src="images/boekenstapel.jpeg")
        a_doc.insert(0, imtag)

    pagination = soup.find("div",{"class":"pagination"})
    anktop = nr + 5
    ankbot = nr - 4
    if anktop > total:
        anktop = total
        ankbot = anktop - 10
    if ankbot <= 0:
        ankbot = 1
        anktop = ankbot + 10
        if anktop > total:
            anktop = total
    #link naar laatste pagina
    if nr < (total - 10):
        link = "gallery_" + str(total) + ".html"
        tekst = u'>>'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        pagination.insert(0,ankerpag)
    while anktop >= ankbot:
        verschil = anktop - nr
        tekst = str(nr + verschil)
        #link = output + str(nr + verschil) + ".html"
        link = "gallery_" + str(nr + verschil) + ".html"
        if anktop == nr:
            ankerpag = soup.new_tag("a", href=link, **{"class":"current"})
        else:
            ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        pagination.insert(0,ankerpag)
        anktop -= 1
    #link naar eerste pagina
    if nr > 10:
        link = "gallery_1.html"
        tekst = u'<<'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        pagination.insert(0,ankerpag)

    bottompagination = soup.find("div",{"class":"bottompagination"})
    anktop = nr + 5
    ankbot = nr - 4
    if anktop > total:
        anktop = total
        ankbot = anktop - 10
    if ankbot <= 0:
        ankbot = 1
        anktop = ankbot + 10
        if anktop > total:
            anktop = total
    #link naar laatste pagina
    if nr < (total - 10):
        link = "gallery_" + str(total) + ".html"
        tekst = u'>>'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        bottompagination.insert(0,ankerpag)
    while anktop >= ankbot:
        verschil = anktop - nr
        tekst = str(nr + verschil)
        #link = output + str(nr + verschil) + ".html"
        link = "gallery_" + str(nr + verschil) + ".html"
        if anktop == nr:
            ankerpag = soup.new_tag("a", href=link, **{"class":"current"})
        else:
            ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        bottompagination.insert(0,ankerpag)
        anktop -= 1
    #link naar eerste pagina
    if nr > 10:
        link = "gallery_1.html"
        tekst = u'<<'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        bottompagination.insert(0,ankerpag)

    div = soup.find('div', {"class":"liveDemo"})
    cur = myvar.current
    for t in lsttupthumb:
        #a_tag = soup.new_tag('a', href=t[0])
        #pdb.set_trace()
        ref=t[0]
        ref = ref.replace(cur,"")
        ref = ".." + ref
        a_tag = soup.new_tag('a', href=ref,**{'class':'xpic','rel':'xgallerij'})
        div.insert(0,a_tag)
        thumbref=t[1]
        thumbref = thumbref.replace(cur,"")
        thumbref = ".." + thumbref
        img_tag = soup.new_tag('img', src=thumbref)
        a_tag.insert(0, img_tag)
    vorige = soup.find("div", {"id": "linkprev"})
    if not nr == 1:
        #linkpr = output + str(nr - 1) + ".html"
        linkpr = "gallery_" + str(nr - 1) + ".html"
        anker = soup.new_tag('a', href=linkpr)
        vorige.insert(0, anker)
        vorigprentje = "images/left.png"
        imtag = soup.new_tag('img', src=vorigprentje)
        anker.insert(0, imtag)
    volgende = soup.find("div", {"id":"linknext"})
    if nr < total:
        #linknxt = output + str(nr + 1) + ".html"
        linknxt = "gallery_" + str(nr + 1) + ".html"
        anker = soup.new_tag('a', href=linknxt)
        volgende.insert(0, anker)
        volgendprentje = "images/right.png"
        imtag = soup.new_tag('img', src=volgendprentje)
        anker.insert(0, imtag)
    htmlstuff = soup.prettify("utf-8")
    out = output + str(nr) + ".html"
    with open(out, "wb") as pagina:
        pagina.write(htmlstuff)



# methode om een webpagina te maken: invoer tuple thumbnails, template, webpaginanummer
def createWebpage(my_thumbs,  template_page, num):
    req = urlopen("file:///"+ template_page)
    soup = BeautifulSoup(req.read(), 'html.parser')
    table = soup.table
    row_thumbs = []
    trtag = soup.new_tag('tr')
    table.insert(0,trtag)
    i = 1
    try:
        for thumb in my_thumbs:
            row_thumbs.append(thumb)
            i += 1
            if i == 9:
                for t in row_thumbs:
                    tdtag = soup.new_tag('td')
                    trtag.insert(0, tdtag)
                    atag = soup.new_tag('a', href=t[0])
                    tdtag.insert(0, atag)
                    img_tag = soup.new_tag('img', src=t[1])
                    atag.insert(0, img_tag)
                newtrtag = soup.new_tag('tr')
                trtag.insert_after(newtrtag)
                trtag = trtag.findNext('tr')
                row_thumbs = []
                i = 1
        if len(row_thumbs) > 0:
            for t in row_thumbs:
                tdtag = soup.new_tag('td')
                trtag.insert(0, tdtag)
                atag = soup.new_tag('a', href=t[0])
                tdtag.insert(0, atag)
                img_tag = soup.new_tag('img', src=t[1])
                atag.insert(0, img_tag)
                newtrtag = soup.new_tag('tr')
                trtag.insert_after(newtrtag)
                trtag = trtag.findNext('tr')


        vorige = soup.find("div", {"id": "linkprev"})
        linkpr = "/home/reginald/scripts/html/pages/outputThumbPages" + str(num - 1) + ".html"
        anker = soup.new_tag('a', href=linkpr)
        vorige.insert(0, anker)
        vorigprentje = "/home/reginald/scripts/html/left.png"
        imtag = soup.new_tag('img', src=vorigprentje)
        anker.insert(0, imtag)
        volgende = soup.find("div", {"id":"linknext"})
        linknxt = "/home/reginald/scripts/html/pages/outputThumbPages" + str(num + 1) + ".html"
        anker = soup.new_tag('a', href=linknxt)
        volgende.insert(0, anker)
        volgendprentje = "/home/reginald/scripts/html/right.png"
        imtag = soup.new_tag('img', src=volgendprentje)
        anker.insert(0, imtag)
    except AttributeError as e:
        print (e)
        pass
    htmlstuff = soup.prettify("utf-8")
    out = "/home/reginald/scripts/html/pages/outputThumbPages" + str(num) + ".html"
    print ("out is %s" % out)
    with open(out, "wb") as pagina:
        pagina.write(htmlstuff)

def createPdfWebpage(my_thumbs ,template_page ,total=1 ,nr=1 ,out="/home/reginald/scripts/html/outputPdfPages" ,vids=False ,pics=False):
    req = urlopen("file:///"+ template_page)
    soup = BeautifulSoup(req.read(), 'html.parser')
    if vids:
        vlink = soup.find("div" ,{"class":"vidslink"})
        a_vid = soup.new_tag("a", href="vidgallery_1.html")
        vlink.insert(0, a_vid)
        imtag = soup.new_tag("img", src="images/vids.png")
        a_vid.insert(0, imtag)
    if pics:
        plink = soup.find("div" ,{"class":"picslink"})
        a_pic = soup.new_tag("a", href="gallery_1.html")
        plink.insert(0, a_pic)
        imtag = soup.new_tag("img", src="images/fotostapel.jpg")
        a_pic.insert(0, imtag)
    vorige = soup.find("div", {"id": "linkprev"})
    if not nr == 1:
        #linkpr = out + str(nr - 1) + ".html"
        linkpr = "outputPdfPages" + str(nr - 1) + ".html"
        anker = soup.new_tag('a', href=linkpr)
        vorige.insert(0, anker)
        vorigprentje = "images/left.png"
        imtag = soup.new_tag('img', src=vorigprentje)
        anker.insert(0, imtag)
    volgende = soup.find("div", {"id":"linknext"})
    if nr < total:
        #linknxt = out + str(nr + 1) + ".html"
        linknxt = "outputPdfPages" + str(nr + 1) + ".html"
        anker = soup.new_tag('a', href=linknxt)
        volgende.insert(0, anker)
        volgendprentje = "images/right.png"
        imtag = soup.new_tag('img', src=volgendprentje)
        anker.insert(0, imtag)
    pagination = soup.find("div",{"class":"pagination"})
    anktop = nr + 4
    ankbot = nr - 3
    if anktop > total:
        anktop = total
        ankbot = anktop - 8
    if ankbot <= 0:
        ankbot = 1
        anktop = ankbot + 8
        if anktop > total:
            anktop = total
    #link naar laatste pagina
    if nr < (total - 8):
        link = "outputPdfPages" + str(total) + ".html"
        tekst = u'>>'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        pagination.insert(0,ankerpag)
    while anktop >= ankbot:
        verschil = anktop - nr
        tekst = str(nr + verschil)
        #link = output + str(nr + verschil) + ".html"
        link = "outputPdfPages" + str(nr + verschil) + ".html"
        if anktop == nr:
            ankerpag = soup.new_tag("a", href=link, **{"class":"current"})
        else:
            ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        pagination.insert(0,ankerpag)
        anktop -= 1
    #link naar eerste pagina
    if nr > 8:
        link = "outputPdfPages1.html"
        tekst = u'<<'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        pagination.insert(0,ankerpag)
    table = soup.table
    row_thumbs = []
    trtag = soup.new_tag('tr')
    table.insert(0,trtag)
    i = 1
    try:
        cur = myvar.current
        for thumb in my_thumbs:
            row_thumbs.append(thumb)
            i += 1
            if i == 7:
                for t in row_thumbs:
                    tdtag = soup.new_tag('td')
                    trtag.insert(0, tdtag)
                    plaats = t[0]
                    plaats = plaats[1:-1]
                    plaats = plaats.replace(cur,'')
                    plaats = ".." + plaats
                    atag = soup.new_tag('a', href=plaats)
                    tdtag.insert(0, atag)
                    bron = t[1]
                    bron = bron[1:-1]
                    bron = bron.replace(cur,'')
                    bron = ".." + bron
                    img_tag = soup.new_tag('img', src=bron)
                    atag.insert(0, img_tag)
                newtrtag = soup.new_tag('tr')
                trtag.insert_after(newtrtag)
                trtag = trtag.findNext('tr')
                row_thumbs = []
                i = 1
    except AttributeError as e:
        print (e)
        pass
    bottompagination = soup.find("div",{"class":"bottompagination"})
    anktop = nr + 4
    ankbot = nr - 3
    if anktop > total:
        anktop = total
        ankbot = anktop - 8
    if ankbot <= 0:
        ankbot = 1
        anktop = ankbot + 8
        if anktop > total:
            anktop = total
    #link naar laatste pagina
    if nr < (total - 8):
        link = "outputPdfPages" + str(total) + ".html"
        tekst = u'>>'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        bottompagination.insert(0,ankerpag)
    while anktop >= ankbot:
        verschil = anktop - nr
        tekst = str(nr + verschil)
        #link = output + str(nr + verschil) + ".html"
        link = "outputPdfPages" + str(nr + verschil) + ".html"
        if anktop == nr:
            ankerpag = soup.new_tag("a", href=link, **{"class":"current"})
        else:
            ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        bottompagination.insert(0,ankerpag)
        anktop -= 1
    #link naar eerste pagina
    if nr > 8:
        link = "outputPdfPages1.html"
        tekst = u'<<'
        ankerpag = soup.new_tag("a", href = link)
        ankerpag.insert(0,tekst)
        bottompagination.insert(0,ankerpag)
    htmlstuff = soup.prettify("utf-8")
    #pdb.set_trace()
    out = out + str(nr) + ".html"
    with open(out, "wb") as pagina:
        pagina.write(htmlstuff)

def createVidplayer(infile, teller, template="file:///home/reginald/scripts/html/index.html", folder="/home/reginald/scripts/html/pages/"):
    #encodedinfile = urls.url_fix(infile)
    base = os.path.basename(infile)
    fname_no_ext = os.path.splitext(base)[0]
    hoofd = fname_no_ext.replace("_"," ")
    inf = infile.replace('"','')
    req = urlopen("file://" + template)
    soup = BeautifulSoup(req.read(), 'html.parser')
    heading = soup.find('h1')
    heading.string = heading.text.replace("hoofding",hoofd)
    video = soup.video
    video['src'] = inf
    video['controls'] = "yes"
    video['width'] = "1200"
    video['height'] = "800"
    htmlstuff = soup.prettify("utf-8")
    htmlfile = folder + "videopagina" + str(teller) + ".html"
    with open(htmlfile, "wb") as pagina:
        pagina.write(htmlstuff)
    return htmlfile

def createThumbnail(fl,outfile,tdir):
    fname, ext, = os.path.splitext(fl)
    if ext == ".jpg" or ext == ".jpeg" or ext == ".JPEG" or ext == ".JPG":
        try:
                size = 128, 128
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
                    print ("made tdir map")
                ofile = tdir + outfile
                im = Image.open(fl)
                im.thumbnail(size)
                im.save(ofile, "JPEG")
        except (IOError, SyntaxError):
                print ("cannot create thumbnail for"+ fl)
                pass
    if ext == ".gif" or ext == ".GIF":
        try:
                size = 128, 128
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
                    print ("made tdir map")
                ofile = tdir + outfile
                im = Image.open(fl)
                im.thumbnail(size)
                im.save(ofile, "gif")
        except (IOError, SyntaxError):
                print ("cannot create thumbnail for"+ fl)
                pass
    if ext == ".png" or ext == ".PNG":
        try:
                size = 128, 128
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
                    print ("made tdir map")
                ofile = tdir + outfile
                im = Image.open(fl)
                im.thumbnail(size)
                im.save(ofile, "png")
        except (IOError, SyntaxError):
                print ("cannot create thumbnail for"+ fl)
                pass
    if ext == ".bmp" or ext == ".BMP":
        try:
                size = 128, 128
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
                    print ("made tdir map")
                ofile = tdir + outfile
                im = Image.open(fl)
                im.thumbnail(size)
                im.save(ofile, "bmp")
        except (IOError, SyntaxError):
                print ("cannot create thumbnail for"+ fl)
                pass


def createJustifiedVideoPage(my_thumbs, template_vids,output="/home/reginald/gallery/pages/vidgallery_",pics=False ,docs=False):
    #pdb.set_trace()
    gallerySize = 50
    numVid = len(my_thumbs)
    numPages = numVid / gallerySize
    np = int(math.ceil(numPages))
    teller = 0
    gedaan = 0
    pag = 0
    huidig = 1
    linkpr = ""
    linknxt = ""
    #proto = 'file://'
    i = 0
    while i < np:
        if pag > 1:
            #linkpr = output + str(pag) + ".html"
            linkpr = "vidgallery_" + str(pag) + ".html"
        if pag >= 0:
            #linknxt = output + str(pag + 2) + ".html"
            linknxt = "vidgallery_" + str(pag + 2) + ".html"
        inhoud = urlopen("file:///" + template_vids)
        soup = BeautifulSoup(inhoud.read(), 'html.parser')
        if pics:
            plink = soup.find("div" ,{"class":"picslink"})
            a_pic = soup.new_tag("a", href="gallery_1.html")
            plink.insert(0, a_pic)
            imtag = soup.new_tag("img", src="images/fotostapel.jpg")
            a_pic.insert(0, imtag)
        if docs:
            dlink = soup.find("div" ,{"class":"docslink"})
            a_doc = soup.new_tag("a", href="outputPdfPages1.html")
            dlink.insert(0, a_doc)
            imtag = soup.new_tag("img", src="images/boekenstapel.jpeg")
            a_doc.insert(0, imtag)
        pagination = soup.find("div",{"class":"pagination"})
        anktop = pag + 5
        ankbot = pag - 4
        if anktop > np:
            anktop = np
            ankbot = anktop - 10
        if ankbot <= 0:
            ankbot = 1
            anktop = ankbot + 10
            if anktop > np:
                anktop = np
        #link naar laatste pagina
        if huidig < (np - 10):
            link = "vidgallery_" + str(np) + ".html"
            tekst = u'>>'
            ankerpag = soup.new_tag("a", href = link)
            ankerpag.insert(0,tekst)
            pagination.insert(0,ankerpag)
        while anktop >= ankbot:
            verschil = anktop - pag
            tekst = str(pag + verschil)
            #link = output + str(pag + verschil) + ".html"
            link = "vidgallery_" + str(pag + verschil) + ".html"
            if anktop == huidig:
                ankerpag = soup.new_tag("a", href=link, **{"class":"current"})
            else:
                ankerpag = soup.new_tag("a", href = link)
            ankerpag.insert(0,tekst)
            pagination.insert(0,ankerpag)
            anktop -= 1
        #link naar eerste pagina
        if huidig > 10:
            link = "vidgallery_1.html"
            tekst = u'<<'
            ankerpag = soup.new_tag("a", href = link)
            ankerpag.insert(0,tekst)
            pagination.insert(0,ankerpag)

        bottompagination = soup.find("div",{"class":"bottompagination"})
        anktop = pag + 5
        ankbot = pag - 4
        if anktop > np:
            anktop = np
            ankbot = anktop - 10
        if ankbot <= 0:
            ankbot = 1
            anktop = ankbot + 10
            if anktop > np:
                anktop = np
        #link naar laatste pagina
        if huidig < (np - 10):
            link = "vidgallery_" + str(np) + ".html"
            tekst = u'>>'
            ankerpag = soup.new_tag("a", href = link)
            ankerpag.insert(0,tekst)
            bottompagination.insert(0,ankerpag)
        while anktop >= ankbot:
            verschil = anktop - pag
            tekst = str(pag + verschil)
            #link = output + str(pag + verschil) + ".html"
            link = "vidgallery_" + str(pag + verschil) + ".html"
            if anktop == huidig:
                ankerpag = soup.new_tag("a", href=link, **{"class":"current"})
            else:
                ankerpag = soup.new_tag("a", href = link)
            ankerpag.insert(0,tekst)
            bottompagination.insert(0,ankerpag)
            anktop -= 1
        #link naar eerste pagina
        if huidig > 10:
            link = "vidgallery_1.html"
            tekst = u'<<'
            ankerpag = soup.new_tag("a", href = link)
            ankerpag.insert(0,tekst)
            bottompagination.insert(0,ankerpag)

        div = soup.find("div", {"class":"liveDemo"})
        overschot = numVid%gallerySize
        if ((np - 1) == 0 and (overschot < gallerySize)):
            gallerySize = overschot
        cur = myvar.current
        while (teller < gallerySize and gedaan < (numVid)):
            #pdb.set_trace()
            t = my_thumbs[gedaan]
            if t[2] == "":
                referentie = t[0]
            else:
                referentie = t[2]
            referentie = referentie.replace('"','')
            referentie = referentie.replace(cur,'')
            hashref = ".." + referentie
            pdb.set_trace()
            hashref = urllib.parse.quote_plus(hashref)
            a_tag = soup.new_tag("a", href= hashref,**{"class":"xpic","rel":"xgallerij"})
            div.insert(0,a_tag)
            bronbestand = t[1]
            bronbestand = bronbestand.replace('"','')
            bronbestand = bronbestand.replace(cur,'')
            bron = ".." + bronbestand
            img_tag = soup.new_tag("img", src= bron)
            a_tag.insert(0, img_tag)
            teller += 1
            gedaan += 1
        pag += 1
        if not (pag == 1):
            vorige = soup.find("div", {"id": "linkprev"})
            anker = soup.new_tag('a', href=linkpr)
            vorige.insert(0, anker)
            vorigprentje = "images/left.png"
            imtag = soup.new_tag('img', src=vorigprentje)
            anker.insert(0, imtag)
        if (np > 1) and (pag < np):
            volgende = soup.find("div", {"id":"linknext"})
            anker = soup.new_tag('a', href=linknxt)
            volgende.insert(0, anker)
            volgendprentje = "images/right.png"
            imtag = soup.new_tag('img', src=volgendprentje)
            anker.insert(0, imtag)
        htmlstuff = soup.prettify("utf-8")
        out = output + str(pag) + ".html"
        with open(out, "wb") as pagina:
            pagina.write(htmlstuff)
        teller = 0
        i += 1
        huidig += 1


def createVidWebpage(my_thumbs, template_page):
    vids = (".mp4", ".mk4", ".m4v", ".mkv")
    req = urlopen("file:///" + template_page)
    soup = BeautifulSoup(req.read(), 'html.parser')
    table = soup.table
    row_thumbs = []
    trtag = soup.new_tag('tr')
    table.insert(0, trtag)
    i = 1
    try:
        for thumb in my_thumbs:
            lengte = len(my_thumbs)
            if lengte < 5:
                tdtag = soup.new_tag('td')
                trtag.insert(0, tdtag)
                extension = os.path.splitext(thumb[0])[1]
                extension = extension[:-1]
                if extension in vids:
                    lokatie = thumb[2]
                    atag = soup.new_tag('a', href=lokatie)
                else:
                    plaats = thumb[0][1:-1]
                    lokatie = plaats
                    atag = soup.new_tag('a', href=lokatie)
                tdtag.insert(0, atag)
                miniatuur = thumb[1]
                miniatuur = miniatuur[1:-1]
                duimnagel = miniatuur
                img_tag = soup.new_tag('img', src=duimnagel)
                atag.insert(0, img_tag)
            else:
                row_thumbs.append(thumb)
                i += 1
                if i == 5:
                    for t in row_thumbs:
                        tdtag = soup.new_tag('td')
                        trtag.insert(0, tdtag)
                        extension = os.path.splitext(t[0])[1]
                        extension = extension[:-1]
                        if extension in vids:
                            lokatie = "file://" + t[2]
                            atag = soup.new_tag('a', href=lokatie)
                        else:
                            plaats = t[0][1:-1]
                            plaats = urllib.parse.quote_plus(plaats)
                            lokatie = "file://" + plaats
                            atag = soup.new_tag('a', href=lokatie)
                        tdtag.insert(0, atag)
                        miniatuur = t[1]
                        miniatuur = miniatuur[1:-1]
                        duimnagel = "file://" + miniatuur
                        img_tag = soup.new_tag('img', src=duimnagel)
                        atag.insert(0, img_tag)
                    newtrtag = soup.new_tag('tr')
                    trtag.insert_after(newtrtag)
                    trtag = trtag.findNext('tr')
                    row_thumbs = []
                    i = 1
    except AttributeError as e:
        print (e)
        pass
    htmlstuff = soup.prettify("utf-8")
    with open("/home/reginald/gallery/pages/outputVidPages.html", "wb") as pagina:
        pagina.write(htmlstuff)




