#!/bin/bash -x
for f  in Ip_apps.Ip.ip Ip_apps.Log.log Ip_apps.Rate_Limit.rate_limit
do
	python3 -m ${f}&
done
