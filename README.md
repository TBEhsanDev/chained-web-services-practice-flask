# Ip_Project_Flask<br/>
‫this is a teaching project that has 4 steps.in this project clients send post request to server and server get some information from request ,save posted<br/>
data as log in file and return request body in addition request ip.<br/>
necessary tools:nginx(used as proxy server),logstash(used to read logs from file and send to db),mongodb(used as db),code coverage(used to check tests <br/>
how much cover the code),apachebench(used to check load test on project)and redis(used to limit count of recieved requests as rate limiter).<br/>
###step1:<br/>
&nbsp;create an ip server that add client ip to response body and its related test script.then apply code coverage and apachebench .<br/>
###step2:<br/>
&nbsp;add logger server between nginx and ip server to log data to jsonline file.this data concludes body request in addition request time.also should modify<br/>
&nbsp;test script.then apply code coverage and apachebenc for this step too.<br/>
###step3:<br/>
&nbsp;setup logstash and mongodb that  records in jsonl file read by logstash and write in db.also should modify test file.<br/>
###step4:<br/>
&nbsp;add rate limiter server between nginx and logger server to control number of requests.(should use redis to control).in this step also should modify test<br/>
&nbsp;and code coverage is used too.<br/>
###instruction for run and test:<br/>
&nbsp;first run bash script "./setup.sh".this script create venv ,activate it and install necessary packages on venv.<br/>
&nbsp;for run servers ,run bash script "./run.sh".for test project run bash script "./test.sh".<br/>
