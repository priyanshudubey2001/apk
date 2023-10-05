from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import cv2
import os

os.system('cls')

def resize_image(image, width=800, height=600):
    return cv2.resize(image, (width, height))

def compare_images(target_image, reference_data):
    target_image = resize_image(target_image)
    best_match = None
    best_similarity = float('inf')

    for ref_image, name in reference_data:
        ref_image = resize_image(ref_image)
        difference = cv2.absdiff(target_image, ref_image)
        gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        similarity = cv2.mean(gray_difference)[0]

        if similarity < best_similarity:
            best_similarity = similarity
            best_match = (ref_image, name)

    return best_match

class Test(MDApp):
    reference_data = [
    (cv2.imread("1.jpg"), "Orion"),
    (cv2.imread("2.jpg"), "Cassiopeia"),
    (cv2.imread("3.jpg"), "Big Dipper")
]

    def build(self):
        self.title = 'StjerneInfo'
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(
            '''
BoxLayout:
    orientation: 'vertical'
    MDTopAppBar:
        title: 'StjerneInfo'
        md_bg_color: app.theme_cls.primary_color
        specific_text_color: 1, 1, 1, 1

    MDBottomNavigation:
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Camera'
            icon: 'camera'
            BoxLayout:
                orientation: 'vertical'
                Image:
                    id: imageView
                    source: 'camera.png'
                Button:
                    text: 'Capture Image'
                    on_release: app.capture_image()

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Profile'
            icon: 'account'
            Image:
                id: imageView
                source: 'profile.png'

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Settings'
            icon: 'apps'
            Image:
                id: imageView
                source: 'settings.png'
'''
        )

    def capture_image(self):
        cap = cv2.VideoCapture(0)

        message = "Hit spacebar to capture an image \n Press Esc to exit"

        while True:
            bool, frame = cap.read()

            frame = cv2.flip(frame, 1)

            cv2.putText(frame, message, (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Webcam", frame)

            key = cv2.waitKey(1)
            if key == ord(' '):
                best_match = compare_images(frame, self.reference_data)

                if best_match is not None:
                    matched_name = best_match[1]
                    print(f"Matched image: {matched_name}")
                    cv2.imshow(f"Matched Image - {matched_name}", best_match[0])
                break

            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

Test().run()
