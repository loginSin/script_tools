#!/bin/bash

# USER               PID  %CPU %MEM      VSZ    RSS   TT  STAT STARTED      TIME COMMAND

#!/bin/bash
interval=1  #设置采集间隔

echo 'cpu \t mem \t time \n' >> proc_memlog.txt
while true
   	do
   		echo $(date +"%y-%m-%d %H:%M:%S"+"\n") >> proc_memlog.txt
   		datas=`ps aux | grep RCE`
		echo "${datas[$1]}" |awk '{printf $3 "\t" $4 "\t" $10 "\n"}' >> proc_memlog.txt

		echo '\n' >> proc_memlog.txt
       	sleep $interval
done