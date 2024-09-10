import cv2
import pyzbar.pyzbar as pyzbar
import pyotp
import argparse
import base64  # The Library For Checking Base32 Format

class QRDecoder:
    def __init__(self, image_path):
        self.image_path = image_path

    def decode_qr(self):
        gray = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2GRAY)
        qr_codes = pyzbar.decode(gray)
        for qr_code in qr_codes:
            decoded_data = qr_code.data.decode("utf-8")
            print("Decoded QR Data:", decoded_data)
            return decoded_data
        print("No QR Code Found In The Image.")
        return None

class OTPGenerator:
    def __init__(self, secret):
        if self.is_valid_base32(secret):
            self.secret = secret
            self.otp = pyotp.TOTP(secret)
        else:
            raise ValueError("Invalid Secret Format. The Secret Must Be A Valid Base32 String.")

    def is_valid_base32(self, secret):
        try:
            base64.b32decode(secret, casefold=True)  # Check If The Secret Is A Valid Base32
            return True
        except base64.binascii.Error:
            return False

    def generate_code(self):
        return self.otp.now()

    def display_info(self):
        print("2FA Secret:", self.secret)
        print("2FA Code:", self.generate_code())

class TwoFactorAuthApp:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='QR Code Decoder & OTP Generator.')
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--image_path', type=str, help='Path To The Image Containing QR Code')
        group.add_argument('--secret', type=str, help='2FA Secret To Generate OTP')

    def run(self):
        args = self.parser.parse_args()

        if args.image_path:
            # Decode QR Code
            decoder = QRDecoder(args.image_path)
            decoder.decode_qr()
        elif args.secret:
            try:
                # Generate OTP
                generator = OTPGenerator(args.secret)
                generator.display_info()
            except ValueError as e:
                print("Error:", e)

def main():
    app = TwoFactorAuthApp()
    app.run()

if __name__ == "__main__":
    main()
