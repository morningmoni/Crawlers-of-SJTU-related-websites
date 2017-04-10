# encoding=utf8
# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import http.cookiejar
import time
import datetime


def Tieba():
    url = 'http://tieba.baidu.com/f?kw=%C9%CF%BA%A3%BD%BB%CD%A8%B4%F3%D1%A7'
    ct = urllib.request.urlopen(url, timeout=5).read()
    soup = BeautifulSoup(ct, 'lxml')
    n = 0
    print('*' * 20 + 'tieba' + '*' * 20)
    for i in soup.findAll('a', {'class': "threadlist_text threadlist_title j_th_tit  "}):
        print(n, ' ', i.get_text())
        tmp = i.get('href', '??')
        tmp = urllib.parse.urljoin(url, tmp)
        print(tmp)
        reply = soup.findAll('div', {'title': '回复'})[n].get_text()
        print('回复：' + reply)
        n += 1
    print('*' * 20 + 'tieba' + '*' * 20)


##        if n>=3:
##            print soup.findAll('div',{'class':'threadlist_abs threadlist_abs_onlyline'})[n-3].get_text()
##        print '\n'

def Tongqu_JWC():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url='https://tongqu.me', headers=headers)
    ct = urllib.request.urlopen(req).read()

    url = 'http://tongqu.me/index.php/act/detail/view/'
    soup = BeautifulSoup(ct, 'lxml')
    nowTime = time.localtime()
    nowDate = datetime.datetime(nowTime[0], nowTime[1], nowTime[2], nowTime[3], nowTime[4], nowTime[5])
    count = 0
    myset = set()
    URLs = []
    newURLs = []
    try:
        f = open('getInfo', 'r')
        for line in f:
            URLs += [line.strip()]
        ##        print URLs
        f.close()
    except:
        pass

    print('*' * 20 + 'Tongqu' + '*' * 20)
    for i in soup.body.findAll('script'):
        s = str(i)
        first_actid = s.find('\"actid\":')
        lf_actid = first_actid

        first_name = s.find('\"name\":')
        lf_name = first_name

        first_starttime = s.find('\"start_time\"')
        lf_starttime = first_starttime

        first_endtime = s.find('\"end_time\"')
        lf_endtime = first_endtime

        first_signstarttime = s.find('\"sign_start_time\"')
        lf_signstarttime = first_signstarttime

        first_signendtime = s.find('\"sign_end_time\"')
        lf_signendtime = first_signendtime

        while first_name != -1:
            last_name = s.find(',', first_name)
            last_starttime = s.find(',', first_starttime)
            last_endtime = s.find(',', first_endtime)
            last_signstarttime = s.find(',', first_signstarttime)
            last_signendtime = s.find(',', first_signendtime)
            last_actid = s.find(',', first_actid)
            if str(nowDate) < s[first_signendtime + 17:last_signendtime] and s[first_name + 7:last_name] not in myset:
                if url + s[first_actid + 9:last_actid - 1].encode().decode("unicode_escape") not in URLs:
                    print("new--->", end=' ')
                    print(count, s[first_name + 7:last_name].encode().decode("unicode_escape"))
                    print("  ", s[first_starttime:last_starttime].encode().decode("unicode_escape"))
                    print("  ", s[first_endtime:last_endtime].encode().decode("unicode_escape"))
                    print("  ", s[first_signstarttime:last_signstarttime].encode().decode("unicode_escape"))
                    print("  ", s[first_signendtime:last_signendtime].encode().decode("unicode_escape"))
                    print("  ", url + s[first_actid + 9:last_actid - 1].encode().decode("unicode_escape"))
                newURLs += [url + s[first_actid + 9:last_actid - 1].encode().decode("unicode_escape")]
                myset.add(s[first_name + 7:last_name].encode().decode("unicode_escape"))
                count += 1
            first_name = s.find('\"name\":', lf_name + 1)
            lf_name = first_name

            first_starttime = s.find('\"start_time\"', lf_starttime + 1)
            lf_starttime = first_starttime

            first_endtime = s.find('\"end_time\"', lf_endtime + 1)
            lf_endtime = first_endtime

            first_signstarttime = s.find('\"sign_start_time\"', lf_signendtime + 1)
            lf_signstarttime = first_signstarttime

            first_signendtime = s.find('\"sign_end_time\"', lf_signendtime + 1)
            lf_signendtime = first_signendtime

            first_actid = s.find('\"actid\"', lf_actid + 1)
            lf_actid = first_actid
    print('*' * 20 + 'Tongqu' + '*' * 20)

    url = 'http://www.jwc.sjtu.edu.cn'
    ct = urllib.request.urlopen(url, timeout=5).read()
    soup = BeautifulSoup(ct, 'lxml')
    s = str(soup)
    ##    s=str(soup).decode('gb2312','ignore')
    ##    s=s.encode('utf8')
    first = s.rfind('通知通告')
    left = s.find('<a href', first)
    lleft = left
    count = 0
    print('*' * 20 + '教务处' + '*' * 20)
    while left != -1:
        right = s.find('>', left)
        if s[left + 9].isdigit():
            url_left = s.find('\"', left)
            url_right = s.find('\"', url_left + 1)
            title_left = s.find('title', left)
            title_right = s.find('\"', title_left + 7)
            if count > 0:
                if url + '/web/sjtu/' + s[url_left + 1:url_right] not in URLs:
                    print("new--->", end=' ')
                    print(count, ' ', s[title_left + 7:title_right])
                    print(url + '/web/sjtu/' + s[url_left + 1:url_right])
                newURLs += [url + '/web/sjtu/' + s[url_left + 1:url_right] + '\n']
            count += 1
        left = s.find('<a href', lleft + 1)
        lleft = left
    print('*' * 20 + '教务处' + '*' * 20)

    try:
        f = open('getInfo', 'w')
        for i in newURLs:
            f.write(i + "\n")
        f.close()
    except:
        pass


def smith():
    print('*' * 20 + 'Smith' + '*' * 20)
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    urllib.request.install_opener(opener)
    postdata = urllib.parse.urlencode({
        'op': 'login',
        'userid': ' ',
        'password': ' '
    })
    req = urllib.request.Request(url='http://seerc.sjtu.edu.cn/select.aspx', data=postdata)
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp.read(), 'lxml')

    for i in soup.findAll('tr'):
        if "选中" in str(i):
            print(i)
            print()

    print('*' * 20 + 'Smith' + '*' * 20)


def electsys(id, pwd, classID, keyword):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)

    ct = urllib.request.urlopen('http://electsys.sjtu.edu.cn/edu/index.aspx', timeout=5).read()
    soup = BeautifulSoup(ct, 'lxml')
    for i in soup.findAll('input', {'name': '__VIEWSTATE'}):
        VIEWSTATE = dict(i.attrs)['value']
    for i in soup.findAll('input', {'name': '__EVENTVALIDATION'}):
        EVENTVALIDATION = dict(i.attrs)['value']
    postdata = urllib.parse.urlencode({
        'txtUserName': id,
        'txtPwd': pwd,
        'rbtnLst': '1',
        'Button1': '登录',
        '__VIEWSTATEGENERATOR': 'E7EB4345',
        '__EVENTVALIDATION': EVENTVALIDATION,
        '__VIEWSTATE': VIEWSTATE
    })
    req = urllib.request.Request(url='http://electsys.sjtu.edu.cn/edu/index.aspx', data=postdata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    resp = urllib.request.urlopen(req)

    postdata = urllib.parse.urlencode({
        'CheckBox1': 'on',
        'btnContinue': '继续'
    })
    req = urllib.request.Request(url='http://electsys.sjtu.edu.cn/edu/student/elect/electwarning.aspx?xklc=3',
                                 data=postdata)
    resp = urllib.request.urlopen(req)

    times = 1
    ##    ct=urllib2.urlopen('http://electsys.sjtu.edu.cn/edu/student/elect/speltyRequiredCourse.aspx',timeout=5).read()
    ##    soup=BeautifulSoup(ct)
    ##    for i in soup.findAll('input',{'name':'__VIEWSTATE'}):
    ##        VIEWSTATE=dict(i.attrs)['value']
    ##    for i in soup.findAll('input',{'name':'__EVENTVALIDATION'}):
    ##        EVENTVALIDATION=dict(i.attrs)['value']
    ##    postdata=urllib.urlencode({
    ##        'SpeltyRequiredCourse1$btnXxk':'限选课',
    ##        '__EVENTVALIDATION':EVENTVALIDATION,
    ##        '__VIEWSTATE':VIEWSTATE
    ##        })
    ##    req=urllib2.Request(url = 'http://electsys.sjtu.edu.cn/edu/student/elect/speltyRequiredCourse.aspx',data = postdata)
    ##    resp=urllib2.urlopen(req)
    ##
    ##    ct=urllib2.urlopen('http://electsys.sjtu.edu.cn/edu/student/elect/speltyLimitedCourse.aspx',timeout=5).read()
    ##    soup=BeautifulSoup(ct)
    ##    for i in soup.findAll('input',{'name':'__VIEWSTATE'}):
    ##        VIEWSTATE=dict(i.attrs)['value']
    ##    for i in soup.findAll('input',{'name':'__EVENTVALIDATION'}):
    ##        EVENTVALIDATION=dict(i.attrs)['value']
    ##    postdata=urllib.urlencode({
    ##        'gridModule$ctl03$radioButton':'radioButton',
    ##        '__EVENTVALIDATION':EVENTVALIDATION,
    ##        '__VIEWSTATE':VIEWSTATE,
    ##        '__EVENTTARGET':'gridModule$ctl03$radioButton'
    ##        })
    ##    req=urllib2.Request(url = 'http://electsys.sjtu.edu.cn/edu/student/elect/speltyRequiredCourse.aspx',data = postdata)
    ##    resp=urllib2.urlopen(req)


    while True:
        ct = urllib.request.urlopen('http://electsys.sjtu.edu.cn/edu/student/elect/speltyRequiredCourse.aspx',
                                    timeout=5).read()
        soup = BeautifulSoup(ct)
        for i in soup.findAll('input', {'name': '__VIEWSTATE'}):
            VIEWSTATE = dict(i.attrs)['value']
        for i in soup.findAll('input', {'name': '__EVENTVALIDATION'}):
            EVENTVALIDATION = dict(i.attrs)['value']
        postdata = urllib.parse.urlencode({
            'myradiogroup': classID,
            'SpeltyRequiredCourse1$lessonArrange': '课程安排',
            '__EVENTVALIDATION': EVENTVALIDATION,
            '__VIEWSTATE': VIEWSTATE
        })
        req = urllib.request.Request(url='http://electsys.sjtu.edu.cn/edu/student/elect/speltyRequiredCourse.aspx',
                                     data=postdata)
        resp = urllib.request.urlopen(req)
        soup = BeautifulSoup(resp.read(), 'lxml')
        for i in soup.findAll('tr', {'class': "tdcolour1"}):
            if "未" in str(i) and keyword in str(i):
                print(i)
        for i in soup.findAll('tr', {'class': "tdcolour2"}):
            if "未" in str(i) and keyword in str(i):
                print(i)
        print(times, " ", end=' ')
        times += 1
        time.sleep(35)


##try:    
##    Tieba()
##except:
##    pass

Tongqu_JWC()
##try:
##    smith()
##except Exception,e:
##    print e


##electsys(studentid,pwd,'PE004','游泳')
