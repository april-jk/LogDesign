event_data = node.xpath("/Event/EventData/Data")
logintype = 0
username = "-"
domain = "-"
ipaddress = "-"
hostname = "-"
status = "-"
sid = "-"
authname = "-"
guid = "-"

###
# Detect admin users
#  EventID 4672: Special privileges assigned to new logon
###
if eventid == 4672:
    for data in event_data:
        if data.get("Name") in "SubjectUserName" and data.text is not None and not re.search(UCHECK, data.text):
            username = data.text.split("@")[0]
            if username[-1:] not in "$":
                username = username.lower() + "@"
            else:
                username = "-"
    if username not in admins and username != "-":
        admins.append(username)
###
# Detect removed user account and added user account.
#  EventID 4720: A user account was created
#  EventID 4726: A user account was deleted
###
elif eventid in [4720, 4726]:
    for data in event_data:
        if data.get("Name") in "TargetUserName" and data.text is not None and not re.search(UCHECK, data.text):
            username = data.text.split("@")[0]
            if username[-1:] not in "$":
                username = username.lower() + "@"
            else:
                username = "-"
    if eventid == 4720:
        addusers[username] = etime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        delusers[username] = etime.strftime("%Y-%m-%d %H:%M:%S")
###
# Detect Audit Policy Change
#  EventID 4719: System audit policy was changed
###
elif eventid == 4719:
    for data in event_data:
        if data.get("Name") in "SubjectUserName" and data.text is not None and not re.search(UCHECK, data.text):
            username = data.text.split("@")[0]
            if username[-1:] not in "$":
                username = username.lower() + "@"
            else:
                username = "-"
        if data.get("Name") in "CategoryId" and data.text is not None and re.search(r"\A%%\d{4}\Z", data.text):
            category = data.text
        if data.get("Name") in "SubcategoryGuid" and data.text is not None and re.search(r"\A{[\w\-]*}\Z", data.text):
            guid = data.text
    policylist.append([etime.strftime("%Y-%m-%d %H:%M:%S"), username, category, guid.lower(), int(stime.timestamp())])
###
# Detect added users from specific group
#  EventID 4728: A member was added to a security-enabled global group
#  EventID 4732: A member was added to a security-enabled local group
#  EventID 4756: A member was added to a security-enabled universal group
###
elif eventid in [4728, 4732, 4756]:
    for data in event_data:
        if data.get("Name") in "TargetUserName" and data.text is not None and not re.search(UCHECK, data.text):
            groupname = data.text
        elif data.get("Name") in "MemberSid" and data.text not in "-" and data.text is not None and re.search(
                r"\AS-[0-9\-]*\Z", data.text):
            usid = data.text
    addgroups[usid] = "AddGroup: " + groupname + "(" + etime.strftime("%Y-%m-%d %H:%M:%S") + ") "
###
# Detect removed users from specific group
#  EventID 4729: A member was removed from a security-enabled global group
#  EventID 4733: A member was removed from a security-enabled local group
#  EventID 4757: A member was removed from a security-enabled universal group
###
elif eventid in [4729, 4733, 4757]:
    for data in event_data:
        if data.get("Name") in "TargetUserName" and data.text is not None and not re.search(UCHECK, data.text):
            groupname = data.text
        elif data.get("Name") in "MemberSid" and data.text not in "-" and data.text is not None and re.search(
                r"\AS-[0-9\-]*\Z", data.text):
            usid = data.text
    removegroups[usid] = "RemoveGroup: " + groupname + "(" + etime.strftime("%Y-%m-%d %H:%M:%S") + ") "
###
# Detect DCSync
#  EventID 4662: An operation was performed on an object
###
elif eventid == 4662:
    for data in event_data:
        if data.get("Name") in "SubjectUserName" and data.text is not None and not re.search(UCHECK, data.text):
            username = data.text.split("@")[0]
            if username[-1:] not in "$":
                username = username.lower() + "@"
            else:
                username = "-"
        dcsync_count[username] = dcsync_count.get(username, 0) + 1
        if dcsync_count[username] == 3:
            dcsync[username] = etime.strftime("%Y-%m-%d %H:%M:%S")
            dcsync_count[username] = 0
###
# Detect DCShadow
#  EventID 5137: A directory service object was created
#  EventID 5141: A directory service object was deleted
###
elif eventid in [5137, 5141]:
    for data in event_data:
        if data.get("Name") in "SubjectUserName" and data.text is not None and not re.search(UCHECK, data.text):
            username = data.text.split("@")[0]
            if username[-1:] not in "$":
                username = username.lower() + "@"
            else:
                username = "-"
        if etime.strftime("%Y-%m-%d %H:%M:%S") in dcshadow_check:
            dcshadow[username] = etime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            dcshadow_check.append(etime.strftime("%Y-%m-%d %H:%M:%S"))
###
# Parse logon logs
#  EventID 4624: An account was successfully logged on
#  EventID 4625: An account failed to log on
#  EventID 4768: A Kerberos authentication ticket (TGT) was requested
#  EventID 4769: A Kerberos service ticket was requested
#  EventID 4776: The domain controller attempted to validate the credentials for an account
###
else:
    for data in event_data:
        # parse IP Address
        if data.get("Name") in ["IpAddress", "Workstation"] and data.text is not None and (
                not re.search(HCHECK, data.text) or re.search(IPv4_PATTERN, data.text) or re.search(
                r"\A::ffff:\d+\.\d+\.\d+\.\d+\Z", data.text) or re.search(IPv6_PATTERN, data.text)):
            ipaddress = data.text.split("@")[0]
            ipaddress = ipaddress.lower().replace("::ffff:", "")
            ipaddress = ipaddress.replace("\\", "")
        # Parse hostname
        if data.get("Name") == "WorkstationName" and data.text is not None and (
                not re.search(HCHECK, data.text) or re.search(IPv4_PATTERN, data.text) or re.search(
                r"\A::ffff:\d+\.\d+\.\d+\.\d+\Z", data.text) or re.search(IPv6_PATTERN, data.text)):
            hostname = data.text.split("@")[0]
            hostname = hostname.lower().replace("::ffff:", "")
            hostname = hostname.replace("\\", "")
        # Parse username
        if data.get("Name") in "TargetUserName" and data.text is not None and not re.search(UCHECK, data.text):
            username = data.text.split("@")[0]
            if username[-1:] not in "$":
                username = username.lower() + "@"
            else:
                username = "-"
        # Parse targeted domain name
        if data.get("Name") in "TargetDomainName" and data.text is not None and not re.search(HCHECK, data.text):
            domain = data.text
        # parse trageted user SID
        if data.get("Name") in ["TargetUserSid", "TargetSid"] and data.text is not None and re.search(r"\AS-[0-9\-]*\Z",
                                                                                                      data.text):
            sid = data.text
        # parse lonon type
        if data.get("Name") in "LogonType" and re.search(r"\A\d{1,2}\Z", data.text):
            logintype = int(data.text)
        # parse status
        if data.get("Name") in "Status" and re.search(r"\A0x\w{8}\Z", data.text):
            status = data.text
        # parse Authentication package name
        if data.get("Name") in "AuthenticationPackageName" and re.search(r"\A\w*\Z", data.text):
            authname = data.text

    if username != "-" and username != "anonymous logon" and ipaddress != "::1" and ipaddress != "127.0.0.1" and (
            ipaddress != "-" or hostname != "-"):
        # generate pandas series
        if ipaddress != "-":
            event_series = pd.Series(
                [eventid, ipaddress, username, logintype, status, authname, int(stime.timestamp())],
                index=event_set.columns)
            ml_series = pd.Series([etime.strftime("%Y-%m-%d %H:%M:%S"), username, ipaddress, eventid],
                                  index=ml_frame.columns)
        else:
            event_series = pd.Series([eventid, hostname, username, logintype, status, authname, int(stime.timestamp())],
                                     index=event_set.columns)
            ml_series = pd.Series([etime.strftime("%Y-%m-%d %H:%M:%S"), username, hostname, eventid],
                                  index=ml_frame.columns)
        # append pandas series to dataframe
        event_set = event_set.append(event_series, ignore_index=True)
        ml_frame = ml_frame.append(ml_series, ignore_index=True)
        # print("%s,%i,%s,%s,%s,%s" % (eventid, ipaddress, username, comment, logintype))
        count_series = pd.Series([stime.strftime("%Y-%m-%d %H:%M:%S"), eventid, username], index=count_set.columns)
        count_set = count_set.append(count_series, ignore_index=True)
        # print("%s,%s" % (stime.strftime("%Y-%m-%d %H:%M:%S"), username))

        if domain != "-":
            domain_set.append([username, domain])

        if username not in username_set:
            username_set.append(username)

        if domain not in domains and domain != "-":
            domains.append(domain)

        if sid != "-":
            sids[username] = sid

        if hostname != "-" and ipaddress != "-":
            hosts[ipaddress] = hostname

        if authname in "NTML" and authname not in ntmlauth:
            ntmlauth.append(username)
###
# Detect the audit log deletion
# EventID 1102: The audit log was cleared
###
if eventid == 1102:
    logtime = node.xpath("/Event/System/TimeCreated")[0].get("SystemTime")
    etime = convert_logtime(logtime, tzone)
    deletelog.append(etime.strftime("%Y-%m-%d %H:%M:%S"))

    namespace = "http://manifests.microsoft.com/win/2004/08/windows/eventlog"
    user_data = node.xpath("/Event/UserData/ns:LogFileCleared/ns:SubjectUserName", namespaces={"ns": namespace})
    domain_data = node.xpath("/Event/UserData/ns:LogFileCleared/ns:SubjectDomainName", namespaces={"ns": namespace})

    if user_data[0].text is not None:
        username = user_data[0].text.split("@")[0]
        if username[-1:] not in "$":
            deletelog.append(username.lower())
        else:
            deletelog.append("-")
    else:
        deletelog.append("-")

    if domain_data[0].text is not None:
        deletelog.append(domain_data[0].text)
    else:
        deletelog.append("-")

print("\n[+] Load finished.")
print("[+] Total Event log is {0}.".format(count))