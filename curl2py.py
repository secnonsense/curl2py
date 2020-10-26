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
    if not "curl" in parse[0]:
        print("input must be a full curl command in quotes")
        quit()
    while x < len(parse):
        if "-" in parse[x] and "http" not in parse[x]:
            if "--url" in parse[x]:
                url="\"" + parse[x+1].strip("'") + "\""
                host=host_from_url(url)
            if "--request" in parse[x]:
                request=parse[x+1]
            elif "-X" in parse[x]:
                request=parse[x+1].strip("'")
            else:
                request="GET"
            if "-H" in parse[x]:
                divide=parse[x+1].split(":")
                key=divide[0]
                value=divide[1:]
                headers[key]=' '.join(value).strip(" ")
                if "Host" in parse[x+1]:
                    host=parse[x+2].strip("'")
                x=x+1               
        elif parse[x-1] !="-X" and "--request" not in parse[x-1]:
            url="\"" + parse[x].strip("'") + "\""
            host=host_from_url(url)
        x=x+1
    return url,request,host,headers

def write_out(url,request,host,headers,raw):
    ua="Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MANM; rv:11.0) like Gecko"
    headers["User-Agent"]=ua
    output = open("curl.py",'w')
    output.write("#!/usr/bin/env python3\n\n")
    output.write("import http.client,ssl\n")
    if not raw:
        output.write("import json,pprint\n")
    output.write("\ndef http_request():\n")
    output.write("\tmethod=\""+ request+"\"\n")
    output.write("\turl="+url+"\n")
    output.write("\theaders =" + str(headers) + "\n")
    output.write("\thost=\""+host+"\"\n")
    output.write("\tconn = http.client.HTTPSConnection(host, context=ssl._create_unverified_context())\n")
    output.write("\tconn.request(method, url, None, headers)\n")
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

def main():
    input,raw=get_input()
    url,request,host,headers=parse_curl(input)
    write_out(url,request,host,headers,raw)

if __name__ == "__main__":
    main()