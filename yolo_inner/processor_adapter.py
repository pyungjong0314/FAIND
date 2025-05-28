from library_processor import run_inference, get_lost_objects_json, cap


def process_frame(frame):
    """
    WebSocket이나 외부 입력 프레임이 들어올 때 호출되는 함수
    """
    run_inference(frame)


def get_lost_json():
    """
    현재까지 누적된 분실 아이템 목록을 JSON 문자열로 반환
    """
    return get_lost_objects_json()


def run_test_video():
    """
    고정 영상을 사용하여 추론을 수행하는 테스트 함수
    """
    fps = cap.get(5)  # CAP_PROP_FPS
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        run_inference(frame)

        # ESC or Q 키로 종료
        import cv2
        cv2.imshow("YOLO Inner Test", frame)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
