#Login Page
Login_Username=(
    "//input[@name='username']",
    "input[placeholder=''][name='username']",
    ""
)

Login_Password= (
    "//input[@name='password']",
    "input[placeholder=''][name='password']",
    ""
)
Login_LoginBtn= (
    "//button[normalize-space()='LOGIN']",
    "button[type='submit']",
    "")

DefaultLogin_AdminPass=(
    "//input[@name='adminPassword']",
    "input[placeholder=''][name='adminPassword']",
    ""
)
DefaultLogin_CnfAdminPass=(
    "//input[@name='confirmAdminPassword']",
    "input[placeholder=''][name='confirmAdminPassword']",
    ""
)
DefaultLogin_GuestPass=(
    "//input[@name='guestPassword']",
    "input[placeholder=''][name='guestPassword']",
    ""
)
DefaultLogin_CnfGuestPass=("//input[@name='confirmGuestPassword']",
                           "input[placeholder=''][name='confirmGuestPassword']",
                           ""
                           )

DefaultLogin_UpdateBtn=(
    "//button[normalize-space()='Update']",
    "button[type='submit']",
    ""
)

#Device Information

WanInfo_MacAddress=(
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[2]/form[1]/div[1]/div[1]/div[3]/div[1]/div[2]",
    "div div div:nth-child(2) form:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(3) div:nth-child(1) div:nth-child(2)"
    ""
)
WanInfo_IPv6=(
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[2]/form[1]/div[1]/div[1]/div[3]/div[3]/div[2]",
    "div div div:nth-child(2) form:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(3) div:nth-child(3) div:nth-child(2)",
    ""
)


#Device Status
SysInfo_FirmwareVersion = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]",
    "body > mainapp:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"
)
SysInfo_SerialNumber = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[1]/div[1]/div[3]/div[5]/div[2]/div[1]",
    "body > mainapp:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(1)"
)
SysInfo_ModelName = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[1]/div[1]/div[3]/div[7]/div[2]",
    "body > mainapp:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(7) > div:nth-child(2)"
)


#Lan Iformation
LANInfo_MACAddress = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]",
    "body mainapp div div div div div:nth-child(2) div:nth-child(1) div:nth-child(3) div:nth-child(3) div:nth-child(2)"
)
LANInfo_IPv4Address = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[3]/div[3]/div[2]",
    "body mainapp div div div div div:nth-child(2) div:nth-child(1) div:nth-child(3) div:nth-child(3) div:nth-child(2)"
)
LANInfo_IPv6Address = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[3]/div[5]/div[2]",
    "body mainapp div div div div div:nth-child(2) div:nth-child(1) div:nth-child(3) div:nth-child(3) div:nth-child(2)"
)

LANInfo_IPv4DHCPServer = (
    "/html[1]/body[1]/mainapp[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[3]/div[7]/div[2]/div[1]",
    "body > mainapp:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(7) > div:nth-child(2) > div:nth-child(1)"
)






