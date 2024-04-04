import tensorflow as tf
import torch
print(tf.__version__)
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # '0'은 첫 번째 GPU를 의미합니다.
gpus = tf.config.list_physical_devices('GPU')
print("TensorFlow 버전:", tf.__version__)
print("GPU 사용 가능 여부:", tf.test.is_gpu_available(cuda_only=True, min_cuda_compute_capability=None))
print("설치된 GPU 디바이스:", tf.config.list_physical_devices('GPU'))
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Available GPUs: {[gpu.name for gpu in gpus]}")
    except RuntimeError as e:
        print(e)
else:
    print("TensorFlow GPU 사용 불가능")
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # TensorFlow가 필요한 만큼 GPU 메모리를 점진적으로 할당하도록 설정
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
print("TensorFlow 버전:", tf.__version__)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print("GPU 사용 가능 여부: True")
    for gpu in gpus:
        print("설치된 GPU 디바이스:", gpu)
else:
    print("GPU 사용 가능 여부: False")

def test_tensorflow_gpu():
    # TensorFlow GPU 사용 여부 확인
    gpu_devices = tf.config.list_physical_devices('GPU')
    if gpu_devices:
        print("TensorFlow GPU 사용 가능")
        for gpu in gpu_devices:
            print("GPU 이름:", gpu.name)
    else:
        print("TensorFlow GPU 사용 불가능")

if __name__ == "__main__":
    print("TensorFlow GPU 테스트")
    test_tensorflow_gpu()


def test_pytorch_gpu():
    # PyTorch GPU 사용 여부 확인
    if torch.cuda.is_available():
        print("PyTorch GPU 사용 가능")
        # GPU 장치 정보 출력
        device = torch.cuda.get_device_name(0)
        print("GPU 이름:", device)
    else:
        print("PyTorch GPU 사용 불가능")

if __name__ == "__main__":
    print("TensorFlow GPU 테스트")
    test_tensorflow_gpu()
    
    print("\nPyTorch GPU 테스트")
    test_pytorch_gpu()
