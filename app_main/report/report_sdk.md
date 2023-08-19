# ����˵��
��sdk�ṩ�����������ݲɼ��Ĺ��ܣ��û�������������˴����������sdk�����з��������Ϣ��Զ���ϱ��������ϱ����ݰ�����
+ �ӿ�url 
+ �������ͣ�ͬ��/�첽�� 
+ ��Ӧ״̬�루200/500��
+ �������
+ ���ؽ��
+ ���ؽ���Ƿ���ȷ  

# ���벽��
#### ��1����������ϵƽ̨����Ա��wangyanjiao@chinamobile.com/kangkailun@chinamobile.com���������

#### ��2���������������ܻ�ƽ̨��SDK���ġ�ҳ�棬�ҵ����������ݲɼ���sdk��Ŀǰ�ṩ��Python��Java
�����汾���˴�ѡ��Python�汾��������
![img.png](img.png)
#### ��3���������ص�zipѹ�������н�ѹ�� ����ѹ���report�ļ��зŵ����������Ŀ¼��

#### ��4��������������������sdkģ�飬�������£���ȷ��Python�汾��3.6���ϣ�
```python
from report.collector import ReportCollector
from report import report_service
```
#### ��5���������������õľ������
```python
collector = ReportCollector.url('/your/path') #�����ʼ��
#�ӿ���κͳ���
collector.single_param('name', 'value').single_param('name2', 'value2')\ 
.multi_param({'name3': 'value3'})\ 
.file_param('file1', file_obj)\
.output_data({'resp':'success'})
#͸������ͷ�е�������Ϣ
collector.header_param('��http����ͷ��ȡ��')
#����ӿڵ���״̬�ͽ��
collector.response_code(200).is_success(True)
```

#### ��6���������ϱ��ӿڽ��з�����Ϣ�ϱ�
```python
report_service.report(collector)
```

# ����˵��

|<div style="width:100px">����</div>| <div style="width:100px">����</div> |<div style="width:400px">����˵��</div>|
|:---:|:---:|:---:|
|url|str|�ӿ�����·��|
|header_param|str|��Http����ͷȡ��'ability_invoking_param'��Ӧ��ֵ|
|is_async|bool|�Ƿ����첽�ӿڣ�Ĭ����False|
|single_param|str|��Ӳ������ƺͲ���ֵ�����������Ҫ��ε��ô˷���|
|multi_param|dict|�����в���������ֵ����ʹ���|
|file_param|file|��Ӳ������ƺ��ļ����󣬶���ļ���Ҫ��ε��ô˷���|
|output_data|dict|�ӿڷ��ؽ��|
|response_code|int|�ӿ���Ӧ״̬�룬�ɹ�:200 �����쳣:500|
|is_success|bool|���ؽ���Ƿ���ȷ��Ĭ��ΪNone|



# ʾ������
```python
import json

from flask import Flask, request
from report.collector import ReportCollector
from report import report_service
import random

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    return 'hello my flask'


# Get �����ȡ Parameter ʾ������
@app.route('/getArg', methods=['GET'])
def test_get():
    name = request.args.get('name', '')
    score = request.args.get('score', '50')
    param = ReportCollector.url('/getArg', True) \
        .header_param(request.headers.get('ability_invoking_param')) \
        .single_param('name', name).single_param('score', score)
    try:
        seed = random.random()
        print('seed: ' + str(seed))
        param.is_success(True).response_code(200)
    except Exception as ex:
        param.is_success(False).response_code(500)
        print("ex= ", ex)
    finally:
        param.output_data({"name": name})
        report_service.report(param)
    print(param.__dict__)
    return {"msg": name}, 200, {"Content-Type": "application/json"}


# Post �����ȡ data-form �� x-www-form-urlencoded ʾ������
@app.route('/postForm', methods=['POST'])
def test_form():
    param = ReportCollector.url('/postForm', True).header_param(request.headers.get('ability_invoking_param'))
    try:
        # biz start
        print(request.form)
        seed = random.random()
        print('seed: ' + str(seed))

        for key in request.form:
            param.single_param(key, request.form[key])
        # biz end
        param.is_success(True).response_code(200)
        param.output_data('{"msg": "suc"}')
    except Exception as ex:
        print(ex)
        param.is_success(False).response_code(500)
    finally:
        report_service.report(param)
        print(param.__dict__)
    file_name = ''
    return json.dumps({
        "form": request.form,
    }), 200, {"Content-Type": "application/json"}


# Post �����ϴ��ļ�ʾ������
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    param = ReportCollector.url('/postForm', True).header_param(request.headers.get('ability_invoking_param'))
    if len(request.files) > 0:
        file_ = request.files['file']
        try:
            # biz start
            seed = random.random()
            print('seed: ' + str(seed))
            # ���� request ���ļ����޷��ظ���ȡ��Ϊ�˲�Ӱ��ҵ�񣬽����Ƚ��ļ������ڱ��أ��ٴ��� collector
            file_.save('tmp/' + file_.filename)
            param.file_param('file', open('tmp/' + file_.filename, mode='rb'))
            # biz end
            param.is_success(True).response_code(200)
            param.output_data('{"msg": "suc"}')
        except Exception as ex:
            print(ex)
            param.is_success(False).response_code(500)
        finally:
            report_service.report(param)
            print(param.__dict__)
        file_name = ''
        if len(request.files) > 0:
            file_name = file_.filename
        return json.dumps({
            "file": file_name
        }), 200, {"Content-Type": "application/json"}
    else:
        return "file not found", 500


# Post �����ȡ data-raw ʾ������
@app.route('/postRequestBody', methods=['GET', 'POST'])
def test_request_body():
    param = ReportCollector.url('/postRequestBody', True).header_param(
        request.headers.get('ability_invoking_param')).multi_param(request.get_json())
    try:
        # biz start
        print(request.get_json())
        seed = random.random()
        print('seed: ' + str(seed))
        param.is_success(True).response_code(200).output_data(request.get_json())
    except Exception:
        param.is_success(False).response_code(500)
    finally:
        report_service.report(param)
    print(param.__dict__)
    # biz end
    return request.get_json(), 200, {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(port=8080)
```

# ע������
1. һ������������һ��report�����ϱ���Ϣ�������ظ�����
2. �¾������߲��������ϵ����Ա���й�����֤