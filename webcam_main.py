import cv2
from yolo import run_yolo_on_frame

def run_webcam_stream():
    cap = cv2.VideoCapture(0)  # 웹캠 기본 장치 열기

    if not cap.isOpened():
        print("❌ 웹캠을 열 수 없습니다.")
        return

    print("✅ 웹캠 스트리밍 시작... 'q'를 누르면 종료됩니다.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 프레임을 읽을 수 없습니다.")
            break

        run_yolo_on_frame(frame)  # YOLO 탐지 수행

        # 실시간 프레임 보기 (imshow 여기서도 가능)
        cv2.imshow("Webcam YOLO", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_stream()
