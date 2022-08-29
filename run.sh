#!/bin/bash -x
file_list=("Ip_apps.Ip.ip" "Ip_apps.Log.log" "Ip_apps.Rate_Limit.rate_limit")
for f  in "${file_list[@]}"
do
	python3 -m ${f}&
done
