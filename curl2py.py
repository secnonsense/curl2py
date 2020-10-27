#!/usr/bin/env python3

import argparse
import shlex

def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--raw", help="Use raw instead of json format", action="store_true")
    parser.add_argument("curl", help="Enter a full curl command in quotes")
    args = parser.parse_args()
    return args.curl,args.raw

def host_from_url(url):
    host_split=url.split("/")
    host=host_split[2]
    return host

def parse_curl(curl_in):
    x=1
    headers={}
    parse=shlex.split(curl_in)
    request="GET"
    if not "curl" in parse[0]:
        print("input must be a full curl command in quotes")
        quit()
    while x < len(parse):
        if "-" in parse[x] and "http" not in parse[x]:
            if "--url" in parse[x]:
                url="\"" + parse[x+1].strip("'") + "\""
                host=host_from_url(url)
            if parse[x].lower()== "--request":
                request=parse[x+1]
            elif "-X" in parse[x]:
                request=parse[x+1].strip("'")
            if "-H" in parse[x] or "--header" in parse[x]:
                divide=parse[x+1].split(":",1)
                key=divide[0]
                value=divide[1:]
                headers[key]=' '.join(value).strip(" ")
                if "Host" in parse[x+1]:
                    host=parse[x+2].strip("'")
                x=x+1  
            if parse[x]=="--data":
                data=parse[x+1]
                x=x+1
            else:
                data="None"
        elif parse[x-1] !="-X" and parse[x-1].lower() != "--request":
            url="\"" + parse[x].strip("'") + "\""
            host=host_from_url(url)
        x=x+1
    return url,request,host,headers,data

def write_out(url,request,host,headers,raw,data):
    ua="Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MANM; rv:11.0) like Gecko"
    headers["User-Agent"]=ua
    output = open("curl.py",'w')
    output.write("#!/usr/bin/env python3\n\n")
    output.write("import http.client,ssl\n")
    if not raw or data != "None":
        output.write("import json,pprint\n")
    output.write("\ndef http_request():\n")
    output.write("\tmethod = \""+ request+"\"\n")
    output.write("\turl = "+url+"\n")
    output.write("\theaders = " + str(headers) + "\n")
    output.write("\thost=\""+host+"\"\n")
    if data == "None":
        output.write("\tdata=None\n")
    else:
        output.write("\tjson_data = " + data + "\n")
        output.write("\tdata = json.dumps(json_data)\n")
    output.write("\tconn = http.client.HTTPSConnection(host, context=ssl._create_unverified_context())\n")
    output.write("\tconn.request(method, url, data, headers)\n")
    output.write("\thttpResponse = conn.getresponse()\n")
    if raw:
        output.write("\toutput = httpResponse.read()\n")
    else:
        output.write("\toutput = json.loads(httpResponse.read())\n")
    output.write("\tconn.close()\n")
    output.write("\treturn output\n\n")
    output.write("def main():\n")
    output.write("\toutput=http_request()\n")
    if raw:
        output.write("\tprint(output)\n\n")
    else:    
        output.write("\tpprint.pprint(output)\n\n")
    output.write("if __name__ == \"__main__\":\n")
    output.write("\tmain()\n")
    output.close()
    print("\nFile curl.py successfully written\n")

def print_out(url,request,host,headers,data):
    print("The request type is: "+request+"\n")
    print("The host header is: "+host+"\n")
    print("The full URL is: "+url+"\n")
    print("The headers for the request are: "+ str(headers)+"\n")
    if request.upper()=="POST":
        print("The Post Data is: "+data+"\n")

def main():
    input,raw=get_input()
    url,request,host,headers,data=parse_curl(input)
    write_out(url,request,host,headers,raw,data)
    print_out(url,request,host,headers,data)

if __name__ == "__main__":
    main()