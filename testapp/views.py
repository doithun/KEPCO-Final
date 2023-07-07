from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from base64 import b64decode
import testapp.model_db.USER_.USER_ as mem
from testapp.model_db.file_util.file_util import File_Util
import testapp.model_db.photosave.photosave as photosave
import time
import os
import cx_Oracle as ora
import shutil




import subprocess


def getBase(request) : 
    return render(request,
                    "testapp/base.html",
                        {})


def index(request):
    
    return render(request,
                  "testapp/index/index.html",
                  {})
    
    
def video(request):
    
    return render(request,
                  "INFO/INFO.html",
                  {})

def memcreate(request):
    return render(request,
                  "testapp/login/mem_create.html")

    
##로그인
def MemberInsert(request):
    
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
    
    rs = mem.setMemberInsert(mem_id, mem_pass, mem_name, mem_email )

    if mem_id == '' :
        msg="""
            <script type='text/javascript'>
                alert('아이디는 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 
    
    if mem_pass == '':
        msg="""
            <script type='text/javascript'>
                alert('비밀번호는 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """        
        return HttpResponse(msg) 
    
    if mem_name == '':
        msg="""
            <script type='text/javascript'>
                alert('이름은 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """    
        return HttpResponse(msg) 

    if mem_email == '':
        msg="""
            <script type='text/javascript'>
                alert('이메일은 필수입력사항 입니다.');
                history.go(-1);
            </script>
        """               
        return HttpResponse(msg)        
    
    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('아이디 비밀번호를 확인하세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
        
        
    msg="""
        <script type='text/javascript'>
            alert('회원가입이 완료되었습니다.');
            location.href='/login_logout/';
        </script>
    """
    return HttpResponse(msg)

def getdelete(request):
    return render(request,
                "testapp/login/mem_delete.html")

def MemberDelete(request):
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
        
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
        
    
    rs = mem.setMemberDelete(mem_id, mem_pass, mem_name, mem_email )
    
    
    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('없는 계정입니다');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
        
    msg="""
        <script type='text/javascript'>
            alert('회원탈퇴가 완료되었습니다.');
            location.href='/test/login_logout/';
        </script>
    """
    return HttpResponse(msg)

def MemberUpdate(request):
    if request.method == "POST" :
        mem_id =request.POST["mem_id"]
        mem_pass =request.POST["mem_pass"]
        mem_name=request.POST["mem_name"]
        mem_email=request.POST["mem_email"]
        
    elif request.method == "GET" :
        mem_id =request.GET["mem_id"]
        mem_pass =request.GET["mem_pass"]
        mem_name=request.GET["mem_name"]
        mem_email=request.GET["mem_email"]
        
    if mem_pass == '' :
        msg="""
            <script type='text/javascript'>
                alert('변경하실 비밀번호를 입력 해주세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 

    if mem_email == '' :
        msg="""
            <script type='text/javascript'>
                alert('변경하실 이메일 주소를 입력 해주세요.');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg) 
    
    rs,sql = mem.setMemberUpdate(mem_id, mem_pass, mem_name, mem_email )

    if rs=='no':
        msg="""
            <script type='text/javascript'>
                alert('오류입니다');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
        
    msg="""
        <script type='text/javascript'>
            alert('회원정보가 저장되었습니다.');
            location.href ='/index/';
        </script>
    """
    return HttpResponse(msg)

################################################################################################

def login_logout(request):
    return render(request,
                "testapp/login/login_logout.html",
                {})
    
def login(request):
    try :
        if request.method == "POST" :
            mem_id = request.POST["mem_id"]
            mem_pass = request.POST["mem_pass"]
                    
        elif request.method == "GET" :        
            mem_id = request.GET["mem_id"]
            mem_pass = request.GET["mem_pass"]
            
    except :
        url = "/login_logout/"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    ## DB
    dict_col = mem.getLogin(mem_id, mem_pass)
# return HttpResponse(dict_col["rs"])
    # return HttpResponse(mem_pass)
    
    ### 성공여부
    if dict_col["rs"] == "no" :
        msg="""
            <script type="text/javascript">
                alert('아이디 또는 비밀번호가 일치하지 않습니다.');
                history.go(-1);
            </script>
        """
        
        return HttpResponse(msg)
        
    request.session["ses_mem_id"]=mem_id
    request.session["ses_mem_name"] = dict_col["mem_name"]
    
    return render(request,
                "testapp/index/index.html",
                    {})
    
def logout(request):
    if request.session.get("ses_mem_id"):
        ### 세션 정보 비우기
        request.session.flush()
        
        msg="""
            <script type='text/javascript'>
                alert('로그아웃 되었습니다.');
                location.href ='/index/';
            </script>
        """
    else :
        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요!!!');
                location.href ='/index/';
            </script>
        """
    return HttpResponse(msg)

def mypage(request):
    try :
        dict_col = mem.getmypage(request.session["ses_mem_id"])
                
    except :
        url = "/login_logout/"

        msg="""
            <script type='text/javascript'>
                alert('잘못된 접근입니다. 로그인하세요');
                location.href ='{}';
            </script>
        """.format(url) 

        return HttpResponse(msg)
    
    return render(request,
            "testapp/login/mem_my.html",
            {"dict_col":dict_col})

##############################################################################
def getPhoto() : 
    url = "/test/index/"
    
    msg = """
    <script type='text/javascript'>
        alert('접수 되었습니다!');
        location.href = '{}';
    </script>
        """.format(url)  
        
    return HttpResponse(msg)




def getPhoto_save(request) :
    
        try:
            if request.FILES['mem_photo'] :
                popfile = request.FILES['mem_photo']
                
            if request.FILES['clt_photo']:
                cltfile = request.FILES['clt_photo']
        except:
            msg = """
                    <script type='text/javascript'>
                        alert('잘못된 접근입니다. 다시 입력하세요!');
                        location.href = '/test/index/'
                    </script>
            """
            return HttpResponse(msg)
        ############################################
        #############[파일 업로드 처리]###############
        ### 모델파일 업로드 폴더 위치 지정
        upload_dir = "./testapp/hr_viton/data/model_org/"
        ### 모델파일 다운로드 폴더 위치 지정
        down_dir = "/hr_viton/data/model_org/"
        
        upload_dir1 = "./testapp/hr_viton/data/cloth"
        down_dir1 = "/hr_viton/data/cloth/"
        
        ### 인물파일 처리
        fu = File_Util()
        fu.setUpload(popfile, upload_dir, down_dir)
        fu.fileUpload()
        
        ## 옷파일 처리
        fu1 = File_Util()
        fu1.setUpload(cltfile, upload_dir1, down_dir1)
        fu1.fileUpload()
        
        
        
        ### 파일사이즈
        file_size = fu.file_size
        
        ### 다운로드 파일명(경로 + 파일명) 
        file_full_name = fu.file_full_name
        file_full_name1 = fu1.file_full_name
        ### 다운로드를 위해 DB의 파일명만 추출하기
        # /static/nonmodelapp/file_manager/dog01_aU2bFG7.jpg을 
        # "/" 기호로 split한 후 마지막 위치의 index번호 값 추출
        filename = file_full_name.split("/")[-1]
        filename1 = file_full_name1.split("/")[-1]
        
        ### 다운로드를 위한 파일명(전체경로 + 파일명)
        downFullName = "/hr_viton/data/model_org/"+filename
        downFullName1 = "/hr_viton/data/cloth/"+filename1
        ### 테이블에 입력 시 아래처럼 파일명 처리
        # 사용하시는 테이블 내에 컬럼명이 downFullName 이라고 한다면...
        # "Insert into 테이블명 (컬럼명1, 컬럼명2, downFullName) 
        #     values({}, {}, '{}')".format(값1, 값2, downFullName) 
        ######################################### 

        try:
                ### 사용자가 입력한 값들 추출하기
                ### get 방식 처리
            #if request.method == "GET" :
                    #mem_photo = request.GET.get("mem_photo","") 
                    #mem_crp = request.GET.get("mem_crp","")  
                    

            ### post 방식 처리
           #elif request.method == "POST" :
                    #mem_photo = request.POST.get("mem_photo","") 
                    #mem_crp = request.POST.get("mem_crp","")  

            data = {
                    'f_mem_id' : request.session["ses_mem_id"],
                    'popfile' : downFullName, 
                    'cltfile' : downFullName1
                    }
            
                
            
            # return HttpResponse(data["f_mem_id"])
            # return HttpResponse(data["popfile"])
            photosave.get_Photo(data)
            
                # return HttpResponse(data["processstate"])
                # return HttpResponse(data["happendt"])
                # return HttpResponse(data["happenplace"])
                # return HttpResponse(data["kindcd"])
                # return HttpResponse(data["colorcd"])
                # return HttpResponse(data["age"])
                # return HttpResponse(data["sexcd"])
                # return HttpResponse(data["neuteryn"])
                # return HttpResponse(data["specialmark"])
                                            
        except:
                msg = """
                        <script type='text/javascript'>
                                alert('저장중 에러가 발생하였습니다!');
                                history.go(-1);
                        </script>
                """
                return HttpResponse(msg)
            
        ### 저장 잘되었다는 창 띄우고,
        #   - 원래 페이지로 가기..
        url = "/index/"
    
        msg = """
        <script type='text/javascript'>
            alert('저장 되었습니다!!!');
            location.href = '{}';
        </script>
        """.format(url)  
        
        return HttpResponse(msg)
    


def getcreate(request):
    query = """SELECT MEM_PHOTO, CLT_PHOTO FROM PHOTO WHERE TO_NUMBER(REQ_NO) = (SELECT MAX(TO_NUMBER(REQ_NO)) FROM PHOTO)"""
    dsn = ora.makedsn("localhost", 1521, "xe")
    conn = ora.connect("ctp", "dbdb", dsn)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.join(base_dir, "testapp", "hr_viton"))

    command = ["python", "preprocess_model.py", "-model", os.path.basename(data[0])]
    subprocess.run(command, shell=True)
    command = ["python", "preprocess_cloth.py", "-cloth", os.path.basename(data[1])]
    subprocess.run(command, shell=True)
    command = ["python", "synth.py", "-model", os.path.basename(data[0]), "-cloth", os.path.basename(data[1])]
    subprocess.run(command, shell=True)

    output_folder_path = os.path.abspath(os.path.join(base_dir, "testapp", "static", "testapp", "file_manager"))
    while True:
        files = os.listdir(output_folder_path)
        if files:
            files.sort(key=lambda x: os.path.getctime(os.path.join(output_folder_path, x)), reverse=True)
            latest_file = files[0]
            output_file_path = os.path.join(output_folder_path, latest_file)
            break
        else:
            time.sleep(1)  # 1초 대기 후 다시 확인

    image_path = output_file_path  # 이미지 파일의 전체 경로를 저장

    context = {
        'image_path': image_path  # 이미지 파일의 전체 경로를 전달
    }

    return render(request, 'testapp/index/index.html', context)


    
    
def getoutput(request):
    return render(request,
                  'testapp/index/output.html',
                  {})



