# Guide: Setting up an OpenVPN connection on a Jetson Nano

## Pre-Setup: Create an OpenVPN Certificate
1. Follow the instructions on the IT Services portal of Esslingen University:
   [Intranet page for VPN setup](https://intranetportal.hs-esslingen.de/meine-hochschule/hochschul-services/rechenzentrum/zugang-zum-hochschulnetz-mobile-net-netzlaufwerke)

2. Copy the following files from your personal OpenVPN-HE folder (e.g., C:\Users\vnnnnn\OpenVPN-HE) to a USB stick:

   - he-ca.txt
   - cert.txt
   - key.txt

## Installation on the Jetson Nano

### Connect Jetson Nano Orin to Wi-Fi

1. Start the Jetson Nano Orin and connect to Wi-Fi.
2. Under **Applications / Settings / Date & Time** (at the bottom of the list), adjust the current date and time.
3. Go to **Applications / Settings / Wi-Fi**, switch on Wi-Fi, and select the WLAN network (e.g., VPN/WEB).

### VPN Setup

1. Open **Applications / Settings / Network**.
2. Click the "+" button to add a new OpenVPN connection.
3. In the **Add VPN** window, select the first option: **OpenVPN (Compatible with OpenVPN Server)**.
4. In the new window under the **Identity** tab, enter the following information:

**Name:** Enter a name of your choice for the connection.

**General:**

- **Gateway:**
   - For employees of Esslingen University: `openvpn-mia.hs-esslingen.de`
   - For students of Esslingen University: `openvpn.hs-esslingen.de`

**Authentication:**

| Setting              | Value                                               |
|----------------------|-----------------------------------------------------|
| **Type:**            | Password with Certificates (TLS)                    |
| **Username:**        | Your university account (e.g., Max Schmidt = mschmidt) |
| **Password:**        | Your university account password                    |
| **CA certificate:**  | Copy `he-ca.txt` from the USB stick                 |
| **User certificate:**| Copy `cert.txt` from the USB stick                  |
| **User private key:**| Copy `key.txt` from the USB stick                   |
| **User key password:**| Your university account password                   |

> **Warning:**
    > Do not save your university account password.
    > Delete the VPN configuration after the workshop.

5. Click **Add** (top right) to confirm the setup.
6. Switch on the OpenVPN connection you just created to activate it.