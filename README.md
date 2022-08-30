# Ip_Project_Flask
‫this is a teaching project that has 4 steps.in this project clients send post request to server and server get some information from request ,save posted
data as log in file and return request body in addition request ip.
necessary tools:nginx(used as proxy server),logstash(used to read logs from file and send to db),mongodb(used as db),code coverage(used to check tests 
how much cover the code),apachebench(used to check load test on project)and redis(used to limit count of recieved requests as rate limiter).
step1:
  create an ip server that add client ip to response body and its related test script.then apply code coverage and apachebench .
step2:
  add logger server between nginx and ip server to log data to jsonline file.this data concludes body request in addition request time.also should modify
  test script.then apply code coverage and apachebenc for this step too.
step3:
  setup logstash and mongodb that  records in jsonl file read by logstash and write in db.also should modify test file.
step4:
  add rate limiter server between nginx and logger server to control number of requests.(should use redis to control).in this step also should modify test
  and code coverage is used too.
#instruction for run and test:
 first run bash script "./setup.sh".this script create venv ,activate it and install necessary packages on venv.
 for run servers ,run bash script "./run.sh".for test project run bash script "./test.sh".
