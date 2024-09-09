**The Project is used To Extract Raw Data From a QR Code & Generate an TOTP From Secret Code Entered Via The Keyboard.**

How To Use
```
# QR Code Decoder and OTP Generator
2fa_decoder [-h] {decode,otp} INPUT
```
| Arguments       | Description                             |
|---------------|-----------------------------------------|
| `decode`      | Decode QR Code With `<INPUT>` - "Path To QR Code" |
| `otp`         | Generate OTP From Secret Code           |
| `-h, --help`  | Show This Help Message and Exit         |

<p><strong><span style="color:red; text-decoration:underline;">Note</span></strong>: The Secret Code Here Only Accepts Strings Encoded In Base32 Format. Other Encoding Formats Like Base64, Hex, or Bytes are Not Yet Supported By This Project (Base32 Only Contains The Characters A-Z And 2-7, Without Characters Like 1, 8, 9, 0, Or Other Special Characters).</p>

Example
| Command	    | Output 		|
| :-------------: |:-------------:|
| # 2fa_decoder decode C:\Users\Test\QR-Code.png	| This-Is-Raw-Data-From-QR-Code
| # 2fa_decoder otp 1233214566547899870				| 123456