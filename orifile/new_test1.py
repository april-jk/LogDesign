import os
import sys
import re
import pickle
import shutil
import argparse
import datetime
import subprocess
from ssl import create_default_context

parser = argparse.ArgumentParser(description="Visualizing and analyzing active directory Windows logon event logs.")
parser.add_argument("-e", "--evtx", dest="evtx", nargs="*", action="store", type=str, metavar="EVTX",
                    help="Import to the AD EVTX file. (multiple files OK)")
parser.add_argument("-x", "--xml", dest="xmls", nargs="*", action="store", type=str, metavar="XML",
                    help="Import to the XML file for event log. (multiple files OK)")

args = parser.parse_args()

def parse_evtx(evtx_list):
    cache_dir = os.path.join(FPATH, 'cache')

    # Load cache files
    if args.add and os.path.exists(cache_dir) and len(os.listdir(cache_dir)):
        print("[+] Load cashe files.")
        event_set = pd.read_pickle(os.path.join(cache_dir, "event_set.pkl"))
        count_set = pd.read_pickle(os.path.join(cache_dir, "count_set.pkl"))
        ml_frame = pd.read_pickle(os.path.join(cache_dir, "ml_frame.pkl"))
        with open(os.path.join(cache_dir, "username_set.pkl"), "rb") as f:
            username_set = pickle.load(f)
        with open(os.path.join(cache_dir, "domain_set.pkl"), "rb") as f:
            domain_set = pickle.load(f)
        with open(os.path.join(cache_dir, "admins.pkl"), "rb") as f:
            admins = pickle.load(f)
        with open(os.path.join(cache_dir, "domains.pkl"), "rb") as f:
            domains = pickle.load(f)
        with open(os.path.join(cache_dir, "ntmlauth.pkl"), "rb") as f:
            ntmlauth = pickle.load(f)
        with open(os.path.join(cache_dir, "deletelog.pkl"), "rb") as f:
            deletelog = pickle.load(f)
        with open(os.path.join(cache_dir, "policylist.pkl"), "rb") as f:
            policylist = pickle.load(f)
        with open(os.path.join(cache_dir, "addusers.pkl"), "rb") as f:
            addusers = pickle.load(f)
        with open(os.path.join(cache_dir, "delusers.pkl"), "rb") as f:
            delusers = pickle.load(f)
        with open(os.path.join(cache_dir, "addgroups.pkl"), "rb") as f:
            addgroups = pickle.load(f)
        with open(os.path.join(cache_dir, "removegroups.pkl"), "rb") as f:
            removegroups = pickle.load(f)
        with open(os.path.join(cache_dir, "sids.pkl"), "rb") as f:
            sids = pickle.load(f)
        with open(os.path.join(cache_dir, "hosts.pkl"), "rb") as f:
            hosts = pickle.load(f)
        with open(os.path.join(cache_dir, "dcsync.pkl"), "rb") as f:
            dcsync = pickle.load(f)
        with open(os.path.join(cache_dir, "dcshadow.pkl"), "rb") as f:
            dcshadow = pickle.load(f)
        with open(os.path.join(cache_dir, "date.pkl"), "rb") as f:
            starttime, endtime = pickle.load(f)
    else:
        event_set = pd.DataFrame(index=[], columns=["eventid", "ipaddress", "username", "logintype", "status", "authname", "date"])
        count_set = pd.DataFrame(index=[], columns=["dates", "eventid", "username"])
        ml_frame = pd.DataFrame(index=[], columns=["date", "user", "host", "id"])
        username_set = []
        domain_set = []
        admins = []
        domains = []
        ntmlauth = []
        deletelog = []
        policylist = []
        addusers = {}
        delusers = {}
        addgroups = {}
        removegroups = {}
        sids = {}
        hosts = {}
        dcsync = {}
        dcshadow = {}
        starttime = None
        endtime = None

    dcsync_count = {}
    dcshadow_check = []
    count = 0
    record_sum = 0

    if os.path.exists(cache_dir) is False:
        os.mkdir(cache_dir)
        print("[+] make cache folder {0}.".format(cache_dir))

    if args.timezone:
        try:
            datetime.timezone(datetime.timedelta(hours=args.timezone))
            tzone = args.timezone
            print("[+] Time zone is {0}.".format(args.timezone))
        except:
            sys.exit("[!] Can't load time zone {0}.".format(args.timezone))
    else:
        tzone = 0

    if args.fromdate:
        try:
            fdatetime = datetime.datetime.strptime(args.fromdate, "%Y-%m-%dT%H:%M:%S")
            print("[+] Parse the EVTX from {0}.".format(fdatetime.strftime("%Y-%m-%d %H:%M:%S")))
        except:
            sys.exit("[!] From date does not match format '%Y-%m-%dT%H:%M:%S'.")

    if args.todate:
        try:
            tdatetime = datetime.datetime.strptime(args.todate, "%Y-%m-%dT%H:%M:%S")
            print("[+] Parse the EVTX from {0}.".format(tdatetime.strftime("%Y-%m-%d %H:%M:%S")))
        except:
            sys.exit("[!] To date does not match format '%Y-%m-%dT%H:%M:%S'.")

    for evtx_file in evtx_list:
        if args.evtx:
            with open(evtx_file, "rb") as fb:
                fb_data = fb.read(8)
                #判断是否为evtx文件
                if fb_data != EVTX_HEADER:
                    sys.exit("[!] This file is not EVTX format {0}.".format(evtx_file))

            with open(evtx_file, "rb") as evtx:
                parser = PyEvtxParser(evtx)
                records = list(parser.records())
                record_sum += len(records)

        if args.xmls:
            with open(evtx_file, "r", encoding="utf8", errors="ignore") as fb:
                fb_header = fb.read(6)
                if "<?xml" not in fb_header:
                    sys.exit("[!] This file is not XML format {0}.".format(evtx_file))
                for line in fb:
                    record_sum += line.count("<System>")

    print("[+] Last record number is {0}.".format(record_sum))

    # Parse Event log
    print("[+] Start parsing the EVTX file.")

    for evtx_file in evtx_list:
        print("[+] Parse the EVTX file {0}.".format(evtx_file))

        for node, err in xml_records(evtx_file):
            if err is not None:
                continue
            count += 1
            #EventID
            eventid = int(node.xpath("/Event/System/EventID")[0].text)

            if not count % 100:
                #进度提示
                sys.stdout.write("\r[+] Now loading {0} records.".format(count))
                sys.stdout.flush()

            if eventid in EVENT_ID:
                logtime = node.xpath("/Event/System/TimeCreated")[0].get("SystemTime")
                etime = convert_logtime(logtime, tzone)
                stime = datetime.datetime(*etime.timetuple()[:4])
                if args.fromdate or args.todate:
                    if args.fromdate and fdatetime > etime:
                        continue
                    if args.todate and tdatetime < etime:
                        endtime = stime
                        break

                if starttime is None:
                    starttime = stime
                elif starttime > etime:
                    starttime = stime

                if endtime is None:
                    endtime = stime
                elif endtime < etime:
                    endtime = stime

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
                        elif data.get("Name") in "MemberSid" and data.text not in "-" and data.text is not None and re.search(r"\AS-[0-9\-]*\Z", data.text):
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
                        elif data.get("Name") in "MemberSid" and data.text not in "-" and data.text is not None and re.search(r"\AS-[0-9\-]*\Z", data.text):
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
                        if data.get("Name") in ["IpAddress", "Workstation"] and data.text is not None and (not re.search(HCHECK, data.text) or re.search(IPv4_PATTERN, data.text) or re.search(r"\A::ffff:\d+\.\d+\.\d+\.\d+\Z", data.text) or re.search(IPv6_PATTERN, data.text)):
                            ipaddress = data.text.split("@")[0]
                            ipaddress = ipaddress.lower().replace("::ffff:", "")
                            ipaddress = ipaddress.replace("\\", "")
                        # Parse hostname
                        if data.get("Name") == "WorkstationName" and data.text is not None and (not re.search(HCHECK, data.text) or re.search(IPv4_PATTERN, data.text) or re.search(r"\A::ffff:\d+\.\d+\.\d+\.\d+\Z", data.text) or re.search(IPv6_PATTERN, data.text)):
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
                        if data.get("Name") in ["TargetUserSid", "TargetSid"] and data.text is not None and re.search(r"\AS-[0-9\-]*\Z", data.text):
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

                    if username != "-" and username != "anonymous logon" and ipaddress != "::1" and ipaddress != "127.0.0.1" and (ipaddress != "-" or hostname != "-"):
                        # generate pandas series
                        if ipaddress != "-":
                            event_series = pd.Series([eventid, ipaddress, username, logintype, status, authname, int(stime.timestamp())], index=event_set.columns)
                            ml_series = pd.Series([etime.strftime("%Y-%m-%d %H:%M:%S"), username, ipaddress, eventid],  index=ml_frame.columns)
                        else:
                            event_series = pd.Series([eventid, hostname, username, logintype, status, authname, int(stime.timestamp())], index=event_set.columns)
                            ml_series = pd.Series([etime.strftime("%Y-%m-%d %H:%M:%S"), username, hostname, eventid],  index=ml_frame.columns)
                        # append pandas series to dataframe
                        event_set = event_set.appendTime(event_series, ignore_index=True)
                        ml_frame = ml_frame.appendTime(ml_series, ignore_index=True)
                        # print("%s,%i,%s,%s,%s,%s" % (eventid, ipaddress, username, comment, logintype))
                        count_series = pd.Series([stime.strftime("%Y-%m-%d %H:%M:%S"), eventid, username], index=count_set.columns)
                        count_set = count_set.appendTime(count_series, ignore_index=True)
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

    if not username_set or not len(event_set):
        sys.exit("[!] This event log did not include logs to be visualized. Please check the details of the event log.")
    else:
        print("[+] Filtered Event log is {0}.".format(len(event_set)))

    tohours = int((endtime - starttime).total_seconds() / 3600)

    # Create Event log cache files
    print("[+] Create cache files.")
    pd.to_pickle(event_set, os.path.join(cache_dir, "event_set.pkl"))
    pd.to_pickle(count_set, os.path.join(cache_dir, "count_set.pkl"))
    pd.to_pickle(ml_frame, os.path.join(cache_dir, "ml_frame.pkl"))
    with open(os.path.join(cache_dir, "username_set.pkl"), "wb") as f:
        pickle.dump(username_set, f)
    with open(os.path.join(cache_dir, "domain_set.pkl"), "wb") as f:
        pickle.dump(domain_set, f)
    with open(os.path.join(cache_dir, "admins.pkl"), "wb") as f:
        pickle.dump(admins, f)
    with open(os.path.join(cache_dir, "domains.pkl"), "wb") as f:
        pickle.dump(domains, f)
    with open(os.path.join(cache_dir, "ntmlauth.pkl"), "wb") as f:
        pickle.dump(ntmlauth, f)
    with open(os.path.join(cache_dir, "deletelog.pkl"), "wb") as f:
        pickle.dump(deletelog, f)
    with open(os.path.join(cache_dir, "policylist.pkl"), "wb") as f:
        pickle.dump(policylist, f)
    with open(os.path.join(cache_dir, "addusers.pkl"), "wb") as f:
        pickle.dump(addusers, f)
    with open(os.path.join(cache_dir, "delusers.pkl"), "wb") as f:
        pickle.dump(delusers, f)
    with open(os.path.join(cache_dir, "addgroups.pkl"), "wb") as f:
        pickle.dump(addgroups, f)
    with open(os.path.join(cache_dir, "removegroups.pkl"), "wb") as f:
        pickle.dump(removegroups, f)
    with open(os.path.join(cache_dir, "sids.pkl"), "wb") as f:
        pickle.dump(sids, f)
    with open(os.path.join(cache_dir, "hosts.pkl"), "wb") as f:
        pickle.dump(hosts, f)
    with open(os.path.join(cache_dir, "dcsync.pkl"), "wb") as f:
        pickle.dump(dcsync, f)
    with open(os.path.join(cache_dir, "dcshadow.pkl"), "wb") as f:
        pickle.dump(dcshadow, f)
    with open(os.path.join(cache_dir, "date.pkl"), "wb") as f:
        pickle.dump([starttime, endtime], f)

    if hosts:
        event_set = event_set.replace(hosts)

    event_set_bydate = event_set
    event_set_bydate["count"] = event_set_bydate.groupby(["eventid", "ipaddress", "username", "logintype", "status", "authname", "date"])["eventid"].transform("count")
    event_set_bydate = event_set_bydate.drop_duplicates()
    event_set = event_set.drop("date", axis=1)
    event_set["count"] = event_set.groupby(["eventid", "ipaddress", "username", "logintype", "status", "authname"])["eventid"].transform("count")
    event_set = event_set.drop_duplicates()
    count_set["count"] = count_set.groupby(["dates", "eventid", "username"])["dates"].transform("count")
    count_set = count_set.drop_duplicates()
    domain_set_uniq = list(map(list, set(map(tuple, domain_set))))

    # Learning event logs using Hidden Markov Model
    if hosts:
        ml_frame = ml_frame.replace(hosts)
    ml_frame = ml_frame.sort_values(by="date")
    if args.learn:
        print("[+] Learning event logs using Hidden Markov Model.")
        learnhmm(ml_frame, username_set, datetime.datetime(*starttime.timetuple()[:3]))

    # Calculate ChangeFinder
    print("[+] Calculate ChangeFinder.")
    timelines, detects, detect_cf = adetection(count_set, username_set, starttime, tohours)

    # Calculate Hidden Markov Model
    print("[+] Calculate Hidden Markov Model.")
    detect_hmm = decodehmm(ml_frame, username_set, datetime.datetime(*starttime.timetuple()[:3]))

    # Calculate PageRank
    print("[+] Calculate PageRank.")
    ranks = pagerank(event_set, admins, detect_hmm, detect_cf, ntmlauth)

    # Create node
    print("[+] Creating a graph data.")

    try:
        graph_http = "http://" + NEO4J_USER + ":" + NEO4J_PASSWORD + "@" + NEO4J_SERVER + ":" + NEO4J_PORT + "/db/data/"
        GRAPH = Graph(graph_http)
    except:
        sys.exit("[!] Can't connect Neo4j Database.")

    if args.postes:
        # Parse Event log
        print("[+] Start sending the ES.")

        # Create a new ES getLog_Client
        if args.espassword and args.escafile:
            context = create_default_context(cafile=FPATH + ES_CAFILE)
            client = Elasticsearch(ES_SERVER, http_auth=(ES_USER, ES_PASSWORD), scheme="https", ssl_context=context)
        elif args.espassword:
            es_hosts = ES_USER + ":" + ES_PASSWORD + "@" + ES_SERVER
            client = Elasticsearch(hosts=[es_hosts])
        else:
            client = Elasticsearch(ES_SERVER)

        if client.indices.exists(index="logontracer-user-index") and client.indices.exists(index="logontracer-host-index") :
            print("[+] Already created index mappings to ES.")
        else:
            create_map(client, "logontracer-host-index")
            create_map(client, "logontracer-user-index")
            print("[+] Creating index mappings to ES.")

        es_timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    tx = GRAPH.begin()
    hosts_inv = {v: k for k, v in hosts.items()}
    for ipaddress in event_set["ipaddress"].drop_duplicates():
        if ipaddress in hosts_inv:
            hostname = hosts_inv[ipaddress]
        else:
            hostname = ipaddress
        # add the IPAddress node to neo4j
        tx.run(statement_ip.format(**{"IP": ipaddress, "rank": ranks[ipaddress], "hostname": hostname}))

        # add host data to Elasticsearch
        if args.postes:
            es_doc = es_doc_ip.format(**{"datetime": es_timestamp, "IP": ipaddress, "rank": ranks[ipaddress], "hostname": hostname})
            post_es("logontracer-host-index", client, es_doc)

    i = 0
    for username in username_set:
        sid = sids.get(username, "-")
        if username in admins:
            rights = "system"
        else:
            rights = "user"
        ustatus = ""
        if username in addusers:
            ustatus += "Created(" + addusers[username] + ") "
        if username in delusers:
            ustatus += "Deleted(" + delusers[username] + ") "
        if sid in addgroups:
            ustatus += addgroups[sid]
        if sid in removegroups:
            ustatus += removegroups[sid]
        if username in dcsync:
            ustatus += "DCSync(" + dcsync[username] + ") "
        if username in dcshadow:
            ustatus += "DCShadow(" + dcshadow[username] + ") "
        if not ustatus:
            ustatus = "-"

        # add the username node to neo4j
        tx.run(statement_user.format(**{"user": username[:-1], "rank": ranks[username], "rights": rights, "sid": sid, "status": ustatus,
                                         "counts": ",".join(map(str, timelines[i*6])), "counts4624": ",".join(map(str, timelines[i*6+1])),
                                         "counts4625": ",".join(map(str, timelines[i*6+2])), "counts4768": ",".join(map(str, timelines[i*6+3])),
                                         "counts4769": ",".join(map(str, timelines[i*6+4])), "counts4776": ",".join(map(str, timelines[i*6+5])),
                                         "detect": ",".join(map(str, detects[i]))}))
        i += 1

        # add user data to Elasticsearch
        if args.postes:
            es_doc = es_doc_user.format(**{"datetime": es_timestamp, "user": username[:-1], "rights": rights, "sid": sid, "status": ustatus, "rank": ranks[username]})
            post_es("logontracer-user-index", client, es_doc)

    for domain in domains:
        # add the domain node to neo4j
        tx.run(statement_domain.format(**{"domain": domain}))

    for _, events in event_set_bydate.iterrows():
        # add the (username)-(event)-(ip) link to neo4j
        tx.run(statement_r.format(**{"user": events["username"][:-1], "IP": events["ipaddress"], "id": events["eventid"], "logintype": events["logintype"],
                                      "status": events["status"], "count": events["count"], "authname": events["authname"], "date": events["date"]}))

    for username, domain in domain_set_uniq:
        # add (username)-()-(domain) link to neo4j
        tx.run(statement_dr.format(**{"user": username[:-1], "domain": domain}))

    # add the date node to neo4j
    tx.run(statement_date.format(**{"Daterange": "Daterange", "start": datetime.datetime(*starttime.timetuple()[:4]).strftime("%Y-%m-%d %H:%M:%S"),
                                     "end": datetime.datetime(*endtime.timetuple()[:4]).strftime("%Y-%m-%d %H:%M:%S")}))

    if len(deletelog):
        # add the delete flag node to neo4j
        tx.run(statement_del.format(**{"deletetime": deletelog[0], "user": deletelog[1], "domain": deletelog[2]}))

    if len(policylist):
        id = 0
        for policy in policylist:
            if policy[2] in CATEGORY_IDs:
                category = CATEGORY_IDs[policy[2]]
            else:
                category = policy[2]
            if policy[3] in AUDITING_CONSTANTS:
                sub = AUDITING_CONSTANTS[policy[3]]
            else:
                sub = policy[3]
            username = policy[1]
            # add the policy id node to neo4j
            tx.run(statement_pl.format(**{"id": id, "changetime": policy[0], "category": category, "sub": sub}))
            # add (username)-(policy)-(id) link to neo4j
            tx.run(statement_pr.format(**{"user": username[:-1], "id": id, "date": policy[4]}))
            id += 1

    #tx.process()
    try:
        # for py2neo 2021.1 or later
        GRAPH.commit(tx)
    except:
        # for py2neo 2021.0 or earlier
        tx.commit()

    print("[+] Creation of a graph data finished.")
# Parse from Elastic Search cluster
# Porting by 0xThiebaut
def parse_es():
    event_set = pd.DataFrame(index=[], columns=["eventid", "ipaddress", "username", "logintype", "status", "authname", "date"])
    count_set = pd.DataFrame(index=[], columns=["dates", "eventid", "username"])
    ml_frame = pd.DataFrame(index=[], columns=["date", "user", "host", "id"])
    username_set = []
    domain_set = []
    admins = []
    domains = []
    ntmlauth = []
    deletelog = []
    policylist = []
    addusers = {}
    delusers = {}
    addgroups = {}
    removegroups = {}
    sids = {}
    hosts = {}
    dcsync_count = {}
    dcsync = {}
    dcshadow_check = []
    dcshadow = {}
    count = 0
    starttime = None
    endtime = None
    fdatetime = None
    tdatetime = None

    if args.timezone:
        try:
            datetime.timezone(datetime.timedelta(hours=args.timezone))
            tzone = args.timezone
            print("[+] Time zone is {0}.".format(args.timezone))
        except:
            sys.exit("[!] Can't load time zone {0}.".format(args.timezone))
    else:
        tzone = 0

    if args.fromdate:
        try:
            fdatetime = datetime.datetime.strptime(args.fromdate, "%Y-%m-%dT%H:%M:%S")
            print("[+] Search ES from {0}.".format(fdatetime.strftime("%Y-%m-%d %H:%M:%S")))
        except:
            sys.exit("[!] From date does not match format '%Y-%m-%dT%H:%M:%S'.")

    if args.todate:
        try:
            tdatetime = datetime.datetime.strptime(args.todate, "%Y-%m-%dT%H:%M:%S")
            print("[+] Search ES to {0}.".format(tdatetime.strftime("%Y-%m-%d %H:%M:%S")))
        except:
            sys.exit("[!] To date does not match format '%Y-%m-%dT%H:%M:%S'.")
    # Parse Event log
    print("[+] Start searching the ES.")

    # Create a new ES getLog_Client
    if args.espassword and args.escafile:
        context = create_default_context(cafile=FPATH + ES_CAFILE)
        client = Elasticsearch(ES_SERVER, http_auth=(ES_USER, ES_PASSWORD), scheme="https", ssl_context=context)
    elif args.espassword:
        es_hosts = ES_USER + ":" + ES_PASSWORD + "@" + ES_SERVER
        client = Elasticsearch(hosts=[es_hosts])
    else:
        client = Elasticsearch(ES_SERVER)

    # Create the search
    s = Search(using=client, index=ES_INDEX)

    if fdatetime or tdatetime:
        filter = {"format": "epoch_millis"}
        if fdatetime:
            filter["gte"] = int(fdatetime.timestamp() * 1000)
        if tdatetime:
            filter["lt"] = int(tdatetime.timestamp() * 1000)
        s = s.filter("range", **{'@timestamp': filter})

    # Split the prefix
    parts = ES_PREFIX.strip(".")
    if len(parts) > 0:
        parts = parts.split(".")
    else:
        parts = []
    # Search for any event in EVENT_ID
    parts.append("event_id")
    field = ".".join(parts)
    parts.pop()
    queries = [Q("term", **{field:1102})]
    for event_id in EVENT_ID:
        queries.append(Q("term", **{field:event_id}))
    query = Q("bool",
              should=queries,
              minimum_should_match=1)
    s = s.query(query)

    # Execute the search
    for hit in s.scan():
        event = hit
        prefixed = True
        for part in parts:
            if hasattr(event, part):
                event = getattr(event, part)
            else:
                prefixed = False
                break

        if not prefixed:
            print("Skipping unexpected event...")
            continue

        count += 1
        eventid = event.event_id

        if not count % 100:
            sys.stdout.write("\r[+] Now loading {0} records.".format(count))
            sys.stdout.flush()

        if eventid in EVENT_ID:
            logtime = hit["@timestamp"].replace("T", " ").split(".")[0]
            etime = convert_logtime(logtime, tzone)

            stime = datetime.datetime(*etime.timetuple()[:4])

            if starttime is None:
                starttime = stime
            elif starttime > etime:
                starttime = stime

            if endtime is None:
                endtime = stime
            elif endtime < etime:
                endtime = stime

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
                username = event.event_data.SubjectUserName.split("@")[0]
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
                username = event.event_data.TargetUserName.split("@")[0]
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
                username = event.event_data.SubjectUserName.split("@")[0]
                if username[-1:] not in "$":
                    username = username.lower() + "@"
                else:
                    username = "-"
                category = event.event_data.CategoryId
                guid = event.event_data.SubcategoryGuid
                policylist.append([etime.strftime("%Y-%m-%d %H:%M:%S"), username, category, guid.lower(), int(stime.timestamp())])
            ###
            # Detect added users from specific group
            #  EventID 4728: A member was added to a security-enabled global group
            #  EventID 4732: A member was added to a security-enabled local group
            #  EventID 4756: A member was added to a security-enabled universal group
            ###
            elif eventid in [4728, 4732, 4756]:
                groupname = event.event_data.TargetUserName
                usid = event.event_data.MemberSid
                addgroups[usid] = "AddGroup: " + groupname + "(" + etime.strftime("%Y-%m-%d %H:%M:%S") + ") "
            ###
            # Detect removed users from specific group
            #  EventID 4729: A member was removed from a security-enabled global group
            #  EventID 4733: A member was removed from a security-enabled local group
            #  EventID 4757: A member was removed from a security-enabled universal group
            ###
            elif eventid in [4729, 4733, 4757]:
                groupname = event.event_data.TargetUserName
                usid = event.event_data.MemberSid
                removegroups[usid] = "RemoveGroup: " + groupname + "(" + etime.strftime("%Y-%m-%d %H:%M:%S") + ") "
            ###
            # Detect DCSync
            #  EventID 4662: An operation was performed on an object
            ###
            elif eventid == 4662:
                username = event.event_data.SubjectUserName.split("@")[0]
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
                username = event.event_data.SubjectUserName.split("@")[0]
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
                # parse IP Address
                if hasattr(event.event_data, "IpAddress"):
                    ipaddress = event.event_data.IpAddress.split("@")[0]
                    ipaddress = ipaddress.lower().replace("::ffff:", "")
                    ipaddress = ipaddress.replace("\\", "")
                elif hasattr(event.event_data, "Workstation"):
                    ipaddress = event.event_data.Workstation.split("@")[0]
                    ipaddress = ipaddress.lower().replace("::ffff:", "")
                    ipaddress = ipaddress.replace("\\", "")
                # Parse hostname
                if hasattr(event.event_data, "WorkstationName"):
                    hostname = event.event_data.WorkstationName.split("@")[0]
                    hostname = hostname.lower().replace("::ffff:", "")
                    hostname = hostname.replace("\\", "")
                # Parse username
                if hasattr(event.event_data, "TargetUserName"):
                    username = event.event_data.TargetUserName.split("@")[0]
                    if username[-1:] not in "$":
                        username = username.lower() + "@"
                    else:
                        username = "-"
                # Parse targeted domain name
                if hasattr(event.event_data, "TargetDomainName"):
                    domain = event.event_data.TargetDomainName
                # parse trageted user SID
                if hasattr(event.event_data, "TargetUserSid"):
                    sid = event.event_data.TargetUserSid
                if hasattr(event.event_data, "TargetSid"):
                    sid = event.event_data.TargetSid
                # parse login type
                if hasattr(event.event_data, "LogonType"):
                    logintype = event.event_data.LogonType
                # parse status
                if hasattr(event.event_data, "Status"):
                    status = event.event_data.Status
                # parse Authentication package name
                if hasattr(event.event_data, "AuthenticationPackageName"):
                    authname = event.event_data.AuthenticationPackageName
                if username != "-" and username != "anonymous logon" and ipaddress != "::1" and ipaddress != "127.0.0.1" and (ipaddress != "-" or hostname != "-"):
                    # generate pandas series
                    if ipaddress != "-":
                        event_series = pd.Series([eventid, ipaddress, username, logintype, status, authname, int(stime.timestamp())], index=event_set.columns)
                        ml_series = pd.Series([etime.strftime("%Y-%m-%d %H:%M:%S"), username, ipaddress, eventid],  index=ml_frame.columns)
                    else:
                        event_series = pd.Series([eventid, hostname, username, logintype, status, authname, int(stime.timestamp())], index=event_set.columns)
                        ml_series = pd.Series([etime.strftime("%Y-%m-%d %H:%M:%S"), username, hostname, eventid],  index=ml_frame.columns)
                    # append pandas series to dataframe
                    event_set = event_set.appendTime(event_series, ignore_index=True)
                    ml_frame = ml_frame.appendTime(ml_series, ignore_index=True)
                    # print("%s,%i,%s,%s,%s,%s" % (eventid, ipaddress, username, comment, logintype))
                    count_series = pd.Series([stime.strftime("%Y-%m-%d %H:%M:%S"), eventid, username], index=count_set.columns)
                    count_set = count_set.appendTime(count_series, ignore_index=True)
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
            logtime = hit["@timestamp"]
            etime = convert_logtime(logtime, tzone)
            deletelog.append(etime.strftime("%Y-%m-%d %H:%M:%S"))

            if hasattr(event.user_data, "SubjectUserName"):
                username = event.user_data.SubjectUserName.split("@")[0]
                if username[-1:] not in "$":
                    deletelog.append(username.lower())
                else:
                    deletelog.append("-")
            else:
                deletelog.append("-")

            if hasattr(event.user_data, "SubjectDomainName"):
                deletelog.append(event.user_data.SubjectDomainName)
            else:
                deletelog.append("-")

    print("\n[+] Load finished.")
    print("[+] Total Event log is {0}.".format(count))

    if not username_set or not len(event_set):
        sys.exit("[!] This event log did not include logs to be visualized. Please check the details of the event log.")
    else:
        print("[+] Filtered Event log is {0}.".format(len(event_set)))

    tohours = int((endtime - starttime).total_seconds() / 3600)

    if hosts:
        event_set = event_set.replace(hosts)
    event_set_bydate = event_set
    event_set_bydate["count"] = event_set_bydate.groupby(["eventid", "ipaddress", "username", "logintype", "status", "authname", "date"])["eventid"].transform("count")
    event_set_bydate = event_set_bydate.drop_duplicates()
    event_set = event_set.drop("date", axis=1)
    event_set["count"] = event_set.groupby(["eventid", "ipaddress", "username", "logintype", "status", "authname"])["eventid"].transform("count")
    event_set = event_set.drop_duplicates()
    count_set["count"] = count_set.groupby(["dates", "eventid", "username"])["dates"].transform("count")
    count_set = count_set.drop_duplicates()
    domain_set_uniq = list(map(list, set(map(tuple, domain_set))))

    # Learning event logs using Hidden Markov Model
    if hosts:
        ml_frame = ml_frame.replace(hosts)
    ml_frame = ml_frame.sort_values(by="date")
    if args.learn:
        print("[+] Learning event logs using Hidden Markov Model.")
        learnhmm(ml_frame, username_set, datetime.datetime(*starttime.timetuple()[:3]))

    # Calculate ChangeFinder
    print("[+] Calculate ChangeFinder.")
    timelines, detects, detect_cf = adetection(count_set, username_set, starttime, tohours)

    # Calculate Hidden Markov Model
    print("[+] Calculate Hidden Markov Model.")
    detect_hmm = decodehmm(ml_frame, username_set, datetime.datetime(*starttime.timetuple()[:3]))

    # Calculate PageRank
    print("[+] Calculate PageRank.")
    ranks = pagerank(event_set, admins, detect_hmm, detect_cf, ntmlauth)

    # Create node
    print("[+] Creating a graph data.")

    try:
        graph_http = "http://" + NEO4J_USER + ":" + NEO4J_PASSWORD + "@" + NEO4J_SERVER + ":" + NEO4J_PORT + "/db/data/"
        GRAPH = Graph(graph_http)
    except:
        sys.exit("[!] Can't connect Neo4j Database.")

    if args.postes:
        # Parse Event log
        print("[+] Start sending the ES.")

        if client.indices.exists(index="logontracer-user-index") and client.indices.exists(index="logontracer-host-index") :
            print("[+] Already created index mappings to ES.")
        else:
            create_map(client, "logontracer-host-index")
            create_map(client, "logontracer-user-index")
            print("[+] Creating index mappings to ES.")

        es_timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    tx = GRAPH.begin()
    hosts_inv = {v: k for k, v in hosts.items()}
    for ipaddress in event_set["ipaddress"].drop_duplicates():
        if ipaddress in hosts_inv:
            hostname = hosts_inv[ipaddress]
        else:
            hostname = ipaddress
        # add the IPAddress node to neo4j
        tx.run(statement_ip.format(**{"IP": ipaddress, "rank": ranks[ipaddress], "hostname": hostname}))

        # add host data to Elasticsearch
        if args.postes:
            es_doc = es_doc_ip.format(**{"datetime": es_timestamp, "IP": ipaddress, "rank": ranks[ipaddress], "hostname": hostname})
            post_es("logontracer-host-index", client, es_doc)

    i = 0
    for username in username_set:
        sid = sids.get(username, "-")
        if username in admins:
            rights = "system"
        else:
            rights = "user"
        ustatus = ""
        if username in addusers:
            ustatus += "Created(" + addusers[username] + ") "
        if username in delusers:
            ustatus += "Deleted(" + delusers[username] + ") "
        if sid in addgroups:
            ustatus += addgroups[sid]
        if sid in removegroups:
            ustatus += removegroups[sid]
        if username in dcsync:
            ustatus += "DCSync(" + dcsync[username] + ") "
        if username in dcshadow:
            ustatus += "DCShadow(" + dcshadow[username] + ") "
        if not ustatus:
            ustatus = "-"

        # add the username node to neo4j
        tx.run(statement_user.format(**{"user": username[:-1], "rank": ranks[username], "rights": rights, "sid": sid, "status": ustatus,
                                         "counts": ",".join(map(str, timelines[i*6])), "counts4624": ",".join(map(str, timelines[i*6+1])),
                                         "counts4625": ",".join(map(str, timelines[i*6+2])), "counts4768": ",".join(map(str, timelines[i*6+3])),
                                         "counts4769": ",".join(map(str, timelines[i*6+4])), "counts4776": ",".join(map(str, timelines[i*6+5])),
                                         "detect": ",".join(map(str, detects[i]))}))
        i += 1

        # add user data to Elasticsearch
        if args.postes:
            es_doc = es_doc_user.format(**{"datetime": es_timestamp, "user": username[:-1], "rights": rights, "sid": sid, "status": ustatus, "rank": ranks[username]})
            post_es("logontracer-user-index", client, es_doc)

    for domain in domains:
        # add the domain node to neo4j
        tx.run(statement_domain.format(**{"domain": domain}))

    for _, events in event_set_bydate.iterrows():
        # add the (username)-(event)-(ip) link to neo4j
        tx.run(statement_r.format(**{"user": events["username"][:-1], "IP": events["ipaddress"], "id": events["eventid"], "logintype": events["logintype"],
                                      "status": events["status"], "count": events["count"], "authname": events["authname"], "date": events["date"]}))

    for username, domain in domain_set_uniq:
        # add (username)-()-(domain) link to neo4j
        tx.run(statement_dr.format(**{"user": username[:-1], "domain": domain}))

    # add the date node to neo4j
    tx.run(statement_date.format(**{"Daterange": "Daterange", "start": datetime.datetime(*starttime.timetuple()[:4]).strftime("%Y-%m-%d %H:%M:%S"),
                                     "end": datetime.datetime(*endtime.timetuple()[:4]).strftime("%Y-%m-%d %H:%M:%S")}))

    if len(deletelog):
        # add the delete flag node to neo4j
        tx.run(statement_del.format(**{"deletetime": deletelog[0], "user": deletelog[1], "domain": deletelog[2]}))

    if len(policylist):
        id = 0
        for policy in policylist:
            if policy[2] in CATEGORY_IDs:
                category = CATEGORY_IDs[policy[2]]
            else:
                category = policy[2]
            if policy[3] in AUDITING_CONSTANTS:
                sub = AUDITING_CONSTANTS[policy[3]]
            else:
                sub = policy[3]
            username = policy[1]
            # add the policy id node to neo4j
            tx.run(statement_pl.format(**{"id": id, "changetime": policy[0], "category": category, "sub": sub}))
            # add (username)-(policy)-(id) link to neo4j
            tx.run(statement_pr.format(**{"user": username[:-1], "id": id, "date": policy[4]}))
            id += 1

    #tx.process()
    try:
        # for py2neo 2021.1 or later
        GRAPH.commit(tx)
    except:
        # for py2neo 2021.0 or earlier
        tx.commit()

    print("[+] Creation of a graph data finished.")

if args.evtx:
    for evtx_file in args.evtx:
        if not os.path.isfile(evtx_file):
            sys.exit("[!] Can't open file {0}.".format(evtx_file))
    parse_evtx(args.evtx)



