# BitSecurity-LFIFinder
<br>
Using This Powerfull Tool, You Can Automate Finding And Exploiting LFI Vulnerability<br>
| BitSecurity LFI Vulnerabillity Test<br>
| Writen By: Reza Sarvani<br>
| JoinUS ==> BitSecurityTeam<br>

<h3><b>Installation</b></h3>
First You Need To Clone The Repository:<br>
    >> apt-get install https://github.com/rezasarvani/BitSecurity-LFIFinder<br>
Then Install Prerequisites:<br>
    python3 -m pip install requests<br>
    python3 -m pip install regex<br>
    python3 -m pip install requests[socks]<br>
Get Ready To Use The Tool !<br>
<br>
<h3><b>Usage</h3></b><br>
Use "python3 BitLFI.py -h" For Information About Configurations That You Can Make
<br>
Options:<br>
  -h, --help:             show this help message and exit<br>
  -p PTYPE, --payloadtype=PTYPE: <br>
                        Windows Payload (1) | Linux Payloads (2) | Both (3)<br>
  -u TURL, --targeturl=TURL: <br>
                        Target URL To Test For LFI Vulnerabillity<br>
  -d DTIME, --delaytime=DTIME: <br>
                        How Much Delay Between Request (In Seconds)<br>
  -w WTIME, --wait=WTIME: <br>
                        After How Much Successfull Exploit You Want To Be
                        Asked Again For Continue<Br>
  -t TUSE, --tor=TUSE:    <br>Use Tor For Requests: (Y/N)<br>
  -a ATYPE, --attacktype=ATYPE: <br>
                        Which Type Of Payload You Want To Test Againt Your
                        Target:<br> 1) Absolute Path Bypass <br>2) Non-Recursively
                        Stripped <br>3) URL Encode <br>4) Double URL Encode <br>5) Null
                        Byte Injection <br>6) Null Byte Injection + Extension
                        Validation <br>7) Start Path Validation <br>8) Using 4096 Byte
                        Bypass Payload <br>9) All Bypass Methods<br>
    Required Options Are: -u And -p<br>
    <h3><b>Default Values</h3></b><br>
    Delay Time: 3 (Seconds)<br>
    WaitTime: After Discovering 10 Successful Payload<br>
    Attack Type: 8 (All Bypass Methods)<br>
    Tor Usage: n (No)<br>
