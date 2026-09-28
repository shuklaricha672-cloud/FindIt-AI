from ultralytics import YOLO

# AI model
model = YOLO("yolo26n.pt")


def detect_objects(image):
    """
    Detect objects from uploaded image.
    """

    results = model(image)

    detected_objects = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            object_name = result.names[class_id]

            detected_objects.append({
                "name": object_name,
                "confidence": round(confidence * 100, 2)
            })

    return detected_objects