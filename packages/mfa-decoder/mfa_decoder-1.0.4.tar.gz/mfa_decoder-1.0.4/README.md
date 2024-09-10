**The Project is Used To Extract Raw Data From a QR Code & Generate a TOTP From Secret Code Entered Via The Keyboard.**

**How To Use**
```
# QR Code Decoder and OTP Generator
mfa_decoder [-h] {decode,otp} INPUT
```
| Arguments       | Description                             |
|---------------|-----------------------------------------|
| `decode`      | Decode QR Code With `<INPUT>` - "Path To QR Code" |
| `otp`         | Generate OTP From Secret Code (Base32 Format)           |
| `-h, --help`  | Show This Help Message and Exit         |

**Note**: The Secret Code Here Only Accepts Strings Encoded In Base32 Format. Other Encoding Formats Like Base64, Hex, or Bytes are Not Yet Supported By This Project (Base32 Only Contains The Characters A-Z And 2-7, Without Characters Like 1, 8, 9, 0, Or Other Special Characters).

**Example**
| Command	    | Output 		|
| :-------------: |:-------------:|
| # mfa_decoder decode C:\Users\Test\QR-Code.png	| This-Is-Raw-Data-From-QR-Code
| # mfa_decoder otp 1233214566547899870				| Invalid Base32 Format
| # mfa_decoder otp 3O2QUFEKB4O7PF3FEVC				| 123456
