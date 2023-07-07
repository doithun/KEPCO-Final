testapp/hr_viton 폴더 용량이 커서 GitHub에 올라가지 않아서.. 제외시키고 GitHub에 올렸습니다.

[ 가상 환경 세팅하기 ]
: hr_viton이 작업 폴더 안에 있는 상태에서 
hr_viton/preprocessing/env_viton.yaml 으로 가상환경 불러오기.

[ 가상 환경 env_viton에 추가로 설치해야 할 것 ]
- torch==1.8.2+cu111
설치하는 방법: 아나콘다 프롬프트에 다음을 붙여 넣어서 실행 (노션)
pip install torch==1.8.2+cu111 torchvision==0.9.2+cu111 torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

- django==4.0.1

- cx_Oracle

- detectron2

- torchgeometry==0.1.2