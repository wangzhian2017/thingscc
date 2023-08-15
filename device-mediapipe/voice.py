import pyaudio
import wave
import speech_recognition as sr
import time
from arm.feishu import feishu
from arm.mechanical_arm import mechanical_arm

base_url="http://localhost:8080"
product_id="iqDUVzCjyD"
device_name="esp32c3"
arm=mechanical_arm(base_url,product_id,device_name)

'''
    用Pyaudio库录制音频
    out_file:输出音频文件名
    rec_time:音频录制时间(秒)
'''
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    
    p = pyaudio.PyAudio()
    # 创建音频流 
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start Recording...")

    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording Done...")

    # 保存音频文件
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# '''
# 读取paudio录制好的音频文件,完成语音识别
#     afile:音频文件
#     afmt:音频文件格式(wav)
# pip install pocketsphinx 
# pip install speechrecognition
# 中文包https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Mandarin/
# 安装中文包路径 C:\Users\wangzhian\AppData\Roaming\Python\Python38\site-packages\speech_recognition\pocketsphinx-data\
# '''
def speech_recognition(fp, lang):
    r = sr.Recognizer()
    sudio = ""
    with sr.AudioFile(fp) as src:
        sudio = r.record(src)
    r = r.recognize_sphinx(sudio,language=lang)
    return r


def process(cmd): 
    if "抓住" in cmd:
        arm.grab(180.0)
    if "松开" in cmd:
        arm.grab(0.0)
    if "上" in cmd:
        arm.lift(180.0)
    if "下" in cmd:
        arm.lift(0.0)
    if "左" in cmd:
        arm.rotate(180.0)
    if "右" in cmd:
        arm.rotate(0.0)
    if "前" in cmd:
        arm.backforward(180.0)
    if "后" in cmd:
        arm.backforward(0.0)
    if "停" in cmd:
        arm.stop()

def main():
    print("voice control")
    fs=feishu()

    AUDIO_OUTPUT="output.wav"
    while(True):
        audio_record(AUDIO_OUTPUT, 3) # 录制语音指令
        result =  fs.speech_to_text(AUDIO_OUTPUT) # 识别语音指令
        if len(result) > 0:
            print(result)
            process(result)

if __name__ == '__main__':
    main()

