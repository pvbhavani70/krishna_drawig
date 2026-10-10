import cv2
import numpy as np
import ctypes




img = cv2.imread("krishna.jpg")

if img is None:
    print("Image not found! Please check 'krishna.jpg'")
    exit()




user32 = ctypes.windll.user32

screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

print("Screen Width:", screen_width)
print("Screen Height:", screen_height)




original_height, original_width = img.shape[:2]

scale = min(
    screen_width / original_width,
    screen_height / original_height
)

new_width = int(original_width * scale)
new_height = int(original_height * scale)

img = cv2.resize(img, (new_width, new_height))

height, width = img.shape[:2]




canvas_img = np.zeros(
    (screen_height, screen_width, 3),
    dtype=np.uint8
)

x_offset = (screen_width - width) // 2
y_offset = (screen_height - height) // 2

canvas_img[
    y_offset:y_offset + height,
    x_offset:x_offset + width
] = img




window_name = "Krishna Neon Art Animation"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

cv2.setWindowProperty(
    window_name,
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)




gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(
    gray, 20, 255, cv2.THRESH_BINARY
)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_NONE
)

all_points = []

for cnt in contours:
    for pt in cnt:
        x, y = pt[0]
        all_points.append((x, y))



canvas = np.zeros(
    (screen_height, screen_width, 3),
    dtype=np.uint8
)

speed = 25

for i in range(0, len(all_points), speed):

    batch = all_points[i:i + speed]

    for x, y in batch:

        screen_x = x + x_offset
        screen_y = y + y_offset

        color = [int(c) for c in img[y, x]]

        cv2.circle(
            canvas,
            (screen_x, screen_y),
            1,
            color,
            -1
        )

    glow = cv2.GaussianBlur(canvas, (15, 15), 0)

    frame = cv2.addWeighted(
        canvas, 1.2,
        glow, 1.4,
        0
    )

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit()



center = (screen_width // 2, screen_height // 2)

for angle in range(0, 360, 6):

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    rotated = cv2.warpAffine(
        canvas_img,
        rotation_matrix,
        (screen_width, screen_height),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0)
    )

    glow = cv2.GaussianBlur(rotated, (15, 15), 0)

    frame = cv2.addWeighted(
        rotated, 1.1,
        glow, 1.2,
        0
    )

    cv2.imshow(window_name, frame)

    if cv2.waitKey(15) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit()



for _ in range(3):

    # Zoom in
    for scale in np.linspace(1.0, 1.15, 20):

        matrix = cv2.getRotationMatrix2D(
            center,
            0,
            scale
        )

        zoomed = cv2.warpAffine(
            canvas_img,
            matrix,
            (screen_width, screen_height),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )

        glow = cv2.GaussianBlur(zoomed, (25, 25), 0)

        frame = cv2.addWeighted(
            zoomed, 1.2,
            glow, 1.5,
            0
        )

        cv2.imshow(window_name, frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()

    # Zoom out
    for scale in np.linspace(1.15, 1.0, 20):

        matrix = cv2.getRotationMatrix2D(
            center,
            0,
            scale
        )

        zoomed = cv2.warpAffine(
            canvas_img,
            matrix,
            (screen_width, screen_height),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )

        glow = cv2.GaussianBlur(zoomed, (15, 15), 0)

        frame = cv2.addWeighted(
            zoomed, 1.2,
            glow, 1.0,
            0
        )

        cv2.imshow(window_name, frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()


final_glow = cv2.GaussianBlur(canvas_img, (15, 15), 0)

final_frame = cv2.addWeighted(
    canvas_img, 1.2,
    final_glow, 1.2,
    0
)

cv2.imshow(window_name, final_frame)

cv2.waitKey(0)

cv2.destroyAllWindows()